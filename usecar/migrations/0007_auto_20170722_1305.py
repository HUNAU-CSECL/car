# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-22 05:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usecar', '0006_auto_20170722_1135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='ab_end',
            field=models.IntegerField(verbose_name='\u9884\u8ba1\u7528\u65f6'),
        ),
    ]
