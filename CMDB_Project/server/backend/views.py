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

def get_data_list(request,model_cls,table_config):
    """
    根据搜索条件进行查询
    :param request:
    :param model_cls:
    :param table_config:
    :return:
    """
    values_list = []
    for row in table_config:
        if not row['q']:
            continue
        values_list.append(row['q'])

    from django.db.models import Q

    condition = request.GET.get('condition')
    condition_dict = json.loads(str(condition))

    con = Q()
    for name,values in condition_dict.items():  # {'hostname__contains': ['c1', 'c2']}
        ele = Q() # select xx from where cabinet_num=sdf or cabinet_num='123'
        ele.connector = 'OR'
        for item in values: #  ['c1', 'c2']
            ele.children.append((name,item))
        con.add(ele, 'AND') # (AND: (OR: ('hostname__contains', 'c1'), ('hostname__contains', 'c2')))

    server_list = model_cls.objects.filter(con).values(*values_list)
    return server_list


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
    if request.method == 'DELETE':
        id_list = json.loads(str(request.body, encoding='utf-8'))  # 需要从body请求体中取出数据
        print(id_list)
        return HttpResponse('--')
    elif request.method == 'POST':
        pass
    elif request.method == 'PUT':
        all_list = json.loads((str(request.body, encoding='utf-8')))   # 编码成字符串
        print(all_list)
        return HttpResponse('---')
    elif request.method == 'GET':
        from backend.page_config import curd as curdConfig
        server_list = get_data_list(request, models.Server, curdConfig.table_config)

        ret = {
            'server_list': list(server_list),  # 将Querylist转换成列表
            'table_config': curdConfig.table_config,
            'search_config': curdConfig.search_config,
            'global_dict':{ # 用于生成下拉框
                'device_type_choices':models.Asset.device_type_choices,
                'device_status_choices':models.Asset.device_status_choices,
            }
        }
        return HttpResponse(json.dumps(ret, cls=JsonCustomEncoder))


# 资产信息展示
def asset(request):
    """
    跳转到资产信息展示页面
    :param request:
    :return:
    """
    return render(request, 'asset.html', )


def asset_json(request):
    """
    ajax获取资产信息数据
    :param reqeust:
    :return:
    """
    from backend.page_config import asset as assetConfig
    server_list = get_data_list(request, models.Asset, assetConfig.table_config)
    print(server_list)

    # global_dict用于生成选择元组中的数字对应的字符串
    ret = {
        'server_list': list(server_list),
        'table_config': assetConfig.table_config,
        'search_config': assetConfig.search_config,
        'global_dict': {
            'device_type_choices': models.Asset.device_type_choices,
            'device_status_choices': models.Asset.device_status_choices,
        }
    }
    return HttpResponse(json.dumps(ret, cls=JsonCustomEncoder))


def idc(request):
    """
    跳转到idc页面
    :param request:
    :return:
    """
    return render(request, 'idc.html')

def idc_json(request):
    if request.method == 'DELETE':
        id_list = json.loads(str(request.body, encoding='utf-8'))
        print(id_list)
        return HttpResponse('删除成功')
    elif request.method == 'PUT':
        all_list = json.loads(str(request.body, encoding='utf-8'))
        print(all_list)
        return HttpResponse('保存成功')
    elif request.method == 'GET':
        from backend.page_config import idc
        values_list = []
        for row in idc.table_config:    # 从配置文件中获取数据库查询所需的字段
            if not row['q']:
                continue
            values_list.append(row['q'])
        server_list = models.IDC.objects.values(*values_list)

        ret={
            'server_list':list(server_list),
            'table_config':idc.table_config,
            'global_dict':{}
        }
    return HttpResponse(json.dumps(ret, cls=JsonCustomEncoder))


def chart(request):
    """
    跳转到页面
    :param request:
    :return:
    """
    return render(request, 'chart.html')


