from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from common.decorators import isLoggedIn,playCookies
from common.models import User

import datetime
import json

from .models import Submission,problems
from .models import hiuser
from .models import submissionTask
from .forms import SubmissionForm
from .tasks import run
from common.consumers import hashinclude_channel_push


@playCookies
@isLoggedIn
def home(request):
    loginUser=request.session['user']
    usr=User.objects.get(user_id=loginUser)
    try:
        obj=hiuser.objects.get(user_id=usr.user_id)
    except hiuser.DoesNotExist:
        obj=hiuser(user_id=usr,rank=(hiuser.objects.count()+1))
        obj.save()
    return JsonResponse({'result' : 'user added hashinclude_db'})

@playCookies
@isLoggedIn
def submit(request):
        if request.method=='POST':
                loginUser=request.session['user']
                usr=hiuser.objects.get(user_id=loginUser)
                form=SubmissionForm(request.POST,request.FILES)
                if form.is_valid():
                        prob = problems.objects.get(pid=request.POST['pid'])
                        obj=Submission(user_id=usr,pid=prob,fid=request.FILES['file'],lang=request.POST['lang'])
                        obj.save()
                        res=run.delay(request.POST['pid'],obj.fid.name,obj.lang,loginUser)
                        obj.tid=res.task_id
                        obj.save()
                        hashinclude_channel_push({'pid':request.POST['pid'],'fid':obj.fid.name,'lang':obj.lang,'tid':res.task_id,'result':'PENDING'})
			#taskobj=submissionTask(user_id=usr,tid=res.task_id)
                        #taskobj.save()
                        return JsonResponse({'taskid':res.task_id})
                else:
                        return JsonResponse({'result':'Error'})

@playCookies
@isLoggedIn
def get_ranklist(request):
    loginUser=request.session['user']
    leaderboard=hiuser.objects.order_by('rank')[:10]
    ranklist=[]
    for user_obj in leaderboard:
        user={'rank':user_obj.rank,'pic':user_obj.user_id.profile_picture,'username':user_obj.user_id.username,'points':user_obj.total_points}
        ranklist.append(user)
    response={'ranklist':ranklist}
    return JsonResponse(response)

@playCookies
@isLoggedIn
def user_rank(request):
    loginUser=request.session['user']
    rank=hiuser.objects.get(user_id=loginUser).rank
    points=hiuser.objects.get(user_id=loginUser).total_points
    response={'rank':rank,'points':points}
    return JsonResponse(response)

@playCookies
@isLoggedIn
def recent_submissions(request):
    loginUser=request.session['user']
    usr=hiuser.objects.get(user_id=loginUser)
    recent_submissions=(Submission.objects.order_by('sub_time')).filter(user_id=usr)[:5]
    sub_list=[]
    for sub_obj in recent_submissions:
        result=submissionTask.objects.get(tid=sub_obj.tid).results
        sub={'pid':sub_obj.pid_id,'fid':sub_obj.fid.name,'lang':sub_obj.lang,'verdict':result}
        sub_list.append(sub)
    response={'sublist':sub_list}
    return JsonResponse(response)

@playCookies
@isLoggedIn
def total_submissions(request):
    prob_lst=problems.objects.all()
    tot_sub={}
    for prob in prob_lst:
        sub={}
        tot_sub[prob.pid]=Submission.objects.filter(pid=prob.pid).count()
    response={'totalSubmissions':tot_sub}
    return JsonResponse(response)

@playCookies
@isLoggedIn
def sub_view(request):
    p=Submission.objects.order_by('-sub_time')[:20]
    sub_list=[]
    for sub_obj in p:
        try:
                result=submissionTask.objects.get(tid=sub_obj.tid).results
                sub={'picture':sub_obj.user_id.user_id.profile_picture,'name':sub_obj.user_id.user_id.username,'pid':sub_obj.pid_id,'fid':sub_obj.fid.name,'lang':sub_obj.lang,'verdict':result,'time':sub_obj.sub_time}
                sub_list.append(sub)
        except submissionTask.DoesNotExist:
                pass
    response={'sub_view ' : sub_list}
    return JsonResponse(response)

@playCookies
@isLoggedIn
def user_submissions(request):
    loginUser=request.session['user']
    usr=hiuser.objects.get(user_id=loginUser)
    recent_submissions=(Submission.objects.order_by('-sub_time')).filter(user_id=usr)
    sub_list=[]
    for sub_obj in recent_submissions:
        try:
                result=submissionTask.objects.get(tid=sub_obj.tid).results
                sub={'pid':sub_obj.pid_id,'fid':sub_obj.fid.name,'lang':sub_obj.lang,'verdict':result}
                sub_list.append(sub)
        except submissionTask.DoesNotExist:
                pass
    response={'sublist':sub_list}
    return JsonResponse(response)
