import os, filecmp, shutil, sys, subprocess, re

class judge :

    def __init__(self, playerId) :
        
        '''
            Initialize arguments required for the functions

        '''
        self.playerId = playerId

        # if not os.path.exists('echo/players') :
        #     os.makedirs('echo/players')

        # if not os.path.exists('echo/skel') :
        #     os.makedirs('echo/skel')

        self.cwd = os.getcwd()
        self.appdir = os.path.join(os.getcwd(), 'players/')

        self.workdir = os.path.join(self.appdir, self.playerId+'/')

        # self.homedir = os.path.join(os.getcwd(), 'skel/home/')

        # if not os.path.exists(self.homedir) :
        #     os.makedirs(self.homedir)

        # if not os.path.exists(self.workdir) :
        #     os.makedirs(self.workdir)

        # subprocess.Popen(['cp', '-r' , self.homedir, self.workdir])

        os.chdir(self.workdir)

    def execute(self, level, code, arg1, arg2) :

        '''
            Create the shell script from the code and make it executable

            Execute the script in restricted bash

        '''
        req_res = ['7', '8']
        tout = False
        # print(code)
        # codearr = code.splitlines()
        # print(codearr)
        codefile = os.path.join(self.workdir, 'code.sh')
        with open(self.workdir+"code.sh", "w") as file :
            file.write(code)
            # for line in codearr :
            #     file.write(line)

        out = subprocess.Popen(['chmod', '+x', self.workdir+'code.sh'])

        with open(self.workdir+'output.txt', 'w') as output :
            with open(self.workdir+'error.txt', 'w') as error :
                # cmd = 
                out = subprocess.Popen(['rbash', codefile, arg1], stdout=output, stderr=error)
                try :
                    out.communicate(timeout=5)
                except subprocess.TimeoutExpired :
                    tout = True
            
                if tout :
                    error.write('Script Execution Timed Out!')

        t = ''
        with open(self.workdir+'output.txt', 'r') as output :
            t = output.read()
        with open(self.workdir+'output.txt', 'w') as output :
            output.write(re.sub(r'/media[/ 0-9 a-z A-Z]+/', r'', t))

        with open(self.workdir+'error.txt', 'r') as error :
            t = error.read()
        with open(self.workdir+'error.txt', 'w') as error :
            error.write(re.sub(r'/media[/ 0-9 a-z A-Z]+/', r'', t))
        state = False
        # levelId = str(level) + str(question)
        testfile = os.path.join(os.path.join(self.cwd, 'testcases/'), level+'1.txt')  
        if not tout :
            state = self.validate(self.playerId, testfile, level)

        if state :
            state = False
            if level in req_res :
                subprocess.Popen(['cp', '-r', '/media/reserve/'+level+'/*', os.getcwd()+'home/'+level+'/'], stdout=subprocess.PIPE)
            with open(self.workdir+'output.txt', 'w') as output :
                with open(self.workdir+'error.txt', 'w') as error :
                    out = subprocess.Popen(['rbash', self.workdir+'code.sh', arg2], stdout=output, stderr=error)

                    try :
                        out.communicate(timeout=5)
                    except subprocess.TimeoutExpired :
                        tout = True
            
                    if tout :
                        error.write('Script Execution Timed Out!')

                # levelId = str(level) + str(question)
            testfile = os.path.join(os.path.join(self.cwd, 'testcases/'), level+'2.txt')  
            if not tout :
                state = self.validate(self.playerId, testfile)
        
        return state

    def validate(self, playerId, testfile, level) :
        '''
            Compare output with the testcases

        '''
        valid = False
        req_res = ['7', '8']
        if level not in req_res :
            valid = filecmp.cmp(self.workdir+'output.txt', testfile)
        else :
            val = ''
            with open(self.workdir+'output.txt', 'w') as out :
                subprocess.Popen(['/media/reserve/'+level+'.sh'], stdout=out)
            with open(self.workdir+'output.txt', 'r') as out :
                val = out.read()
            if val == 'True' :
                valid = True
        return valid

def main() :
    '''
        Run the judge for the player

    '''
    playerId = sys.argv[1]
    level = sys.argv[2]
    # question = sys.argv[3]
    # code = '\n'.join(sys.argv[3:])
    code = sys.argv[3]

    # with open('/tmp/'+playerId+'.txt', 'r') as temp :
    #     code = '\n'.join(str(line) for line in temp)
    arg1 = sys.argv[3]
    arg2 = sys.argv[4]
    obj = judge(playerId)
    
    print(obj.execute(level, code, arg1, arg2))

if __name__ == "__main__" : main()