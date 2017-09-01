# Sample file to test hashinclude

from hashinclude.tasks import run

run.delay(1,'test.cpp','C++')
run.delay(1,'test2.py','Python3')
run.delay(1,'test4.py','Python3')
run.delay(1,'test5.py','Python3')
run.delay(1,'test3.java','Java')
