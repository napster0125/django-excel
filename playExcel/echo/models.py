# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class echoplayer(models.Model) :
    playerId = models.CharField(primary_key = True, max_length = 100)
    playerLevel = models.IntegerField(default = 1)
    playerQn = models.IntegerField(default = 1)
    partCode = models.TextField(default = '')
    startDate = models.DateTimeField(auto_now_add = True)

    def __str__(self) :
        return str(self.playerId)

class echolevel(models.Model) :
    levelId = models.IntegerField(default = 1)
    qnId = models.IntegerField(default = 1)
    qnDesc = models.TextField()
    qnAns = models.TextField()
    
    def __str__(self) :
        return str(self.levelId + self.qnId)
    
    class Meta :
        unique_together = ('levelId', 'qnId')