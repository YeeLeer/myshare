#!/usr/bin/env bash

# Define Environment Variables
export V_PORT=${V_PORT:-'8080'}
export CFPORT=${CFPORT:-'443'} # 2053 2083 2087 2096 8443
export UUID=${UUID:-'7160b696-dd5e-42e3-a024-145e92cec916'}
export VMESS_WSPATH=${VMESS_WSPATH:-'startvm'}
export VLESS_WSPATH=${VLESS_WSPATH:-'startvl'}
export CF_IP=${CF_IP:-'icook.tw'}
export SUB_NAME=${SUB_NAME:-'streamlit'}
export FILE_PATH=${FILE_PATH:-'./.tmp'}

export SUB_URL=${SUB_URL:-'https://myjyup.shiguangda.nom.za/upload-a4aa34be-4373-4fdb-bff7-0a9c23405dac'}

export NEZHA_SERVER=${NEZHA_SERVER:-'nezha.tcguangda.eu.org'}
export NEZHA_KEY=${NEZHA_KEY:-'rZYB3POw666WxuEcDG'}
export NEZHA_PORT=${NEZHA_PORT:-'443'}

export ARGO_DOMAIN=${ARGO_DOMAIN:-''}
export ARGO_AUTH=${ARGO_AUTH:-''}

if [ ! -d "$FILE_PATH" ]; then
  mkdir -p "$FILE_PATH"
fi

