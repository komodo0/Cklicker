# coding: utf-8
from types import NoneType
from django.shortcuts import render_to_response, redirect
from django.contrib import auth
from drive.models import Department, OperatorToDepartnemt
from django.contrib.auth.models import Group, PermissionsMixin, User
def myProfile(request):

    args = {}
    args['username'] = auth.get_user(request).username

    if not args['username']:
        args['user_is_staff'] = False
        return redirect("/auth/login/")
    else:
        args['user_is_staff'] = auth.get_user(request).is_staff

    user = auth.get_user(request)
    args['first_name'] = user.first_name
    args['last_name'] = user.last_name
    args['email'] = user.email
    args['department'] = OperatorToDepartnemt.objects.get(operator=user).department


    args['supervisor'] = None

    args['success_change'] = request.GET.get('success', '')

    response = render_to_response('userProfile_my_profile.html', args)

    return response



def userProfiles(request):

    args = {}
    args['username'] = auth.get_user(request).username

    if not args['username']:
        args['user_is_staff'] = False
        return redirect("/auth/login/")
    else:
        args['user_is_staff'] = auth.get_user(request).is_staff

    user = auth.get_user(request)
    args['first_name'] = user.first_name
    args['last_name'] = user.last_name
    args['email'] = user.email
    args['department'] = OperatorToDepartnemt.objects.get(operator=user).department


    args['supervisor'] = None
    args['path'] = request.path

    response = render_to_response('userProfile_user_profiles.html', args)

    return response


def changeParams(request):

    args = {}
    args['username'] = auth.get_user(request).username

    if not args['username']:
        args['user_is_staff'] = False
        return redirect("/auth/login/")
    else:
        args['user_is_staff'] = auth.get_user(request).is_staff


    username = request.POST.get('username', '')

    first_name = request.POST.get('first_name', '')
    last_name = request.POST.get('last_name', '')
    email = request.POST.get('email', '')

    if username == args['username']:
        #редактируем личный профиль
        try:
            user = User.objects.get(username = username)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            response = redirect('/profile/?success=1')
        except:
            response = redirect('/profile/?success=0')
    elif True: #вместо True ставить проверку на наличие прав редактирования группы пользователей
        #редактируем профиль юзера
        try:
            user = User.objects.get(username = username)
            response = redirect('/profile/userprofiles/?source=' + str(user.id) + '&success=1')
        except:
            response = redirect('/profile/userprofiles/?success=0')

    return response