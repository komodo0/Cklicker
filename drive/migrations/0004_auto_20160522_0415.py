# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-05-22 00:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drive', '0003_auto_20160425_2252'),
    ]

    operations = [
        migrations.CreateModel(
            name='DriveTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('drive_time', models.CharField(default=None, max_length=5, null=True)),
                ('is_available', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': '\u0412\u0440\u0435\u043c\u044f \u0440\u0430\u0437\u0432\u043e\u0437\u043a\u0438',
                'verbose_name_plural': '\u0412\u0440\u0435\u043c\u044f \u0440\u0430\u0437\u0432\u043e\u0437\u043a\u0438',
            },
        ),
        migrations.AlterField(
            model_name='drivelist',
            name='drive_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='operatortodepartnemt',
            name='operator',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='drivelist',
            name='drive_time',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='drive.DriveTime'),
        ),
    ]
