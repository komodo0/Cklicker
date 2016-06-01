# coding: utf-8
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from feedback.models import FeedBackNote
from Cklicker.project_config import PROJECT_ADMIN_USER_LOGIN
from django.db.models import Count,Max


def FeedbackBeenRead(request):
    if request.is_ajax():
        try:
            messages_for = auth.get_user(request)
            message_from_id = request.POST.get('usr', '')
            messages_from = User.objects.get(id=message_from_id)
            messages = FeedBackNote.objects.filter(from_user = messages_from, to_user = messages_for, has_been_read = False)
            messages.update(has_been_read=True)
            messages.save()
            return HttpResponse("1")
        except:
            return HttpResponse("-1")

# Create your views here.
def SendFeedbackView(request):
    if request.is_ajax():
        args = {}
        args['username'] = auth.get_user(request).username
        if not args['username']:
            return HttpResponse("-1")

        try:
            is_addressed = request.POST.get('addressed', '')
            if is_addressed == "yes":
                is_addressed = True
            else:
                is_addressed = False

            if is_addressed:
                try:
                    feedback_to = User.objects.get(id=request.POST.get('feedback_to_user', ''))
                except:
                    return HttpResponse("-1")
            else:
                feedback_to = User.objects.get(username=PROJECT_ADMIN_USER_LOGIN)

            feedback_from = User.objects.get(username=args['username'])
            feedback_body = request.POST.get('feedback_comment', '')

            if (feedback_from == User.objects.get(username=PROJECT_ADMIN_USER_LOGIN)):
                has_been_read = True
            else:
                has_been_read = False

            feedback = FeedBackNote(from_user = feedback_from, to_user = feedback_to, feedback_body = feedback_body, has_been_read = has_been_read)
            feedback.save()
            result = "1"
        except:
            result = "-1"

        return HttpResponse(result)


def ShowFeedbackView(request):
    args={}
    args['username'] = auth.get_user(request).username
    if (auth.get_user(request).username != PROJECT_ADMIN_USER_LOGIN):
        return redirect("/auth/login/")
    else:
        The_creator = User.objects.get(username=PROJECT_ADMIN_USER_LOGIN)
        args['user_is_staff'] = True
        args['The_Creator_is_here'] = True
        args['new_feedback_count'] = len(FeedBackNote.objects.filter(has_been_read=False).exclude(from_user= The_creator))

        address_list = FeedBackNote.objects.filter(to_user = The_creator).values("from_user").annotate(last_id=Max('id')).order_by("-last_id")
        address_list = list(address_list)
        messages_count = FeedBackNote.objects.filter(to_user = The_creator).exclude(has_been_read = True).values('from_user').annotate(count=Count('id'))
        for address in address_list:
            address['user'] = User.objects.get(id=address['from_user'])
            for usr_nw_msg in messages_count:
                if (usr_nw_msg['from_user']==address['from_user']):
                    address['message_count'] = usr_nw_msg['count']
        args['address_list'] = address_list

        user_id = request.GET.get('usr', '')

        if not user_id:
            return render_to_response('feedback_view_for_creator.html', args)
        else:
            try:
                user = User.objects.get(id=user_id)
                args['target_user'] = user
                user_messages = FeedBackNote.objects.filter(from_user=user, to_user=The_creator)
                admin_messages = FeedBackNote.objects.filter(from_user = The_creator, to_user=user)
                all_messages = list(set(user_messages) | set(admin_messages))
                all_messages.sort(key= lambda x: x.feedback_date, reverse=True)
                args['feedback_notes'] = all_messages
            except:
                return render_to_response('feedback_view_for_creator.html', args)

    return render_to_response('feedback_view_for_creator.html', args)