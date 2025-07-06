import os #line:1
import re #line:2
import shutil #line:3
import subprocess #line:4
import requests #line:5
import json #line:6
import time #line:7
import base64 #line:8
import asyncio #line:9
import streamlit as st #line:10
FILE_PATH =os .environ .get ('FILE_PATH','./.tmp')#line:12
XCONF_PATH =os .path .join (FILE_PATH ,'xconf')#line:13
INTERVAL_SECONDS =int (os .environ .get ("TIME",100 ))#line:14
OPENSERVER =os .environ .get ('OPENSERVER','true').lower ()=='true'#line:15
KEEPALIVE =os .environ .get ('KEEPALIVE','true').lower ()=='true'#line:16
CFIP =os .environ .get ('CFIP','ip.sb')#line:17
PORT =int (os .environ .get ('SERVER_PORT')or os .environ .get ('PORT')or 3000 )#line:18
V_PORT =int (os .environ .get ('V_PORT',8080 ))#line:19
CFPORT =int (os .environ .get ('CFPORT',443 ))#line:20
SUB_URL =os .environ .get ('SUB_URL','https://myjyup.shiguangda.nom.za/upload-a4aa34be-4373-4fdb-bff7-0a9c23405dac')#line:21
VLPATH =os .environ .get ('VLPATH','startvl')#line:23
XHPPATH =os .environ .get ('XHPPATH','')#line:24
UUID =os .environ .get ('UUID','2b77e1df-a473-4b2e-a738-47f541b222b2')#line:26
NEZHA_VERSION =os .environ .get ('NEZHA_VERSION','V1')#line:27
NEZHA_SERVER =os .environ .get ('NEZHA_SERVER','nazha.tcguangda.eu.org')#line:28
NEZHA_KEY =os .environ .get ('NEZHA_KEY','ilovehesufeng520')#line:29
NEZHA_PORT =os .environ .get ('NEZHA_PORT','443')#line:30
SUB_NAME =os .environ .get ('SUB_NAME','streamlit')#line:31
MY_DOMAIN =os .environ .get ('MY_DOMAIN','')#line:32
ARGO_DOMAIN =os .environ .get ('ARGO_DOMAIN','str.tcgd001.cf')#line:34
ARGO_AUTH =os .environ .get ('ARGO_AUTH','eyJhIjoiNjFmNmJhODg2ODkxNmJmZmM1ZDljNzM2NzdiYmIwMDYiLCJ0IjoiNjQ0OWRjOWQtZWVkZC00ZDY5LWIyYmItY2ExNTQ4MzRkYzlhIiwicyI6Ik1UTTNPVFF4TXpJdE5tVTNOUzAwTldJekxXSTFNR1l0TkRrd016bGxNR1ExTm1ZMyJ9')#line:35
def createFolder (O000O000O0000000O ):#line:37
    if not os .path .exists (O000O000O0000000O ):#line:38
        os .makedirs (O000O000O0000000O )#line:39
        print (f"{O000O000O0000000O} is created")#line:40
    else :#line:41
        print (f"{O000O000O0000000O} already exists")#line:42
pathsToDelete =['config.yml','xconf','tunnel.json','tunnel.yml','boot.log','log.txt']#line:44
def cleanupOldFiles ():#line:45
    for O00000O0OO00O0O00 in pathsToDelete :#line:46
        OOO0O0O0O00000OO0 =os .path .join (FILE_PATH ,O00000O0OO00O0O00 )#line:47
        try :#line:49
            if os .path .exists (OOO0O0O0O00000OO0 ):#line:50
                if os .path .isdir (OOO0O0O0O00000OO0 ):#line:51
                    shutil .rmtree (OOO0O0O0O00000OO0 )#line:52
                else :#line:54
                    os .remove (OOO0O0O0O00000OO0 )#line:55
            else :#line:57
                pass #line:59
        except Exception as O0000O0OOOO0O0000 :#line:60
            pass #line:62
def display_homepage ():#line:65
    st .markdown ("""
    <html>
    <head>
        <title>my home page</title>
    </head>
    <body>
        <h1>Welcome to my space!</h1>
        <p>Very happy to make friends with you all!</p>
    </body>
    </html>
    """,unsafe_allow_html =True )#line:76
