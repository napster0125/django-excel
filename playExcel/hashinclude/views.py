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

@csrf_exempt
def submit(request):
	if request.method=='POST':
		form=SubmissionForm(request.POST,request.FILES)
		print(form.errors)
		if form.is_valid():
			obj=Submission(pid=1,fid=request.FILES['cfile'],lang=request.POST['lang'])
			obj.save()
			run.delay(str(obj.pid),obj.fid.name,obj.lang)
			return JsonResponse({'result':'Success'})	
		else:
			return JsonResponse({'result':'Failed'})
	else:
		return render(request,'upload.html')
