import glob
import os
from sklearn.externals import joblib
import Algorithmia

#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')


"""
def CountTheEmptyFiles():
	name_file=['bash','c++','php','javascript','sql','c#','html','c','r','python','css','perl','objective-c','java','vb.net','ruby','swift','haskell','lua','scala']

	countAllEmptyflie = 0
	for languageName in name_file:
		file_list = glob.glob(os.path.join(os.getcwd(), ("code/" + languageName), "*.txt"))

		corpus = []
		count = 0

		for file_path in file_list:
		    with open(file_path) as f_input:
		        #corpus.append(f_input.read()
		        #if f_input.read() == None:
		        if os.stat(file_path).st_size == 0:
					count = count + 1
					countAllEmptyflie = countAllEmptyflie + 1
		        #print file_path

		print ("The number of empty code for " + languageName + " is " + str(count))
		#print corpus
	print("The Total empty flies is " + str(countAllEmptyflie))
"""


def CountTheNumberOfLineOfCode():
	code_loc='/Users/MSR/Desktop/DataAlogithmia/code25/'
	code_loc_out='/Users/MSR/Desktop/algorithmia/output/'
	
	#name_file=['python-3.x','python-2.7','python-3.5','python-3.4','python-2.x','python-3.6','python-3.3','python-2.6','java-8','java-7','c++11','c++03','c++98','c++14']
	name_file=['javascript','markdown','java','php','c','lua','html','objective-c','sql','css','c++','swift','bash','ruby','perl','c#','scala','python','r','haskell','vb.net']
	#name_file=['scala']
	dict_file_loc ={}
	dict_file_char={}
	client = Algorithmia.client('simYGBMWHTC86IxZZV04RrjtN8Q1')
	algo = client.algo('PetiteProgrammer/ProgrammingLanguageIdentification/0.1.3')
	for item in name_file:
		code_loc_current=code_loc+item+'/'
		#os.mkdir(code_loc_output)
		dict_file_loc[item]=[]
		dict_file_char[item]=[]
		#for languageName in name_file:
		file_list = glob.glob(os.path.join(code_loc_current, "*.txt"))
		count=0
		count_code_snippet = 0
		small=0;medium=0;large=0;
		individual_count={};individual_count['large']=1;individual_count['medium']=1;individual_count['small']=1;
		print (item)
		for file_path in file_list:
			with open(file_path) as f_input:
				no_char=os.stat(file_path).st_size
				if no_char==0:
					continue
				count+=1
				no_loc= sum(1 for _ in f_input)
			dict_file_loc[item].append(no_loc)
			dict_file_char[item].append(no_char) 
			
			#s=''
			#if no_loc >24:
			#	s='large'
			#elif no_loc > 12:
			#	s='medium'
			#else:
			#	s='small'
			count_code_snippet = count_code_snippet + 1
			if count_code_snippet == 151:
				break
			#if individual_count[s] > 25:
			#	continue
			#individual_count[s]+=1	
			#We open the same file again and read
			new_file=code_loc_out+ file_path.split('/')[-1]
			#print (new_file)
			file_in=open(file_path,'r')
			file_out=open(new_file,'w')
			data=file_in.read()
			results=algo.pipe(data).result
			#file_out.write(item+" " +str(no_loc)+" " +str(no_char)+" " +s+ '\n')
			file_out.write(item+" " +str(no_loc)+" " +str(no_char)+" " + '\n')
			for result in results:
				file_out.write(str(result[0])+" "+str(result[1])+'\n')
			file_out.close()
			file_in.close()	
			#print (count)
		print (individual_count)
		
		print (item,count,sum(dict_file_loc[item])/len(dict_file_loc[item]),sum(dict_file_char[item])/len(dict_file_char[item]))  
		
	joblib.dump(dict_file_loc,'dict_file_loc_standard.pkl')
	joblib.dump(dict_file_char,'dict_file_char_standard.pkl')
		




CountTheNumberOfLineOfCode()






