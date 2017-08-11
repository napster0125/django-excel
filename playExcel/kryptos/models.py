# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class level(models.Model):
	level = models.IntegerField(default =1)
	answer = models.CharField(max_length=250)
	level_image =  models.ImageField(upload_to = 'level_images/')
	

class kryptosuser(models.Model):
	user_id = models.CharField(primary_key=True,max_length=200)
	user_level = models.IntegerField(default =1	)