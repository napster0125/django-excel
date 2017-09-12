# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse

from common.decorators import isLoggedIn
from common.models import User

from .models import echoplayer, echolevel
# from common.utilities import pushChangesEchoLeaderboard
import json
import subprocess
from threading import Timer
# Create your views here.

@isLoggedIn
def echoHome(request) :
    loginUser = request.session.get('user')

    usrObj = User.objects.get(user_id = loginUser)   
    playerObj, created = echoplayer.objects.get_or_create(playerId = usrObj.user_id,
    defaults={'playerLevel' : 1, 'playerQn' : 1, 'partCode' : ''},
    ) 

    if created == True :
        subprocess.Popen('mkdir ./echo/players/'+playerObj.playerId, shell=True, stdout=subprocess.PIPE)
        subprocess.Popen('cp -r ./echo/home/* ./echo/players/'+playerObj.playerId, shell=True, stdout=subprocess.PIPE)
        subprocess.Popen('cp ./echo/home/.bashrc ./echo/players/'+playerObj.playerId, shell=True, stdout=subprocess.PIPE)
    termOut = ''
    status = False
    levelObj = echolevel.objects.get(levelId = playerObj.playerLevel, qnId = playerObj.playerQn)
    if request.POST :
        print(request.POST.get('field'))

        #If Save Button is clicked       
        if 'save' in request.POST :
            playerObj.partCode = request.POST.get('field')
            playerObj.save()
            
        #If Execute Button is clicked
        if 'execute' in request.POST :
            playerObj.partCode = request.POST.get('field').replace('\r', '')
            playerObj.save()

            #Script Execution
            with open(playerObj.playerId+'code.sh', 'w') as shcode :
                shcode.write(playerObj.partCode)
            out = subprocess.Popen(['rbash ', playerObj.playerId+'code.sh', '5'], executable="/bin/rbash", stdout=subprocess.PIPE)
            timer = Timer(1, out.kill)
            timer.start()

            termOut = out.stdout.read().decode('ascii')
            with open('echo/outputs/'+playerObj.playerId+'.txt','w') as tmp :
                tmp.write(out.stdout.read().decode('ascii'))
                print(playerObj.partCode)
                print("Working!")
            fileName = str(playerObj.playerLevel*100+playerObj.playerQn*10+1)
            testComm = 'diff -w echo/outputs/'+str(playerObj.playerId)+'.txt echo/answers/'+fileName+'.txt'
            test = subprocess.Popen(testComm, shell=True, stdout=subprocess.PIPE)
            comp = test.stdout.read().decode('ascii')
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
            if status == True :
                if playerObj.playerQn == 5 :
                    playerObj.playerLevel = playerObj.playerLevel + 1
                    playerObj.playerQn = 1
                else :
                    playerObj.playerQn = playerObj.playerQn + 1
                playerObj.partCode = ''
                playerObj.save()
                toptenplayers = echoplayer.objects.order_by('-playerLevel', '-playerQn', 'ansTime')
                topten = []
                for player in toptenplayers :
                    topten.append(playerObj.playerId)
                # pushChangesEchoLeaderboard(topten)

    response = {'level' : playerObj.playerLevel, 'qno' : playerObj.playerQn, 'question' : levelObj.qnDesc, 'termOut' : termOut, 'status' : status}
    return JsonResponse(response)


#Player Ranking

@isLoggedIn
def echoRank(request) :
    loginUser = request.session.get('user')
    allPlayers = echoplayer.objects.order_by('-playerLevel', '-playerQn', 'ansTime')
    rank = 1
    leaderBoard = []
    for player in allPlayers :
        playerInfo = {'rank' : rank, 'userId' : player.playerId, 'level' : player.playerLevel, 'question' : player.playerQn}
        leaderBoard.append(playerInfo)
        if loginUser == player.playerId :
            myrank = rank
        rank = rank + 1
    print(leaderBoard)
    response = {'ranklist' : leaderBoard, 'myrank' : myrank}
    return JsonResponse(response)
