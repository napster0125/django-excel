from django.conf.urls import url
from .views import *

urlpatterns=[
        url(r'submitanswer',submit),
        url(r'',home),
        #url(r'ranklist',get_ranklist),
        #url(r'myrank',user_rank),
        #url(r'mysub',recent_submissions),
        ]