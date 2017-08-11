from django.conf.urls import url,include
from .views import kryptoshome
from .views import matchanswer

urlpatterns = [
    url(r'submitanswer',matchanswer),

    url(r'^', kryptoshome),
    
    
]