# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-04 05:04
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drive', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='area',
            options={'verbose_name': '\u0413\u043e\u0440\u043e\u0434\u0441\u043a\u043e\u0439 \u0440\u0430\u0439\u043e\u043d', 'verbose_name_plural': '\u0413\u043e\u0440\u043e\u0434\u0441\u043a\u0438\u0435 \u0440\u0430\u0439\u043e\u043d\u044b'},
        ),
        migrations.AlterModelOptions(
            name='department',
            options={'verbose_name': '\u041f\u043e\u0434\u0440\u0430\u0437\u0434\u0435\u043b\u0435\u043d\u0438\u0435', 'verbose_name_plural': '\u041f\u043e\u0434\u0440\u0430\u0437\u0434\u0435\u043b\u0435\u043d\u0438\u044f'},
        ),
        migrations.AlterModelOptions(
            name='drivelist',
            options={'verbose_name': '\u0417\u0430\u043f\u0438\u0441\u044c \u043d\u0430 \u0440\u0430\u0437\u0432\u043e\u0437\u043a\u0443', 'verbose_name_plural': '\u0417\u0430\u043f\u0438\u0441\u0438 \u043d\u0430 \u0440\u0430\u0437\u0432\u043e\u0437\u043a\u0443'},
        ),
        migrations.AlterModelOptions(
            name='fulladdress',
            options={'verbose_name': '\u0410\u0434\u0440\u0435\u0441 \u043e\u043f\u0435\u0440\u0430\u0442\u043e\u0440\u0430', 'verbose_name_plural': '\u0410\u0434\u0440\u0435\u0441\u0430 \u043e\u043f\u0435\u0440\u0430\u0442\u043e\u0440\u043e\u0432'},
        ),
        migrations.AlterModelOptions(
            name='operatortodepartnemt',
            options={'verbose_name': '\u0421\u043e\u043e\u0442\u043d\u043e\u0448\u0435\u043d\u0438\u0435 "\u041e\u043f\u0435\u0440\u0430\u0442\u043e\u0440 - \u041f\u043e\u0434\u0440\u0430\u0437\u0434\u0435\u043b\u0435\u043d\u0438\u0435"', 'verbose_name_plural': '\u0421\u043e\u043e\u0442\u043d\u043e\u0448\u0435\u043d\u0438\u044f  "\u041e\u043f\u0435\u0440\u0430\u0442\u043e\u0440 - \u041f\u043e\u0434\u0440\u0430\u0437\u0434\u0435\u043b\u0435\u043d\u0438\u0435"'},
        ),
        migrations.AlterField(
            model_name='drivelist',
            name='drive_date',
            field=models.DateField(default=datetime.date(2016, 3, 4)),
        ),
    ]
