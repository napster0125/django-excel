from __future__ import absolute_import,unicode_literals
from celery import shared_task
import sys,os,django
import subprocess,shlex

from common.consumers import hashinclude_channel_push

from .models import problems,hiuser,Submission,submissionTask

'''
# To test celery without running django-runserver


sys.path.append("/home/sivasama/works/Play.Excel/playExcel/")
os.environ["DJANGO_SETTINGS_MODULE"]="playExcel.settings"
django.setup()
'''

@shared_task
def run(pid,fid,lang,loginUser):
        usr = hiuser.objects.get(user_id_id=loginUser)
        sq=" "
        cmd="bash hashinclude/dockerrun.sh "+str(pid)+sq+fid+sq+lang.title()
        print(cmd)
        p=subprocess.Popen(shlex.split(cmd),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        res=p.communicate()
        p.kill() 
        primes=[2,3,5,7,11,13,17]
        print(res)
        obj=submissionTask(user_id=usr,tid=run.request.id)
        print(res[0]==(b'AC\r\n'))
        if(res[0]==(b'AC\r\n')):
            p=problems.objects.get(pid=pid)
            obj.results="AC"
            hashinclude_channel_push({'result':obj.results,'tid':obj.tid})
            newrank=usr.rank
            if usr.tries%int(primes[int(pid)-1]) == 0:
                usr.total_points+=p.points 
                usr.tries=usr.tries/int(primes[int(pid)-1])
                su=hiuser.objects.order_by('-total_points','last_sub')
                for i in enumerate(su):
                    if i[1].total_points==usr.total_points and i[1].last_sub==usr.last_sub:
                               newrank=i[0]+1
                print(usr.rank,newrank)
                fu=hiuser.objects.filter(rank__lt=usr.rank,rank__gte=newrank)
                for i in fu:
                        change_obj=hiuser.objects.get(user_id=i.user_id)
                        change_obj.rank+=1
                        change_obj.save()
                usr.rank=newrank
            print(usr.total_points)
        else:
            hashinclude_channel_push({'result':res[0].decode('utf8')})
            obj.results=res[0].decode('utf8')
        obj.save()
        usr.save()
        return obj.results

@shared_task
def add(a,b):
	return a+b