async def exec_promise (O0000OOO0OOOO000O ,options =None ,wait_for_completion =False ):#line:78
    if options is None :#line:79
        options ={}#line:80
    try :#line:82
        O000O0O0OOO0O0O0O =await asyncio .create_subprocess_shell (O0000OOO0OOOO000O ,stdout =asyncio .subprocess .PIPE ,stderr =asyncio .subprocess .PIPE ,**options )#line:88
        if wait_for_completion :#line:90
            O00OOO0O00O0O00O0 ,O0O000OO00000000O =await O000O0O0OOO0O0O0O .communicate ()#line:91
            if O000O0O0OOO0O0O0O .returncode !=0 :#line:93
                O0000OOO0OOOOOO00 =Exception (f"Command failed with exit code {O000O0O0OOO0O0O0O.returncode}")#line:94
                O0000OOO0OOOOOO00 .code =O000O0O0OOO0O0O0O .returncode #line:95
                O0000OOO0OOOOOO00 .stderr =O0O000OO00000000O .decode ().strip ()#line:96
                raise O0000OOO0OOOOOO00 #line:97
            return O00OOO0O00O0O00O0 .decode ().strip ()#line:99
        else :#line:100
            return O000O0O0OOO0O0O0O #line:102
    except Exception as OOO0O0OO00O00O0OO :#line:104
        if not hasattr (OOO0O0OO00O00O0OO ,'code'):#line:105
            OOO0O0OO00O00O0OO .code =-1 #line:106
        if not hasattr (OOO0O0OO00O00O0OO ,'stderr'):#line:107
            OOO0O0OO00O00O0OO .stderr =str (OOO0O0OO00O00O0OO )#line:108
        raise #line:109
async def detect_process (OOOO0OOO0O00O0000 ):#line:111
    O000O0OO0O0O0O00O =[{'cmd':f'pidof "{OOOO0OOO0O00O0000}"','name':'pidof'},{'cmd':f'pgrep -x "{OOOO0OOO0O00O0000}"','name':'pgrep'},{'cmd':f'ps -eo pid,comm | awk -v name="{OOOO0OOO0O00O0000}" \'$2 == name {{print $1}}\'','name':'ps+awk'}]#line:116
    for O00O000O000O0O000 in O000O0OO0O0O0O00O :#line:118
        try :#line:119
            O0OOOO0O00O0O00OO =await exec_promise (O00O000O000O0O000 ['cmd'],wait_for_completion =True )#line:120
            if O0OOOO0O00O0O00OO :#line:121
                return re .sub (r'\n+',' ',O0OOOO0O00O0O00OO )#line:122
        except Exception as OOOOO00O0OO0OOO0O :#line:123
            if hasattr (OOOOO00O0OO0OOO0O ,'code')and OOOOO00O0OO0OOO0O .code not in (127 ,1 ):#line:124
                print (f'[detect_process] {O00O000O000O0O000["name"]} error:',str (OOOOO00O0OO0OOO0O ))#line:125
            continue #line:126
    return ''#line:128
async def kill_process (OO000000OO0OO00O0 ):#line:130
    print (f"Attempting to kill process: {OO000000OO0OO00O0}")#line:131
    try :#line:133
        OOO0O00OO000O0OOO =await detect_process (OO000000OO0OO00O0 )#line:134
        if not OOO0O00OO000O0OOO :#line:136
            print (f"Process '{OO000000OO0OO00O0}' not found.")#line:137
            return #line:138
        O0OOO0O0OOO0OOO00 =await exec_promise (f"kill -9 {OOO0O00OO000O0OOO}")#line:140
        OO00OO0000OO0O0OO =f"Killed process (PIDs: {OOO0O00OO000O0OOO})"#line:142
        print (OO00OO0000OO0O0OO )#line:143
        return {'success':True ,'message':OO00OO0000OO0O0OO }#line:144
    except Exception as O000000OO00O0000O :#line:146
        OO00OO0000OO0O0OO =f"Kill failed: {str(O000000OO00O0000O)}"#line:147
        print (f"Error: {OO00OO0000OO0O0OO}")#line:148
        return {'success':False ,'message':OO00OO0000OO0O0OO }#line:149
