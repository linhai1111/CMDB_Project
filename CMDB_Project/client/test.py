############### 客户端发送动态令牌完成API验证 ###############
import requests
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

# 将添加了时间的动态令牌添加到请求头中发往API
response = requests.get('http://127.0.0.1:8000/api/asset.html', headers={'OpenKey': md5_time_key})
print(response.text)  # 获得响应结果
