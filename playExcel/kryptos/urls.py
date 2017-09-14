from django.conf.urls import url,include
from .views import kryptoshome
from .views import matchanswer
from .views import myrank
from .views import rankList

urlpatterns = [
    url(r'submitanswer',matchanswer),
    url(r'ranklist',rankList),
    url(r'myrank',myrank),
    url(r'^', kryptoshome),   
]