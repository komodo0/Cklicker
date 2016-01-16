# coding: utf-8
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class State(models.Model):
    class Meta():
        db_table = 'state'

    parent = models.ForeignKey('self', null=True, blank=True)
    state_title = models.CharField(max_length=200)
    move_title = models.CharField(max_length=300)
    move_description = models.TextField(max_length=2000, blank=True)

    def __str__(self):
        parent = self.parent
        parentTitle = parent.__str__()
        return parentTitle + " > " + \
               self.state_title.encode("utf8") + \
               " (" + self.move_title.encode("utf-8") + ")"

class Tip(models.Model):
    class Meta():
        db_table = 'tip'

    state_id = models.ForeignKey(State)
    tip_title = models.CharField(max_length=300)
    tip_description = models.TextField(max_length=2000, blank=True)

    def __str__(self):
        state_title = self.state_id.__str__()
        return state_title + " > " +  self.tip_title.encode("utf8")

class CheckboxInput(models.Model):
    class Meta():
        db_table = 'checkbox_input'

    state_input_id = models.ForeignKey(State)
    checkbox_input_title = models.CharField(max_length=300)

    def __str__(self):
        return self.state_input_id.__str__() + ": [ v ]  " + \
               self.checkbox_input_title.encode("utf8")

class TextInput(models.Model):
    class Meta():
        db_table = 'text_input'

    state_input_id = models.ForeignKey(State)
    text_input_title = models.CharField(max_length=300, blank=True)
    text_input_max_width = models.IntegerField(max_length=3)
    text_input_after = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.state_input_id.__str__() + ": " + \
               self.text_input_title.encode("utf8") + " [ ] " + \
               self.text_input_after.encode("utf8")

class RadioInput(models.Model):
    class Meta():
        db_table = 'radio_input'

    state_input_id = models.ForeignKey(State)
    radio_input_title = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.state_input_id.__str__() + ": ( o )  " + \
               self.radio_input_title.encode("utf8")


class RadioInputVariant(models.Model):
    class Meta():
        db_table = 'radio_input_variant'

    radio_input_id = models.ForeignKey(RadioInput)
    radio_input_variant_title = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.radio_input_id.__str__() + " " + \
               self.radio_input_variant_title.encode("utf8")