# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^test/$', views.test),
    url(r'^login/$', views.login),  # 登录
    url(r'^send_mes/$', views.send_mes),  # 短信验证码
    url(r'^login_check/$', views.login_check),  # 登录验证
    url(r'^login_success/$', views.login_success),  # 登录成功与失败
    url(r'^exam_persons/$', views.exam_persons),  # 本单位审核人
    url(r'^cc_persons/$', views.cc_persons),  # 本单位抄送人
]
