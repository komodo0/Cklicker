# coding: utf-8
from types import NoneType
from django.db import models


class TreeOrderField(models.CharField):
     def pre_save(self, model_instance, add):
         parent=(model_instance.parent)
         if type(parent) != NoneType:
             parent.seq+=1
             parent.save()
             value=('%s%03d'%(getattr(parent, self.attname, ''), parent.seq, ))[:255]
         else:
             value = "001"
         setattr(model_instance, self.attname, value)
         return value


class State(models.Model):
    class Meta():
        db_table = 'state'

    parent = models.ForeignKey('self', null=True, blank=True, related_name='child_set')
    state_title = models.CharField(max_length=200)
    move_title = models.CharField(max_length=300)
    move_description = models.TextField(max_length=2000, blank=True)
    seq = models.PositiveIntegerField(default=0)
    path = TreeOrderField(max_length=255, blank=True)

    @property
    def level(self):
        return max(0, len(self.path)/3-1)

    def alredyUpdated(self):
        if self.seq == 0:
            return False
        else:
            return True

    def __str__(self):
        parent = self.parent
        if type(parent) == NoneType:
            parentTitle = "[root]"
        else:
            parentTitle = parent.state_title.encode("utf8") + " (" + parent.move_title.encode("utf-8") + ")"
            pro_parent = parent.parent
            if type(pro_parent) == NoneType:
                parentTitle = parentTitle + "< [root]"
            else:
                parentTitle = parentTitle + " < " + pro_parent.state_title.encode("utf8") + " (" + pro_parent.move_title.encode("utf-8") + ")"

        return self.state_title.encode("utf8") + \
               " (" + self.move_title.encode("utf-8") + ")" + \
               " < " + parentTitle



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
    text_input_max_width = models.IntegerField()
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


class FunctionsBase():
    def printPreTags(self, currentState, preState, postState):
        isLeaf = False
        if currentState['depth'] >= postState['depth']:
            isLeaf = True
        result = ""

        count = currentState['depth'] - preState['depth']
        if count > 0:
            if isLeaf:
                result = "<ul class='Container'><li class='Node ExpandLeaf'>"
            else:
                result = "<ul class='Container'><li class='Node ExpandClosed'>"
        if count <= 0:
            if isLeaf:
                result = "<li class='Node ExpandLeaf'>"
            else:
                result = "<li class='Node ExpandClosed'>"
        return result.encode("utf8")

    def printPreTagsForLast(self, currentState, preState):
        count = currentState['depth'] - preState['depth']
        if count > 0:
            result = "<ul class='Container'><li class='Node ExpandLeaf'>"
        if count <= 0:
            result = "<li class='Node ExpandClosed ExpandLeaf'>"
        return result.encode("utf8")

    def printPostTags(self, currentState, postState):
        result = ""
        count = currentState['depth'] - postState['depth']

        if count > 0:
            j = 0
            while j < count:
                result+="</li></ul>"
                j+=1
            result+="</li>"
        if count < 0:
            result = ""
        if count == 0:
            result = "</li>"
        return result.encode("utf8")

    def printPostTagsForLast(self, currentState):
        result = ""
        count = currentState['depth']
        if count > 0:
            j = 0
            while j <= count:
                result+="</li></ul>"
                j+=1
        if count == 0:
            result = "</li>"
        return result.encode("utf8")


    #Позволяет "Починить дерево, когда оно едет. Связано это с кривым pre_save в TreeOrderField"
    #Я его, конечно, починю, но пока не до этого
    #Данная прикручено
    #Прежде чем запускать требуется переопределить pre_save для TreeOrderField следующим образом:
    #     def pre_save(self, model_instance, add):
    #         value = model_instance.path
    #         setattr(model_instance, self.attname, value)
    #         return value
    def reinitializeStates(self):
        states = State.objects.all()
        for state in states:
            seq = 0
            for inner_state in states:
                if inner_state.parent_id == state.id:
                    seq+=1
            state.seq = seq

            if type(state.parent) == NoneType:
                state.path = "001"
            else:
                counter = 1
                parent_seq = state.parent.seq
                parent_path = state.parent.path
                current_path = parent_path + "001"
                for inner_state in states:
                    if inner_state.path == current_path:
                        counter += 1
                        current_path = parent_path + "00" + str(counter)

                state.path = current_path

            state.save()
