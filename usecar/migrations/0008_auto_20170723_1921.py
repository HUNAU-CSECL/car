# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-23 11:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usecar', '0007_auto_20170722_1305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='ab_end',
            field=models.DateTimeField(verbose_name='\u9884\u8ba1\u7ed3\u675f\u65f6\u95f4'),
        ),
    ]
