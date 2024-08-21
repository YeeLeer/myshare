#!/usr/bin/env bash

# 设置 Github CDN 及若干变量
export GH_PROXY=${GH_PROXY:-''}  # 国外不填
export GRPC_PROXY_PORT=${GRPC_PROXY_PORT:-'443'}
export GRPC_PORT=${GRPC_PORT:-'5555'}
export WEB_PORT="$SERVER_PORT"  # discord玩具自动  cf隧道按F佬格式，http端口用玩具端口。其他不变
# export WEB_PORT=${WEB_PORT:-'80'}} # 其他nodejs
export CADDY_HTTP_PORT=${CADDY_HTTP_PORT:-'2052'}
export LOCAL_TOKEN=${LOCAL_TOKEN:-'abcdefghijklmnopqr'}  # 本地key

# openkeepalive为1时保活进程,为0或者为空时不保活进程
export openkeepalive=${openkeepalive:-'1'}

# 自己填写这段变量
export GH_USER=${GH_USER:-''}
export ARGO_DOMAIN=${ARGO_DOMAIN:-''}
export ARGO_AUTH=${ARGO_AUTH:-''}
export GH_CLIENTID=${GH_CLIENTID:-''}
export GH_CLIENTSECRET=${GH_CLIENTSECRET:-''}

error() { echo -e "\033[31m\033[01m$*\033[0m" && exit 1; } # 红色
info() { echo -e "\033[32m\033[01m$*\033[0m"; }   # 绿色
hint() { echo -e "\033[33m\033[01m$*\033[0m"; }   # 黄色

# 如参数不齐全，容器退出，另外处理某些环境变量填错后的处理
[[ -z "$GH_USER" || -z "$GH_CLIENTID" || -z "$GH_CLIENTSECRET" ]] && error " There are variables that are not set. "
[[ "$ARGO_AUTH" =~ ey[A-Z0-9a-z=]{120,250}$ ]] && ARGO_AUTH=$(awk '{print $NF}' <<< "$ARGO_AUTH") # Token 复制全部，只取最后的 ey 开始的

# 检测是否需要启用 Github CDN，如能直接连通，则不使用
[ -n "$GH_PROXY" ] && wget --server-response --quiet --output-document=/dev/null --no-check-certificate --tries=2 --timeout=3 https://raw.githubusercontent.com/fscarmen2/Argo-Nezha-Service-Container/main/README.md >/dev/null 2>&1 && unset GH_PROXY

# 判断处理器架构
case "$(uname -m)" in
  aarch64|arm64 )
    ARCH=arm64
    ;;
  x86_64|amd64 )
    ARCH=amd64
    ;;
  armv7* )
    ARCH=arm
    ;;
  * ) error ""
esac

# 下载需要的应用
[ ! -d data ] && mkdir data

