# coding: utf-8
from types import NoneType
from django.shortcuts import render_to_response, redirect
from django.contrib import auth

def Index(request):

    args = {}
    args['username'] = auth.get_user(request).username

    if not args['username']:
        args['user_is_staff'] = False
        return redirect("/auth/login/")
    else:
        args['user_is_staff'] = auth.get_user(request).is_staff

    response = render_to_response('mainpage.html', args)

    return response