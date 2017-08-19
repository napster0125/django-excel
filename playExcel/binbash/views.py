# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from common.models import User
from .models import bbplayer, bblevel
# Create your views here.

@csrf_exempt
def bbHome(request) :
    loginUser = request.session.get('user')

    print(loginUser)
    
    usrObj = User.objects.get(user_id = loginUser)
    
    playerObj, created = bbplayer.objects.get_or_create(playerId = usrObj.user_id,
    defaults={'playerLevel' : 1, 'playerQn' : 1},
    ) 
    print(playerObj.playerQn)
    levelObj = bblevel.objects.get(levelId = playerObj.playerLevel, qnId = playerObj.playerQn)
    if request.POST :
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
    return render(request, 'binbash.html', {'problem' : levelObj.qnDesc})

