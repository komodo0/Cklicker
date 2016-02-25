# coding: utf-8
from django.contrib import admin
from drive.models import Area, FullAddress, DriveList,Department, OperatorToDepartnemt
# Register your models here.


admin.site.register(Area)
admin.site.register(FullAddress)
admin.site.register(DriveList)
admin.site.register(Department)
admin.site.register(OperatorToDepartnemt)