def generate_config ():#line:151
    O00OOO000000O000O ='/'+str (VLPATH )#line:152
    OOOOO00000OO0000O ='/'+str (XHPPATH )#line:153
    OOO0OOOOO00O0O000 ={"log":{"access":"/dev/null","error":"/dev/null","loglevel":"none"},"dns":{"servers":["https+local://8.8.8.8/dns-query"]}};#line:165
    with open (os .path .join (XCONF_PATH ,'inbound.json'),'w',encoding ='utf-8')as O0O0O000OO0000000 :#line:166
        json .dump (OOO0OOOOO00O0O000 ,O0O0O000OO0000000 ,ensure_ascii =False ,indent =2 )#line:167
    if VLPATH :#line:169
        OO0000O0OOO0OO000 ={"inbounds":[{"port":V_PORT ,"listen":"::","protocol":"vless","settings":{"clients":[{"id":UUID ,"level":0 }],"decryption":"none"},"streamSettings":{"network":"ws","security":"none","wsSettings":{"path":O00OOO000000O000O }},"sniffing":{"enabled":True ,"destOverride":["http","tls","quic"],"metadataOnly":False }}]};#line:203
        with open (os .path .join (XCONF_PATH ,'inbound_v.json'),'w',encoding ='utf-8')as OO0000O00O0O0O00O :#line:204
            json .dump (OO0000O0OOO0OO000 ,OO0000O00O0O0O00O ,ensure_ascii =False ,indent =2 )#line:205
    elif XHPPATH :#line:206
        OO0000O0OOO0OO000 ={"inbounds":[{"port":V_PORT ,"listen":"::","protocol":"vless","settings":{"clients":[{"id":UUID }],"decryption":"none"},"streamSettings":{"network":"xhttp","security":"none","xhttpSettings":{"mode":"packet-up","path":OOOOO00000OO0000O }},"sniffing":{"enabled":True ,"destOverride":["http","tls","quic"],"metadataOnly":False }}]};#line:240
        with open (os .path .join (XCONF_PATH ,'inbound_v.json'),'w',encoding ='utf-8')as OO0000O00O0O0O00O :#line:241
            json .dump (OO0000O0OOO0OO000 ,OO0000O00O0O0O00O ,ensure_ascii =False ,indent =2 )#line:242
    OO000O00OO000OO00 ={"outbounds":[{"tag":"direct","protocol":"freedom"},{"tag":"block","protocol":"blackhole"}]};#line:255
    with open (os .path .join (XCONF_PATH ,'outbound.json'),'w',encoding ='utf-8')as OO0000O000O0O000O :#line:256
        json .dump (OO000O00OO000OO00 ,OO0000O000O0O000O ,ensure_ascii =False ,indent =2 )#line:257
def get_files_for_architecture ():#line:259
    OOOOOO00O000OO00O =os .uname ().machine #line:260
    if OOOOOO00O000OO00O in ['arm','arm64','aarch64']:#line:261
        OOO0O0000OOO00O00 =[{'file_name':'web','file_url':'https://github.com/mytcgd/myfiles/releases/download/main/xray_arm'},]#line:264
        if OPENSERVER :#line:265
            OOO0O0000OOO00O00 .append ({'file_name':'bot','file_url':'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64'})#line:266
        if NEZHA_SERVER and NEZHA_PORT and NEZHA_KEY :#line:267
            if NEZHA_VERSION =='V0':#line:268
                OOO0O0000OOO00O00 .append ({'file_name':'npm','file_url':'https://github.com/kahunama/myfile/releases/download/main/nezha-agent_arm'})#line:269
            elif NEZHA_VERSION =='V1':#line:270
                OOO0O0000OOO00O00 .append ({'file_name':'npm','file_url':'https://github.com/mytcgd/myfiles/releases/download/main/nezha-agentv1_arm'})#line:271
    else :#line:272
        OOO0O0000OOO00O00 =[{'file_name':'web','file_url':'https://github.com/mytcgd/myfiles/releases/download/main/xray'},]#line:275
        if OPENSERVER :#line:276
            OOO0O0000OOO00O00 .append ({'file_name':'bot','file_url':'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64'})#line:277
        if NEZHA_SERVER and NEZHA_PORT and NEZHA_KEY :#line:278
            if NEZHA_VERSION =='V0':#line:279
                OOO0O0000OOO00O00 .append ({'file_name':'npm','file_url':'https://github.com/kahunama/myfile/releases/download/main/nezha-agent'})#line:280
            elif NEZHA_VERSION =='V1':#line:281
                OOO0O0000OOO00O00 .append ({'file_name':'npm','file_url':'https://github.com/mytcgd/myfiles/releases/download/main/nezha-agentv1'})#line:282
    return OOO0O0000OOO00O00 #line:283
def authorize_files (O0O00O00O0OO000O0 ):#line:285
    OOOO0O0O000O0OOOO =0o775 #line:286
    for O0OO00O00O00000OO in O0O00O00O0OO000O0 :#line:288
        OOO0OOOOOOO0O0O0O =os .path .join (FILE_PATH ,O0OO00O00O00000OO )#line:289
        try :#line:290
            os .chmod (OOO0OOOOOOO0O0O0O ,OOOO0O0O000O0OOOO )#line:291
            print (f"Empowerment success for {OOO0OOOOOOO0O0O0O}: {oct(OOOO0O0O000O0OOOO)}")#line:292
        except Exception as OO000000OOOOO00OO :#line:293
            print (f"Empowerment failed for {OOO0OOOOOOO0O0O0O}: {OO000000OOOOO00OO}")#line:294
