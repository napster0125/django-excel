from django.conf.urls import url,include
from .views import echoHome, echoRank, echoSubmit, echoLeaderboard

urlpatterns = [
    url(r'^$', echoHome),
    url(r'submit', echoSubmit),
    url(r'myrank', echoRank),
    url(r'leaderboard', echoLeaderboard),
]