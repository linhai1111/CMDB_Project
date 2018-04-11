from lib.conf.config import settings
from .client import Agent
from .client import SSHSALT


def run():
    """
    根据配置文件中的内容选择不同的采集方式
    :param object:
    :return:
    """
    if settings.MODE == 'AGENT':
        obj = Agent()
    else:
        obj = SSHSALT()
    obj.excute()
