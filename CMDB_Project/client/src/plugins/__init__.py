from lib.conf.config import settings
import importlib
import traceback

class PluginManager(object):
    def __init__(self, hostname=None):  # 为agent/salt模式预留的主机名参数值
        self.hostname = hostname
        self.plugin_dict = settings.PLUGINS_DICT

        self.mode = settings.MODE   # 采集模式
        self.debug = settings.DEBUG
        if self.mode == 'SSH':
            self.ssh_user = settings.SSH_USER
            self.ssh_port = settings.SSH_PORT
            self.ssh_pwd = settings.SSH_PWD
            self.ssh_key = settings.SSH_KEY

    def exec_plugin(self):
        """
        获取所有插件，并执行插件中的方法获得返回值
        :return:
        """
        response = {}
        for k,v in self.plugin_dict.items():
         #  'basic': "src.plugins.basic.Basic",
            ret={'stauts':True, 'data':None}
            try:
                module_path, class_name = v.rsplit('.',1)   # 切分字符串获得模块路径和类名
                m = importlib.import_module(module_path)    # 根据字符串获得模块
                cls = getattr(m, class_name)    # 通过类名字符串，反射获得模块中的类
                if hasattr(cls, 'initial'):
                    obj = cls.initial()
                else:
                    obj = cls()
                result = obj.process(self.command,self.debug)   # result = "根据v获取类，并执行其方法采集资产"
                ret['data'] = result
            except Exception as e:
                ret['stauts']=False
                # traceback.format_exc()获得具体的错误信息   k表示插件名称
                ret['data']='[%s][%s]采集数据出现错误：%s'%(self.hostname if self.hostname else 'AGENT', k, traceback.format_exc())
            response[k]= ret
        return response


######判断采集方法############
    def command(self, cmd):
        if self.mode == 'AGENT':
            return self.__agent(cmd)
        elif self.mode == 'SSH':
            return self.__ssh(cmd)
        elif self.mode == 'SALT':
            return self.__salt(cmd)
        else:
            raise Exception('模式只能是 AGENT/SSH/SALT')



########## 执行对应的采集方法##########
    def __agent(self, cmd): # 私有方法，只有当前类的对象可调用
        import subprocess
        output = subprocess.getoutput(cmd)
        return output

    def __ssh(self, cmd):
        import paramiko
        # 通过公钥私钥方式登陆远程服务器
        # private_key = paramiko.RSAKey.from_private_key_file(self.ssh_key)
        # ssh = paramiko.SSHClient()
        # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # ssh.connect(hostname=self.hostname, port=self.ssh_port, username=self.ssh_user, pkey=private_key)
        # stdin, stdout, stderr = ssh.exec_command(cmd)
        # result = stdout.read()
        # ssh.close()

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh.connect(hostname=self.hostname, port=self.ssh_port, username=self.ssh_user, password=self.ssh_pwd)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = stdout.read()
        ssh.close()
        return result

    #   通过salt方式获得远程服务器信息
    def __salt(self, cmd):
        salt_cmd = "salt '%s' cmd.run '%s'" %(self.hostname,cmd,)
        import subprocess
        output = subprocess.getoutput(salt_cmd)
        return output
