from django.shortcuts import render
import json
from django.shortcuts import HttpResponse
from repository import models
import time
from server import settings
import hashlib

api_key_record = {  # 访问记录表，由动态令牌作为key， 生成动态令牌中所需的时间+10s 作为value，表示该值保存10s
    # "1b96b89695f52ec9de8292a5a7945e38|1501472467.4977243":1501472477.4977243
}

def asset(request):
    client_md5_time_key = request.META.get('HTTP_OPENKEY')  # 客户端通过请求头中发送过来的数据
    client_md5_key, client_ctime = client_md5_time_key.split('|')  # 切分出动态令牌和时间
    client_ctime = float(client_ctime)
    server_time = time.time()  # 获得服务器当前时间

    # 第一关验证：客户端第二次发送动态令牌的时间不能超过10s，完成第一层黑客攻击过滤
    if server_time - client_ctime > 10:
        return HttpResponse('第一关通过失败，时间超时')

    # 第二关验证：生成动态令牌的时间不匹配,防止黑客获得动态令牌，并通过第一关到达第二关
    temp = '%s|%s' % (settings.AUTH_KEY, client_ctime)
    m = hashlib.md5()
    m.update(bytes(temp, encoding='utf-8'))
    server_md5_key = m.hexdigest()
    if server_md5_key != client_md5_key:
        return HttpResponse('第二关通过失败，生成服务端动态令牌中的时间与生成动态令牌中的时间不一致')

    # 对api_key_record记录表中进行数据更新，用于第三关验证
    for k in list(api_key_record.keys()):
        v = api_key_record[k]
        if server_time > v:  # 如果服务器当前时间大于动态令牌有效时间，则删除该令牌，减少记录表容量占比
            del api_key_record[k]

    # 第三关：保持记录表中的唯一性,如果发送过请求，则其它请求无效
    if client_md5_time_key in api_key_record:
        return HttpResponse('第三关通过失败，已经有人访问过了')
    else:
        api_key_record[client_md5_time_key] = client_ctime + 10  # 将是第一次的请求写入记录表中

    if request.method == 'GET':
        ys = 'api验证成功'
        return HttpResponse(ys)

    elif request.method == 'POST':
        # 新资产信息
        server_info = json.loads(request.body.decode('utf-8'))  # 将发送的数据解码成字符串，再通过json反序列化成字典格式
        hostname = server_info['basic']['data']['hostname']  # 获得采集器中发过来的信息中的主机名
        server_obj = models.Server.objects.filter(hostname=hostname).first()  # 根据主机名获得服务器QuuerySet对象

        if not server_obj:
            return HttpResponse('当前主机名在资产中未录入')

        # 将硬盘信息入库
        # 'disk': {'stauts': True, 'data': {
        #     '0': {'slot': '0', 'pd_type': 'SAS', 'capacity': '279.396',
        #           'model': 'SEAGATE ST300MM0006     LS08S0K2B5NV'},
        #     '1': {'slot': '1', 'pd_type': 'SAS', 'capacity': '279.396',
        #           'model': 'SEAGATE ST300MM0006     LS08S0K2B5AH'},
        #     '2': {'slot': '2', 'pd_type': 'SATA', 'capacity': '476.939',
        #           'model': 'S1SZNSAFA01085L     Samsung SSD 850 PRO 512GB               EXM01B6Q'},
        #     '3': {'slot': '3', 'pd_type': 'SATA', 'capacity': '476.939',
        #           'model': 'S1AXNSAF912433K     Samsung SSD 840 PRO Series              DXM06B0Q'},
        #     '4': {'slot': '4', 'pd_type': 'SATA', 'capacity': '476.939',
        #           'model': 'S1AXNSAF303909M     Samsung SSD 840 PRO Series              DXM05B0Q'},
        #     '5': {'slot': '5', 'pd_type': 'SATA', 'capacity': '476.939',
        #           'model': 'S1AXNSAFB00549A     Samsung SSD 840 PRO Series              DXM06B0Q'}}},

        if not server_info['disk']['stauts']:  # 采集信息中状态为False时，将错误信息添加到错误日志中
            models.ErrorLog.objects.create(content=server_info['disk']['data'], asset_obj=server_obj.asset,
                                           title='【%s】硬盘采集错误信息' % hostname)

        new_disk_dict = server_info['disk']['data']  # 获得服务器中最新的硬盘信息数据
        """
               {
                   5: {'slot':5,capacity:476...}
                   3: {'slot':3,capacity:476...}
               }
               """
        old_disk_list = models.Disk.objects.filter(server_obj=server_obj)  # 获得服务器中之前的所有硬盘数据QuerySer对象列表
        """
                [
                    Disk('slot':5,capacity:476...)
                    Disk('slot':4,capacity:476...)
                ]
                """

        new_slot_list = list(new_disk_dict.keys())  # 获得最新硬盘数据中的插槽ID ,[0,1,2,3,4,5]

        old_slot_list = []  # 获得之前的硬盘数据中的插槽ID
        for item in old_disk_list:
            old_slot_list.append(item.slot)

        # 采用交集运算后的结果作为硬盘数据的 更新，获得共有的数据进行比较
        update_list = set(new_slot_list).intersection(old_slot_list)  # 采用集合进行交集运算
        #  采用差集运算后的结果作为硬盘数据的 创建（新数据有，老数据没有）
        create_list = set(new_slot_list).difference(old_slot_list)
        # 采用差集运算后的结果作为硬盘数据的 删除（老数据有，新数据没有）
        del_list = set(old_slot_list).difference(new_slot_list)

        ###################从硬盘数据表中删除数据#################3
        if del_list:
            models.Disk.objects.filter(server_obj=server_obj, slot__in=del_list).delete()
            # 记录日志信息
            models.AssetRecord.objects.create(asset_obj=server_obj.asset, content='移除硬盘：%s' % ('、'.join(del_list)))

        ###################从硬盘数据表中增加数据#################
        record_list = []
        for slot in create_list:
            disk_dict = new_disk_dict[
                slot]  # {'capacity': '476.939', 'slot': '4', 'model': 'S1AXNSAF303909M     Samsung SSD 840 PRO Series
            disk_dict['server_obj'] = server_obj  # 同时将服务器对象添加到该字典中一同添加到Disk数据表中
            models.Disk.objects.create(**disk_dict)  # 以字典的形式添加数据到Disk数据表中

            # 组装硬盘变更记录信息
            temp = "新增硬盘:位置{slot},容量{capacity},型号:{model},类型:{pd_type}".format(**disk_dict)
            record_list.append(temp)
        if record_list:
            content = ';'.join(record_list)  # 将所有变更信息拼接成一个字符串
            models.AssetRecord.objects.create(asset_obj=server_obj.asset, content=content)  # 将变更记录添加到记录表中

        ###################从硬盘数据表中修改数据#################
        record_list = []  # 变更记录列表
        row_map = {'capacity': '容量', 'pd_type': '类型', 'model': '型号'}
        for slot in update_list:
            new_disk_row = new_disk_dict[slot]  # 获得新采集过来的单条硬盘数据
            old_disk_row = models.Disk.objects.filter(slot=slot, server_obj=server_obj).first()
            for k, v in new_disk_row.items():
                # k: capacity;  slot;   pd_type;    model
                # v: '476.939'  'xxies              DXM05B0Q'   'SATA'
                value = getattr(old_disk_row, k)  # 通过反射获得对象中属性的值
                if v != value:  # 如果两者中的值不相等则表示需要更新
                    setattr(old_disk_row, k, v)  # 将对象中的属性值重新赋值
                    record_list.append('槽位%s,%s由%s变更为%s' % (slot, row_map[k], value, v))
            old_disk_row.save()  # 保存更新后的硬盘数据

            # 将变更信息保存到变更记录表中
            if record_list:
                content = ";".join(record_list)
                models.AssetRecord.objects.create(asset_obj=server_obj.asset, content=content)

        return HttpResponse('')
