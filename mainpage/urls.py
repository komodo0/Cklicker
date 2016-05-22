# coding: utf-8
from django.conf.urls import patterns, include, url

from mainpage import views

urlpatterns = patterns('',
    url(r'^', 'mainpage.views.Index'),
)