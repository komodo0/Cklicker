# coding: utf-8
from django.contrib import admin
from drive.models import Area, FullAddress, DriveList,Department, OperatorToDepartnemt, DriveTime
# Register your models here.


class AreaAdmin(admin.ModelAdmin):
    list_display = ("name", "id")
    list_filter = ("name", "id")

class FullAddressAdmin(admin.ModelAdmin):
    list_display = ("operator", "area", "address", "was_deleted")
    list_filter = ("operator", "area", "address", "was_deleted")

class DriveListAdmin(admin.ModelAdmin):
    list_display = ("drive_date", "address")
    list_filter = ("drive_date", "address")

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "id")
    list_filter = ("name", "id")

class OperatorToDepartnemtAdmin(admin.ModelAdmin):
    list_display = ("operator", "department")
    list_filter = ("operator", "department")

class DriveTimeAdmin(admin.ModelAdmin):
    list_display = ("drive_time", "is_available")
    list_filter = ("drive_time", "is_available")

admin.site.register(Area, AreaAdmin)
admin.site.register(FullAddress, FullAddressAdmin)
admin.site.register(DriveList, DriveListAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(OperatorToDepartnemt, OperatorToDepartnemtAdmin)
admin.site.register(DriveTime, DriveTimeAdmin)