import os, filecmp, shutil, sys, subprocess

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

        self.homedir = os.path.join(os.getcwd(), 'skel/home/')

        # if not os.path.exists(self.homedir) :
        #     os.makedirs(self.homedir)

        # if not os.path.exists(self.workdir) :
        #     os.makedirs(self.workdir)

        # subprocess.Popen(['cp', '-r' , self.homedir, self.workdir])

        os.chdir(os.path.join(self.workdir, 'home/'))

    def execute(self, level, code, arg1, arg2) :

        '''
            Create the shell script from the code and make it executable

            Execute the script in restricted bash

        '''
        tout = False
        codefile = os.path.join(self.workdir, 'home/code.sh')
        with open(self.workdir+"home/code.sh", "w") as file :
            # print(code)
            file.writelines(code)

        out = subprocess.Popen(['chmod', '+x', self.workdir+'home/code.sh'])
   
        with open(self.workdir+'home/output.txt', 'w') as output :
            with open(self.workdir+'home/error.txt', 'w') as error :
                # cmd = 
                out = subprocess.Popen(['bash', codefile], stdout=output, stderr=error)
                try :
                    out.communicate(timeout=120)
                except subprocess.TimeoutExpired :
                    tout = True
            
                if tout :
                    error.write('Script Execution Timed Out!')

        state = False
        # levelId = str(level) + str(question)
        testfile = os.path.join(os.path.join(self.cwd, 'testcases/'), '1test.txt')  
        if not tout :
            state = self.validate(self.playerId, testfile)

        if state :
            state = False
            with open(self.workdir+'home/output.txt', 'w') as output :
                with open(self.workdir+'home/error.txt', 'w') as error :
                    out = subprocess.Popen(['rbash', self.workdir+'home/code.sh', arg2], stdout=output, stderr=error)

                    try :
                        out.communicate(timeout=120)
                    except subprocess.TimeoutExpired :
                        tout = True
            
                    if tout :
                        error.write('Script Execution Timed Out!')

                # levelId = str(level) + str(question)
            testfile = os.path.join(os.path.join(self.cwd, 'testcases/'), '1test.txt')  
            if not tout :
                state = self.validate(self.playerId, testfile)
        
        return state

    def validate(self, playerId, testfile) :
        '''
            Compare output with the testcases

        '''
        valid = filecmp.cmp(self.workdir+'home/output.txt', testfile)
        
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