from django.conf.urls import url,include
from .views import kryptoshome
from .views import matchanswer
from .views import rank
from .views import myrank


urlpatterns = [
    url(r'submitanswer',matchanswer),
    url(r'ranklist',rank),
    url(r'myrank',myrank),


    url(r'^', kryptoshome),
    
    
]