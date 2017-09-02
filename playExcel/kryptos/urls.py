from django.conf.urls import url,include
from .views import kryptoshome
from .views import matchanswer
from .views import rank

urlpatterns = [
    url(r'submitanswer',matchanswer),
    url(r'ranklist',rank),

    url(r'^', kryptoshome),
    
    
]