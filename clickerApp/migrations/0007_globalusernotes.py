# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-06-01 14:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clickerApp', '0006_stateusernotes'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalUserNotes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note_body', models.TextField(blank=True, default=b'')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u0413\u043b\u043e\u0431\u0430\u043b\u044c\u043d\u0430\u044f \u0437\u0430\u043c\u0435\u0442\u043a\u0438 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f',
                'verbose_name_plural': '\u0413\u043b\u043e\u0431\u0430\u043b\u044c\u043d\u044b\u0435 \u0437\u0430\u043c\u0435\u0442\u043a\u0438 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f',
            },
        ),
    ]
