from django.shortcuts import render
import json
from django.shortcuts import HttpResponse
# Create your views here.
def asset(request):
    if request.method == 'POST':
        # 新资产信息
        server_info = json.loads(request.body.decode('utf-8')) # 将发送的数据解码成字符串，再通过json反序列化成字典格式
        return HttpResponse('')
