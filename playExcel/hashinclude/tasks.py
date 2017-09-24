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
        obj=submissionTask(user_id=usr,tid=run.request.id)
        if res[0].decode('utf8')=='AC':
            p=problems.object.get(pid=pid)
            obj.results="AC"
            hashinclude_channel_push({'result':obj.result})
            if usr.tries%primes[pid-1] == 0:
                usr.total_points+=p.points 
                usr.tries=usr.tries/primes[pid-1]
                su=hiuser.objects.order_by('total_points','sub_time')
                for i in enumerate(su):
                    if i[1].total_points==usr.total_points and i[1].sub_time==usr.sub_time:
                               newrank=i[0]+1
                fu=hiuser.objects.filter(rank>usr.rank and rank<=newrank)
                for i in fu:
                    i.rank+=1
                usr.rank=newrank
        else:
            hashinclude_channel_push({'result':res[0].decode('utf8')})
            obj.results=res[0].decode('utf8')
        obj.save()
        usr.save()
        return obj.results
