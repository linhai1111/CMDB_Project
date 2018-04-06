"""
用户自定义配置文件
"""
USER = 'lh' # 服务器登陆信息
PWD = '152303832'

import os
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ##############插件所需的配置参数################
MODE = 'AGENT'  # 采用agent模式采集服务器信息
# MODE = 'SALT'  # 采用salt模式采集服务器信息
# MODE = 'SSH'  # 采用SSH模式采集服务器信息

DEBUG = True

SSH_USER = 'root'   # 连接远程服务器的用户名
SSH_PWD = 'root'    # 连接远程服务器的密码
SSH_KEY = '/XX/XX/XX'   # 通过公钥私钥来连接远程服务器实现免密登陆
SSH_PORT = 22

PLUGINS_DICT ={     # 插件字典，通过字符串导入模块
    'basic':'src.plugins.basic.Basic',
    'board':'src.plugins.basic.Board',
    'cpu':'src.plugins.basic.Cpu',
    'disk':'src.plugins.basic.Disk',
    'memory':'src.plugins.basic.Memory',
    'nic':'src.plugins.basic.Nic',
}


# api接口 url地址
API = "http://www.oldboyedu.com"