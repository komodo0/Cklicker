# coding: utf-8
from tempfile import template

from django.shortcuts import render_to_response
from clickerApp.models import State, Tip, CheckboxInput, TextInput, RadioInput, RadioInputVariant, FunctionsBase

def IndexView(request):
    fun = FunctionsBase()
    args = {}
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
        i+=1


    args['states'] = states
    args['tips'] = Tip.objects.all().values()
    args['checkbox_inputs'] = CheckboxInput.objects.all().values()
    args['text_inputs'] = TextInput.objects.all().values()
    args['radio_inputs'] = RadioInput.objects.all().values()
    args['radio_input_variants'] = RadioInputVariant.objects.all().values()
    return render_to_response('IndexView.html', args)

def AboutView(request):
    args = {}
    return render_to_response('about.html', args)
