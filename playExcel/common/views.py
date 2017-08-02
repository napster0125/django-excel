# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse

from .models import *

import json
import urllib2
# Create your views here.

def home(request):
	return render(request,'signup.html',{})

def getUserData(token):
	return json.loads( urllib2.urlopen('https://www.googleapis.com/oauth2/v3/tokeninfo?id_token=%s'%token).read() )

def signin(request):
	data = getUserData(request.POST['token'])
	obj,created = User.objects.get_or_create(user_id = data['sub'],
		username = data['name'],
		profile_picture = data['picture'],
		email = data['email']
		)

	return JsonResponse({ 'success' : True })

def signout(request):
	request.session.flush()
	return JsonResponse({ 'success' : True })