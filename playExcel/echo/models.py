# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class echoplayer(models.Model) :
    playerId = models.CharField(primary_key = True, max_length = 200)
    playerLevel = models.IntegerField(default = 0)
    playerQn = models.IntegerField(default = 0)

    def __str__(self) :
        return str(self.playerId)

class echolevel(models.Model) :
    levelId = models.IntegerField(default = 1)
    qnId = models.IntegerField(default = 1)
    qnDesc = models.CharField(max_length = 500)
    qnAns = models.CharField(max_length = 500)
    
    def __str__(self) :
        return str(self.levelId + self.qnId)
    
    class Meta :
        unique_together = ('levelId', 'qnId')