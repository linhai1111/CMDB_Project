from lib.conf.config import settings
from .client import Agent
from .client import SSHSALT

def run():
    """

    :param object:
    :return:
    """
    if settings.MODE == 'AGENT':
        obj = Agent()
    else:
        obj = SSHSALT()
    obj.excute()


