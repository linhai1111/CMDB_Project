from django.conf.urls import url, include
from django.contrib import admin
from backend import views

urlpatterns =[
    url(r'^curd.html$', views.curd), # 进入到数据展示页面
    url(r'^curd_json.html$', views.curd_json),   # 通过页面加载时启动的js获得数据呈现在页面中
    # 资产信息展示
    url(r'asset.html$', views.asset),   # 进入页面
    url(r'asset_json.html$', views.asset_json),   # ajax方式获取数据

    # idc机房信息展示
    url(r'^idc.html$', views.idc),
    url(r'^idc_json.html$', views.idc_json),

    url(r'^chart.html$', views.chart ),

]