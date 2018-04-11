import os
import sys

# 程序启动入口文件
os.environ['USER_SETTINGS'] = "config.settings"  # 将用户级别的配置文件路径添加到环境变量中

from lib.conf.config import settings  # 备注：需要将该导入放置在添加环境变量语句后面，否则报错

# print(settings.USER)

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASEDIR)

from src import script

if __name__ == '__main__':
    script.run()
