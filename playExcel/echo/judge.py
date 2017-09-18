import os, filecmp, shutil, sys, subprocess

class judge :

    def __init__(self, playerId) :
        
        '''
            Initialize arguments required for the functions

        '''
        self.playerId = playerId

        if not os.path.exists('players') :
            os.makedirs('players')

        if not os.path.exists('skel') :
            os.makedirs('skel')

        self.cwd = os.getcwd()

        self.appdir = os.path.join(os.getcwd(), 'players/')

        self.workdir = os.path.join(self.appdir, self.playerId+'/')

        self.homedir = os.path.join(os.getcwd(), 'skel/home/')

        if not os.path.exists(self.homedir) :
            os.makedirs(self.homedir)

        if not os.path.exists(self.workdir) :
            os.makedirs(self.workdir)

        subprocess.Popen(['cp', '-r' , self.homedir, self.workdir])

        os.chdir(os.path.join(self.workdir, 'home/'))

    def execute(self, level, question, code, arg1, arg2) :

        '''
            Create the shell script from the code and make it executable

            Execute the script in restricted bash

        '''
        tout = False
        with open(self.workdir+'home/code.sh', 'w+') as file :
            file.write(code)

        subprocess.Popen(['chmod', '+x', self.workdir+'home/code.sh'])

        with open(self.workdir+'home/output.txt', 'w') as output :
            out = subprocess.Popen(['rbash', self.workdir+'home/code.sh', arg1], stdout=output)

            try :
                out.communicate(timeout=1)
            except out.TimeoutExpired :
                tout = True
            
            if tout :
                output.write('Script Execution Timed Out!')

        state = False
        levelId = str(level) + str(question)
        testfile = os.path.join(os.path.join(self.cwd, 'testcases/'), levelId+'1.txt')  
        if not tout :
            state = self.validate(self.playerId, testfile)

        if state :
            state = False
            with open(self.workdir+'home/output.txt', 'w') as output :
                out = subprocess.Popen(['rbash', self.workdir+'home/code.sh', arg2], stdout=output)

                try :
                    out.communicate(timeout=1)
                except out.TimeoutExpired :
                    tout = True
            
                if tout :
                    output.write('Script Execution Timed Out!')

                levelId = str(level) + str(question)
            testfile = os.path.join(os.path.join(self.cwd, 'testcases/'), levelId+'2.txt')  
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
    print(sys.argv[1])
    playerId = sys.argv[1]
    level = sys.argv[2]
    question = sys.argv[3]
    code = sys.argv[4]

    arg1 = sys.argv[5]
    arg2 = sys.argv[6]

    obj = judge(playerId)

    print(obj.execute(level, question, code, arg1, arg2))

if __name__ == "__main__" : main()