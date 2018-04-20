import requests
from lib.conf.config import settings
from src.plugins import PluginManager
import json
from concurrent.futures import ThreadPoolExecutor
from lib.utils import encrypt
from lib.utils import auth

class Base(object):
    """
    负责往api发送数据
    """

    def post_asset(self, server_info):
        # 将数据转换成json字符串格式发送
        data = encrypt(json.dumps(server_info))    # 将字典格式的数据转换成encrypt所需的字符串格式,然后加密
        response = requests.post(
            url=settings.API,
            data = data,
            headers={'OpenKey':auth(), 'Content-Type':'application/json'}   # 
        )
        print(response.text)
    
class Agent(Base):
    """
    用agent方式采集数据并提交到api
    """

    def excute(self):
        servier_info = PluginManager().exec_plugin()  # 采集数据

        # 唯一标识符处理
        hostname = servier_info['basic']['data']['hostname']  # 获得主机名，用来验证唯一标识符
        certname = open(settings.CERT_PATH, 'r', encoding='utf-8').read().strip()  # 获得服务器上的文件中的主机名
        if not certname:
            with open(settings.CERT_PATH, 'w', encoding='utf-8') as f:  # 如果文件中不存在该主机名，表示该主机名未初始化，写入文件即可
                f.write(hostname)
        else:
            # 用文件中的主机名覆盖被用户修改过的主机名，防止出现主机重复导致数量叠加错误
            servier_info['basic']['data']['hostname'] = certname

        self.post_asset(servier_info)  # 子类对象调用父类方法来发送数据


class SSHSALT(Base):
    """
    用SSH方式和SALT方式采集数据和发送
    """

    def get_host(self):  # 该方式先获取未采集过数据的主机列表
        response = requests.get(settings.API)
        result = json.load(response.text)  # "{status:'True',data: ['c1.com','c2.com']}"
        if result['status']:
            return None
        return result['data']

    # 执行服务器信息采集，并将该信息发送给API
    def run(self, host):
        server_info = PluginManager(host).exec_plugin()  # 该两种采集方式都需传入主机host信息
        self.post_asset(server_info)

    # 基于线程池实现并发采集资产
    def excute(self):
        host_list = self.get_host()
        # 开启线程池并发任务，一次使用10个线程同时完成任务即可，多了会占用更多的系统资源
        pool = ThreadPoolExecutor(10)
        for host in host_list:
            pool.submit(self.run, host)  # 提交要执行的任务及对应的参数
