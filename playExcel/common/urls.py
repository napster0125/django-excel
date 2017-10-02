from django.conf.urls import url
from .views import signout,testCache,testLoginCheck,sign_in,getUserCount,getCookieAsJson,user_rank
urlpatterns = [
	#url(r'signin', signin ),
	url(r'sign_in', sign_in ),
	url(r'signout', signout ),
	#url(r'test/(\d+)', test ),
	url(r'testCache', testCache ),
	url(r'testLoginCheck', testLoginCheck ),
	url(r'getCookieAsJson',getCookieAsJson),
	url(r'getUserCount', getUserCount ),
	url(r'getRank',user_rank),
	#url(r'',home),
]
