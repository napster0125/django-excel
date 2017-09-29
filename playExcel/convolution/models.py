from django.db import models
from common.models import User
from django.utils import timezone 

class convolution_user(models.Model):
    user_id=models.OneToOneField(User,primary_key=True,on_delete=models.CASCADE)
    score=models.IntegerField()
    tries=models.IntegerField(default=5)
    def __str__(self):
        return self.user_id.username

class Submission(models.Model):
    user_id=models.ForeignKey(convolution_user,on_delete=models.CASCADE)
    csv_file=models.FileField(upload_to='')
    sub_time=models.DateTimeField(auto_now_add=True,blank=True)
    score=models.IntegerField()
    task_id=models.IntegerField()
    top_score=models.IntegerField()
