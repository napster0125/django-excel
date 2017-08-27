# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from common.models import User
# Create your models here.

class level(models.Model):
	level = models.IntegerField(default =1)
	answer = models.TextField(max_length=250)
	level_image =  models.FileField(upload_to = 'level_images/')
	

class kryptosuser(models.Model):
	user_id = models.OneToOneField(User,primary_key=True, on_delete=models.CASCADE)
	user_level = models.IntegerField(default =1	)

class submittedanswer(models.Model):
	user_id = models.ForeignKey(kryptosuser,on_delete=models.CASCADE)
	submitted_answer =  models.TextField()
	def __unicode__(self):
		return self.submitted_answer


