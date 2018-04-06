class Basic:
    """
    获取服务器基本信息（服务器名称...）
    """

    def __init__(self):
        pass

    @classmethod
    def inital(cls):  # 定义类方法，用于扩展，在执行init方法时提前执行的扩展方法
        return cls()

    def process(self, command_func, debug):
        if debug:  # 用于在windows环境下的测试
            output = {
                'os_platform': "linux",
                'os_version': "CentOS release 6.6 (Final)\nKernel \r on an \m",
                'hostname': 'c1.com'
            }
        else:  # 在linux系统下执行的命令
            output = {
                'os_platform': command_func("uname").strip(),  # 采集系统名称
                'os_version': command_func("cat /etc/issue").strip().split('\n')[0],  # 采集系统版本
                'hostname': command_func("hostname").strip(),  # 采集系统版本名称
            }
        return output
