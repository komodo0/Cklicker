# coding: utf-8
from tempfile import template

from django.shortcuts import render_to_response
from clickerApp.models import State, Tip, CheckboxInput, TextInput, RadioInput, RadioInputVariant

def IndexView(request):
    args = {}
    args['states'] = State.objects.all()
    args['tips'] = Tip.objects.all()
    args['checkbox_inputs'] = CheckboxInput.objects.all()
    args['text_inputs'] = TextInput.objects.all()
    args['radio_inputs'] = RadioInput.objects.all()
    args['radio_input_variants'] = RadioInputVariant.objects.all()
    return render_to_response('IndexView.html', args)

def AboutView(request):
    args = {}
    return render_to_response('about.html', args)
