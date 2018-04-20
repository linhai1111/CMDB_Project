from lib.conf.config import settings
from Crypto.Cipher import AES


def encrypt(message):
    """
    AES加密资产数据
    :param message:
    :return:
    """
    key = settings.DATA_KEY
    cipher = AES.new(key, AES.MODE_CBC, key)  # 初始化AES对象
    ba_data = bytearray(message, encoding='utf-8')  # 字符串编码成字节数组
    v1 = len(ba_data)  # 计算需要加密的数据的长度
    v2 = v1 % 16  # AES只对16的倍数的字节长度进行加密
    if v2 == 0:
        v3 = 16
    else:
        v3 = 16 - v2
    for i in range(v3):  # 需要为不是16倍数的字节数组添加字节，只至满足是16的倍数
        ba_data.append(v3)  # 添加的字节内容采用需补齐的长度值
    final_data = ba_data.decode('utf-8')  # 字节解码成字符串

    msg = cipher.encrypt(final_data)  # 对字符串进行加密,成为字节
    return msg


def decrypt(msg):
    """
    数据解密
    :param msg:
    :return:
    """
    from Crypto.Cipher import AES
    key = settings.DATA_KEY
    cipher = AES.new(key, AES.MODE_CBC, key)
    result = cipher.decrypt(msg)
    data = result[0:-result[-1]]  # 获取补齐到16位长度前真正的内容，result[-1]表示补齐的长度值
    return str(data, encoding='utf-8')  # 转换成字符串


def auth():
    """
    API验证
    :return:
    """
    import time
    import hashlib

    # 生成动态令牌
    ctime = time.time()  # 动态时间戳
    key = "asdfasdfasdfasdf098712sdfs"  # 假定API发送过来的令牌
    new_key = '%s|%s' % (key, ctime)  # 在原有的随机字符串上加入动态时间，形成动态令牌
    print(ctime)
    # 动态令牌通过md5进行加密
    m = hashlib.md5()  # 初始化md5
    m.update(bytes(new_key, encoding='utf-8'))  # 将动态令牌转换成字节，将由md5进行计算
    md5_key = m.hexdigest()  # 获得加密后的令牌
    print(md5_key)
    md5_time_key = '%s|%s' % (md5_key, ctime)  # 将生成动态令牌所需的时间一同发给API，让API进行md5进行加密，以便完成加密数据的比对
    return md5_time_key
