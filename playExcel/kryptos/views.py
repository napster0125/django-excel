# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from common.models import User
from .models import level
from .models import kryptosuser
import json

# Create your views here.
@csrf_exempt
def kryptoshome(request):
	#getuser and level ,render clue
	loginUser = request.session['user']

	usr = User.objects.get(user_id=loginUser)
	print usr.username
	print loginUser
	
	print num
	usrobj, created = kryptosuser.objects.get_or_create(user_id = usr.user_id,
    defaults={'user_level' : 1},)
	levelint = usrobj.user_level
	#check whether last level
	last_level = 10
	if levelint > last_level :
		levelint = 100
		#image - 'new levels coming' 
	#check for advanced levels here
	levelobj = level.objects.get(level = levelint)
	response = {'level':levelobj.level,'image':json.dumps(str(levelobj.level_image))}
	return JsonResponse(response)

	#return render(request,'kryptos.html')

@csrf_exempt
def matchanswer(request):
	data = request.POST
	# user = 'usertwo'
	loginUser = request.session['user']
	print loginUser
	usr = User.objects.get(user_id=loginUser)
	print usr.username
	# print data['answer']
	kryptosplayer = kryptosuser.objects.get(user_id=loginUser)
	# print curr_level.user_level
	curr_level = level.objects.get(level = kryptosplayer.user_level)
	if curr_level.answer == data['answer']:
		state = True
		kryptosplayer.user_level = kryptosplayer.user_level + 1
		kryptosplayer.save()
	else:
		state = False	

	response = {'valid' : state}
	return JsonResponse(response)

	# return render(request,'kryptos.html')
@csrf_exempt
def ranking(request):
	#to find top five positions
	
	return True


