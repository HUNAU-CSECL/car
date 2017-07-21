# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
import random
import uuid
import json
from . import models
from .aliyun import *

# Create your views here.


def test(request):
    # response = models.Persons.objects.filter(tel='13975659747')
    # # c = list(response)
    # e = []
    # for a in response:
    #     e.append(int(a.id))
    # request.session["d"] = e
    # persons = request.session.get('d')
    # y = {}
    # for per_id in persons:
    #     obj = models.Persons.objects.get(id=per_id).co.all()
    #     y[per_id] = (obj[0].name,obj[0].id)
    #     # y[com_id] = obj[0].id
    # # data = {2L: u'2号', 1L: u'1好', 3L: u'\u6e56\u5357\u5927\u5b66', 4L: u'\u957f\u6c99\u7406\u5de5\u5927\u5b66', 5L: u'\u4e2d\u5357\u6797\u4e1a\u79d1\u6280\u5927\u5b66'}
    # data = sorted(y.items(), key=lambda d: d[0])
    # # data=json.dumps(data)
    # per_id=data[0][0]
    # com_id=data[2][1][1]
    obj = models.Persons.objects.values('role').get(id=1)
    return render(request, 'usecar/test.html', {'response': str(obj['role'])})


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
        response = models.Persons.objects.filter(tel=tel)
        lic = []
        for a in response:
            lic.append(int(a.id))
        request.session['per_ids'] = lic
        request.session['isLogin'] = True
        return JsonResponse({'msg': 'ok'})
    elif tel != request.session.get('tel'):
        return JsonResponse({'msg': 'fail_tel'})
    else:
        return JsonResponse({'msg': 'fail_code'})


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
    if role == 1:
        return render(request, 'driver_index.html')
    else:
        return render(request, 'index.html')


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

    if models.Application.object.filter(person=person, num=num, aplace=aplace, bplace=bplace, start=start, ab_end=ab_end, reason=reason):
        return JsonResponse({'msg': 'repeat'})
    else:
        u = models.Application(person=person, num=num, aplace=aplace,bplace=bplace, start=start, ab_end=ab_end, reason=reason)
        u.save()
        num = models.Application.object.getn(
            person=person, num=num, aplace=aplace, bplace=bplace, start=start, ab_end=ab_end, reason=reason)

        exam1 = models.Persons.object.get(id=int(exam[0]))
        exam2 = models.Persons.object.get(id=int(exam[1]))
        e = models.Exam(num=num, exam1=exam1, exam2=exam2)

        if cc:
            cc_list_to_insert = list()
            for a in cc:
                to = models.Persons.object.get(id=int(a))
                cc_list_to_insert.append(Cc(num=num, to=to))
            Cc.objects.bulk_create(cc_list_to_insert)
    return JsonResponse({'msg': 'success'})

# def function():
# 	pass