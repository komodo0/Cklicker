# coding: utf-8
from django.contrib import admin
from clickerApp.models import State, Tip, CheckboxInput, TextInput, RadioInput, RadioInputVariant


class ClickerTip(admin.TabularInline):
    model = Tip
    extra = 3


class ClickerRadioInput(admin.TabularInline):
    model = RadioInput
    extra = 1


class ClickerCheckboxInput(admin.TabularInline):
    model = CheckboxInput
    extra = 1


class ClickerTextInput(admin.TabularInline):
    model = TextInput
    extra = 1


class ClickerState(admin.ModelAdmin):
    inlines = [ClickerTip, ClickerCheckboxInput, ClickerTextInput, ClickerRadioInput]

    fieldsets = (
        ('ParentChoise', {
            'fields': ('parent', 'state_title', 'add_title_to_comment', 'variant_description'),
        }),
        ('CurrentContent', {
            'fields': ('move_title', 'move_description')
        }),
    )

    list_display = ('move_title', 'state_title', 'parent_move', 'parent_title',  'pro_parent_move', 'pro_parent_title')
    list_filter = ('move_title', 'state_title')


class ClickerRadioInputVariant(admin.TabularInline):
    model = RadioInputVariant
    extra = 2


class RadioInputAdmin(admin.ModelAdmin):
    inlines = [ClickerRadioInputVariant]


admin.site.register(State, ClickerState)
admin.site.register(RadioInput, RadioInputAdmin)
