# coding: utf-8
from django.conf.urls import patterns, include, url

from clickerApp import views

urlpatterns = patterns('',

    url(r'^', 'clickerApp.views.IndexView'),
#    url(r'^about/', views.AboutView.as_view(), name='about'),

)
