from django.contrib import admin

# Register your models here.

from .models import convolution_user,Submission

admin.site.register(convolution_user)
admin.site.register(Submission)
