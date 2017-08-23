# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json

from .forms import ScriptForm
from common.models import User
from .models import echoplayer, echolevel

import json
# Create your views here.

# @login_required
@csrf_exempt
def echoHome(request) :
    loginUser = request.session.get('user')

    form = ScriptForm()
    print(loginUser)
    
    usrObj = User.objects.get(user_id = loginUser)
    
    playerObj, created = echoplayer.objects.get_or_create(playerId = usrObj.user_id,
    defaults={'playerLevel' : 1, 'playerQn' : 1},
    ) 
    print(playerObj.playerQn)
    status = True
    requireHead = ['1-1', '1-4']
    levelObj = echolevel.objects.get(levelId = playerObj.playerLevel, qnId = playerObj.playerQn)
    if request.POST :
        print(form)
        print(request.POST.get('field'))
        if 'answer' in request.POST :
            playerAns = request.POST['answer']
            print(playerAns)
            print(levelObj.qnAns)
        
            if playerAns == levelObj.qnAns :
                print("Success!")
                if playerObj.playerQn == 5 :
                    playerObj.playerLevel = playerObj.playerLevel + 1
                    playerObj.playerQn = 1
                else :
                    playerObj.playerQn = playerObj.playerQn + 1
                playerObj.save()
            else :
                status = False
        if 'proceed' in request.POST :
            status = False
      
    else :
        status = True
    print(request.POST)
    print(status)
    json_data = open('echo/templates/intro.json')
    data = json.load(json_data)

    for d in data :
        if d['level'] == playerObj.playerLevel and d['question'] == playerObj.playerQn :
            break      

    levelqn = str(playerObj.playerLevel) + '-' + str(playerObj.playerQn) 
    print(levelqn)
    if(levelqn in requireHead) and (status == True) :
        return render(request, 'echohead.html', d)
        # return JsonResponse(d)

    levelObj = echolevel.objects.get(levelId = playerObj.playerLevel, qnId = playerObj.playerQn)

    return render(request, 'echohome.html', {'problem' : levelObj.qnDesc, 'form' : form})
    # return JsonResponse({'problem' : levelObj.qnDesc})
