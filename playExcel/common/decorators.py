from threading import Thread, Lock
from django.http import JsonResponse
from django.middleware.csrf import get_token as getCsrfToken
def isLoggedIn(view_func):
	def new_view_func(request):
		if request.session.get('logged_in',False):
			return view_func(request)
		else:
			return JsonResponse({'error' : 'User not logged in'})
	return new_view_func


def playCookies(view_func):
	def new_view_func(request):
		ret = view_func(request)
		if 'csrftoken' not in request.COOKIES:
			ret.set_cookie('csrftoken',getCsrfToken(request),2592000)
		return ret
	return new_view_func
