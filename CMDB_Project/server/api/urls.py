from django.conf.urls import url,include
from django.contrib import admin
from api import views
urlpatterns = [
    url(r'^asset.html$', views.asset),

    # restful面向资源编程
    url(r'^servers.html$',  views.servers),
    url(r'^servers/(\d+).html$',  views.servers_detail),
]
