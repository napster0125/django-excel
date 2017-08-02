from django.conf.urls import url
from .views import signin,home,signout
urlpatterns = [
	url(r'signin', signin ),
	url(r'signout', signout ),
	url(r'',home),
]
