# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-05-25 06:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedbacknote',
            name='has_been_read',
            field=models.BooleanField(default=False),
        ),
    ]
