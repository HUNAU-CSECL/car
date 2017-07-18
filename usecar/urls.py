# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/$', views.login),#登录
    url(r'^send_mes/$', views.send_mes),#短信验证码
    url(r'^login_check/$', views.login_check),#登录验证
    url(r'^login_success/$', views.login_success),#登录成功与失败
]