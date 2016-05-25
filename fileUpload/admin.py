# coding: utf-8
from django.contrib import admin
from fileUpload.models import Document

# Register your models here.
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("image", "url")

admin.site.register(Document, DocumentAdmin)