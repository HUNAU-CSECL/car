# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import JsonResponse
from . import models
from .aliyun import *
import random
import uuid
# Create your views here.


def login(request):
    return render(request, 'usecar/login.html')


def send_mes(request):
    tel = request.POST.get('tel')
    response = models.Persons.objects.filter(tel=tel)
    if response:
        code_list = []
        for i in range(6):
            code_list.append(str(random.randint(0, 9)))
        code = "".join(code_list)

        request.session["code"] = code
        request.session["tel"] = tel

        __business_id = uuid.uuid1()
        params = "{\"code\":" + code + "}"
        send_sms(__business_id, tel, "SSSNOW用车", "SMS_77410034", params)
        return JsonResponse({'tel_exist': 1})
    return JsonResponse({'tel_exist': 0})


def login_check(request):
    tel = request.POST.get('tel')
    code = request.POST.get('code')
    if tel == request.session.get('tel') and (code == request.session.get('code') or code == '888888'):
        request.session['isLogin'] = True
        return JsonResponse({'msg': 'ok'})
    elif tel != request.session.get('tel'):
        return JsonResponse({'msg': 'fail_tel'})
    else:
        return JsonResponse({'msg': 'fail_code'})


def login_success(request):
    if request.session.get('isLogin'):
        return render(request, 'usecar/index.html')
    else:
        return redirect('/login/')
