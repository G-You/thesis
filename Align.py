import xlrd
import jieba
import jieba.posseg as pseg
from collections import Counter
import pickle

#Data file
book = xlrd.open_workbook("CleanedData.xlsx")
sh = book.sheet_by_index(0)

first = ""
person1 = []  
person2 = []
#stopwords = ["是","不","吧","没","有","不是","没有","好","就","就是","了","啊","那"," ","？","一","的","什么","。","，","哦","对","你","我","嗯","恩","鼻子","眼睛","嘴巴","眉毛","脸"]
stopwords = []
interlist = []
jointlist = []
lexicons = []
tags = []
turns = []

#column0:sender; 1:text; 2:process
for rx in range(sh.nrows):
    if (sh.row(rx)[0].value=="New"):    #A new dyad
#        print(person1)
#        print(person2)
        inter = list(set(person1)&set(person2))  #shared lexical items
        if (inter!=[]):
            lexicons.append(list(set(person1+person2)))
            interlist.append(inter)
            tags.append(turns)
            jointlist = jointlist + inter
#        cut_inter = list(set(inter)-set(stopwords))
#        print(cut_inter)
        first = ""
        person1 = []  
        person2 = []
        turns = []
    else:
        text = sh.row(rx)[1].value
        if isinstance(text, float):	#a new trial
            continue
        #=====POS TAG=====#
        words = pseg.cut(text)
        sent = []
        for w in words:
            if w.flag in ["n","nr","nt","nz","nl","ng","a","an","ag","al"]:
                sent.append(w.word)
        turns.append(sent)
        #=================#

        if (first==""): #person1 hasn't been set
            first = sh.row(rx)[0].value
            person1 = person1 + jieba.lcut_for_search(text)
            
        else:
            if (sh.row(rx)[0].value == first):
                person1 = person1 + jieba.lcut_for_search(text)
            else:
                person2 = person2 + jieba.lcut_for_search(text)

inter = list(set(person1)&set(person2))
lexicons.append(list(set(person1+person2)))
interlist.append(inter)
tags.append(turns)
jointlist = jointlist + inter

for item in jointlist:
    if (jointlist.count(item)>3):
        stopwords.append(item)		#>6: stopwords


shared_items=[]
print(set(stopwords))
for l in interlist:
    cut_inter = list(set(l)-set(stopwords))
#    print(len(cut_inter))
#    print(cut_inter)
    shared_items.append(cut_inter)

#pickle.dump(shared_items,open("shared_items.p","wb"))

noun_list = sum(sum(tags,[]),[]) #fucking clever
noun_dict = Counter(noun_list)

fn = open("chn_ref_list.txt","w+")

for n in noun_dict:
    fn.write(str(n)+"\n")
#---------------lexiconPool--------------------#



