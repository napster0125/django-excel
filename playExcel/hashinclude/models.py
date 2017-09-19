from django.db import models
from common.models import User

class problems(model.Model)
        problems=model.IntegerField(primary_key=True)
        points=model.IntegerField()

class hiuser(models.Model):
	user_id=models.OneToOneField(User,primary_key=True,on_delete=models.CASCADE)
	last_sub=models.DateTimeField()
	points=models.IntegerField()
	rank=models.IntegerField()
	def __str__(self):
		return self.user_id.username

class Submission(models.Model):
	user_id=models.ForeignKey(hiuser,on_delete=models.CASCADE)
        pid=models.IntegerField(default=1)
	fid=models.FileField(upload_to='')
	lang=models.CharField(max_length=9,default='C++')
