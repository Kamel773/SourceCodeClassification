from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer
import glob,os
import tkinter
from sklearn.model_selection import GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from tkinter import *
import sys

#Loading the dataset
print('Loading the dataset')
X=[]
y=[]
code_loc='/Users/kamel/Downloads/DataAlogithmia/code25/'
name_file= ['c', 'c#', 'c++','java', 'css', 'haskell', 'html', 'java', 'javascript', 'lua', 'objective-c', 'perl', 'php', 'python','ruby', 'r', 'scala', 'sql', 'swift', 'vb.net','markdown','bash']
for item in name_file:
    code_loc_current=code_loc+item+'/'
    file_list = glob.glob(os.path.join(code_loc_current, "*.txt"))
    i = 0
    for file_path in file_list:
        f=open(file_path,'r')
        data=f.read()
        label=item
        num_lines = sum(1 for line in open(file_path))
        X.append(data)
        y.append(label)
    #print(item)


print('Extracting features from dataset')
#Extracting features from text files
#count_vect = CountVectorizer()
count_vect = TfidfVectorizer(input ='X',stop_words = {'english'},lowercase=True,analyzer ='word')
X_train_counts = count_vect.fit_transform(X)
X_train_counts.shape


#From occurrences to frequencies
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
X_train_tfidf.shape

print('Training a Multinomial Naive Bayes (MNB)')
#Training a classifier¶
clf = MultinomialNB().fit(X_train_tfidf, y)


var = input("Please enter a code snippet: ")
docs_new =  [var]
X_new_counts = count_vect.transform(docs_new)
X_new_tfidf = tfidf_transformer.transform(X_new_counts)

predicted = clf.predict(X_new_tfidf)
print('predicted as',predicted)
