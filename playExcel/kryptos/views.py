# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import level
from .models import kryptosuser
import json

# Create your views here.
@csrf_exempt
def kryptoshome(request):
	print 'haha'
	#getuser and level ,render clue
	user = 'usertwo'
	
	userobj = kryptosuser.objects.get(user_id=user)
	levelint = userobj.user_level
	print levelint
	#check for advanced levels here
	levelobj = level.objects.get(level = levelint)
	response = {'level':levelobj.level,'image':json.dumps(str(levelobj.level_image))}
	
	print levelobj.level_image
	# return JsonResponse(response)

	return render(request,'kryptos.html')

@csrf_exempt
def matchanswer(request):
	data = request.POST
	user = 'usertwo'
	print data['answer']
	curr_level = kryptosuser.objects.get(user_id=user)
	print curr_level.user_level
	finalans = level.objects.get(level = curr_level.user_level)
	if finalans.answer == data['answer']:
		state = True
	else:
		state = False	

	response = {'valid' : state}
	return JsonResponse(response)

	# return render(request,'kryptos.html')


