# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from common.models import User
from common.decorators import isLoggedIn
from .models import echoplayer, echolevel

import json
import subprocess
# Create your views here.

@isLoggedIn
@csrf_exempt
def echoHome(request) :
    loginUser = request.session.get('user')

    # form = ScriptForm()
    # print(loginUser)
    usrObj = User.objects.get(user_id = loginUser)
    
    playerObj, created = echoplayer.objects.get_or_create(playerId = usrObj.user_id,
    defaults={'playerLevel' : 1, 'playerQn' : 1, 'partCode' : ''},
    ) 
    # print(playerObj.playerQn)
    status = False
    # requireHead = ['1-1', '1-4']
    levelObj = echolevel.objects.get(levelId = playerObj.playerLevel, qnId = playerObj.playerQn)
    if request.POST :
        # print(form)
        # print(request.POST)
        print(request.POST.get('field'))
        # partCode = request.POST.get('field')

        #If Save Button is clicked       
        if 'save' in request.POST :
            playerObj.partCode = request.POST.get('field')
            playerObj.save()
            
        #If Execute Button is clicked
        if 'execute' in request.POST :
            playerObj.partCode = request.POST.get('field')
            playerObj.save()

            #Script Execution
            out = subprocess.Popen(str(playerObj.partCode), shell=True, executable="/bin/rbash", stdout=subprocess.PIPE)
            tmp = open('echo/outputs/'+playerObj.playerId+'.txt','w')
            tmp.write(out.stdout.read().decode('ascii'))
            tmp.close()
            fileName = str(playerObj.playerLevel*100+playerObj.playerQn*10+1)
            testComm = 'diff -w echo/outputs/'+str(playerObj.playerId)+'.txt echo/answers/'+fileName+'.txt'
            test = subprocess.Popen(testComm, shell=True, stdout=subprocess.PIPE)
            comp = test.stdout.read().decode('ascii')
            print(comp)
            print(testComm)
            if comp != '' :
                status = False
            else :
                print("Step1")
                fileName = str(playerObj.playerLevel*100+playerObj.playerQn*10+2)
                testComm = "diff -w echo/outputs/"+str(playerObj.playerId)+".txt echo/answers/"+fileName+".txt"
                test = subprocess.Popen(testComm, shell=True, stdout=subprocess.PIPE)
                comp = test.stdout.read().decode('ascii')
                if comp != '' :
                    status = False
                else :
                    status = True
            print(status)
            if status == True :
                if playerObj.playerQn == 5 :
                    playerObj.playerLevel = playerObj.playerLevel + 1
                    playerObj.playerQn = 1
                else :
                    playerObj.playerQn = playerObj.playerQn + 1
                playerObj.partCode = ''
                playerObj.save()
 
    json_data = open('echo/templates/intro.json')
    data = json.load(json_data)

    #Player Ranking
    allPlayers = echoplayer.objects.all()
    rank = 1
    leaderBoard = {}
    print(allPlayers)
    rankPlayers = sorted(allPlayers, key = lambda x: (x.playerLevel, x.playerQn, x.startDate), reverse = True)
    for r in rankPlayers :
        leaderBoard[rank] = r
        rank = rank + 1
    print(leaderBoard)

    levelObj = echolevel.objects.get(levelId = playerObj.playerLevel, qnId = playerObj.playerQn)
    context = {}
    context['level'] = levelObj
    context['player'] = playerObj
    context['status'] = status
    context['leaderboard'] = leaderBoard

    return render(request, 'echohome.html', context)
    # return JsonResponse(context)
