# coding: utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class NewsPost(models.Model):
    title = models.CharField(max_length=300, null=False, blank=False)
    body = models.TextField(null=False, blank=False)
    author = models.ForeignKey(User, null=False, blank=False)
    creation_time = models.DateTimeField(auto_now_add=True)