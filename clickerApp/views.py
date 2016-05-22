# coding: utf-8
from types import NoneType
from django.shortcuts import render_to_response, redirect
from clickerApp.models import State, Tip, CheckboxInput, TextInput, RadioInput, RadioInputVariant, FunctionsBase
from django.contrib import auth

def IndexView(request):

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

    i = 0
    for state in states:
        state['depth'] = len(state['path'])/3 - 1
        i += 1

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


