# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-06-23 06:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0025_member_membernumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='membernumber',
            field=models.CharField(default=b'', max_length=250, null=True),
        ),
    ]
