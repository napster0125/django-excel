from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from common.decorators import isLoggedIn,playCookies
from common.models import User

import datetime
import json

from .models import Submission
from .models import hiuser
from .forms import SubmissionForm
from .tasks import run

@playCookies
@isLoggedIn
def home(request):
    loginUser=request.session['user']
    try:
        obj=hiuser.objects.get(user_id=loginUser)
    except hiuser.DoesNotExist
        obj=hiuser(user_id=loginUser,rank=(hiuser.objects.count()+1))
        obj.save()

@playCookies
@isLoggedIn
@csrf_exempt
def submit(request):
        if request.method=='POST':
                loginUser=request.session['user']    
                form=SubmissionForm(request.POST,request.FILES)
                if form.is_valid():
                        obj=Submission(user_id=loginUser,pid=request.POST['pid'],fid=request.FILES['cfile'],lang=request.POST['lang'])
                        obj.save()
                        res=run.delay(str(obj.pid),obj.fid.name,obj.lang)
                        print(res)
                        return JsonResponse({'result':'Success'})	
                else:
                        return JsonResponse({'result':'Failed'})
        else:
            return render(request,'upload.html')

@playCookies
@isLoggedIn
def get_ranklist(request):
    loginUser=request.session['user']
    leaderboard=hiuser.objects.order_by('rank')[:10]
    ranklist=[]
    for user_obj in leaderboard:
        user={'rank':user_obj.rank,'pic':user_obj.user_id.profile_picture,'username':user_obj.user_id.username,'points':user_obj.points}
        ranklist.append(user)
    response={'ranklist':ranklist}
    return JsonResponse(response)

@playCookies
@isLoggedIn
def user_rank(request):
    loginUser=request.session['user']
    rank=hiuser.objects.get(user_id=loginUser).rank
    response={'rank':rank}
    return JsonResponse(response)

@playCookies
@isLoggedIn
def recent_submissions(request):
    loginUser=request.session['user']
    recent_submissions=(Submissions.objects.order_by('sub_time')).filter(user_id=loginUser)[:5]
    sub_list=[]
    for sub_obj in recent_submissions:
        sub={'pid':sub_obj.pid,'fid':sub_obj.fid,'lang':sub_obj.lang}
        sub_list.append(sub)
    response={'sublist':sub_list}
    return JsonResponse(response)