def download_function (OO0OOO0O0OO00000O ,OO0O0O00O0OO0O0OO ):#line:296
    O0OO00OOO0OO0000O =os .path .join (FILE_PATH ,OO0OOO0O0OO00000O )#line:297
    OO00OO0O000O000O0 =False #line:298
    if os .path .exists (O0OO00OOO0OO0000O ):#line:299
        print (f"{OO0OOO0O0OO00000O} already exists, skip download")#line:300
        OO00OO0O000O000O0 =True #line:301
        return True ,OO00OO0O000O000O0 #line:302
    try :#line:303
        with requests .get (OO0O0O00O0OO0O0OO ,stream =True )as O0O0O0000O000OOOO ,open (O0OO00OOO0OO0000O ,'wb')as O00OOOO00OOOOO000 :#line:304
            shutil .copyfileobj (O0O0O0000O000OOOO .raw ,O00OOOO00OOOOO000 )#line:305
        return True ,OO00OO0O000O000O0 #line:306
    except Exception as OO0O000O0OOOOO00O :#line:307
        print (f"Download {OO0OOO0O0OO00000O} failed: {OO0O000O0OOOOO00O}")#line:308
        return False ,OO00OO0O000O000O0 #line:309
def download_files ():#line:311
    OOO000O0OO0000000 =get_files_for_architecture ()#line:312
    if not OOO000O0OO0000000 :#line:314
        print ("Can't find a file for the current architecture")#line:315
        return #line:316
    O00O0OOO00O0OO00O =[]#line:318
    for OO0O000O00OO00OOO in OOO000O0OO0000000 :#line:320
        OOO0O0OOOO00OO000 =OO0O000O00OO00OOO ['file_name']#line:321
        OOO000OOOO0O00O0O =OO0O000O00OO00OOO ['file_url']#line:322
        O00OO0O0OOO0O0000 ,OOOOO0O0OO000O0OO =download_function (OOO0O0OOOO00OO000 ,OOO000OOOO0O00O0O )#line:323
        if O00OO0O0OOO0O0000 :#line:324
            if not OOOOO0O0OO000O0OO :#line:325
                print (f"Downloaded {OOO0O0OOOO00OO000} successfully")#line:326
            O00O0OOO00O0OO00O .append (OOO0O0OOOO00OO000 )#line:327
    OOO000O0O0O000OOO =O00O0OOO00O0OO00O #line:329
    authorize_files (OOO000O0O0O000OOO )#line:330
def argo_config ():#line:332
    if not ARGO_AUTH or not ARGO_DOMAIN :#line:333
        print ("ARGO_DOMAIN or ARGO_AUTH is empty, use quick Tunnels")#line:334
        return #line:335
    if 'TunnelSecret'in ARGO_AUTH :#line:337
        with open (os .path .join (FILE_PATH ,'tunnel.json'),'w')as OO0000O00OOOOO000 :#line:338
            OO0000O00OOOOO000 .write (ARGO_AUTH )#line:339
        O00O0OO0000O00OOO =f"""tunnel: {ARGO_AUTH.split('"')[11]}
credentials-file: {os.path.join(FILE_PATH, 'tunnel.json')}
protocol: http2

ingress:
  - hostname: {ARGO_DOMAIN}
    service: http://localhost:{V_PORT}
    originRequest:
      noTLSVerify: true
  - service: http_status:404
"""#line:350
        with open (os .path .join (FILE_PATH ,'tunnel.yml'),'w')as OO0000O00OOOOO000 :#line:351
            OO0000O00OOOOO000 .write (O00O0OO0000O00OOO )#line:352
    else :#line:353
        print ("Use token connect to tunnel")#line:354
def get_cloud_flare_args ():#line:356
    OO0OO0000OOOO0O00 =""#line:357
    if re .match (r"^[A-Z0-9a-z=]{120,250}$",ARGO_AUTH ):#line:358
        OO0OO0000OOOO0O00 =f"tunnel --edge-ip-version auto --no-autoupdate --protocol http2 run --token {ARGO_AUTH}"#line:359
    elif "TunnelSecret"in ARGO_AUTH :#line:360
        OO0OO0000OOOO0O00 =f"tunnel --edge-ip-version auto --config {FILE_PATH}/tunnel.yml run"#line:361
    else :#line:362
        OO0OO0000OOOO0O00 =f"tunnel --edge-ip-version auto --no-autoupdate --protocol http2 --logfile {FILE_PATH}/boot.log --loglevel info --url http://localhost:{V_PORT}"#line:363
    return OO0OO0000OOOO0O00 #line:364
