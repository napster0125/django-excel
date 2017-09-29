from django.conf.urls import url
from .views import *

urlpatterns=[
        url(r'submitanswer',submit),
        url(r'ranklist',leaderboard),
        url(r'',home),
]