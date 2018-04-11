from lib.conf.config import settings
import os


class Board:
    """
    获取服务器主板信息
    """

    def __init__(self):
        pass

    @classmethod
    def initial(cls):
        return cls()

    def process(self, command_func, debug):
        if debug:
            output = open(os.path.join(settings.BASEDIR, 'files/board.out'), 'r', encoding='utf-8').read()
        else:
            output = command_func('sudo dmidecode -t1')  # 调用command_func方法来执行对应的采集方式
        return self.parse(output)

    # 解析服务器信息结果
    def parse(self, content):
        result = {}
        key_map = {
            'Manufacturer': 'manufacturer',
            'Product Name': 'model',
            'Serial Number': 'sn',
        }
        for item in content.split('\n'):
            row_data = item.strip().split(':')
            if len(row_data) == 2:
                if row_data[0] in key_map:
                    result[key_map[row_data[0]]] = row_data[1].strip() if row_data[1] else row_data[1]

        return result
