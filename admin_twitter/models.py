from django.db import models
import uuid
from decimal import Decimal
import hashlib
import logging
import datetime

class Tweet(models.Model):
    id = models.CharField(primary_key=True,max_length=200, blank=True)
    date = models.DateTimeField('Date imported', default=datetime.datetime.now)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    replied = models.BooleanField(default=False)
    favourited = models.BooleanField(default=False)
    search = models.CharField(max_length=200, blank=True)

class Author(models.Model):
    id = models.CharField(primary_key=True,max_length=200, blank=True)
    date = models.DateTimeField('date', default=datetime.datetime.now)
    followed = models.BooleanField(default=False)

class Message(models.Model):
    date = models.DateTimeField('date', default=datetime.datetime.now)
    message = models.CharField(max_length=160)
    active = models.BooleanField(default=True)
