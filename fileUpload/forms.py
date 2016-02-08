# -*- coding: utf-8 -*-
from django import forms

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Выберите файл:',
        help_text='(максимальный размер - 42 Мегабайта)'
    )