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
        #print(cmd)
        p=subprocess.Popen(shlex.split(cmd),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        res=p.communicate()
        p.kill() 
        primes=[2,3,5,7,11,13,17]
        #print(res)
        obj=submissionTask(user_id=usr,tid=run.request.id)
        #print(str(res[0]).strip()=='AC')
        #print("reached hereeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",1234567)
        if(res[0]==b'AC\r\n'):
            #print("reached hereeeeeeeeeee222222222222222222222222222")
            p=problems.objects.get(pid=pid)
            #print("pid: ",pid)
            obj.results="AC"
            hashinclude_channel_push({'verdict':obj.results,'tid':obj.tid,'time':usr.last_sub})
            newrank=usr.rank
            #print(usr.tries%int(primes[int(pid)-1]))
            if usr.tries%int(primes[int(pid)-1]) == 0:
                usr.total_points+=p.points 
                usr.tries=usr.tries/int(primes[int(pid)-1])
                usr.save()
                su=hiuser.objects.order_by('-total_points','last_sub')
                for i,j in enumerate(su):                              
                        j = hiuser.objects.get(user_id=j.user_id)
                        j.rank=i+1
                        #print("modified rank of %s is %d"%(j.user_id.username,j.rank))
                        j.save()
                print(usr.total_points)
        else:
            hashinclude_channel_push({'verdict':res[0].decode('utf8'),'tid':obj.tid,'time':usr.last_sub})
            obj.results=res[0].decode('utf8')
        obj.save()
        return obj.results

