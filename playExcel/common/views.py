# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse,HttpResponse

from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from common.decorators import isLoggedIn, playCookies, androidFriendly
from .models import *
from .consumers import user_count_channel_push, disconnectAll
from dalalbull.consumers import disconnectFromDalalbullCh
from hashinclude.models import hiuser
from kryptos.models import kryptosuser
from urllib import request as rq
import json

# Create your views here.


# This function (and the associated html,js) is temporary,
# will be replaced once UI is ready.
# def home(request):
# 	return render(request,'signup.html',{})

# This function puts the login info inside request.session
# from where all the other app can take the info like user_id
# by accessing request.session['user']

from dalalbull.consumers import sellDataPush,niftyChannelDataPush,leaderboardChannelDataPush,graphDataPush,portfolioDataPush,tickerDataPush

@csrf_exempt
def test_db_channels(request):
	if request.method=="POST":
		print(request.POST)
		if 'ticker' in request.POST:
			tickerDataPush()
		if 'nifty' in request.POST:
			niftyChannelDataPush()
		if 'protfolio' in request.POST: 
			portfolioDataPush()
		if 'graph' in request.POST:
			graphDataPush()
		if 'leaderboard' in request.POST:
			leaderboardChannelDataPush()
		if 'sell' in request.POST:
			sellDataPush()

	return render(request,'try_channels.html')

@csrf_exempt
@playCookies
@androidFriendly
def sign_in(request):
	if 'access_token' in request.POST:
		access_token = request.POST['access_token']
	else:
		return JsonResponse({ 'success' : False })

	try:
		headers = { 'Authorization' : 'Bearer %s'%access_token }
		req = rq.Request('https://excelplay2k17.auth0.com/userinfo',headers=headers)
		data = json.loads( rq.urlopen(req).read().decode("utf-8") )
	except:
		return JsonResponse({ 'success' : False })

		
	obj,created = User.objects.get_or_create(user_id = data['sub'],
		username = data['name'],
		profile_picture = data['picture'],
		email = data['email']
		)

	if created:
		user_count_channel_push({'count': User.objects.all().count() })

	request.session['user'] = obj.user_id

	request.session['logged_in'] = True

	return JsonResponse({ 'success' : True })



@playCookies
@isLoggedIn
def getUserCount(request):
	return JsonResponse({'count': User.objects.all().count() })

@playCookies
def signout(request):
	disconnectAll(request.session['user'])
	disconnectFromDalalbullCh(request.session['user'])
	request.session.flush()
	return JsonResponse({ 'success' : True })



#This is how we cache a view. Here the result of function will be cached for 10secs.
@playCookies
def testCache(request):
	print('This func called')
	return JsonResponse({'message': 'Testing django cache'})


# This will ensure that the function testLoginCheck is 
# only executed when user is logged in
# otherwise it would return -> JsonResponse({'error' : 'User not logged in'})
@playCookies
@isLoggedIn
def testLoginCheck(request):
	print("Cookies: ",request.COOKIES)
	return JsonResponse({'message': 'this user is logged in'})


# Function that returns rank of all events

@playCookies
@isLoggedIn

def user_rank(request):
    loginUser=request.session['user']
    try:
        kryptos_rank=kryptosuser.objects.get(user_id=loginUser).rank
    except kryptosuser.DoesNotExist:
        kryptos_rank="N/A"
    try:
        hi_rank=hiuser.objects.get(user_id=loginUser).rank
    except hiuser.DoesNotExist:
        hi_rank="N/A"
    user_ranklist=[{'krytosrank':kryptos_rank},{'hirank':hi_rank},{'echorank':'N/A'},{'dbrank':'N/A'},{'convrank':'N/A'}]
    response={'userRankList':user_ranklist}
    return JsonResponse(response)

"""
@csrf_exempt
def signin(request):
	# Get token from the js client in frontend 
	try:
		data = client.verify_id_token(request.POST['token'], CLIENT_ID)
	except:
		return JsonResponse({ 'success' : False })

	obj,created = User.objects.get_or_create(user_id = data['sub'],
		username = data['name'],
		profile_picture = data['picture'],
		email = data['email']
		)

	if 'user' not in request.session:
		request.session['user'] = obj.user_id

	request.session['logged_in'] = True

	return JsonResponse({ 'success' : True })


def test(request,req_no):
	for i in range(20):
		y = 0
		x = 0
		for j in range(10000000):
			x = y + 1
		print('Processing req %s'%req_no)
	return HttpResponse('Received req %s'%req_no)
"""
