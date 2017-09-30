# -*- coding: utf-8 -*-
import os, filecmp, shutil, sys, subprocess, re, shlex

class judge :

    def __init__(self, playerId) :
        
        '''
            Initialize arguments required for the functions

        '''
        self.playerId = playerId

        self.cwd = os.getcwd()
        self.appdir = os.path.join(os.getcwd(), 'echo/media/players/')

        self.workdir = os.path.join(self.appdir, self.playerId+'/')


    def execute(self, level, code, arg1, arg2) :

        '''
            Create the shell script from the code and make it executable

            Execute the script in restricted bash

        '''
        os.chdir(os.path.join(self.workdir, 'home/level'+level+'/'))
        req_res = ['7', '8']
        tout = False
        codefile = os.path.join(os.getcwd(), '/code.sh')
        with open(os.getcwd()+"/code.sh", "w") as file :
            file.write(code)

        out = subprocess.Popen(['chmod', '+x', os.getcwd()+'/code.sh'])

        with open(os.getcwd()+'/output.txt', 'w') as output :
            with open(os.getcwd()+'/error.txt', 'w') as error :
                cmd = 'docker run --memory=64M -i --rm -v '+os.getcwd()+':/tmp -w /tmp echojudge rbash ./code.sh '+arg1
                out = subprocess.Popen(shlex.split(cmd), stdout=output, stderr=error)
                try :
                    out.communicate(timeout=10)
                except subprocess.TimeoutExpired :
                    tout = True
                    cmd = self.cwd+'/echo/dockerkill.sh'
                    subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
                    error.write('Script Execution Timed Out!')

        t = ''
        
        with open(os.getcwd()+'/output.txt', 'r') as output :
            t = output.read()
        with open(os.getcwd()+'/output.txt', 'w') as output :
            query = re.compile(r'\x1b[^m]*m').sub('', t)
            output.write(re.sub(r"\w+_test.txt\b", "", query))

        with open(os.getcwd()+'/error.txt', 'r') as error :
            t = error.read()
        with open(os.getcwd()+'/error.txt', 'w') as error :
            query = re.compile(r'\x1b[^m]*m').sub('', t)
            error.write(re.sub(r"\w+_test.txt\b", "", query))
  
        state = False

        testfile = os.path.join(os.path.join(self.cwd, 'echo/testcases/'), level+'1.txt')  
        if not tout :
            state = self.validate(self.playerId, testfile)
        print(state)
        if state == True :
            state = False

            with open(os.getcwd()+'/output.txt', 'w') as output :
                with open(os.getcwd()+'/error.txt', 'w') as error :
                    cmd = 'docker run --memory=64M -i --rm -v'+os.getcwd()+':/tmp -w /tmp echojudge rbash ./code.sh '+arg2
                    out = subprocess.Popen(shlex.split(cmd), stdout=output, stderr=error)
                    try :
                        out.communicate(timeout=10)
                    except subprocess.TimeoutExpired :
                        tout = True
            
                    if tout :
                        error.write('Script Execution Timed Out!')

            testfile = os.path.join(os.path.join(self.cwd, 'echo/testcases/'), level+'2.txt')  
            if not tout :
                state = self.validate(self.playerId, testfile)
        os.chdir(self.cwd)

        return state

    def validate(self, playerId, testfile) :
        '''
            Compare output with the testcases

        '''
        valid = False
        valid = filecmp.cmp(os.getcwd()+'/output.txt', testfile, shallow=False)
        print(valid)
        return valid

def main(playerId, level, code, arg1, arg2) :
    '''
        Run the judge for the player

    '''
    obj = judge(playerId)
    
    return obj.execute(level, code, arg1, arg2)

if __name__ == "__main__" : main()
