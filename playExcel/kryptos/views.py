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
	last_level = 20
	if levelint > last_level :
		levelint = 100
		#image - 'new levels coming' 
	levelobj = level.objects.get(level = levelint)
	response = {'level':levelobj.level,'type':levelobj.filetype,'source':levelobj.source_hint ,'image':str(levelobj.level_file)}
	return JsonResponse(response)

	# return render(request,'kryptos.html')

@csrf_exempt
@isLoggedIn
def matchanswer(request):
	data = request.POST
	loginUser = request.session['user']
	print(loginUser)
	usr = User.objects.get(user_id=loginUser)
	print(usr.username)
	kryptosplayer = kryptosuser.objects.get(user_id=usr.user_id)
	ans_obj = submittedanswer(user_id = kryptosplayer,submitted_answer = data['answer'])
	ans_obj.save()
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

@csrf_exempt
@isLoggedIn
def rank(request):
	loginUser = request.session['user']
	allkryptosusers =kryptosuser.objects.order_by('user_level','last_anstime')
	ranklist = []
	rank=1
	for userobj in allkryptosusers:
		user = {'rank':rank,'pic':userobj.user_id.profile_picture,'username':userobj.user_id.username,'level':userobj.user_level}
		ranklist.append(user)
		if userobj.user_id.user_id == loginUser:
			print("Iam user")
			myrank = rank
		rank = rank +1
	response = {'ranklist':ranklist,'myrank':myrank}
	return JsonResponse(response)



