import json, sys, os, xmltodict, csv
from os.path import join
from utils import *
import shutil
from sklearn.externals import joblib
import time
from bs4 import BeautifulSoup
import sqlite3
import re
from spacy.en.language_data import STOP_WORDS
from spacy.en import English
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from nltk.corpus import stopwords
import spacy
import time
import csv
from bs4 import BeautifulSoup
from spacy.pipeline import DependencyParser
import nltk
def clean(x):
    #neo4j-import doesn't support: multiline (coming soon), quotes next to each other and escape quotes with '\""'
    return x.replace('\n','').replace('\r','').replace('\\','').replace('"','')

"""
def body_split(body):
    # print(body)
    soup = BeautifulSoup(body, "html5lib")
    t2_soup=soup.find_all('code')
    code_text = ""
    for item in t2_soup:
        if len(item.text)< 10:
            continue
        code_text = code_text + str(item.text) + "\n"

    return code_text
"""
def NamedEntities(nlp,text):
    doc = nlp(text)
    temp =[]
    for ent in doc.ents:
        temp.append(ent.text)

    return " ".join(temp)
def remove_stopwords_lemmatize(clean_text, stop_words, nlp):
    stop_words_removed = ' '.join(filter(lambda x: x.lower() not in stop_words,  clean_text.split()))
    doc = nlp(stop_words_removed)
    lemmatized_sentence = ' '.join([x.lemma_ for x in doc])
    return lemmatized_sentence


def clean_data(text, stop_words, nlp):

    clean_text = re.sub(r'[^a-zA-Z#++.-]', ' ', text).lower()
    #print (clean_text)
    # print("***************")
    # print("TEXT WITH STOP WORDS:")
    # print(clean_text)
    text_without_stop_words = remove_stopwords_lemmatize(clean_text, stop_words, nlp)
    return text_without_stop_words

def dependencyparser(parser,combined):
    temp=[]
    for sentence in nltk.sent_tokenize(combined):
        parsed = parser(sentence)
        for token in parsed :
            #if (token.text.isalpha()) and (len(token.text) >2):
            if (len(token.text) >2):
                if (token.tag_ == "NNP") or (token.tag_ == "NNPS") or (token.tag_ == "NN") :
                    temp.append(token.text)
    return " ".join(temp)


def body_split(body):
    #print ('body')
    #print(body)
    soup = BeautifulSoup(body, "html5lib")
    t2_soup=soup.find_all('code')
    code_text = ""
    #text_without_code = re.sub(r'<code>.*?</code>', ' ', body)
    text_without_code = re.sub(r'<code>.*?</code>', ' ', body)
    soup2 = BeautifulSoup(text_without_code, "html5lib")
    text_without_code_tags = soup2.get_text()
    
    for item in t2_soup:
        code_text = code_text + str(item.text) + "\n"
    
    t3_soup = soup.find_all('p')
    text_only = ""
    for item in t3_soup:
        text_only = text_only + str(item.text) + "\n"
    #print('Text')
    #print (text_only)
    #print('Code')
    #print(code_text)
    #print('Kamel Text')
    #print (soup3.text.strip())
    return text_only, code_text
tag_file=['javascript','sql','java','c#','python','php','c++','c','typescript','ruby','swift','objective-c','vb.net','assembly','r','perl','vba','matlab','go','scala','groovy','coffeescript','lua','haskell']
#tag_file=['javascript','markdown','java','php','c','lua','html','objective-c','sql','css','c++','swift','bash','ruby','perl','c#','scala','python','r','haskell','vb.net']
tag_file= ['c++11','c++14','c++17','c#-4.0','c#-5.0','c#-3.0','c#-2.0','c#-6.0','c#-7.0']
en_stopwords = stopwords.words('english')
stop_words = list(STOP_WORDS) + list(ENGLISH_STOP_WORDS) + list(en_stopwords)

