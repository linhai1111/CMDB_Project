from django.shortcuts import render
import json
from repository import models
from django.shortcuts import HttpResponse
from datetime import datetime
from datetime import date
# Create your views here.
class JsonCustomEncoder(json.JSONEncoder):
    """
    json扩展：针对日期格式数据进行自定义转换成字符串处理
    """

    def default(self, value):
        if isinstance(value, datetime):
            return value.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(value, date):
            return value.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, value)  # 调用父类中的default方法


def curd(request):
    """
    进入到curd.html页面
    :param request:
    :return:
    """
    return render(request, 'curd.html')


def curd_json(request):
    """
    ajax请求方法
    :param request:
    :return:
    """

    table_config = [  # 配置文件，用于前端页面数据定制显示
        # 生成checkbox多选框字段
        {
            'q': None,  # 不作为数据库查询字段
            'title': '选择',
            'display': True,
            'text': {
                'tpl': "<input type='checkbox' value='{n1}' />",
                'kwargs': {'n1': '@id',}
            },
            'attrs': {'nid': '@id'}
        },

        # 生成id字段
        {
            'q': 'id',  # 用于数据库查询字段名
            'title': 'ID',  # 用于前端页面中表头字段名的显示
            'display':False,# display表示该字段在前端页面表格表头是否显示
            'text': { # text用来将数据库中取出的值进行字符串格式化
                'tpl': '{n1}',  # 用于生成格式化字符串中的占位符模板
                'kwargs': {'n1': '@id'}  # 占位符中具体的id数值,用于生成链接中对单条数据的操作
            },
             'attrs':{'k1':'v1','k2':'@hostname'}   # 为前端标签添加属性及属性值
        },
        {
            'q': 'hostname',
            'title': '主机名',
            'display': True,
            'text': {
                'tpl': '{n1}-{n2}',
                'kwargs': {'n1': '@hostname', 'n2': '@id'}
            },
            'attrs':{'edit-enable':'true', 'k2':'@hostname'}    # edit-enable允许编辑， k2表示字段当前值，用于进行值的前后对比完成值的修改
        },

        # 页面显示 操作： 删除，编辑，a标签生成
        {
            'q':None,
            'title':'操作',
            'display': True,
            'text':{
                'tpl': "<a href='/del?nid={nid}'>删除</a>",
                'kwargs':{'nid':'@id'},
            },
            'attrs': {'k1': 'v1', 'k2': '@hostname'}
        },
    ]

    # 组装数据库查询所需的字段
    value_list = []
    for row in table_config:
        if not row['q']:
            continue
        value_list.append(row['q'])

    server_list = models.Server.objects.values(*value_list)   # 传入列表获得字典格式数据
    ret = {
        'server_list':list(server_list),   # 将Querylist转换成列表
        'table_config':table_config,
    }
    return HttpResponse(json.dumps(ret, cls=JsonCustomEncoder))



# 资产信息展示
def asset(request):
    """
    跳转到资产信息展示页面
    :param request:
    :return:
    """
    return render(request, 'asset.html',)

def asset_json(reqeust):
    """
    ajax获取资产信息数据
    :param reqeust:
    :return:
    """
    # @代表需要字符串格式化，@@用于将数字结果转换成对应字符串展示
    table_config = [    # 配置文件
        # 生成checkbox多选框字段
        {
            'q': None,  # 不作为数据库查询字段
            'title': '选择',
            'display': True,
            'text': {
                'tpl': "<input type='checkbox' value='{n1}' />",
                'kwargs': {'n1': '@id', }
            },
            'attrs': {'nid': '@id'}
        },

        {
            'q':'id',
            'title':'ID',
            'display':False,
            'text':{
                'tpl': "{n1}",
                'kwargs': {'n1': '@id'}
            },
            'attrs':{'k1':'v1', 'k2':'@id'}
        },
        {
            'q': 'device_type_id',
            'title': '资产类型',
            'display': True,
            'text': {
                'tpl': "{n1}",
                'kwargs': {'n1': '@@device_type_choices'}
            },
            # origin表示数据库字段id对应的值，  global_key表示数据库中下拉框的数据
            'attrs':{'k1':'v1','origin':'@device_type_id','edit-enable':'true','edit-type':'select','global_key':'device_type_choices'}
        },
        {
            'q': 'device_status_id',
            'title': '状态',
            'display': True,
            'text': {
                'tpl': "{n1}",
                'kwargs': {'n1': '@@device_status_choices'}
            },
            'attrs':{'edit-enable':'true','origin': '@device_status_id','edit-type':'select','global_key':'device_status_choices' }
        },
        {
            'q': 'cabinet_num',
            'title': '机柜号',
            'display': True,
            'text': {
                'tpl': "{n1}",
                'kwargs': {'n1': '@cabinet_num'}
            },
            'attrs': {'k1': 'v1', 'k2': '@id'}
        },

        {
            'q': 'idc__name',
            'title': '机房',
            'display': True,
            'text': {
                'tpl': "{n1}",
                'kwargs': {'n1': '@idc__name'}
            },
            'attrs': {'k1': 'v1', 'k2': '@id'}
        },
        # 页面显示：标题：操作；删除，编辑：a标签
        {
            'q': None,
            'title': '操作',
            'display': True,
            'text': {
                'tpl': "<a href='/del?nid={nid}'>删除</a>",
                'kwargs': {'nid': '@id'}
            },
            'attrs': {'k1': 'v1', 'k2': '@id'}
        },
    ]
    # 用于数据库查询字段
    value_list = []
    for row in table_config:
        if not row['q']:
            continue
        value_list.append(row['q'])
    server_list = models.Asset.objects.values(*value_list)

    # global_dict用于生成选择元组中的数字对应的字符串
    ret={
        'server_list': list(server_list),
        'table_config':table_config,
        'global_dict':{
            'device_type_choices':models.Asset.device_type_choices,
            'device_status_choices':models.Asset.device_status_choices,
        }
    }
    return HttpResponse(json.dumps(ret, cls=JsonCustomEncoder))