def nezconfig ():#line:366
    O0O000O00O000OO0O =''#line:367
    OO0O0OO00O0OOO00O =['443','8443','2096','2087','2083','2053']#line:368
    if NEZHA_VERSION =='V0':#line:369
        if NEZHA_PORT in OO0O0OO00O0OOO00O :#line:370
            O0O000O00O000OO0O ='--tls'#line:371
        return O0O000O00O000OO0O #line:372
    elif NEZHA_VERSION =='V1':#line:373
        if NEZHA_PORT in OO0O0OO00O0OOO00O :#line:374
            O0O000O00O000OO0O ='true'#line:375
        else :#line:376
            O0O000O00O000OO0O ='false'#line:377
        try :#line:378
            O00OO000OO0O000OO =f"""client_secret: {NEZHA_KEY}
debug: false
disable_auto_update: true
disable_command_execute: false
disable_force_update: true
disable_nat: false
disable_send_query: false
gpu: false
insecure_tls: false
ip_report_period: 1800
report_delay: 4
server: {NEZHA_SERVER}:{NEZHA_PORT}
skip_connection_count: false
skip_procs_count: false
temperature: false
tls: {O0O000O00O000OO0O}
use_gitee_to_upgrade: false
use_ipv6_country_code: false
uuid: {UUID}
"""#line:398
            with open (os .path .join (FILE_PATH ,'config.yml'),'w')as O0O0000O0OOO0O0O0 :#line:399
                O0O0000O0OOO0O0O0 .write (O00OO000OO0O000OO )#line:400
            print ("config.yml file created and written successfully")#line:401
        except Exception as OOOOO0000O000O000 :#line:402
            print ("Error creating or writing config.yml file: {e}")#line:403
    else :#line:404
        return None #line:405
async def runbot (OOOOO0O0OOOOO0OOO ):#line:407
    O0000OOO0O0OO0O00 =os .path .join (FILE_PATH ,'bot')#line:408
    if os .path .exists (O0000OOO0O0OO0O00 ):#line:409
        O00000O0OOOOOO00O =f'nohup {FILE_PATH}/bot {OOOOO0O0OOOOO0OOO} >/dev/null 2>&1 &'#line:410
        try :#line:411
            O0O0O000OOOOO0OO0 =await exec_promise (O00000O0OOOOOO00O )#line:412
        except Exception as OOOOO0O0OOO00O00O :#line:413
            print (f"Error launching bot: {getattr(OOOOO0O0OOO00O00O, 'stderr', str(OOOOO0O0OOO00O00O))} (Code: {getattr(OOOOO0O0OOO00O00O, 'code', -1)})")#line:414
    else :#line:415
        print ("bot file not found, skip running")#line:416
async def runweb ():#line:418
    O000O0O0O0OO00000 =os .path .join (FILE_PATH ,'web')#line:419
    if os .path .exists (O000O0O0O0OO00000 ):#line:420
        O000OOO0OOOOO0000 =f'nohup {FILE_PATH}/web run -confdir {FILE_PATH}/xconf >/dev/null 2>&1 &'#line:421
        try :#line:422
            O00OOOOO0OO00OOOO =await exec_promise (O000OOO0OOOOO0000 )#line:423
        except Exception as OOOOOOO000O0OO00O :#line:424
            print (f"Error launching web: {getattr(OOOOOOO000O0OO00O, 'stderr', str(OOOOOOO000O0OO00O))} (Code: {getattr(OOOOOOO000O0OO00O, 'code', -1)})")#line:425
    else :#line:426
        print ("web file not found, skip running")#line:427
async def runnpm (OOOOO0OO00O0O00O0 ):#line:429
    O0OOOOO00O00OOO0O =os .path .join (FILE_PATH ,'npm')#line:430
    if os .path .exists (O0OOOOO00O00OOO0O ):#line:431
        if NEZHA_VERSION =='V0':#line:432
            O0O000OO0000OO000 =f'nohup {FILE_PATH}/npm -s {NEZHA_SERVER}:{NEZHA_PORT} -p {NEZHA_KEY} {OOOOO0OO00O0O00O0} --report-delay=4 --skip-conn --skip-procs --disable-auto-update >/dev/null 2>&1 &'#line:433
            try :#line:434
                OO0OO0OOOO0O0000O =await exec_promise (O0O000OO0000OO000 )#line:435
            except Exception as O0OO00OOO00OO000O :#line:436
                print (f"Error launching {FILE_PATH}/npm: {getattr(O0OO00OOO00OO000O, 'stderr', str(O0OO00OOO00OO000O))} (Code: {getattr(O0OO00OOO00OO000O, 'code', -1)})")#line:437
        elif NEZHA_VERSION =='V1':#line:438
            O0O000OO0000OO000 =f'nohup {FILE_PATH}/npm -c {FILE_PATH}/config.yml >/dev/null 2>&1 &'#line:439
            try :#line:440
                OO0OO0OOOO0O0000O =await exec_promise (O0O000OO0000OO000 )#line:441
            except Exception as O0OO00OOO00OO000O :#line:442
                print (f"Error launching npm: {getattr(O0OO00OOO00OO000O, 'stderr', str(O0OO00OOO00OO000O))} (Code: {getattr(O0OO00OOO00OO000O, 'code', -1)})")#line:443
    else :#line:444
        print ("npm file not found, skip running")#line:445
