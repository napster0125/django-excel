from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from common.decorators import isLoggedIn,playCookies
from common.models import User

import datetime
import json

from .models import Submission,problems
from .models import hiuser
from .forms import SubmissionForm
from .tasks import run
from common.consumers import hashinclude_channel_push


#send data to specific user by calling userDataPush. Eg: hashinclude_channel_push(
#                                                                      {
#                                                                           'tid':  { 'submit_result' : "....." }
#                                                                      }
#                                                                     )
#
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
                        obj=Submission(user_id=usr,pid=prob,fid=request.FILES['cfile'],lang=request.POST['lang'])
                        obj.save()
                        res=run.delay(str(obj.pid),obj.fid.name,obj.lang)
                        return JsonResponse({'taskid':res.task_id})
                else:
                        return JsonResponse({'result':'Error'})
        else:
            return render(request,'upload.html')

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
    response={'rank':rank}
    return JsonResponse(response)

@playCookies
@isLoggedIn
def recent_submissions(request):
    loginUser=request.session['user']
    usr=hiuser.objects.get(user_id=loginUser)
    recent_submissions=(Submission.objects.order_by('sub_time')).filter(user_id=usr)[:5]
    sub_list=[]
    for sub_obj in recent_submissions:
        sub={'pid':sub_obj.pid,'fid':sub_obj.fid,'lang':sub_obj.lang}
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
        # tot_sub.append(sub)
    response={'totalSubmissions':tot_sub}
    return JsonResponse(response)
