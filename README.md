# MoviePilot-Plugins
## 1. 转种插件
  基于官方插件TorrentTransfer二次开发
- 支持自定义下载器
## 2. 转发webhook通知插件
基于SynologyNotify二次开发
- 支持自定义通知标题
- 支持post

>3001端口为mp配置中的PORT（即API端口）  
>安装插件后访问该接口，若提示404/405，重启MoviePilot即可

### 用法
get: 
``` 
http://{ip}:3001/api/v1/plugin/TransferHookNotify/webhook?apikey={API_TOKEN}&title=自定义标题&text=内容
```

post:
```
http://{ip}:3001/api/v1/plugin/TransferHookNotify/postwebhook

{
    "apikey": {API_TOKEN},
    "title": "自定义标题",
    "text": "内容"
}
```
### 场景
- apprise自定义通知，通过该插件将请求转发到mp应用中
  - Configuration配置: `json://{ip}:3001/api/v1/plugin/TransferHookNotify/postwebhook?:apikey={API_TOKEN}&:version&:type&:message=text`