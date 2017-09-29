from django.shortcuts import render
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from common.decorators import isLoggedIn,playCookies

import json
import datetime

from .models import convolution_user
from .models import Submission

from .forms import SubmissionForm
# Create your views here.

def home(request):
    loginUser=request.session['user']
    usr=User.objects.get(user_id=loginUser)
    try:
        user_obj=convolution_user.get(user_id=usr.user_id)
    except convolution_user.DoesNotExist:
        user_obj=convolution_user(user_id=usr,rank=(convolution_user.objects.count()+1))
        user_obj.save()
        return JsonResponse({'result': ' Added user to convolution db '})

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

def leaderboard(request):
    loginUser=request.session['user']
    top_users=hiuser.objects.order_by('rank')[:100]
    ranklist=[]
    for user in top_users:
        user_obj={'rank':user.rank,'pic':user_obj.user_id.profile_picture,'username':user_obj.user_id.username,'score':user_obj.score}
        ranklist.append(user_obj)
    return JsonResponse({'ranklist':ranklist})
