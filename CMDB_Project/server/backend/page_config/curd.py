table_config = [  # 配置文件，用于前端页面数据定制显示
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

    # 生成id字段
    {
        'q': 'id',  # 用于数据库查询字段名
        'title': 'ID',  # 用于前端页面中表头字段名的显示
        'display': False,  # display表示该字段在前端页面表格表头是否显示
        'text': {  # text用来将数据库中取出的值进行字符串格式化
            'tpl': '{n1}',  # 用于生成格式化字符串中的占位符模板
            'kwargs': {'n1': '@id'}  # 占位符中具体的id数值,用于生成链接中对单条数据的操作
        },
        'attrs': {'k1': 'v1', 'k2': '@hostname'}  # 为前端标签添加属性及属性值
    },
    {
        'q': 'hostname',
        'title': '主机名',
        'display': True,
        'text': {
            'tpl': '{n1}-{n2}',
            'kwargs': {'n1': '@hostname', 'n2': '@id'}
        },
        'attrs': {'edit-enable': 'true', 'k2': '@hostname', 'origin': '@hostname', 'name': 'hostname'}
        # edit-enable允许编辑， k2表示字段当前值，用于进行值的前后对比完成值的修改
    },

    # 页面显示 操作： 删除，编辑，a标签生成
    {
        'q': None,
        'title': '操作',
        'display': True,
        'text': {
            'tpl': "<a href='/del?nid={nid}'>删除</a>",
            'kwargs': {'nid': '@id'},
        },
        'attrs': {'k1': 'v1', 'k2': '@hostname'}
    },

]

# 搜索框部分所需的配置
# hostname__contains用于实现模糊查询
search_config=[
    {'name':'hostname__contains', 'text':'主机名','search_type':'input'},
    # {'name':'sn__contains', 'text':'SN号','search_type':'input'},
]