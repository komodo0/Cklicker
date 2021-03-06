# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-04 05:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clickerApp', '0003_remove_state_testchar'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='checkboxinput',
            options={'verbose_name': '\u0427\u0435\u043a\u0431\u043e\u043a\u0441 \u0430\u0442\u0440\u0438\u0431\u0443\u0442', 'verbose_name_plural': '\u0427\u0435\u043a\u0431\u043e\u043a\u0441 \u0430\u0442\u0440\u0438\u0431\u0443\u0442\u044b'},
        ),
        migrations.AlterModelOptions(
            name='radioinput',
            options={'verbose_name': '\u0420\u0430\u0434\u0438\u043e \u0430\u0442\u0440\u0438\u0431\u0443\u0442', 'verbose_name_plural': '\u0420\u0430\u0434\u0438\u043e \u0430\u0442\u0440\u0438\u0431\u0443\u0442\u044b'},
        ),
        migrations.AlterModelOptions(
            name='radioinputvariant',
            options={'verbose_name': '\u0412\u0430\u0440\u0438\u0430\u043d\u0442 \u0440\u0430\u0434\u0438\u043e \u0430\u0442\u0440\u0438\u0431\u0443\u0442\u0430', 'verbose_name_plural': '\u0412\u0430\u0440\u0438\u0430\u043d\u0442\u044b \u0440\u0430\u0434\u0438\u043e \u0430\u0442\u0440\u0438\u0431\u0443\u0442\u044b'},
        ),
        migrations.AlterModelOptions(
            name='state',
            options={'verbose_name': '\u0428\u0430\u0433 \u0434\u0438\u0430\u0433\u043d\u043e\u0441\u0442\u0438\u043a\u0438', 'verbose_name_plural': '\u0428\u0430\u0433\u0438 \u0434\u0438\u0430\u0433\u043d\u043e\u0441\u0442\u0438\u043a\u0438'},
        ),
        migrations.AlterModelOptions(
            name='textinput',
            options={'verbose_name': '\u0422\u0435\u043a\u0441\u0442\u043e\u0432\u044b\u0439 \u0430\u0442\u0440\u0438\u0431\u0443\u0442', 'verbose_name_plural': '\u0422\u0435\u043a\u0441\u0442\u043e\u0432\u044b\u0435 \u0430\u0442\u0440\u0438\u0431\u0443\u0442\u044b'},
        ),
        migrations.AlterModelOptions(
            name='tip',
            options={'verbose_name': '\u041f\u043e\u0434\u0441\u043a\u0430\u0437\u043a\u0430', 'verbose_name_plural': '\u041f\u043e\u0434\u0441\u043a\u0430\u0437\u043a\u0438'},
        ),
        migrations.AddField(
            model_name='state',
            name='variant_description',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
