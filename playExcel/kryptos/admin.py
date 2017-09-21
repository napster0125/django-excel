# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import level
from .models import kryptosuser
from .models import submittedanswer


# Register your models here.
admin.site.register(level)
admin.site.register(kryptosuser)
admin.site.register(submittedanswer)