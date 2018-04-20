"""
用户自定义的配置文件
"""
USER = 'lh'  # 服务器登陆信息
PWD = '152303832'

import os

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ##############插件所需的配置参数################
MODE = 'AGENT'  # 采用agent模式采集服务器信息
# MODE = 'SALT'  # 采用salt模式采集服务器信息
# MODE = 'SSH'  # 采用SSH模式采集服务器信息

DEBUG = True

SSH_USER = 'root'  # 连接远程服务器的用户名
SSH_PWD = 'root'  # 连接远程服务器的密码
SSH_KEY = '/XX/XX/XX'  # 通过公钥私钥来连接远程服务器实现免密登陆
SSH_PORT = 22

PLUGINS_DICT = {  # 插件字典，通过字符串导入模块
    'basic': "src.plugins.basic.Basic",
    'board': "src.plugins.board.Board",
    'cpu': "src.plugins.cpu.Cpu",
    'disk': "src.plugins.disk.Disk",
    'memory': "src.plugins.memory.Memory",
    'nic': "src.plugins.nic.Nic",
}

# api接口 url地址
# API = "http://www.oldboyedu.com"
API = "http://127.0.0.1:8000/api/asset.html"

# 用于服务器唯一标识符，防止服务器数量出现叠加错误
CERT_PATH = os.path.join(BASEDIR, 'config', 'cert')

DATA_KEY = b'dfdsdfsasdfdsdfs'  # AES加密和解密所需的Key