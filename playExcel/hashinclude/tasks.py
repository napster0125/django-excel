from __future__ import absolute_import,unicode_literals
from celery import shared_task
import sys,os,django
import subprocess,shlex

from common.consumers import hashinclude_channel_push

from .models import problems

# To test celery without running django-runserver

'''

sys.path.append("/home/sivasama/works/Play.Excel/playExcel/")
os.environ["DJANGO_SETTINGS_MODULE"]="playExcel.settings"
django.setup()

'''

@shared_task
def run(pid,fid,lang):
        sq=" "
        cmd="bash hashinclude/dockerrun.sh "+str(pid)+sq+fid+sq+lang
        p=subprocess.Popen(shlex.split(cmd),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        res=p.communicate()
        p.kill() 
        if res[0].decode('utf8')=='AC':
            p=problems.object.get(pid=pid)
            hashinclude_channel_push({'result':'AC'},{'score':p.points})
        else:
            hashinclude_channel_push({'result':res[0].decode('utf8')},{'score':0})
        return res[0].decode('utf8')  
