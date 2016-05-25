# coding: utf-8
from types import NoneType
from django.shortcuts import render_to_response, redirect
from django.contrib import auth
from feedback.models import FeedBackNote
from django.contrib.auth.models import User
from Cklicker.project_config import PROJECT_ADMIN_USER_LOGIN
from feedback.models import FeedBackNote

def Index(request):

    args = {}
    args['username'] = auth.get_user(request).username

    if not args['username']:
        args['user_is_staff'] = False
        return redirect("/auth/login/")
    else:
        args['user_is_staff'] = auth.get_user(request).is_staff
        if (auth.get_user(request).username == PROJECT_ADMIN_USER_LOGIN):
            args['The_Creator_is_here'] = True
            args['new_feedback_count'] = len(FeedBackNote.objects.filter(has_been_read=False).exclude(from_user= User.objects.get(username=PROJECT_ADMIN_USER_LOGIN)))
        else:
            args['The_Creator_is_here'] = False



    user_messages = FeedBackNote.objects.filter(from_user=auth.get_user(request), to_user=User.objects.get(username=PROJECT_ADMIN_USER_LOGIN))
    admin_messages = FeedBackNote.objects.filter(from_user = User.objects.get(username="kotelnikov.ii"), to_user=auth.get_user(request))

    all_messages = list(user_messages)+ list(admin_messages)
    all_messages.sort(key= lambda x: x.feedback_date, reverse=True)

    args['feedback_notes'] = all_messages

    response = render_to_response('mainpage_basic.html', args)

    return response