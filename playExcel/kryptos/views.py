# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from common.decorators import isLoggedIn, playCookies
from common.models import User
import datetime
from .models import level
from .models import submittedanswer
from .models import kryptosuser
from common.utility import pushChangesKrytposLeaderboard
import json

# Create your views here.
@playCookies
@isLoggedIn
def kryptoshome(request):
	#getuser and level ,render clue
	loginUser = request.session['user']

	usr = User.objects.get(user_id=loginUser)
	print(usr.username)
	print(loginUser)
	usrobj, created = kryptosuser.objects.get_or_create(user_id = usr,
    defaults={'user_level' : 1,'last_anstime':datetime.datetime.now(),'rank':10000},)

	if created:
		print('created')
		print(kryptosuser.objects.all().count())
		usrobj.rank = kryptosuser.objects.all().count()
		usrobj.save()

	levelint = usrobj.user_level
	#check whether last level
	# last_level = 30
	# if levelint > last_level :
	# 	levelint = 100
	# 	#image - 'new levels coming'
	try:
		levelobj = level.objects.get(level = levelint)
	except level.DoesNotExist:
		levelobj = level(level=levelint)
		levelobj.save()
	response = {'level':levelobj.level,'type':levelobj.filetype,'source':levelobj.source_hint ,'image':str(levelobj.level_file)}
	return JsonResponse(response)

	# return render(request,'kryptos.html')

@playCookies
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
	if kryptosplayer.user_level == 9:
		name = ''.join(kryptosplayer.user_id.username.split()).lower()
		level_ans = name
		print(name)
	else :
		curr_level = level.objects.get(level = kryptosplayer.user_level)
		level_ans =  curr_level.answer
	if level_ans == data['answer']:
		state = True
		submittedanswer.objects.filter(user_id=kryptosplayer).delete()
		samelevelusers = kryptosuser.objects.filter(user_level=kryptosplayer.user_level)
		newrank = samelevelusers.order_by('last_anstime')[0]
		# print ('newrank')
		# print (newrank.rank)
		for slu in samelevelusers:
			if slu.last_anstime < kryptosplayer.last_anstime:
				slu.rank = slu.rank+1
				slu.save()
		kryptosplayer.user_level = kryptosplayer.user_level + 1
		kryptosplayer.last_anstime = datetime.datetime.now()
		kryptosplayer.rank = newrank.rank
		kryptosplayer.save()
		# toptenkryptosusers = kryptosuser.objects.order_by('rank')[:10]
		# topten = []
		# for userobj in toptenkryptosusers:
		# 	user = {'rank':userobj.rank,'pic':userobj.user_id.profile_picture,'username':userobj.user_id.username,'level':userobj.user_level}
		# 	topten.append(user)
		# pushChangesKrytposLeaderboard(topten)	
		pushChangesKrytposLeaderboard(rank(request))
	else:
		state = False
	response = {'valid' : state}
	return JsonResponse(response)


def rank(request):
	loginUser = request.session['user']
	topkryptosusers =kryptosuser.objects.order_by('rank')[:10]
	ranklist = []
	# rank=1
	myrank = kryptosuser.objects.get(user_id=loginUser).rank
	for userobj in topkryptosusers:
		user = {'rank':userobj.rank,'pic':userobj.user_id.profile_picture,'username':userobj.user_id.username,'level':userobj.user_level}
		ranklist.append(user)
		# if userobj.user_id.user_id == loginUser:
		# 	print("Iam user")
		# 	myrank = rank
		# rank = rank +1
	response = {'ranklist':ranklist}
	return response


def allplayersrank(request):
	topkryptosusers =kryptosuser.objects.order_by('rank')
	ranklist = []
	for userobj in topkryptosusers:
		user = {'rank':userobj.rank,'username':userobj.user_id.username,'level':userobj.user_level}
		ranklist.append(user)
		
	response = {'ranklist':ranklist}
	return JsonResponse(response)

@playCookies
@isLoggedIn
def rankList(request):
	return JsonResponse(rank(request))


@playCookies
@isLoggedIn
def myrank(request):
	loginUser = request.session['user']
	rank = kryptosuser.objects.get(user_id=loginUser).rank
	response = {'rank':rank}
	return JsonResponse(response)