cleanup_files() {
  rm -rf ${FILE_PATH}/*.log ${FILE_PATH}/*.json ${FILE_PATH}/*.txt ${FILE_PATH}/*.sh ${FILE_PATH}/tunnel.*
}
cleanup_files

# Download Dependency Files
set_download_url() {
  local program_name="$1"
  local default_url="$2"
  local x64_url="$3"

  if [ "$(uname -m)" = "x86_64" ] || [ "$(uname -m)" = "amd64" ] || [ "$(uname -m)" = "x64" ]; then
    download_url="$x64_url"
  else
    download_url="$default_url"
  fi
}

download_program() {
  local program_name="$1"
  local default_url="$2"
  local x64_url="$3"

  set_download_url "$program_name" "$default_url" "$x64_url"

  if [ ! -f "$program_name" ]; then
    if [ -n "$download_url" ]; then
      echo "Downloading $program_name..." > /dev/null
      # wget -qO "$program_name" "$download_url"
      curl -sSL "$download_url" -o "$program_name"
      echo "Downloaded $program_name" > /dev/null
    else
      echo "Skipping download for $program_name" > /dev/null
    fi
  else
    echo "$program_name already exists, skipping download" > /dev/null
  fi
}

if [ -n "${NEZHA_SERVER}" ] && [ -n "${NEZHA_KEY}" ]; then
  download_program "${FILE_PATH}/npm" "https://raw.githubusercontent.com/kahunama/myfile/main/nezha/nezha-agent(arm)" "https://raw.githubusercontent.com/kahunama/myfile/main/nezha/nezha-agent"
  chmod +x ${FILE_PATH}/npm
  sleep 3
fi

download_program "${FILE_PATH}/web" "https://raw.githubusercontent.com/kahunama/myfile/main/my/web.js(arm)" "https://raw.githubusercontent.com/kahunama/myfile/main/my/web.js"
chmod +x ${FILE_PATH}/web
sleep 3

download_program "${FILE_PATH}/server" "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64" "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64"
chmod +x ${FILE_PATH}/server
sleep 3

# Generate configuration
generate_config() {
  cat > ${FILE_PATH}/out.json << EOF
{
    "log":{
        "access":"/dev/null",
        "error":"/dev/null",
        "loglevel":"none"
    },
    "inbounds":[
        {
            "port":$V_PORT,
            "protocol":"vless",
            "settings":{
                "clients":[
                    {
                        "id":"${UUID}",
                        "flow":"xtls-rprx-vision"
                    }
                ],
                "decryption":"none",
                "fallbacks":[
                    {
                        "dest":3001
                    },
                    {
                        "path":"/${VLESS_WSPATH}",
                        "dest":3002
                    },
                    {
                        "path":"/${VMESS_WSPATH}",
                        "dest":3003
                    }
                ]
            },
            "streamSettings":{
                "network":"tcp"
            }
        },
        {
            "port":3001,
            "listen":"127.0.0.1",
            "protocol":"vless",
            "settings":{
                "clients":[
                    {
                        "id":"${UUID}"
                    }
                ],
                "decryption":"none"
            },
            "streamSettings":{
                "network":"ws",
                "security":"none"
            }
        },
        {
            "port":3002,
            "listen":"127.0.0.1",
            "protocol":"vless",
            "settings":{
                "clients":[
                    {
                        "id":"${UUID}",
                        "level":0
                    }
                ],
                "decryption":"none"
            },
            "streamSettings":{
                "network":"ws",
                "security":"none",
                "wsSettings":{
                    "path":"/${VLESS_WSPATH}"
                }
            },
            "sniffing":{
                "enabled":true,
                "destOverride":[
                    "http",
                    "tls",
                    "quic"
                ],
                "metadataOnly":false
            }
        },
        {
            "port":3003,
            "listen":"127.0.0.1",
            "protocol":"vmess",
            "settings":{
                "clients":[
                    {
                        "id":"${UUID}",
                        "alterId":0
                    }
                ]
            },
            "streamSettings":{
                "network":"ws",
                "wsSettings":{
                    "path":"/${VMESS_WSPATH}"
                }
            },
            "sniffing":{
                "enabled":true,
                "destOverride":[
                    "http",
                    "tls",
                    "quic"
                ],
                "metadataOnly":false
            }
        }
    ],
    "dns":{
        "servers":[
            "https+local://8.8.8.8/dns-query"
        ]
    },
    "outbounds":[
        {
            "protocol":"freedom"
        },
        {
            "tag":"WARP",
            "protocol":"wireguard",
            "settings":{
                "secretKey":"YFYOAdbw1bKTHlNNi+aEjBM3BO7unuFC5rOkMRAz9XY=",
                "address":[
                    "172.16.0.2/32",
                    "2606:4700:110:8a36:df92:102a:9602:fa18/128"
                ],
                "peers":[
                    {
                        "publicKey":"bmXOC+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=",
                        "allowedIPs":[
                            "0.0.0.0/0",
                            "::/0"
                        ],
                        "endpoint":"162.159.193.10:2408"
                    }
                ],
                "reserved":[78, 135, 76],
                "mtu":1280
            }
        }
    ],
    "routing":{
        "domainStrategy":"AsIs",
        "rules":[
            {
                "type":"field",
                "domain":[
                    "domain:openai.com",
                    "domain:ai.com"
                ],
                "outboundTag":"WARP"
            }
        ]
    }
}
EOF
}

argo_type() {
  if [ -z "$ARGO_AUTH" ] && [ -z "$ARGO_DOMAIN" ]; then
    echo "ARGO_AUTH or ARGO_DOMAIN is empty, use Quick Tunnels" > /dev/null
    return
  fi

  if [ -n "$(echo "$ARGO_AUTH" | grep TunnelSecret)" ]; then
    echo $ARGO_AUTH > ${FILE_PATH}/tunnel.json
    cat > ${FILE_PATH}/tunnel.yml << EOF
tunnel=$(echo "$ARGO_AUTH" | cut -d\" -f12)
credentials-file: ${FILE_PATH}/tunnel.json
protocol: http2

ingress:
  - hostname: $ARGO_DOMAIN
    service: http://localhost: $V_PORT
    originRequest:
      noTLSVerify: true
  - service: http_status:404
EOF
  else
    echo "ARGO_AUTH Mismatch TunnelSecret" > /dev/null
  fi
}

args() {
if [ -e ${FILE_PATH}/server ]; then
  if [ -n "$(echo "$ARGO_AUTH" | grep '^[A-Z0-9a-z=]\{120,250\}$')" ]; then
    args="tunnel --edge-ip-version auto --protocol http2 run --url http://localhost:$V_PORT --token ${ARGO_AUTH}"
  elif [ -n "$(echo "$ARGO_AUTH" | grep TunnelSecret)" ]; then
    args="tunnel --edge-ip-version auto --config tunnel.yml run"
  else
    args="tunnel --edge-ip-version auto --protocol http2 --no-autoupdate --logfile ${FILE_PATH}/boot.log --url http://localhost:$V_PORT"
  fi
fi
}

generate_config
argo_type
args

# 上传订阅
upload_subscription() {
    if [ "$download_tool" = "curl" ]; then
        response=$(curl -s -X POST -H "Content-Type: application/json" -d "{\"URL_NAME\":\"$SUB_NAME\",\"URL\":\"$UPLOAD_DATA\"}" $SUB_URL)
    else
        response=$(wget -qO- --post-data="{\"URL_NAME\":\"$SUB_NAME\",\"URL\":\"$UPLOAD_DATA\"}" --header="Content-Type: application/json" $SUB_URL)
    fi

    # 代码检查最后一个命令是否运行没有任何问题。如果是，则将执行随后的代码块
    if [ $? -eq 0 ]; then
        sleep 1
    else
        echo "Sub Upload failed"
    fi

}

# get country
get_country_code() {
  export country_abbreviation=$(curl -s https://speed.cloudflare.com/meta | awk -F\" '{print $26"-"$18}' | sed -e 's/ /_/g')   # 显示ISP及国家简称
  # export country_abbreviation=$(curl -s https://speed.cloudflare.com/meta | tr ',' '\n' | grep -E '"country"\s*:\s*"' | sed 's/.*"country"\s*:\s*"\([^"]*\)".*/\1/')   # 只显示国家简称
  # echo "${country_abbreviation}"
}

