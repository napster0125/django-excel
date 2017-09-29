# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse

from common.decorators import isLoggedIn
from common.models import User
from common.utility import pushChangesEchoLeaderboard

from .models import echoplayer,echolevel

import json
import subprocess, os, re, shlex
from threading import Timer
from . import judge
# Create your views here.

@isLoggedIn
def echoHome(request) :
    loginUser = request.session.get('user')

    usrObj = User.objects.get(user_id = loginUser)   
    playerObj, created = echoplayer.objects.get_or_create(playerId = usrObj.user_id.split('|')[1],
    defaults={'playerLevel' : 1, 'partCode' : ''},
    ) 

    if not os.path.exists(os.path.join(os.getcwd(), 'echo/media/')) :
        os.makedirs(os.path.join(os.getcwd(), 'echo/media/players/'))

    if not os.path.exists(os.path.join(os.getcwd(), 'echo/media/players/')) :
        os.makedirs(os.path.join(os.getcwd(), 'echo/media/players/'))
        
    if not os.path.exists(os.path.join(os.getcwd(), 'echo/media/players/'+playerObj.playerId+'/')) :
        os.makedirs(os.path.join(os.getcwd(), 'echo/media/players/'+playerObj.playerId+'/'))

    subprocess.Popen(['cp', '-r' , os.path.join(os.getcwd(), 'echo/skel/home/'), os.path.join(os.getcwd(), 'echo/media/players/'+playerObj.playerId+'/')])
    levelObj = echolevel.objects.get(levelId = playerObj.playerLevel)
    status = False
        
    response = {'player' : playerObj.playerId, 'level' : playerObj.playerLevel, 'question' : levelObj.qnDesc, 'partCode' : playerObj.partCode, 'status' : status}
    # return JsonResponse(response)
    return render(request, 'echohome.html', response)

@isLoggedIn
def echoSubmit(request) :
    loginUser = request.session.get('user')

    usrObj = User.objects.get(user_id = loginUser)   
    playerObj, created = echoplayer.objects.get_or_create(playerId = usrObj.user_id.split('|')[1],
    defaults={'playerLevel' : 1, 'partCode' : ''},
    ) 
    levelObj = echolevel.objects.get(levelId = playerObj.playerLevel)
    status = False
    termOut = ''
    if 'term' in request.POST :
        termStatus = True
        termIn = request.POST.get('term')
        trm = ''
        with open('/tmp/'+playerObj.playerId+'.txt', 'w') as temp :

            cmd = 'docker run -it --rm -v'+os.getcwd()+'/echo/media/players/'+str(playerObj.playerId)+'/home/level'+str(playerObj.playerLevel)+':/tmp -w /tmp echojudge rbash -c \"'+termIn+'\"'

            t = subprocess.Popen(shlex.split(str(cmd)), stdout=temp, stderr=temp)
            try :
                t.communicate(timeout=5)

            except subprocess.TimeoutExpired :
                print("Timed Out!")
        t = ''
        with open('/tmp/'+playerObj.playerId+'.txt', 'r') as temp :
            t = temp.read()
        with open('/tmp/'+playerObj.playerId+'.txt', 'w') as temp :
            query = re.compile(r'\x1b[^m]*m').sub('', t)
            temp.write(re.sub(r"\w+_test.txt\b", "", query))
        
        with open('/tmp/'+playerObj.playerId+'.txt', 'r') as temp :
            termOut = '\n'.join(str(line) for line in temp)
                    
    elif 'save' in request.POST :
        
        playerObj.partCode = request.POST.get('code')
        playerObj.save()
        termStatus = False

    elif 'execute' in request.POST :
        playerObj.partCode = request.POST.get('code').replace('\r', '')
        playerObj.save()

        termStatus = False

        status = judge.main(str(playerObj.playerId), str(playerObj.playerLevel), playerObj.partCode, levelObj.testArg1, levelObj.testArg2)

        if status == True :

            playerObj.playerLevel = playerObj.playerLevel + 1
            playerObj.partCode = ''
            playerObj.save()
                
            with open('echo/media/players/'+playerObj.playerId+'/home/level'+str(playerObj.playerLevel-1)+'/output.txt', 'r') as output :
                termOut = output.read()
            # toptenplayers = echoplayer.objects.order_by('-playerLevel', 'ansTime')[:10]
            # topten = []
            # for player in toptenplayers :
            #     topten.append(playerObj.playerId)
            # pushChangesEchoLeaderboard(topten)

        else :
            
            with open('echo/media/players/'+playerObj.playerId+'/home/level'+str(playerObj.playerLevel)+'/output.txt', 'r') as out :
                termOut = out.read()
            with open('echo/media/players/'+playerObj.playerId+'/home/level'+str(playerObj.playerLevel)+'/error.txt', 'r') as error :
                termOut += error.read()

    response = {'player' : playerObj.playerId, 'level' : playerObj.playerLevel, 'question' : levelObj.qnDesc, 'partCode' : playerObj.partCode, 'termOut' : termOut, 'status' : status}
    # return JsonResponse(response)
    return render(request, 'echohome.html', response)

#Player Ranking

@isLoggedIn
def echoRank(request) :
    loginUser = request.session.get('user')
    usrObj = User.objects.get(user_id = loginUser)
    thisUser = usrObj.user_id.split('|')[1]
    allPlayers = echoplayer.objects.order_by('-playerLevel', 'ansTime')
    rank = 1
    leaderBoard = []
    for player in allPlayers :
        playerInfo = {'rank' : rank, 'userId' : player.playerId, 'level' : player.playerLevel}
        leaderBoard.append(playerInfo)
        if thisUser == player.playerId :
            myrank = rank
        rank = rank + 1
    # print(leaderBoard)
    response = {'ranklist' : leaderBoard, 'myrank' : myrank}
    return JsonResponse(response)

@isLoggedIn
def echoLeaderboard(request) :
    allPlayers = echoplayer.objects.order_by('-playerLevel', 'ansTime')[:100]
    rank = 1
    leaderBoard = []
    for player in allPlayers :
        playerInfo = {'rank' : rank, 'userId' : player.playerId, 'level' : player.playerLevel}
        leaderBoard.append(playerInfo)
        rank = rank + 1
    response = {'ranklist' : leaderBoard}
    return JsonResponse(response)
