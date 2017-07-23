# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.forms.models import model_to_dict
from django.db.models import Q
import datetime
import random
import time
import uuid
import json
from . import models
from .aliyun import *
from .clean import *

# Create your views here.

# 您有一${type}任务急需处理，请您及时登录<SSSNOW用车>。您正在登录<SSSNOW用车>，此次登录验证码为${code}，请不要泄露给其他人。


def test(request):
    return render(request, 'usecar/test.html', {'response': 1})


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
        send_sms(__business_id, tel, "SSSNOW用车", "SMS_78560123", params)
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
    start_data=datetime.datetime.fromtimestamp(int(start))
    ab_end = datetime.datetime.fromtimestamp(int(request.POST.get('ab_end'))+int(start))
    reason = request.POST.get('reason')

    if models.Application.objects.filter(person=person, num=num, aplace=aplace, bplace=bplace, start=start_data, ab_end=ab_end, reason=reason):
        return JsonResponse({'msg': 'repeat'})
    else:
        u = models.Application(person=person, num=num, aplace=aplace,
                               bplace=bplace, start=start_data, ab_end=ab_end, reason=reason)
        u.save()
        num = models.Application.objects.getn(
            person=person, num=num, aplace=aplace, bplace=bplace, start=start_data, ab_end=ab_end, reason=reason)

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

# 待完成


def stay_away(request):
    last = request.POST.get('last')
    amount = request.POST.get('amount')
    per_obj = models.Persons.objects.get(id=request.get.session('per_id'))
    count = models.Application.objects.filter(
        car__isnull=False, end__isnull=True, driver=per_obj).count()
    obj = models.Application.objects.filter(car__isnull=False, end__isnull=True, driver=per_obj).order_by(
        '-id')[int(amount):int(amount) + int(last)]
    json_str = clean(obj, count)
    return HttpResponse(json_str)


# 点击完成按钮
def finish(request):
    appl_id = int(request.POST.get('id'))
    end = datetime.now()
    obj = models.Application.objects.get(id=appl_id)
    obj.end = end
    obj.save()
    return JsonResponse({'msg': ok})

# 已完成


def finished_away(request):
    last = request.POST.get('last')
    amount = request.POST.get('amount')
    per_obj = models.Persons.objects.get(id=request.get.session('per_id'))
    count = models.Application.objects.filter(
        car__isnull=False, end__isnull=False, driver=per_obj).count()
    obj = models.Application.objects.filter(car__isnull=False, end__isnull=False, driver=per_obj).order_by(
        '-id')[int(amount):int(amount) + int(last)]
    json_str = clean(obj, count)
    return HttpResponse(json_str)


# 申请中
def appling(request):
    last = request.POST.get('last')
    amount = request.POST.get('amount')
    per_obj = models.Persons.objects.get(id=request.get.session('per_id'))
    count = models.Application.objects.filter(
        car__isnull=True, person=per_obj, start__gte=datetime.now()).exclude(Q(exam__att1=0) | Q(exam__att2=0)).count()
    obj = models.Application.objects.filter(car__isnull=True, person=per_obj, start__gte=datetime.now()).exclude(Q(exam__att1=0) | Q(exam__att2=0)).order_by(
        '-id')[int(amount):int(amount) + int(last)]
    json_str = clean(obj, count)
    return HttpResponse(json_str)

# 催办
def quick(request):
    appl_id = request.POST.get('id')
    obj = models.Application.objects.get(id=appl_id).exam
    if obj.att1 == None:
        tel = obj.exam1.tel
        __business_id = uuid.uuid1()
        params = "{\"type\":\" 审批\"}"
        send_sms(__business_id, tel, "SSSNOW用车", "SMS_78770137", params)
    elif obj.att2 == None:
        tel = obj.exam2.tel
        __business_id = uuid.uuid1()
        params = "{\"type\":\" 审批\"}"
        send_sms(__business_id, tel, "SSSNOW用车", "SMS_78770137", params)
    else:
        obj2 = models.Persons.objects.filter(role=2).order_by('?')[:1]
        tel = obj2[0].tel
        __business_id = uuid.uuid1()
        params = "{\"type\":\" 调车\"}"
        send_sms(__business_id, tel, "SSSNOW用车", "SMS_78770137", params)
    return JsonResponse({'quick': 'ok'})

# 撤销
# 申请成功


def appl_succ(request):
    last = request.POST.get('last')
    amount = request.POST.get('amount')
    per_obj = models.Persons.objects.get(id=request.get.session('per_id'))
    count = models.Application.objects.filter(
        car__isnull=False, driver__isnull=False, person=per_obj).count()
    obj = models.Application.objects.filter(car__isnull=False, driver__isnull=False, person=per_obj).order_by(
        '-id')[int(amount):int(amount) + int(last)]
    json_str = clean(obj, count)
    return HttpResponse(json_str)


# 申请失败
def appl_fail(request):
    last = request.POST.get('last')
    amount = request.POST.get('amount')
    per_obj = models.Persons.objects.get(id=request.get.session('per_id'))
    count = models.Application.objects.filter(Q(person=per_obj), Q(
        start__lte=datetime.now()) | Q(exam__att1=0) | Q(exam__att2=0)).count()
    obj = models.Application.objects.filter(Q(person=per_obj), Q(start__lte=datetime.now()) | Q(exam__att1=0) | Q(exam__att2=0)).order_by(
        '-id')[int(amount):int(amount) + int(last)]
    json_str = clean(obj, count)
    return HttpResponse(json_str)

