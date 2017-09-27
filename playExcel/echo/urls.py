from django.conf.urls import url,include
from .views import echoHome, echoRank, echoSubmit

urlpatterns = [
    url(r'^$', echoHome),
    url(r'submit', echoSubmit),
    url(r'leaderboard', echoRank),
]