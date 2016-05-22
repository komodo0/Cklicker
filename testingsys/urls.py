# coding: utf-8
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',

    url(r'^my_results/', 'testingsys.views.Results'),
    url(r'^statistic/', 'testingsys.views.Statistic'),
    url(r'^top/', 'testingsys.views.Tops'),
    url(r'^', 'testingsys.views.TestList'),
)