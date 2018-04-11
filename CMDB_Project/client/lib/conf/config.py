"""
整合用户配置文件和内置配置文件
"""
import os
import importlib
from . import global_settings


class Settings(object):
    def __init__(self):
        ######## 找到默认内置配置文件 ########
        for name in dir(global_settings):
            if name.isupper():
                value = getattr(global_settings, name)  # 反射获得模块中的属性值
                setattr(self, name, value)  # 为传入的参数对象添加该属性名及属性值

        # ######## 找到自定义配置 ########
        # 根据字符串导入模块
        settings_module = os.environ.get('USER_SETTINGS')  # 获得环境变量（内存）中的自定义配置文件的路径值
        if not settings_module:
            return

        custom_settings = importlib.import_module(settings_module)  # 根据字符串导入应对的模块
        for name in dir(custom_settings):
            if name.isupper():
                value = getattr(custom_settings, name)
                setattr(self, name, value)


settings = Settings()  # 将实例化的对象作为属性值
