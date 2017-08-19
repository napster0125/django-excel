from threading import Thread, Lock
from django.http import JsonResponse

def isLoggedIn(view_func):
	def new_view_func(request):
		if request.session.get('logged_in',False):
			return view_func(request)
		else:
			return JsonResponse({'error' : 'User not logged in'})
	return new_view_func
