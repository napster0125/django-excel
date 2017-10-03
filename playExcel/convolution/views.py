from django.shortcuts import render
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from common.decorators import isLoggedIn,playCookies
from common.models import User

import json
import datetime

from .models import convolution_user
from .models import Submission

from .forms import SubmissionForm
# Create your views here.

@isLoggedIn
@playCookies
def home(request):
    loginUser=request.session['user']
    usr=User.objects.get(user_id=loginUser)
    try:
        user_obj=convolution_user.objects.get(user_id=usr.user_id)
    except convolution_user.DoesNotExist:
        user_obj=convolution_user(user_id=usr,rank=(convolution_user.objects.count()+1))
        user_obj.save()
        return JsonResponse({'result': ' Added user to convolution db '})
    return JsonResponse({'result': ' User in convolution db ' })

def submit(request):
    if request.method=='POST':
            loginUser=request.session['user']
            usr=convolution_objects.get(user_id=loginUser)
            form=SubmissionForm(request.POST,request.FILES)
            if form.is_valid():
                sub_obj=Submission(user_id=usr,csvfile=request.FILES['file'])
                sub_obj.save()
                return JsonResponse({'task_id':sub_obj.task_id})
            else:
                return JsonResponse({'result':error})

@isLoggedIn
@playCookies
def leaderboard(request):
    loginUser=request.session['user']
    top_users=convolution_user.objects.order_by('rank')[:100]
    ranklist=[]
    for user in top_users:
        user_obj={'rank':user.rank,'pic':user.user_id.profile_picture,'username':user.user_id.username,'score':user.score}
        ranklist.append(user_obj)
    return JsonResponse({'ranklist':ranklist})
