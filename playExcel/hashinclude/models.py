from django.db import models
from common.models import User

class hiuser(models.Model):
	user_id=models.OneToOneField(User,primary_key=True,on_delete=models.CASCADE)
	last_sub=models.DateTimeField()
	points=models.IntegerField()
	rank=models.IntegerField()
	def __str__(self):
		return self.user_id.username

class Submission(models.Model):
	pid=models.IntegerField(default=1)
	fid=models.FileField(upload_to='')
	lang=models.CharField(max_length=9,default='C++')
