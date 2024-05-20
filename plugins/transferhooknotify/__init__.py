from app.plugins import _PluginBase
from typing import Any, List, Dict, Tuple, Optional
from app.log import logger
from app.schemas import NotificationType
from app import schemas
from app.core.config import settings
from pydantic import BaseModel

class notifyInfo(BaseModel):
    apikey: str
    text: str
    title: Optional[str] = "webhook通知"
    
class TransferHookNotify(_PluginBase):
    # 插件名称
    plugin_name = "转发webhook通知"
    # 插件描述
    plugin_desc = "接收webhook通知并推送。(基于SynologyNotify二次开发)"
    # 插件图标
    plugin_icon = "webhook.png"
    # 插件版本
    plugin_version = "1.0.1"
    # 插件作者
    plugin_author = "thsrite,tk"
    # 作者主页
    author_url = "https://github.com/arnonoyo"
    # 插件配置项ID前缀
    plugin_config_prefix = "transferhooknotify_"
    # 加载顺序
    plugin_order = 30
    # 可使用的用户级别
    auth_level = 1

    # 任务执行间隔
    _enabled = False
    _notify = False

    def init_plugin(self, config: dict = None):
        if config:
            self._enabled = config.get("enabled")
            self._notify = config.get("notify")

    def send_notify_get(self, apikey: str, text: str, title: str = 'webhook通知') -> schemas.Response:
        return self.send_notify(apikey, text, title)

    def send_notify_post(self, data: notifyInfo) -> schemas.Response:
        return self.send_notify(data.apikey, data.text, data.title)

    def send_notify(self, apikey: str, text: str, title: str = 'webhook通知') -> schemas.Response:
        if apikey != settings.API_TOKEN:
            return schemas.Response(success=False, message="API密钥错误")
        
        logger.info(f"webhook: {text}")

        if self._enabled:
            text = text.replace('\r\n', '\n')
            self.post_message(title=title,
                              mtype=NotificationType.Manual,
                              text=text)

        return schemas.Response(
            success=True,
            message="发送成功"
        )
    

    def get_state(self) -> bool:
        return self._enabled

    @staticmethod
    def get_command() -> List[Dict[str, Any]]:
        pass

    def get_api(self) -> List[Dict[str, Any]]:
        """
        获取插件API
        [{
            "path": "/xx",
            "endpoint": self.xxx,
            "methods": ["GET", "POST"],
            "summary": "API说明"
        }]
        """
        return [
        {
            "path": "/webhook",
            "endpoint": self.send_notify_get,
            "methods": ["GET"],
            "summary": "转发Webhook通知",
            "description": "接收webhook通知并推送",
        },
        {
            "path": "/webhook",
            "endpoint": self.send_notify_post,
            "methods": ["POST"],
            "summary": "转发Webhook通知",
            "description": "接收webhook通知并推送",
        }]

    def get_form(self) -> Tuple[List[dict], Dict[str, Any]]:
        """
        拼装插件配置页面，需要返回两块数据：1、页面配置；2、数据结构
        """
        return [
            {
                'component': 'VForm',
                'content': [
                    {
                        'component': 'VRow',
                        'content': [
                            {
                                'component': 'VCol',
                                'props': {
                                    'cols': 12,
                                    'md': 6
                                },
                                'content': [
                                    {
                                        'component': 'VSwitch',
                                        'props': {
                                            'model': 'enabled',
                                            'label': '启用插件',
                                        }
                                    }
                                ]
                            },
                            {
                                'component': 'VCol',
                                'props': {
                                    'cols': 12,
                                    'md': 6
                                },
                                'content': [
                                    {
                                        'component': 'VSwitch',
                                        'props': {
                                            'model': 'notify',
                                            'label': '开启通知',
                                        }
                                    }
                                ]
                            },
                        ]
                    },
                    {
                        'component': 'VRow',
                        'content': [
                            {
                                'component': 'VCol',
                                'props': {
                                    'cols': 12,
                                },
                                'content': [
                                    {
                                        'component': 'VAlert',
                                        'props': {
                                            'type': 'info',
                                            'variant': 'tonal',
                                            'text': 'webhook配置http://ip:3001/api/v1/plugin/TransferHookNotify/webhook?title=自定义标题&text=hello world。'
                                                    'title参数类型是标题内容，text参数类型是消息内容，更多内容查看github。此插件安装完需要重启生效api。消息类型默认为手动处理通知。'
                                        }
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        'component': 'VRow',
                        'content': [
                            {
                                'component': 'VCol',
                                'props': {
                                    'cols': 12,
                                },
                                'content': [
                                    {
                                        'component': 'VAlert',
                                        'props': {
                                            'type': 'info',
                                            'variant': 'tonal',
                                            'text': '如安装完插件后，发送webhook提示404，重启MoviePilot即可。'
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ], {
            "enabled": False,
            "notify": False
        }

    def get_page(self) -> List[dict]:
        pass

    def stop_service(self):
        """
        退出插件
        """
        pass