nlp = spacy.load('en')
parser = English()
output_dir1 ='/Users/MSR/Desktop/SCAM/code25/'
output_dir2 ='/Users/MSR/Desktop/SCAM/text25/'
output_dir3 ='/Users/MSR/Desktop/SCAM/CodeText25/'
os.mkdir(output_dir1)
os.mkdir(output_dir2)
os.mkdir(output_dir3)
#Read the tag list file for SO and load into dictionary for faster hashing.

#tag_file=['python-3.x','python-2.7','python-3.5','python-3.4','python-2.x','python-3.6','python-3.3','python-2.6','java-8','java-7','c++11','c++03','c++98','c++14']
print (len(tag_file))
set_tag_file=set(tag_file)
tag_dict ={}
for tag in tag_file:
    os.mkdir(output_dir1+tag)
    os.mkdir(output_dir2+tag)
    os.mkdir(output_dir3+tag)
    tag_dict[tag] = 0


a = time.time()
for i, line in enumerate(open("/Users/MSR/Desktop/Cleanup/stackoverflow-neo4j/extracted/Posts.xml")):
    line = line.strip()
    if i %1000000==0:
        print(tag_dict)
        print (i,time.time() -a)
        a = time.time()
    try:
    #if True:
        if line.startswith("<row"):
            el = xmltodict.parse(line)['row']
            el = replace_keys(el)
            #postid= el.get('id')
            posttype = el['posttypeid']
            if (int(posttype) ==1): #These are questions, we need only title,Body and Tag(Primary)
                CreationDate=el['creationdate'][0:10].replace('-',"")
                Score=clean(el.get('score',''))
                if el.get('tags'):
                    eltags = [x.replace('<','') for x in el.get('tags').split('>')]
                    tags= set([x.lower() for x in eltags if x])


                common_tag=tags.intersection(set_tag_file)
                if not len(common_tag)==1:
                    continue
                #if len(common_tag) == 0:
                #    continue
                tag=list(common_tag)[0]
                if tag_dict[tag] >5000:
                    continue
                
                
                #print(list(common_tag)[0])
                #print (len(common_tag))
                #print (tags)
                #tag = (list(common_tag)[0])
                """
                temptag=tags    
                for tag in tags:      
                    if tag in tag_dict:
                        
                        if tag_dict[tag] >20000:
                            #print(11)
                            continue
                        #if int(CreationDate[0:4]) < 2008:#2012
                            #print(12)
                            #continue
                        #if int(CreationDate[0:4]) > 2019:
                            #print(13)
                            #continue
                        #if int(Score) <1:
                            #print(14)
                            #continue
                        #print(tag)


                """ 


                postid= el.get('id')
                body_code = el.get('body','')
                title=el.get('title','')
                #if 'c#' not in tags:
                #    continue


                #print('body')
                #print(body_code)
               
                #break
                body_text,body_code=body_split(body_code)
                #body_text combined with title.
                #print('body_text')
                #print(body_text)
                #print('body_code')
                #print(body_code)
                if len(body_code) < 10:
                    continue
                #print ('tags',tag)
                combined=title +" "+body_text
                '''
                #found a Green post by looking for a words
                found_Word = 0
                for word in tag_file:
                    if word in combined:
                        found_Word = found_Word + 1
                if found_Word == 0:
                    continue
                '''
                dp =dependencyparser(parser,combined)
                body_cleaned=clean_data(dp, stop_words, nlp)
                body_with_code=body_cleaned+" "+body_code
                name1=output_dir1+tag+"/"+str(postid)+".txt"
                name2=output_dir2+tag+"/"+str(postid)+".txt"
                name3=output_dir3+tag+"/"+str(postid)+".txt"
                file1= open(name1,"w")
                file2= open(name2,"w")
                file3= open(name3,"w")
                file1.write(body_code)
                file2.write(body_cleaned)
                file3.write(body_with_code)
                file1.close()
                file2.close()
                file3.close()
                
                tag_dict[tag] +=1 
                        #continue
            else:
                continue
    except Exception as e:
        print('x',e)

joblib.dump(tag_dict,'tag_standard_count.pkl')


