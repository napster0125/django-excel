# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from common.decorators import isLoggedIn
from common.models import User
import datetime
from .models import level
from .models import submittedanswer
from .models import kryptosuser
import json

# Create your views here.
@csrf_exempt
@isLoggedIn
def kryptoshome(request):
	#getuser and level ,render clue
	loginUser = request.session['user']

	usr = User.objects.get(user_id=loginUser)
	print(usr.username)
	print(loginUser)
	usrobj, created = kryptosuser.objects.get_or_create(user_id = usr,
    defaults={'user_level' : 1,'last_anstime':datetime.datetime.now()},)
	levelint = usrobj.user_level
	#check whether last level
	last_level = 3
	if levelint > last_level :
		levelint = 100
		#image - 'new levels coming' 
	#check for advanced levels here
	levelobj = level.objects.get(level = levelint)
	response = {'level':levelobj.level,'type':levelobj.filetype,'source':levelobj.source_hint ,'image':str(levelobj.level_file)}
	return JsonResponse(response)

	# return render(request,'kryptos.html')

@csrf_exempt
@isLoggedIn
def matchanswer(request):
	data = request.POST
	# user = 'usertwo'
	loginUser = request.session['user']
	print(loginUser)
	usr = User.objects.get(user_id=loginUser)
	print(usr.username)
	# print data['answer']
	kryptosplayer = kryptosuser.objects.get(user_id=usr.user_id)
	ans_obj = submittedanswer(user_id = kryptosplayer,submitted_answer = data['answer'])
	ans_obj.save()
	# print curr_level.user_level
	curr_level = level.objects.get(level = kryptosplayer.user_level)
	if curr_level.answer == data['answer']:
		state = True
		kryptosplayer.user_level = kryptosplayer.user_level + 1
		kryptosplayer.last_anstime = datetime.datetime.now()
		kryptosplayer.save()
	else:
		state = False	

	response = {'valid' : state}
	return JsonResponse(response)

	# return render(request,'kryptos.html')



