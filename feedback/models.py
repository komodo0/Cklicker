# coding: utf-8
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

class FeedBackNote(models.Model):
    class Meta():
        verbose_name = u"Отзыв обратной связи"
        verbose_name_plural = u"Отзывы обратной связи"

    from_user = models.ForeignKey(User, blank=False, null=False, related_name="from_user")
    to_user = models.ForeignKey(User, blank=False, null=False)
    feedback_date = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    feedback_body = models.TextField(blank=False, null=False)
    has_been_read = models.BooleanField(blank=False, null=False, default=False)

    def __str__(self):
        return self.date + " " + self.from_user