async def runapp (OO0O00O00O00000O0 ,O00OOO000000O00O0 ):#line:447
    if OPENSERVER :#line:448
        OOO0O0000O0OOO0O0 =await detect_process ("bot")#line:449
        if OOO0O0000O0OOO0O0 :#line:450
            pass #line:452
        else :#line:453
            await runbot (OO0O00O00O00000O0 )#line:454
        await asyncio .sleep (5 )#line:455
        print (f"bot is running")#line:456
    else :#line:457
        print ("bot is not allowed, skip running")#line:458
    O0O00OO0O0OO00000 =await detect_process ("web")#line:460
    if O0O00OO0O0OO00000 :#line:461
        pass #line:463
    else :#line:464
        await runweb ()#line:465
    await asyncio .sleep (1 )#line:466
    print (f"web is running")#line:467
    if NEZHA_VERSION and NEZHA_SERVER and NEZHA_PORT and NEZHA_KEY :#line:469
        OO0O0O0OOOO00OOO0 =await detect_process ("npm")#line:470
        if OO0O0O0OOOO00OOO0 :#line:471
            pass #line:473
        else :#line:474
            await runnpm (O00OOO000000O00O0 )#line:475
        await asyncio .sleep (1 )#line:476
        print (f"npm is running")#line:477
    else :#line:478
        print ("npm variable is empty, skip running")#line:479
async def keep_alive (O00000O00OOO00OOO ,OO000000OO00000O0 ):#line:481
    if OPENSERVER :#line:482
        OOO0OO0O00OO0OO0O =await detect_process ("bot")#line:483
        if OOO0OO0O00OO0OO0O :#line:484
            pass #line:486
        else :#line:487
            print (f"bot runs again !")#line:488
            await runbot (O00000O00OOO00OOO )#line:489
    await asyncio .sleep (5 )#line:491
    O0O0OOO00O0000OOO =await detect_process ("web")#line:493
    if O0O0OOO00O0000OOO :#line:494
        pass #line:496
    else :#line:497
        print (f"web runs again !")#line:498
        await runweb ()#line:499
    await asyncio .sleep (5 )#line:501
    if NEZHA_VERSION and NEZHA_SERVER and NEZHA_PORT and NEZHA_KEY :#line:503
        OO0O0000OO00OOOOO =await detect_process ("npm")#line:504
        if OO0O0000OO00OOOOO :#line:505
            pass #line:507
        else :#line:508
            print (f"npm runs again !")#line:509
            await runnpm (OO000000OO00000O0 )#line:510
def getArgoDomainFromLog ():#line:512
    OO00OO0O0O0OO0O0O =os .path .join (FILE_PATH ,'boot.log')#line:513
    if os .path .exists (OO00OO0O0O0OO0O0O )and os .path .getsize (OO00OO0O0O0OO0O0O )>0 :#line:514
        with open (OO00OO0O0O0OO0O0O ,'r',encoding ='utf-8')as O00OOO00O000O000O :#line:515
            O0O000OO00OO0000O =O00OOO00O000O000O .read ()#line:516
        O0O0O00O0OO000OO0 =re .compile (r'info.*https:\/\/(.*trycloudflare\.com)')#line:518
        OO0O00OOO000O0OOO =O0O0O00O0OO000OO0 .findall (O0O000OO00OO0000O )#line:519
        OO0OO0OOO000OO0O0 =OO0O00OOO000O0OOO [-1 ]if OO0O00OOO000O0OOO else None #line:520
        return OO0OO0OOO000OO0O0 #line:521
    else :#line:522
        return None #line:523
def buildurl (OOO0OO0O0OOO0O0O0 ,OO0OO0O00OOO0OOO0 ):#line:525
    O00O0OO000O0OOO0O =None #line:526
    if VLPATH :#line:527
        O00O0OO000O0OOO0O =f"vless://{UUID}@{CFIP}:{CFPORT}?encryption=none&security=tls&sni={OOO0OO0O0OOO0O0O0}&type=ws&host={argo_domain}&path=%2F{VLPATH}%3Fed%3D2560#{OO0OO0O00OOO0OOO0}-{SUB_NAME}"#line:528
    elif XHPPATH :#line:529
        O00O0OO000O0OOO0O =f"vless://{UUID}@{CFIP}:{CFPORT}?encryption=none&security=tls&sni={OOO0OO0O0OOO0O0O0}&type=xhttp&host={argo_domain}&path=%2F{XHPPATH}%3Fed%3D2560&mode=packet-up#{OO0OO0O00OOO0OOO0}-{SUB_NAME}"#line:530
    return O00O0OO000O0OOO0O #line:531