if [ ! -f caddy ]; then
  CADDY_LATEST=$(wget -qO- "${GH_PROXY}https://api.github.com/repos/caddyserver/caddy/releases/latest" | awk -F [v\"] '/"tag_name"/{print $5}' || echo '2.7.6')
  # wget -c ${GH_PROXY}https://github.com/caddyserver/caddy/releases/download/v${CADDY_LATEST}/caddy_${CADDY_LATEST}_linux_${ARCH}.tar.gz -qO- | tar xz -C . caddy
  curl -fsSL "${GH_PROXY}https://github.com/caddyserver/caddy/releases/download/v${CADDY_LATEST}/caddy_${CADDY_LATEST}_linux_${ARCH}.tar.gz" | tar xz -C . caddy
fi

if [ ! -f dashboard ]; then
  DASHBOARD_LATEST=$(wget -qO- "${GH_PROXY}https://api.github.com/repos/naiba/nezha/releases/latest" | awk -F '"' '/"tag_name"/{print $4}')
  # wget -O dashboard.zip ${GH_PROXY}https://github.com/naiba/nezha/releases/download/$DASHBOARD_LATEST/dashboard-linux-$ARCH.zip
  curl -sSL ${GH_PROXY}https://github.com/naiba/nezha/releases/download/$DASHBOARD_LATEST/dashboard-linux-$ARCH.zip -o dashboard.zip
  unzip dashboard.zip -d . >/dev/null
  mv -f ./dist/dashboard-linux-$ARCH dashboard
  rm -rf dist dashboard.zip
fi

if [ ! -f cloudflared ]; then
  # wget -qO cloudflared ${GH_PROXY}https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-$ARCH
  curl -sSL ${GH_PROXY}https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-$ARCH -o cloudflared
fi

if [ ! -f nezha-agent ]; then
  # wget -O nezha-agent.zip ${GH_PROXY}https://github.com/nezhahq/agent/releases/latest/download/nezha-agent_linux_$ARCH.zip
  curl -sSL ${GH_PROXY}https://github.com/nezhahq/agent/releases/latest/download/nezha-agent_linux_$ARCH.zip -o nezha-agent.zip
  unzip nezha-agent.zip -d . >/dev/null
  rm -rf nezha-agent.zip
fi

# 根据参数生成哪吒服务端配置文件
  cat > ./data/config.yaml << ABC
Debug: false
HTTPPort: $WEB_PORT
Language: zh-CN
GRPCPort: $GRPC_PORT
GRPCHost: $ARGO_DOMAIN
ProxyGRPCPort: $GRPC_PROXY_PORT
TLS: true
Oauth2:
  Type: "github" #Oauth2 登录接入类型，github/gitlab/jihulab/gitee/gitea ## Argo-容器版本只支持 github
  Admin: "$GH_USER" #管理员列表，半角逗号隔开
  ClientID: "$GH_CLIENTID" # 在 ${GH_PROXY}https://github.com/settings/developers 创建，无需审核 Callback 填 http(s)://域名或IP/oauth2/callback
  ClientSecret: "$GH_CLIENTSECRET"
  Endpoint: "" # 如gitea自建需要设置 ## Argo-容器版本只支持 github
site:
  Brand: "Nezha Probe"
  Cookiename: "nezha-dashboard" #浏览器 Cookie 字段名，可不改
  Theme: "default"
ABC

  cat > Caddyfile  << EOF
{
    http_port $CADDY_HTTP_PORT
}

:$GRPC_PROXY_PORT {
    reverse_proxy {
        to localhost:$GRPC_PORT
        transport http {
            versions h2c 2
        }
    }
    tls nezha.pem nezha.key
}
EOF

# 生成自签署SSL证书
openssl genrsa -out nezha.key 2048 > /dev/null 2>&1
openssl req -new -subj "/CN=$ARGO_DOMAIN" -key nezha.key -out nezha.csr > /dev/null 2>&1
openssl x509 -req -days 36500 -in nezha.csr -signkey nezha.key -out nezha.pem > /dev/null 2>&1

# 运行
run_caddy() {
  if [ -e caddy ]; then
    chmod +x caddy
    ./caddy run --config Caddyfile --watch > /dev/null 2>&1 &
  fi
}

run_cloudflared() {
  if [ -e cloudflared ]; then
    chmod +x cloudflared
    cat > cfstart.sh << DEF
#!/usr/bin/env bash

./cloudflared tunnel --edge-ip-version auto --protocol http2 run --token ${ARGO_AUTH} > /dev/null 2>&1 &
DEF
    [ -e cfstart.sh ] && chmod +x cfstart.sh && bash cfstart.sh
  fi
}

run_dashboard() {
  if [ -e dashboard ]; then
    chmod +x dashboard
    ./dashboard > /dev/null 2>&1 &
  fi
}

run_agent() {
  if [ -e nezha-agent ]; then
    chmod +x nezha-agent
    cat > nzstart.sh << KLM
#!/usr/bin/env bash

./nezha-agent -s localhost:$GRPC_PORT -p $LOCAL_TOKEN > /dev/null 2>&1 &
KLM
    [ -e nzstart.sh ] && chmod +x nzstart.sh && bash nzstart.sh
  fi
}

keep_alive() {
  if [[ $(pgrep -laf caddy) ]]; then
    hint "caddy is already running !"
  else
    run_caddy
    info "caddy runs again !"
  fi

  if [[ $(pgrep -laf cloudflared) ]]; then
    hint "cloudflared is already running !"
  else
    run_cloudflared
    info "cloudflared runs again !"
  fi

  if [[ $(pgrep -laf dashboard) ]]; then
    hint "dashboard is already running !"
  else
    run_dashboard
    info "dashboard runs again !"
  fi

  if [[ $(pgrep -laf nezha-agent) ]]; then
    hint "nezha-agent is already running !"
  else
    run_agent
    info "nezha-agent runs again !"
  fi
}

run() {
  echo "Server is running on port : ${SERVER_PORT}"
  run_caddy
  run_cloudflared
  run_dashboard
  run_agent

  if [ -n "$openkeepalive" ] && [ "$openkeepalive" != "0" ]; then
    while true
    do
    keep_alive
    sleep 50
    done
  elif [ -z "$openkeepalive" ]; then
    tail -f /dev/null
  else
    tail -f /dev/null
  fi
}

run
