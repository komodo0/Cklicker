# coding: utf-8
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^send/', 'feedback.views.SendFeedbackView'),
    url(r'^show/', 'feedback.views.ShowFeedbackView'),
    url(r'^feedback-been-read/', 'feedback.views.FeedbackBeenRead'),
    url(r'^', 'mainpage.views.Index'),
)