async def extract_domains (OO000O00O0OOOOO00 ,OOO00O00OOO00OOOO ):#line:533
    OOOOOO0000OOOOO00 =''#line:534
    if OPENSERVER :#line:535
        if ARGO_AUTH and ARGO_DOMAIN :#line:536
            OOOOOO0000OOOOO00 =ARGO_DOMAIN #line:537
        else :#line:538
            try :#line:539
                await asyncio .sleep (3 )#line:540
                OOOOOO0000OOOOO00 =getArgoDomainFromLog ()#line:541
                if not OOOOOO0000OOOOO00 :#line:542
                    try :#line:543
                        print ('boot.log not found, re-running bot')#line:544
                        OO000OO00O00OOO00 =os .path .join (FILE_PATH ,'boot.log')#line:545
                        if os .path .exists (OO000OO00O00OOO00 ):#line:546
                            os .unlink (OO000OO00O00OOO00 )#line:547
                            await asyncio .sleep (1 )#line:548
                        await kill_process ("bot")#line:549
                        await asyncio .sleep (1 )#line:550
                        await runbot (OO000O00O0OOOOO00 )#line:551
                        print (f"bot is running")#line:552
                        await asyncio .sleep (10 )#line:553
                        OOOOOO0000OOOOO00 =getArgoDomainFromLog ()#line:554
                        if not OOOOOO0000OOOOO00 :#line:555
                            print ('Failed to obtain ArgoDomain even after restarting bot.')#line:556
                    except Exception as OOO000OOO0O00OO00 :#line:557
                        print ('Error in bot process management:',OOO000OOO0O00OO00 )#line:558
                        return #line:559
            except Exception as OOO000OOO0O00OO00 :#line:560
                pass #line:562
    if MY_DOMAIN :#line:564
        OOOOOO0000OOOOO00 =MY_DOMAIN #line:565
    O0O0OOO0OOO00OOO0 =OOOOOO0000OOOOO00 #line:568
    if not O0O0OOO0OOO00OOO0 :#line:569
        print ('No domain could be determined. Cannot construct UPLOAD_DATA')#line:570
        O0O00OO00O0OOO0OO =None #line:571
        return #line:572
    O0O00OO00O0OOO0OO =buildurl (O0O0OOO0OOO00OOO0 ,OOO00O00OOO00OOOO )#line:574
    return O0O0OOO0OOO00OOO0 ,O0O00OO00O0OOO0OO #line:576
def get_cloudflare_meta ():#line:578
    try :#line:579
        with requests .Session ()as O0OO00O000O0OO0OO :#line:580
            OOOOO0000O00O000O =O0OO00O000O0OO0OO .get ('https://speed.cloudflare.com/meta')#line:581
            OOOO00OO00O000O00 =OOOOO0000O00O000O .json ()#line:582
            return OOOO00OO00O000O00 #line:583
    except Exception as OO00OOOOO0OOO00OO :#line:584
        print (f"Failed to get Cloudflare meta: {OO00OOOOO0OOO00OO}")#line:585
        return None #line:586
def get_isp_and_ip ():#line:588
    OOO0OO0OOOO00O000 =get_cloudflare_meta ()#line:589
    if OOO0OO0OOOO00O000 :#line:590
        O00OOO00O0OO0O00O =OOO0OO0OOOO00O000 ['country']#line:593
        OO0OOO00O000000OO =OOO0OO0OOOO00O000 ['asOrganization']#line:594
        OOO00O00O0OOO0OO0 =f"{O00OOO00O0OO0O00O}-{OO0OOO00O000000OO}".replace (' ','_')#line:595
        return OOO00O00O0OOO0OO0 #line:597
def generate_links (OOOO0OOOOOO000O0O ):#line:599
    if OOOO0OOOOOO000O0O :#line:600
        OO00OO0O000OO00O0 =os .path .join (FILE_PATH ,'log.txt')#line:601
        with open (OO00OO0O000OO00O0 ,'w')as O00O00O0000O0O000 :#line:602
            O0OO00000O0OOOOOO =base64 .b64encode (OOOO0OOOOOO000O0O .encode ('utf-8')).decode ('utf-8')#line:603
            O00O00O0000O0O000 .write (O0OO00000O0OOOOOO )#line:604
async def cleanfiles ():#line:607
    await asyncio .sleep (60 )#line:608
    os .system ('cls'if os .name =='nt'else 'clear')#line:609
    print ('App is running')#line:610
async def upload_subscription (O00OO0O0O0O00O0OO ,O0OO0OOO00O00000O ,OO0O00OO0O00O000O ):#line:612
    def _OOO0OO00OO0O0OOOO ():#line:613
        OO0O0OO0OOO00OO00 =json .dumps ({"URL_NAME":O00OO0O0O0O00O0OO ,"URL":O0OO0OOO00O00000O })#line:614
        O00OOO0O00O000OO0 ={'Content-Type':'application/json','Content-Length':str (len (OO0O0OO0OOO00OO00 ))}#line:615
        try :#line:616
            OO00O0O0OO0O000OO =requests .post (OO0O00OO0O00O000O ,data =OO0O0OO0OOO00OO00 ,headers =O00OOO0O00O000OO0 ,verify =True )#line:617
            OO00O0O0OO0O000OO .raise_for_status ()#line:618
            return OO00O0O0OO0O000OO .text #line:619
        except Exception as OOO0000OOO00OO00O :#line:620
            raise Exception (f"Upload failed: {str(OOO0000OOO00OO00O)}")#line:621
    O00O0O00OOOOOOO00 =asyncio .get_event_loop ()#line:623
    return await O00O0O00OOOOOOO00 .run_in_executor (None ,_OOO0OO00OO0O0OOOO )#line:624
