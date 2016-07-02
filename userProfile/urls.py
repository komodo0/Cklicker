# coding: utf-8
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^change/', 'userProfile.views.changeParams'),
    url(r'^userprofiles/', 'userProfile.views.userProfiles'),
    url(r'^', 'userProfile.views.myProfile'),
)