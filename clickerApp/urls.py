# coding: utf-8
from django.conf.urls import patterns, include, url

from clickerApp import views

urlpatterns = patterns('',
    url(r'^reinitializeStates/', 'clickerApp.views.ReinitializeSteps'),
    url(r'^schema/', 'clickerApp.views.SchemaView'),
    url(r'^statistic/', 'clickerApp.views.Statistic'),
    url(r'^', 'clickerApp.views.IndexView'),
)
