from django.conf.urls import url,include
from .views import echoHome, echoRank

urlpatterns = [
    url(r'^$', echoHome),
    url(r'leaderboard', echoRank)
]