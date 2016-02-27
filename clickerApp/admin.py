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
    list_filter = ["state_title", "parent", "move_title"]
    inlines = [ClickerTip, ClickerCheckboxInput, ClickerTextInput, ClickerRadioInput]

    fieldsets = (
        ('ParentChoise', {
            'fields': ('parent', 'state_title', 'add_title_to_comment'),
        }),
        ('CurrentContent', {
            'fields': ('move_title', 'move_description')
        }),
    )


class ClickerRadioInputVariant(admin.TabularInline):
    model = RadioInputVariant
    extra = 2


class RadioInputAdmin(admin.ModelAdmin):
    inlines = [ClickerRadioInputVariant]


admin.site.register(State, ClickerState)
admin.site.register(RadioInput, RadioInputAdmin)
