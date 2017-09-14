# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class User(models.Model):
	user_id = models.CharField(primary_key=True,max_length=100)
	username = models.CharField(max_length=100)
	profile_picture = models.URLField()
	email = models.EmailField()
	
	def __str__(self):
		return self.username

