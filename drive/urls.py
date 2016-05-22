# coding: utf-8
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^signup/', 'drive.views.SignUpDriveView'),
    url(r'^addresses/add/', 'drive.views.AddAddress'),
    url(r'^addresses/delete/', 'drive.views.DeleteAddress'),
    url(r'^addresses/', 'drive.views.AdressesDriveView'),
    url(r'^history/', 'drive.views.DriveHistory'),
    url(r'^', 'drive.views.DriveView'),

)
