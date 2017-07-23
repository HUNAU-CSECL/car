# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# Create your models here.


class Persons(models.Model):
    name = models.CharField(u'姓名', max_length=16)
    tel = models.CharField(u'手机号', max_length=14)
    role = models.SmallIntegerField(u'角色：（1司机、2调度人、3申请人、45审核人）', default=3)
    state = models.SmallIntegerField(u'状态：（0离职、1在岗、2忙碌）', default=1)
    co = models.ManyToManyField('Companies')

    def __unicode__(self):
        return self.name


class Cars(models.Model):
    license = models.CharField(u'车牌号', max_length=8)
    brand = models.CharField(u'品牌', max_length=10)
    style = models.CharField(u'类型', max_length=10)
    cap = models.IntegerField(u'容量')
    state = models.SmallIntegerField(u'车辆状态（0报废、1在岗、2忙碌）', default=1)
    co = models.ForeignKey('Companies')

    def __unicode__(self):
        return self.brand + self.style


class Companies(models.Model):
    name = models.CharField(u'单位名称', max_length=20)

    def __unicode__(self):
        return self.name


class Application(models.Model):
    person = models.ForeignKey('Persons',related_name="self_set")
    num = models.IntegerField(u'乘车人数')
    aplace = models.CharField(u'出发地', max_length=100)
    bplace = models.CharField(u'目的地', max_length=100)
    start = models.DateTimeField(u'出发时间')
    ab_end = models.IntegerField(u'预计用时')
    reason = models.TextField(u'用车原由')
    driver = models.ForeignKey('Persons',blank=True, null=True,related_name="driver_set")
    car = models.ForeignKey('Cars', blank=True, null=True)
    end = models.DateTimeField(u'到达时间', blank=True, null=True)

    def __unicode__(self):
        return self.aplace


class Exam(models.Model):
    num = models.OneToOneField('Application')
    exam1 = models.ForeignKey('Persons', related_name='exam1_examset')
    exam2 = models.ForeignKey('Persons', related_name='exam2_examset')
    att1 = models.SmallIntegerField(u'审核人1意见（0不同意、1同意）', blank=True, null=True)
    att2 = models.SmallIntegerField(u'审核人2意见（0不同意、1同意）', blank=True, null=True)

    def __unicode__(self):
        return self.num


class Cc(models.Model):
    num = models.ForeignKey('Application')
    to = models.ForeignKey('Persons')

    def __unicode__(self):
        return self.num
