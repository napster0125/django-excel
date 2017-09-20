# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class echoplayer(models.Model) :
    playerId = models.CharField(primary_key = True, max_length = 100)
    playerLevel = models.IntegerField(default = 1)
    # playerQn = models.IntegerField(default = 1)
    partCode = models.CharField(max_length = 1000, default = '')
    ansTime = models.DateTimeField(auto_now = True)

    def __str__(self) :
        return str(self.playerId)

class echolevel(models.Model) :
    levelId = models.IntegerField(primary_key = True, default = 1)
    # qnId = models.IntegerField(default = 1)
    qnDesc = models.TextField()
    testArg1 = models.CharField(default = '', max_length = 100)
    testArg1 = models.CharField(default = '', max_length = 100)
    
    def __str__(self) :
        # return str(self.levelId) + '-' + str(self.qnId)
        return str(self.levelId)
    
    # class Meta :
    #     unique_together = ('levelId', 'qnId')