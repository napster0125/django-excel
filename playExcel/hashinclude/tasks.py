from __future__ import absolute_import,unicode_literals
from celery import shared_task
import sys,os,django
import subprocess,shlex

# To test celery without running django-runserver

sys.path.append("/home/sivasama/works/Play.Excel/playExcel/")
os.environ["DJANGO_SETTINGS_MODULE"]="playExcel.settings"
django.setup()

### 

@shared_task
def run(pid,fid,lang):
        sq=" "
        cmd="bash hashinclude/dockerrun.sh "+str(pid)+sq+fid+sq+lang
        p=subprocess.Popen(shlex.split(cmd),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        res=p.communicate()
        p.kill()
        return res[0].decode('utf8')  
