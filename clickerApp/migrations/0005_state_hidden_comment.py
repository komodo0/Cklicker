# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-25 18:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clickerApp', '0004_auto_20160304_0804'),
    ]

    operations = [
        migrations.AddField(
            model_name='state',
            name='hidden_comment',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
