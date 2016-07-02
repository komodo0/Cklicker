# coding: utf-8
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^files/', include('fileUpload.urls')),
    url(r'^auth/', include('loginsys.urls')),
    url(r'^drive/', include('drive.urls')),
    url(r'^diagnostic/', include('clickerApp.urls')),
    url(r'^testing/', include('testingsys.urls')),
    url(r'^feedback/', include('feedback.urls')),
    url(r'^profile/', include('userProfile.urls')),
    url(r'^', include('mainpage.urls')),
)
