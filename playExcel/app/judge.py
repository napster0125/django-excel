# excel-online-judge 

import os,subprocess,re,signal,sys,filecmp,shlex
import time

class judge:
    
	def __init__(self,cwd):
        
		"""
	
		The function initializes the paramters required during execution of the judge.

		Args :

			cwd : The current working directory 
		
		"""

		# langarray is a dictionary with the language names as keys
		# The values contains compile and execution command templates of that particular language. 

		self.langarray={"C":{"compile":"gcc [filename].c -O2 -fomit-frame-pointer -o [filename]","exec":"./[filename]"},
             		"C++":{"compile":"g++ [filename].cpp -O2 -fomit-frame-pointer -o [filename]","exec":"./[filename]"},
             		"Java":{"compile":"javac [filename].java","exec":"java -cp [classpath] [filename]"},
             		"Python2":{"exec":"python2 [filename].py"},
             		"Python3":{"exec":"python3 [filename].py"}}
        
        

		# timelimit is the execution time threshold of the particular problem. 
		self.timelimit=1

		self.cwd=cwd
		
		# Change directory 
		os.chdir(self.cwd)





	def compile(self,fid,lang):
	
		"""

		This function runs the compilation command 

		Args :
		
			lang : The respective language for which the compile commands has to be executed.
			fid : The id of the file to compiled.
		
		Returns :
	
			CE : (Compilation-Error) If the program failes to compile.
			CS : If the program compiled successfully.
	
		"""
	
        
		with open(self.cwd+"/tmp/err.txt","w") as err:
			cmd=self.langarray[lang]["compile"]
			cmd=cmd.replace("[filename]",fid)
			t=subprocess.Popen(shlex.split(cmd),preexec_fn=os.setsid,cwd=os.getcwd(),stderr=err)
			t.communicate()
			response=t.returncode
			t.kill()
			if response==0:
				return "CS"
			else:
				return "CE"






	def execute(self,pid,fid,lang):
	
		"""
		
		This function runs the execution command
		
		Args :
			
			pid : The id of the problem against which the execution command is to be evaluated
			fid : The id of the file to be compiled.
			lang : The respective language for which the execution commands have to be executed

		Returns :
		
			TLE : If execution time exceeds timelimit.
			RTE : If there is a runtime exception.
			ES : If the command executed successfully.

		"""

		with open(self.cwd+"/env/testcases/testcase"+str(pid)+".txt","r") as input:
			with open(self.cwd+"/tmp/output.txt","w") as output:
				with open(self.cwd+"/tmp/execerr.txt","w") as err:
					cmd=self.langarray[lang]["exec"]
					if lang=="Java":
						fid=fid.split('/')
						cmd=cmd.replace("[classpath]",fid[0])
						cmd=cmd.replace("[filename]",fid[1])
					else:
						cmd=cmd.replace("[filename]",fid)
					start=time.time()
					t=0
					process=subprocess.Popen(shlex.split(cmd),preexec_fn=os.setsid,cwd=os.getcwd(),stdin=input,stdout=output,stderr=err)
					try:
						process.communicate(timeout=self.timelimit)
					except subprocess.TimeoutExpired:
						t=124
					end=time.time()
					exec_resp=process.returncode
					process.kill()
					if t==124:
						return "TLE"
					elif exec_resp==1:
						return "RTE"
					else:
						return "ES"
        
	




	def validate(self,pid):
            
		"""
		
		This function compares the output file with the key

		Args :
		
			pid : The id of the problem to map to the correct key.

		Returns :

			WA : Wrong Answer , if comparison fails.
			AC : Accepted , if comparison succeeds.

		"""

		if filecmp.cmp(self.cwd+"/tmp/output.txt",self.cwd+"/env/key/key"+str(pid)+".txt")==True:
                    return "AC"
		else:
                    return "WA"







def run(pid,filename,lang):
	
	"""

	This function runs the judge and respective compile , execute and validate commands

	Args :
	
		pid : The id of the problem.
		fid : The unique file id.
		lang : The respective language for which judge needs to be executed.

	Returns :

		CE : If compilation failed.
		TLE : If time limit exceeded.
		RTE : In case of runtime error.
		WA : Wrong Answer
		AC : Accepted

	"""
	cwd=os.getcwd()	
	fid=os.path.splitext(filename)[0]
	ext=os.path.splitext(filename)[1]
	obj=judge(cwd)
	if lang not in ["Python2","Python3"]:
		ccf=obj.compile(fid,lang)
		if ccf=="CE":
			return ccf
	ecf=obj.execute(pid,fid,lang)
	if ecf!="ES":
		return ecf
	return(obj.validate(pid))