#待调度
def to_distribute(request):
    last = request.POST.get('last')
    amount = request.POST.get('amount')
    count = models.Application.objects.filter(
        car__isnull=True, driver__isnull=True,exam__att1=1,exam__att2=1).count()
    obj = models.Application.objects.filter(car__isnull=True, driver__isnull=True,exam__att1=1,exam__att2=1).order_by(
        '-id')[int(amount):int(amount) + int(last)]
    json_str = clean(obj, count)
    return HttpResponse(json_str)

#调度
def dris_cars(request):
    start=request.POST.get('start')
    ab_end=request.POST.get('ab_end')
    end=int(start)+int(ab_end)
    start_data=datetime.datetime.fromtimestamp(int(start))
    end_data=datetime.datetime.fromtimestamp(int(end))
    obj=models.Application.objects.filter(Q(end__isnull=False),Q(start__range=(start_data,end_data))|Q(ab_end__range=(start_data,end_data))|Q(start__lt=start_data,ab_end__gt=end_data))
    per_obj=models.Persons.objects.filter(role=1)
    car_obj=models.Cars.objects.all()
    dic={}
    dic1={}
    dic2={}
    for per in per_obj:
        dic1[str(per.id)]={'name':per.name,'tel':per.tel,'state':'1'}
    for car in car_obj:
        dic2[str(car.id)]={'style':car.brand+car.style,'lic':car.license,'cap':car.cap,'state':'1'}
    for a in obj:
        dic1[str(a.driver.id)]['state']='0'
        dic2[str(a.car.id)]['state']='0'
    dic['drivers']=dic1
    dic['cars']=dic2
    json_str=json.dumps(dic)
    return HttpResponse(json_str)

#已调度
def distributed(request):
    last = request.POST.get('last')
    amount = request.POST.get('amount')
    count = models.Application.objects.filter(
        car__isnull=False, driver__isnull=False).count()
    obj = models.Application.objects.filter(car__isnull=False, driver__isnull=False).order_by(
        '-id')[int(amount):int(amount) + int(last)]
    json_str = clean(obj, count)
    return HttpResponse(json_str)

#待审核
def to_check(request):
    last = request.POST.get('last')
    amount = request.POST.get('amount')
    role=request.get.session('role')
    per_obj = models.Persons.objects.get(id=request.get.session('per_id'))
    if role==4:
        count = models.Exam.objects.filter(exam1=per_obj, att1__isnull=True).count()
        obj = models.Application.objects.filter(exam__exam1=per_obj, exam__att1__isnull=True).order_by('-id')[int(amount):int(amount) + int(last)]
        json_str = clean(obj, count)
    else:
        count = models.Exam.objects.filter(exam2=per_obj, att2__isnull=True,att1__isnull=False).count()
        obj = models.Application.objects.filter(exam__exam2=per_obj, exam__att2__isnull=True,att1__isnull=False).order_by('-id')[int(amount):int(amount) + int(last)]
        json_str = clean(obj, count)
    return HttpResponse(json_str)
#审核
def check(request):
    appl_id=request.POST.get('id')
    role=request.get.session('role')
    att=int(request.POST.get('att'))
    obj = models.Application.objects.get(id=appl_id)
    if role==4:
        obj.exam.att1 = att
    else:
        obj.exam.att2 = att
    obj.exam.save()
    return JsonResponse({'msg': ok})
#审核成功
def checked(request):
    last = request.POST.get('last')
    amount = request.POST.get('amount')
    role=request.get.session('role')
    per_obj = models.Persons.objects.get(id=request.get.session('per_id'))
    if role==4:
        count = models.Exam.objects.filter(exam1=per_obj, att1__isnull=False).count()
        obj = models.Application.objects.filter(exam__exam1=per_obj, exam__att1__isnull=False).order_by('-id')[int(amount):int(amount) + int(last)]
        json_str = clean(obj, count)
    else:
        count = models.Exam.objects.filter(exam2=per_obj, att2__isnull=False).count()
        obj = models.Application.objects.filter(exam__exam2=per_obj, exam__att2__isnull=False).order_by('-id')[int(amount):int(amount) + int(last)]
        json_str = clean(obj, count)
    return HttpResponse(json_str)

#车辆
def allCars(request):
    last = request.POST.get('last')
    amount = request.POST.get('amount')
    count=models.Cars.objects.all().count()
    obj=models.Cars.objects.all().order_by('-id')[int(amount):int(amount) + int(last)]
    json_str = cars_info(obj, count)
    return HttpResponse(json_str)
#司机
def allDrivers(request):
    last = request.POST.get('last')
    amount = request.POST.get('amount')
    count=models.Persons.objects.filter(role=1).count()
    obj=models.Persons.objects.filter(role=1).order_by('-id')[int(amount):int(amount) + int(last)]
    json_str=drivers_info(obj, count)
    return HttpResponse(json_str)
#添加车辆
def inser_car(request):
    obj=models.Companies.objects.get(id=request.session.get('com_id'))
    u = models.Cars(license=request.POST.get('lic'), brand=request.POST.get('brand'), style=request.POST.get('style'),cap=request.POST.get('cap'),co=obj)
    u.save()
    return JsonResponse({'msg': ok})
#添加司机
def inser_driver(request):
    obj=models.Companies.objects.get(id=request.session.get('com_id'))
    u = models.Persons(name=request.POST.get('name'), tel=request.POST.get('tel'), role=1,co=obj)
    u.save()
    return JsonResponse({'msg': ok})