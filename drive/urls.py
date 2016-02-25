# coding: utf-8
from django.conf.urls import patterns, include, url

from clickerApp import views

urlpatterns = patterns('',
    url(r'^signup/', 'drive.views.SignUpDriveView'),
    url(r'^addresses/add/', 'drive.views.AddAddress'),
    url(r'^addresses/delete/', 'drive.views.DeleteAddress'),
    url(r'^addresses/', 'drive.views.AdressesDriveView'),
    url(r'^', 'drive.views.DriveView'),

)
