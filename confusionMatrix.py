import os
import glob
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
import itertools
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import svm, datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from matplotlib import rc,rcParams
def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
	"""
	This function prints and plots the confusion matrix.
	Normalization can be applied by setting `normalize=True`.
	"""
	if normalize:
		cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
		print("Normalized confusion matrix")
	else:
		print('Confusion matrix, without normalization')

	sns.set(font_scale=1.1)
	sns.set_style("dark")
	sns.set_style("white",{"xtick.major.size": 10})
	plt.figure(figsize=(14,14))
	plt.imshow(cm, interpolation='nearest', cmap=cmap)
	plt.title(title,weight='bold').set_fontsize('22')
	plt.colorbar()
	tick_marks = np.arange(len(classes))
	plt.xticks(tick_marks, classes, rotation=90)
	plt.yticks(tick_marks, classes)

	fmt = '.2f' if normalize else 'd'
	thresh = cm.max() / 2.
	for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
		plt.text(j, i, format(cm[i, j], fmt),
			horizontalalignment="center",
			color="white" if cm[i, j] > thresh else "black")

	plt.tight_layout()
	plt.gcf().subplots_adjust(bottom=0.05,left=0.15)
	plt.ylabel('True label',weight='bold').set_fontsize('16')
	plt.xlabel('Predicted Label',weight='bold').set_fontsize('16')
	plt.xticks(weight='bold',size=16)
	plt.yticks(weight='bold',size=16)
	#plt.ylabel(r'\textbf{Y-AXIS}', fontsize=20)
	#plt.xlabel(r'\textbf{X-AXIS}', fontsize=20)
	plt.savefig("ConfusionMatrixAlgorithmia21.png", dpi=300)	



def GetMetrics():

	#name_file= ['c++','bash','php','javascript','c#','html','c','r','python','sql','css','perl','objective-c','java','vb.net','ruby','swift','haskell','lua','scala']
	#name_file=['python-3.x','python-2.7','python-3.5','python-3.4','python-2.x','python-3.6','python-3.3','python-2.6','java-8','java-7','c++11','c++03','c++98','c++14']
	name_file= ['javascript','markdown','java','php','c','lua','html','objective-c','sql','css','c++','swift','bash','ruby','perl','c#','scala','python','r','haskell','vb.net']
	labeL_mapping ={}
	for i in range(len(name_file)):
		labeL_mapping[name_file[i]]=i

	#print (labeL_mapping)
	y_pred =[]
	y_test =[]
	#code_loc_current='/Users/MSR/Desktop/Extract_and_load_data/codeout/'
	code_loc_current = '/Users/MSR/Desktop/algorithmia/output/'
	file_list = glob.glob(os.path.join(code_loc_current, "*.txt"))
	loc_correct={}
	loc_incorrect={}
	for file_path in file_list:
		algofile=open(file_path,'r')
		out=algofile.readline().replace("\n","").split(" ")
		size=out[3]
		loc=out[1]
		#print (file_path)
		#print (out)
		#raise Exception("")
		#if size=='medium':
		name=out[0]
		#if (name == 'css' or name =='html' or name =='bash'):
		#	continue
		name=labeL_mapping[name]
		y_test.append(name)
		predicted=algofile.readline().replace("\n","").split(" ")[0]
		
		#if predicted=='markdown' or predicted=='css' or predicted=='html' or predicted=='bash':
		#	predicted=algofile.readline().replace("\n","").split(" ")[0]
		if predicted=='vb':
			predicted='vb.net'
		#if predicted=='markdown':
		#	predicted=algofile.readline().replace("\n","").split(" ")[0]
		predicted=labeL_mapping[predicted]
		y_pred.append(predicted)
	print (precision_recall_fscore_support(y_test, y_pred, average='weighted'))
	print (f1_score(y_test, y_pred, average='weighted'))
	print(accuracy_score(y_test, y_pred))
	cnf_matrix = confusion_matrix(y_test, y_pred)
	
	from sklearn.externals import joblib
	

	#[cnf_matrix,y_pred,y_test,name_file]=joblib.load('/Users/MSR/Desktop/Codeonly.pkl')
	
	plot_confusion_matrix(cnf_matrix, classes=name_file,title='Confusion Matrix for Algorithmia PLI Tool',normalize=True)
	from sklearn.metrics import classification_report
	print(classification_report(y_test,y_pred,target_names=name_file))
	print (precision_recall_fscore_support(y_test, y_pred, average='weighted'))
	print('ee')
	print (f1_score(y_test, y_pred, average='weighted'))
	print(accuracy_score(y_test, y_pred))
GetMetrics()