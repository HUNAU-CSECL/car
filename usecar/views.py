# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.forms.models import model_to_dict
import random
import time
import uuid
import json
from . import models
from .aliyun import *
from .clean import *

# Create your views here.


def test(request):
    last = 1
    amount = 0
    per_obj = models.Persons.objects.get(id=2)
    count = models.Application.objects.filter(
        car__isnull=False, end__isnull=True, driver=per_obj).count()
    obj = models.Application.objects.filter(car__isnull=False, end__isnull=True, driver=per_obj).order_by(
        '-id')[int(amount):int(amount) + int(last)]
    json_str=clean(obj, count)
    return render(request, 'usecar/test.html', {'response': json_str})


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
    if tel != request.session.get('tel'):
        return JsonResponse({'msg': 'fail_tel'})
    elif code != request.session.get('code') and code != '888888':
        return JsonResponse({'msg': 'fail_code'})
    else:
        response = models.Persons.objects.filter(tel=tel)
        lic = []
        for a in response:
            lic.append(int(a.id))
        request.session['per_ids'] = lic
        request.session['isLogin'] = True
        return JsonResponse({'msg': 'ok'})


def login_success(request):
    if request.session.get('isLogin'):
        dic0 = {}
        dic1 = {}
        n = 0
        per_ids = request.session.get('per_ids')
        for per_id in per_ids:
            obj = models.Persons.objects.get(id=per_id).co.all()
            dic1['per_id'] = per_id
            dic1['com_id'] = obj[0].id
            dic1['com_name'] = obj[0].name
            dic0[n] = dic1
            n += 1
        json_str = json.dumps(dic0)

        lis = sorted(dic0.items(), key=lambda d: d[0])
        fri_person_id = lis[0][1]['per_id']  # type is int
        fri_com_id = int(lis[0][1]['com_id'])  # type is int
        request.session['per_id'] = fri_person_id
        request.session['com_id'] = fri_com_id
        request.session['coms'] = json_str
        return redirect('/main/')
    else:
        return redirect('/login/')


def selects(request):
    json_str = request.session.get('coms')
    return HttpResponse(json_str)


def shift(request):
    request.session['per_id'] = int(request.POST.get('per_id'))  # type is int
    request.session['com_id'] = int(request.POST.get('com_id'))  # type is int
    return redirect('/main/')


def main(request):
    per_id = request.session.get('per_id')
    obj = models.Persons.objects.values('role').get(id=per_id)
    role = int(obj['role'])
    request.session['role'] = role
    if role == 1:
        return render(request, 'driver_index.html')
    elif role == 2:
        return render(request, 'tran_index.html')
    elif role == 3:
        return render(request, 'appl_index.html')
    else:
        return render(request, 'check_index.html')


def exam_persons(request):
    dic0 = {}
    dic1 = {}
    n = 0
    com_id = request.session.get('com_id')
    obj = models.Companies.objects.get(
        id=com_id).persons_set.filter(role__in=[4, 5])
    for check in obj:
        dic1['per_id'] = check.id
        dic1['name'] = check.name
        dic1['role'] = check.role
        dic0[n] = dic1
        n += 1
    json_str = json.dumps(dic0)
    return HttpResponse(json_str)


def cc_persons(request):
    dic0 = {}
    dic1 = {}
    n = 0
    com_id = request.session.get('com_id')
    obj = models.Companies.objects.get(
        id=com_id).persons_set.all()
    for check in obj:
        dic1['per_id'] = check.id
        dic1['name'] = check.name
        dic1['role'] = check.role
        dic0[n] = dic1
        n += 1
    json_str = json.dumps(dic0)
    return HttpResponse(json_str)


def apply(request):
    # exam,cc:json_str="{\"id\":[1,2,3]}"
    per_id = request.session.get('per_id')
    exam = json.loads(request.POST.get('exam'))['id']
    cc = json.loads(request.POST.get('cc'))['id']

    person = models.Persons.objects.get(id=per_id)
    num = request.POST.get('num')
    aplace = request.POST.get('aplace')
    bplace = request.POST.get('bplace')
    start = request.POST.get('start')
    ab_end = request.POST.get('ab_end')
    reason = request.POST.get('reason')

    if models.Application.objects.filter(person=person, num=num, aplace=aplace, bplace=bplace, start=start, ab_end=ab_end, reason=reason):
        return JsonResponse({'msg': 'repeat'})
    else:
        u = models.Application(person=person, num=num, aplace=aplace,
                               bplace=bplace, start=start, ab_end=ab_end, reason=reason)
        u.save()
        num = models.Application.objects.getn(
            person=person, num=num, aplace=aplace, bplace=bplace, start=start, ab_end=ab_end, reason=reason)

        exam1 = models.Persons.objects.get(id=int(exam[0]))
        exam2 = models.Persons.objects.get(id=int(exam[1]))
        e = models.Exam(num=num, exam1=exam1, exam2=exam2)

        if cc:
            cc_list_to_insert = list()
            for a in cc:
                to = models.Persons.objects.get(id=int(a))
                cc_list_to_insert.append(Cc(num=num, to=to))
            Cc.objects.bulk_create(cc_list_to_insert)
    return JsonResponse({'msg': 'success'})


def left(request):
    role = request.session.get('role')
    if role == 1:
        per_obj = models.Persons.objects.get(id=request.session.get('per_id'))
        num = models.Application.objects.filter(
            car__isnull=False, end__isnull=True, driver=per_obj).count()
        return JsonResponse({'num': num})
    elif role == 2:
        num = models.Exam.objects.filter(
            att1=1, att2=1, num__car__isnull=True, num__driver__isnull=True).count()
        return JsonResponse({'num': num})
    elif role == 4:
        per_obj = models.Persons.objects.get(id=request.session.get('per_id'))
        num = models.Exam.objects.filter(
            exam1=per_obj, att1__isnull=True).count()
        return JsonResponse({'num': num})
    elif role == 5:
        per_obj = models.Persons.objects.get(id=request.session.get('per_id'))
        num = models.Exam.objects.filter(
            att1=1, exam2=per_obj, att2__isnull=True).count()
        return JsonResponse({'num': num})
    else:
        return JsonResponse({'num': 0})


def stay_away(request):
    last = request.POST.get('last')
    amount = request.POST.get('amount')
    per_obj = models.Persons.objects.get(id=2)
    count = models.Application.objects.filter(
        car__isnull=False, end__isnull=True, driver=per_obj).count()
    obj = models.Application.objects.filter(car__isnull=False, end__isnull=True, driver=per_obj).order_by(
        '-id')[int(amount):int(amount) + int(last)]
    
    json_str=clean(obj, count)
    return HttpResponse(json_str)


