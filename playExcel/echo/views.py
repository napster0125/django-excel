# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse

from common.decorators import isLoggedIn
from common.models import User
from common.utility import pushChangesEchoLeaderboard

from .models import echoplayer,echolevel

import json
import subprocess, os
from threading import Timer
# Create your views here.

@isLoggedIn
def echoHome(request) :
    loginUser = request.session.get('user')

    usrObj = User.objects.get(user_id = loginUser)   
    # playerObj, created = echoplayer.objects.get_or_create(playerId = usrObj.user_id,
    # defaults={'playerLevel' : 1, 'playerQn' : 1, 'partCode' : ''},
    # ) 
    playerObj, created = echoplayer.objects.get_or_create(playerId = usrObj.user_id.split('|')[1],
    defaults={'playerLevel' : 1, 'partCode' : ''},
    ) 
    if not os.path.exists(os.path.join(os.getcwd(), 'echo/skel/home/')) :
        os.makedirs(os.path.join(os.getcwd(), 'echo/skel/home/'))

    if not os.path.exists(os.path.join(os.getcwd(), 'echo/players/'+playerObj.playerId+'/home/')) :
        os.makedirs(os.path.join(os.getcwd(), 'echo/players/'+playerObj.playerId+'/home/'))

    subprocess.Popen(['cp', '-r' , os.path.join(os.getcwd(), 'echo/skel/home/'), os.path.join(os.getcwd(), 'echo/players/'+playerObj.playerId+'/home/')])
    
    termStatus = False
    # if created == True :
    #     subprocess.Popen('mkdir ./echo/players/'+playerObj.playerId, shell=True, stdout=subprocess.PIPE)
    #     subprocess.Popen('cp -r ./echo/home/* ./echo/players/'+playerObj.playerId, shell=True, stdout=subprocess.PIPE)
    #     subprocess.Popen('cp ./echo/home/.bashrc ./echo/players/'+playerObj.playerId, shell=True, stdout=subprocess.PIPE)
    # termOut = ''
    # status = False
    # levelObj = echolevel.objects.get(levelId = playerObj.playerLevel, qnId = playerObj.playerQn)
    levelObj = echolevel.objects.get(levelId = playerObj.playerLevel)

    termOut = ''
    status = False
    if request.POST :
        status = False
        if 'term' in request.POST :
            termStatus = True
            termIn = request.POST.get('term')
            with open('/tmp/'+playerObj.playerId+'.txt', 'w') as temp :
                t = subprocess.Popen([os.path.join(os.getcwd(),'echo/dockerscript.sh'), str(termStatus), termIn], stdout=temp, stderr=temp)
            # with open('/tmp/'+playerObj.playerId+'.txt', 'r') as tmp :
                try :
                    t.communicate(timeout=10)
                except subprocess.TimeoutExpired :
                    print("Timed Out!")
            with open('/tmp/'+playerObj.playerId+'.txt', 'r') as temp :
                termOut = '\n'.join(str(line) for line in temp)
                
        #If Save Button is clicked       
        elif 'save' in request.POST :
            
            playerObj.partCode = request.POST.get('code')
            playerObj.save()
            termStatus = False

            
        #If Execute Button is clicked
        elif 'execute' in request.POST :
            playerObj.partCode = request.POST.get('code').replace('\r', '')
            playerObj.save()
            termStatus = False

            #Script Execution
            # with open(playerObj.playerId+'code.sh', 'w') as shcode :
            #     shcode.write(playerObj.partCode)
            # out = subprocess.Popen(['rbash ', playerObj.playerId+'code.sh', '5'], executable="/bin/rbash", stdout=subprocess.PIPE)
            # timer = Timer(1, out.kill)
            # timer.start()

            # termOut = out.stdout.read().decode('ascii')
            # with open('echo/outputs/'+playerObj.playerId+'.txt','w') as tmp :
            #     tmp.write(out.stdout.read().decode('ascii'))
            #     print(playerObj.partCode)
            #     print("Working!")
            # fileName = str(playerObj.playerLevel*100+playerObj.playerQn*10+1)
            # testComm = 'diff -w echo/outputs/'+str(playerObj.playerId)+'.txt echo/answers/'+fileName+'.txt'
            # test = subprocess.Popen(testComm, shell=True, stdout=subprocess.PIPE)
            # comp = test.stdout.read().decode('ascii')
            # if comp != '' :
            #     status = False
            # else :
            #     print("Step1")
            #     fileName = str(playerObj.playerLevel*100+playerObj.playerQn*10+2)
            #     testComm = "diff -w echo/outputs/"+str(playerObj.playerId)+".txt echo/answers/"+fileName+".txt"
            #     test = subprocess.Popen(testComm, shell=True, stdout=subprocess.PIPE)
            #     comp = test.stdout.read().decode('ascii')
            #     if comp != '' :
            #         status = False
            #     else :
            #         status = True
            with open('/tmp/'+playerObj.playerId+'status.txt', 'w') as stat :
                t = subprocess.Popen([os.path.join(os.getcwd(),'echo/dockerscript.sh'), str(termStatus), playerObj.playerId, str(playerObj.playerLevel), playerObj.partCode, levelObj.testArg1, levelObj.testArg1], stdout=stat)
                try :
                    t.communicate(timeout=1200)
                except subprocess.TimeoutExpired :
                    print("Timed Out!")
            with open('/tmp/'+playerObj.playerId+'status.txt', 'r') as stat :        
                status = stat.read()
            print(status)
            
            if status == True :
                # if playerObj.playerQn == 5 :
                playerObj.playerLevel = playerObj.playerLevel + 1
                #     playerObj.playerQn = 1
                # else :
                #     playerObj.playerQn = playerObj.playerQn + 1
                playerObj.partCode = ''
                playerObj.save()

                with open('echo/player/'+playerObj.playerId+'/home/output.txt', 'r') as output :
                    termOut = output.read()
                # toptenplayers = echoplayer.objects.order_by('-playerLevel', '-playerQn', 'ansTime')
                toptenplayers = echoplayer.objects.order_by('-playerLevel', '-playerQn', 'ansTime')
                topten = []
                for player in toptenplayers :
                    topten.append(playerObj.playerId)
                pushChangesEchoLeaderboard(topten)

            else :
                with open('echo/players/'+playerObj.playerId+'/home/output.txt', 'r') as out :
                    termOut = out.read()
                with open('echo/players/'+playerObj.playerId+'/home/error.txt', 'r') as error :
                    termOut += error.read()

    # response = {'level' : playerObj.playerLevel, 'qno' : playerObj.playerQn, 'question' : levelObj.qnDesc, 'termOut' : termOut, 'status' : status}
    response = {'player' : playerObj.playerId, 'level' : playerObj.playerLevel, 'question' : levelObj.qnDesc, 'partCode' : playerObj.partCode, 'termOut' : termOut, 'status' : status}
    # return JsonResponse(response)
    return render(request, 'echohome.html', response)


#Player Ranking

@isLoggedIn
def echoRank(request) :
    loginUser = request.session.get('user')
    # allPlayers = echoplayer.objects.order_by('-playerLevel', '-playerQn', 'ansTime')
    allPlayers = echoplayer.objects.order_by('-playerLevel', 'ansTime')
    rank = 1
    leaderBoard = []
    for player in allPlayers :
        # playerInfo = {'rank' : rank, 'userId' : player.playerId, 'level' : player.playerLevel, 'question' : player.playerQn}
        playerInfo = {'rank' : rank, 'userId' : player.playerId, 'level' : player.playerLevel}
        leaderBoard.append(playerInfo)
        if loginUser == player.playerId :
            myrank = rank
        rank = rank + 1
    print(leaderBoard)
    response = {'ranklist' : leaderBoard, 'myrank' : myrank}
    return JsonResponse(response)
