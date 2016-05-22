# coding: utf-8
from types import NoneType
from django.shortcuts import render_to_response, redirect
from django.contrib import auth

def Tops(request):

    args = {}
    args['username'] = auth.get_user(request).username

    if not args['username']:
        args['user_is_staff'] = False
        return redirect("/auth/login/")
    else:
        args['user_is_staff'] = auth.get_user(request).is_staff

    response = render_to_response('testing_tops.html', args)

    return response





def Results(request):

    args = {}
    args['username'] = auth.get_user(request).username

    if not args['username']:
        args['user_is_staff'] = False
        return redirect("/auth/login/")
    else:
        args['user_is_staff'] = auth.get_user(request).is_staff

    response = render_to_response('testing_results.html', args)

    return response




def Statistic(request):

    args = {}
    args['username'] = auth.get_user(request).username

    if not args['username']:
        args['user_is_staff'] = False
        return redirect("/auth/login/")
    else:
        args['user_is_staff'] = auth.get_user(request).is_staff

    response = render_to_response('testing_statistic.html', args)

    return response




def TestList(request):

    args = {}
    args['username'] = auth.get_user(request).username

    if not args['username']:
        args['user_is_staff'] = False
        return redirect("/auth/login/")
    else:
        args['user_is_staff'] = auth.get_user(request).is_staff

    response = render_to_response('testing_test_list.html', args)

    return response