from django.conf.urls import url,include
from .views import bbHome

urlpatterns = [
    url(r'^', bbHome),
]