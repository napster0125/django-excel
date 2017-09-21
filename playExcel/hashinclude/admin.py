from django.contrib import admin

# Register your models here.
from .models import problems,hiuser,Submission
admin.site.register(problems)
admin.site.register(hiuser)
admin.site.register(Submission)