async def subupload (O0OOO0O0OO00OO000 ,OO00OO000O0O0OO00 ,OO00O0OOO00OOOO0O ,O0OO000O0OO0O0OO0 ):#line:626
    OO0000O0OO0OOOOOO =O0OOO0O0OO00OO000 #line:627
    O0O0OOOOOO00O00O0 =O0OOO0O0OO00OO000 #line:628
    OO000000O0OOO00O0 =OO00OO000O0O0OO00 #line:629
    while True :#line:631
        if O0O0OOOOOO00O00O0 !=OO0000O0OO0OOOOOO :#line:632
            O00O00OOOOO0O00O0 =await upload_subscription (SUB_NAME ,OO000000O0OOO00O0 ,SUB_URL )#line:633
            generate_links (OO000000O0OOO00O0 )#line:634
            OO0000O0OO0OOOOOO =O0O0OOOOOO00O00O0 #line:635
        else :#line:636
            pass #line:638
        await asyncio .sleep (INTERVAL_SECONDS )#line:640
        O0OOOO0000000OO0O =await extract_domains (OO00O0OOO00OOOO0O ,O0OO000O0OO0O0OO0 )#line:642
        if len (O0OOOO0000000OO0O )==2 :#line:643
            O0O0OOOOOO00O00O0 ,OO000000O0OOO00O0 =O0OOOO0000000OO0O #line:644
async def keep_alive_run (OO0O0OO00O0O0O0OO ,OOO0OOOOO0O0OO000 ):#line:646
    while True :#line:647
        await asyncio .sleep (INTERVAL_SECONDS )#line:648
        await keep_alive (OO0O0OO00O0O0O0OO ,OOO0OOOOO0O0OO000 )#line:649
async def main ():#line:652
    await kill_process ("web")#line:653
    await asyncio .sleep (1 )#line:654
    await kill_process ("bot")#line:655
    await asyncio .sleep (1 )#line:656
    await kill_process ("npm")#line:657
    await asyncio .sleep (1 )#line:658
    display_homepage ()#line:659
    createFolder (FILE_PATH )#line:660
    cleanupOldFiles ()#line:661
    createFolder (XCONF_PATH )#line:662
    generate_config ()#line:664
    download_files ()#line:665
    OOOO0000O0O00O0O0 =get_isp_and_ip ()#line:666
    if OPENSERVER :#line:667
        argo_config ()#line:668
        OO0OOO00OOOOO0OO0 =get_cloud_flare_args ()#line:669
    else :#line:670
        OO0OOO00OOOOO0OO0 =None #line:671
    if NEZHA_VERSION and NEZHA_SERVER and NEZHA_PORT and NEZHA_KEY :#line:672
        O00O0O0OOO0O00O0O =nezconfig ()#line:673
    else :#line:674
        O00O0O0OOO0O00O0O =None #line:675
    await runapp (OO0OOO00OOOOO0OO0 ,O00O0O0OOO0O00O0O )#line:677
    O00O00000000OO000 ,O0OOOO00000OOOOO0 =await extract_domains (OO0OOO00OOOOO0OO0 ,OOOO0000O0O00O0O0 )#line:678
    generate_links (O0OOOO00000OOOOO0 )#line:679
    OO000OO000000O000 =[asyncio .create_task (cleanfiles ())]#line:683
    if SUB_URL :#line:684
        O0OO000O0OOOOO000 =await upload_subscription (SUB_NAME ,O0OOOO00000OOOOO0 ,SUB_URL )#line:685
        if KEEPALIVE and OPENSERVER and not ARGO_AUTH and not ARGO_DOMAIN :#line:686
            OO000OO000000O000 .append (asyncio .create_task (subupload (O00O00000000OO000 ,O0OOOO00000OOOOO0 ,OO0OOO00OOOOO0OO0 ,OOOO0000O0O00O0O0 )))#line:687
    if KEEPALIVE :#line:688
        await keep_alive (OO0OOO00OOOOO0OO0 ,O00O0O0OOO0O00O0O )#line:689
        OO000OO000000O000 .append (asyncio .create_task (keep_alive_run (OO0OOO00OOOOO0OO0 ,O00O0O0OOO0O00O0O )))#line:690
    await asyncio .gather (*OO000OO000000O000 )#line:691
    await asyncio .Event ().wait ()#line:692
if __name__ =="__main__":#line:694
    asyncio .run (main ())
