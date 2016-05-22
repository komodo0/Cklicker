#coding: utf-8
from __future__ import unicode_literals
from datetime import date
from django.db import models
from django import utils
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone


#Подразделение
class Department(models.Model):
    class Meta():
        verbose_name = u"Подразделение"
        verbose_name_plural = u"Подразделения"

    name = models.CharField(max_length=10)
    def __str__(self):
        return self.name.encode("utf-8")

#Принадлежность оператора к подразделению
class OperatorToDepartnemt(models.Model):
    class Meta():
        verbose_name = u'Соотношение "Оператор - Подразделение"'
        verbose_name_plural = u'Соотношения  "Оператор - Подразделение"'
    #operator = models.ForeignKey(User, unique=True, )
    operator = models.OneToOneField(User)
    department = models.ForeignKey(Department)
    def __str__(self):
        return (self.operator.username + " - " + self.department.name).encode("utf-8")

#Класс - район проживания
class Area(models.Model):
    class Meta():
        verbose_name = u'Городской район'
        verbose_name_plural = u"Городские районы"
    name = models.CharField(max_length=100, blank=False, null=False)
    def __str__(self):
        return (self.name).encode("utf-8")

#Класс - адрес, с привязкой к оператору
class FullAddress(models.Model):
    class Meta():
        verbose_name = u'Адрес оператора'
        verbose_name_plural = u"Адреса операторов"
    operator = models.ForeignKey(User, blank=False, null=False)
    area = models.ForeignKey(Area, blank=False, null=False)
    address = models.CharField(max_length=300, blank=False, null=False)
    was_deleted = models.BooleanField(default=False, blank=False, null=False)
    def __str__(self):
        return (self.operator.username + " | " + self.area.name + " | " + self.address).encode("utf-8")


#Класс - возможное время для записи на развозку.
class DriveTime(models.Model):
    class Meta():
        verbose_name = u'Время развозки'
        verbose_name_plural = u"Время развозки"

    drive_time = models.CharField(default=None, null=True, blank=False, max_length=5)
    is_available = models.BooleanField(default=True, null=False, blank=False)

    def __str__(self):
        return self.drive_time.__str__()


#Класс - лист развозки
class DriveList(models.Model):
    class Meta():
        verbose_name = u'Запись на развозку'
        verbose_name_plural = u"Записи на развозку"
    drive_time = models.ForeignKey(DriveTime, blank=False, null=True, default=None)
    drive_date = models.DateField(blank=False, null=False, auto_now_add=True)
    address = models.ForeignKey(FullAddress, blank=False, null=False)

    def __str__(self):
        return (str(self.drive_date.strftime('%Y.%m.%d')) + " | ").encode("utf-8") + self.address.__str__()


