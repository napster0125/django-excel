from django.conf.urls import url,include
from .views import echoHome

urlpatterns = [
    url(r'^', echoHome),
]