import requests
from lib.conf.config import settings
from src.plugins import PluginManager
import json
class Base(object):
    """
    往api发送数据
    """
    def post_asset(self, server_info):
        # 将数据转换成json字符串格式发送
        requests.post(settings.API, json=server_info)   # 数据封装在body中: 会在源码中自动转换 json.dumps(server_info)
        # headers= {'content-type':'application/json'}
        # request.body   # 需从body中取出数据
        # json.loads(request.body)

class Agent(Base):
    """
    agent方式采集数据并提交到api
    """
    def excute(self):
        servier_info = PluginManager.exec_plugin()
        self.post_asset(servier_info)   # 子类对象调用父类方法来发送数据

class SSHSALT(Base):
        """
        针对SSH方式和SALT方式采集数据和发送
        """
        def get_host(self): # 先获取未采集过数据的主机列表
            response = requests.get(settings.API)
            result = json.load(response.text)   # "{status:'True',data: ['c1.com','c2.com']}"
            if result['status']:
                return None
            return result['data']

        def excute(self):
            host_list = self.get_host()
            for host in host_list:
                server_info = PluginManager.exec_plugin(host).exec_plugin() # 该两种采集方式都需传入主机host信息
                self.post_asset(server_info)
