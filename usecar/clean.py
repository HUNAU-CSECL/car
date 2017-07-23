# -*- coding: utf-8 -*-
import json
import time


def clean(obj, count):
    dic0 = {}
    i = 0
    for a in obj:
        dic1 = {}
        i += 1
        dic1['id'] = int(a.id)
        dic1['name'] = a.person.name
        dic1['tel'] = a.person.tel
        dic1['num'] = int(a.num)
        dic1['aplace'] = a.aplace
        dic1['bplace'] = a.bplace
        dic1['start'] = time.mktime(a.start.timetuple())
        dic1['ab_end'] = time.mktime(a.start.timetuple())-time.mktime(a.ab_end.timetuple())
        dic1['reason'] = a.reason
        dic1['att1'] = a.exam.att1
        dic1['att2'] = a.exam.att2
        if a.car:
            dic1['car'] = a.car.brand + a.car.style
            dic1['lic'] = a.car.license
        else:
            dic1['car'] = None
            dic1['lic'] = None
        if a.driver:
            dic1['driver'] = a.driver.name
            dic1['driver_tel'] = a.driver.tel
        else:
            dic1['driver'] = None
            dic1['driver_tel'] = None
        if a.end:
            dic1['end'] = time.mktime(a.end.timetuple())
        else:
            dic1['end'] = None
        dic0[i] = dic1
    dic0['count'] = int(count)
    return json.dumps(dic0)

def cars_info(obj,count):
    dic0={}
    i=0
    for a in obj:
        dic1={}
        i += 1
        dic1['lic']=a.lic
        dic1['style']=a.brand+a.style
        dic1['cap']=a.cap
        dic0[i] = dic1
    dic0['count'] = int(count)
    return json.dumps(dic0)

def drivers_info(obj,count):
    dic0={}
    i=0
    for a in obj:
        dic1={}
        i += 1
        dic1['name']=a.name
        dic1['tel']=a.tel
        dic0[i] = dic1
    dic0['count'] = int(count)
    return json.dumps(dic0)