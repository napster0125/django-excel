# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse,HttpResponse

from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from common.decorators import isLoggedIn
from .models import *

from oauth2client import client, crypt
# Create your views here.

CLIENT_ID = "1085661962609-79u3us6bbkp6m9gponccdomgrlv7m9pv.apps.googleusercontent.com"


# This function (and the associated html,js) is temporary,
# will be replaced once UI is ready.
def home(request):
	return render(request,'signup.html',{})


# This function puts the login info inside request.session
# from where all the other app can take the info like user_id
# by accessing request.session['user']
@csrf_exempt
def signin(request):
	''' Get token from the js client in frontend '''
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

def signout(request):
	request.session.flush()
	return JsonResponse({ 'success' : True })



#This is how we cache a view. Here the result of function will be cached for 10secs.
@cache_page(10)
def testCache(request):
	print('This func called')
	return JsonResponse({'message': 'Testing django cache'})


# This will ensure that the function testLoginCheck is 
# only executed when user is logged in
# otherwise it would return -> JsonResponse({'error' : 'User not logged in'})
@isLoggedIn
def testLoginCheck(request):
	print(request.META)
	return JsonResponse({'message': 'this user in logged in'})





'''
def test(request,req_no):
	for i in range(20):
		y = 0
		x = 0
		for j in range(10000000):
			x = y + 1
		print('Processing req %s'%req_no)
	return HttpResponse('Received req %s'%req_no)
'''
