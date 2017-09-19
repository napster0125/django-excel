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
@csrf_exempt
def submit(request):
        if request.method=='POST':
                form=SubmissionForm(request.POST,request.FILES)
                if form.is_valid():
                        obj=Submission(pid=10,fid=request.FILES['cfile'],lang=request.POST['lang'])
                        obj.save()
                        res=run.delay(str(obj.pid),obj.fid.name,obj.lang)
                        return JsonResponse({'result':'Success'})	
                else:
                        return JsonResponse({'result':'Failed'})
        else:
            return render(request,'upload.html')

@playCookies
@isLoggedIn
def get_ranklist(request):
    loginUser=request.session['User']
    leaderboard=hiuser.objects.order_by('rank')[:10]
    ranklist=[]
    for user_obj in leaderboard:
        user={'rank':user_obj.rank,'pic':user_obj.user_id.profile_picture,'username':user_obj.user_id.username,'points':user_obj.points}
        ranklist.append(user)
    response={'ranklist':ranklist}
    return JsonResponse(ranklist)

@playCookies
@isLoggedIn
def user_rank(request):
    loginUser=request.session['User']
    rank=hiuser.objects.get(user_id=loginUser).rank
    response={'rank':rank}
    return JsonResponse(response)
