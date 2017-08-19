from django.conf.urls import url
from .views import signin,home,signout,testCache,testLoginCheck
urlpatterns = [
	url(r'signin', signin ),
	url(r'signout', signout ),
	#url(r'test/(\d+)', test ),
	url(r'testCache', testCache ),
	url(r'testLoginCheck', testLoginCheck ),
	url(r'',home),
]