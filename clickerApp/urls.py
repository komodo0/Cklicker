# coding: utf-8
from django.conf.urls import patterns, include, url

from clickerApp import views

urlpatterns = patterns('',
    url(r'^', 'clickerApp.views.IndexView'),
)
