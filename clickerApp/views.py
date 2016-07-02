# coding: utf-8
from types import NoneType
from django.shortcuts import render_to_response, redirect
from clickerApp.models import State, StateUserNotes, Tip, CheckboxInput, TextInput, RadioInput, RadioInputVariant, FunctionsBase, GlobalUserNotes
from django.contrib import auth
from django.http import HttpResponse

def IndexView(request):
    if request.is_ajax():
        try:
            comment_usr = auth.get_user(request)
            is_global = request.POST.get('is_global', '')
            comment = request.POST.get('note_body', '')
            if is_global == "true":
                try:
                    note = GlobalUserNotes.objects.get(user=comment_usr)
                    note.delete()
                    GlobalUserNotes.objects.create(user=comment_usr, note_body=comment)
                except:
                    GlobalUserNotes.objects.create(user=comment_usr, note_body=comment)
                return HttpResponse("1")
            else:
                state_id = request.POST.get('state_id', '')
                try:
                    note = StateUserNotes.objects.get(state=State.objects.get(id=state_id), user=comment_usr)
                    note.delete()
                    StateUserNotes.objects.create(state=State.objects.get(id=state_id), user=comment_usr, note_body=comment)
                except:
                    StateUserNotes.objects.create(state=State.objects.get(id=state_id), user=comment_usr, note_body=comment)
                return HttpResponse("1")
        except:
            return HttpResponse("-1")

    beginState = -1
    fun = FunctionsBase()
    args = {}


    args['username'] = auth.get_user(request).username

    if not args['username']:
        args['user_is_staff'] = False
        return redirect("/auth/login/")
    else:
        args['user_is_staff'] = auth.get_user(request).is_staff

    states = State.objects.order_by("path").values()

    for state in states:
        state['depth'] = len(state['path'])/3 - 1

    i = 0
    for state in states:
        if i==0:
            state['pre_tags'] = "<ul class='Container'><li class='Node IsRoot ExpandClosed'>".encode("utf8")
            state['post_tags'] = fun.printPostTags(state, states[i+1])
        if i==len(states)-1:
            state['pre_tags'] = fun.printPreTagsForLast(state, states[i-1])
            state['post_tags'] = fun.printPostTagsForLast(state)
        if i!=len(states)-1 and i!=0:
            state['pre_tags'] = fun.printPreTags(state, states[i-1], states[i+1])
            state['post_tags'] = fun.printPostTags(state, states[i+1])
        if type(state['parent_id']) == NoneType:
            beginState = state['id']
        i+=1

    args['states'] = states
    args['tips'] = Tip.objects.all().values()
    args['checkbox_inputs'] = CheckboxInput.objects.all().values()
    args['text_inputs'] = TextInput.objects.all().values()
    args['radio_inputs'] = RadioInput.objects.all().values()
    args['radio_input_variants'] = RadioInputVariant.objects.all().values()
    args['state_usernotes'] = StateUserNotes.objects.filter(user = auth.get_user(request)).values()
    response = render_to_response('clicker_content.html', args)
    response.set_cookie("fist_step_id", beginState)
    return response

def ReinitializeSteps(request):
    fun = FunctionsBase()
    fun.reinitializeStates()
    return render_to_response(IndexView)

def SchemaView(request):

    fun = FunctionsBase()

    args = {}

    args['username'] = auth.get_user(request).username

    if not args['username']:
        args['user_is_staff'] = False
        return redirect("/auth/login/")
    else:
        if not auth.get_user(request).is_staff:
            return redirect("/")
        args['user_is_staff'] = auth.get_user(request).is_staff


    states = State.objects.all()

    for state in states:
        state.state_level = fun.getStateLevel(state)
        state.state_width = len(fun.getLeavesId(state))
        state.cell_rowspan = fun.getStateRowspan(state)


    full_depth = fun.getTreeDepth()
    formatted_states = []

    i = 1
    while i <= full_depth:
        formatted_states.append(i)
        formatted_states[i-1] = []
        for state in states:
            if state.state_level == i:
                formatted_states[i-1].append(state)
        i += 1


    for level in formatted_states:
        if len(level) == 1:
            level[0].position = 0
        else:
            i = 0
            while i < len(level):
                state = level[i]
                if (i==0):
                    if state.parent == level[i+1].parent:
                        state.position = 1
                    else:
                        state.position = 0
                elif (i==len(level)-1):
                    if state.parent == level[i-1].parent:
                        state.position = 3
                    else:
                        state.position = 0
                else:
                    if state.parent == level[i-1].parent:
                        if state.parent == level[i+1].parent:
                            state.position = 2
                        else:
                            state.position = 3
                    elif state.parent == level[i+1].parent:
                        state.position = 1
                    else:
                        state.position = 0

                i+=1













    args['states'] = formatted_states



    response = render_to_response('clicker_schema.html', args)
    return response

def Statistic(request):

    args = {}

    args['username'] = auth.get_user(request).username

    if not args['username']:
        args['user_is_staff'] = False
        return redirect("/auth/login/")
    else:
        if not auth.get_user(request).is_staff:
            return redirect("/")
        args['user_is_staff'] = auth.get_user(request).is_staff


    response = render_to_response('clicker_statistic.html', args)
    return response