# check_hostname
check_hostname_change() {
  if [ -z "$ARGO_AUTH" ] && [ -z "$ARGO_DOMAIN" ]; then
    [ -s ${FILE_PATH}/boot.log ] && export ARGO_DOMAIN=$(cat ${FILE_PATH}/boot.log | grep -o "info.*https://.*trycloudflare.com" | sed "s@.*https://@@g" | tail -n 1)
    # [ -s ${FILE_PATH}/boot.log ] && export ARGO_DOMAIN=$(cat ${FILE_PATH}/boot.log | grep -o "https://.*trycloudflare.com" | tail -n 1 | sed 's/https:\/\///')
  fi
}

# build_urls
build_urls() {
  check_hostname_change

  export VMESS="{ \"v\": \"2\", \"ps\": \"vmess-${country_abbreviation}-${SUB_NAME}\", \"add\": \"${CF_IP}\", \"port\": \"${CFPORT}\", \"id\": \"${UUID}\", \"aid\": \"0\", \"scy\": \"none\", \"net\": \"ws\", \"type\": \"none\", \"host\": \"${ARGO_DOMAIN}\", \"path\": \"/${VMESS_WSPATH}?ed=2048\", \"tls\": \"tls\", \"sni\": \"${ARGO_DOMAIN}\", \"alpn\": \"\" }"

vless_url="vless://${UUID}@${CF_IP}:${CFPORT}?host=${ARGO_DOMAIN}&path=%2F${VLESS_WSPATH}%3Fed%3D2048&type=ws&encryption=none&security=tls&sni=${ARGO_DOMAIN}#vless-${country_abbreviation}-${SUB_NAME}"
export UPLOAD_DATA="$vless_url"
}

# run
run() {
  # openserver等于1
  if [ -e ${FILE_PATH}/server ]; then
    [[ $(pidof server) ]] && return
    ${FILE_PATH}/server $args >/dev/null 2>&1 &
  fi

  if [ -e ${FILE_PATH}/web ]; then
    [[ $(pidof web) ]] && return
    ${FILE_PATH}/web run -c ${FILE_PATH}/out.json >/dev/null 2>&1 &
  fi

  if [ -n "${NEZHA_SERVER}" ] && [ -n "${NEZHA_KEY}" ] && [ -e ${FILE_PATH}/npm ]; then
    [[ $(pidof npm) ]] && return
    tlsPorts=("443" "8443" "2096" "2087" "2083" "2053")
    if [[ " ${tlsPorts[@]} " =~ " ${NEZHA_PORT} " ]]; then
      NEZHA_TLS="--tls"
    else
      NEZHA_TLS=""
    fi
    ${FILE_PATH}/npm -s ${NEZHA_SERVER}:${NEZHA_PORT} -p ${NEZHA_KEY} ${NEZHA_TLS} >/dev/null 2>&1 &
  fi

  sleep 10

  get_country_code && build_urls

  if [ -n "${SUB_URL}" ]; then
  while true
  do
    upload_subscription
    sleep 100
  done
  fi
}

run
