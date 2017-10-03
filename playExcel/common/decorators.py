from django.http import JsonResponse
from django.middleware.csrf import get_token as getCsrfToken
import json

from django.views.decorators.csrf import ensure_csrf_cookie,csrf_exempt,csrf_protect

def isLoggedIn(view_func):
	def new_view_func(request):
		if request.session.get('logged_in',False):
			print('User is logged in')
			return view_func(request)
		else:
			print('User is not logged in')
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
def convert(inp):
        try:
                return int(inp)
        except ValueError:
                try:
                        return float(inp)
                except:
                        return inp

def androidFriendly(view_func):
    @csrf_exempt    
    def new_view_func(request):
        print('Cookies: ',request.COOKIES,'\n\n\n',request.META)
        if request.method == 'POST':
            if request.META.get('HTTP_MOBILE',False):
                print('\n\nData: ',request.body,'\n\n')

                #temp = str(request.body)[2:-1].split('&')
                #try:
                request.POST = json.loads(request.body.decode('utf-8'))#.replace('\0', '')) 
                #except:
                #    request.POST = { i.split('=')[0] : convert(i.split('=')[1]) for i in temp }

        print("%s is about to be called"%view_func.__name__)
        ret = csrf_protect(view_func)(request)
        print("%s was called"%view_func.__name__)
        return ret
    return new_view_func

