from django.http import JsonResponse
from django.middleware.csrf import get_token as getCsrfToken
import json

def isLoggedIn(view_func):
	def new_view_func(request):
		if request.session.get('logged_in',False):
			return view_func(request)
		else:
			return JsonResponse({'error' : 'User not logged in'})
	return new_view_func

def isLoggedInCh(conn_func):
	def new_conn_func(message):
		if message.http_session.get('logged_in',False):
			return conn_func(message)
		else:
			message.reply_channel.send({
				'text' : json.dumps({ "close" : True })
			})
	return new_conn_func

def playCookies(view_func):
	def new_view_func(request):
		ret = view_func(request)
		if 'csrftoken' not in request.COOKIES:
			ret.set_cookie('csrftoken',getCsrfToken(request),2592000)
		return ret
	return new_view_func


def androidFriendly(view_func):
	def new_view_func(request):
		if request.method == 'POST':
			if request.META.get('HTTP_MOBILE',False):
				request.POST = json.loads(request.body.decode('utf-8')) 
		ret = view_func(request)
		return ret
	return new_view_func