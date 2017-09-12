# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from common.models import User
# Create your models here.

class level(models.Model):
	options = (
        ('A', 'Audio'),
        ('I', 'Image'),
        ('G', 'Gif'),
    )
	level = models.IntegerField(default =1)
	answer = models.TextField()
	source_hint = models.TextField(blank=True,null=True)
	level_file =  models.FileField(upload_to = 'level_images/',null=True)
	filetype = models.CharField(max_length = 10,choices=options,default='Audio')
	def __str__(self):
		return str(self.level)
	

class kryptosuser(models.Model):
	user_id = models.OneToOneField(User,primary_key=True, on_delete=models.CASCADE)
	user_level = models.IntegerField(default =1	)
	last_anstime = models.DateTimeField()
	rank = models.IntegerField()
	def __str__(self):
		return self.user_id.username
	


class submittedanswer(models.Model):
	user_id = models.ForeignKey(kryptosuser,on_delete=models.CASCADE)
	submitted_answer =  models.TextField()
	def __str__(self):
		return self.submitted_answer


