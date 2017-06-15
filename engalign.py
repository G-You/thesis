import xlrd
import jieba
import nltk
import pickle
from collections import Counter

#Data file
book = xlrd.open_workbook("EngCleanedData.xlsx")
sh = book.sheet_by_index(0)

first = ""
person1 = []  
person2 = []
stopwords = []
interlist = []
jointlist = []
lexicons = []
tags = []
turns = []

#-------------shared-items------------------#

#column0:sender; 1:text; 2:process
for rx in range(sh.nrows):
    if (sh.row(rx)[0].value=="New"):    #A new dyad
#        print(person1)
#        print(person2)
        inter = list(set(person1)&set(person2))  #shared lexical items
        if (inter!=[]):
            lexicons.append(person1+person2)
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
        if isinstance(text, float):
            continue
        #=====POS TAG=====#
        words = nltk.word_tokenize(text)
        pos = nltk.pos_tag(words)
        sent = []
        for w in pos:
            if w[1] in ["NN","NNS","NNP","NNPS","JJ"]:
                sent.append(w[0])
        turns.append(sent)
        #=================#

        if (first==""): #person1 hasn't been set
            first = sh.row(rx)[0].value
            person1 = person1 + text.split()
        else:
            if (sh.row(rx)[0].value == first):
                person1 = person1 + text.split()
            else:
                person2 = person2 + text.split()

inter = list(set(person1)&set(person2))
interlist.append(inter)
lexicons.append(person1+person2)
tags.append(turns)
jointlist = jointlist + inter

for item in jointlist:
    if (jointlist.count(item)>3):
        stopwords.append(item)		#>6: stopwords

shared_items = []

print(set(stopwords))
for l in interlist:
    cut_inter = list(set(l)-set(stopwords))
#    print(len(cut_inter))
#    print(cut_inter)
    shared_items.append(cut_inter)

#pickle.dump(shared_items,open("eng_shared_items.p","wb"))

noun_list = sum(sum(tags,[]),[]) #fucking clever
noun_dict = Counter(noun_list)

fn = open("eng_ref_list.txt","w+")

for n in noun_dict:
    fn.write(str(n)+"\n")

#print(len(lexicons))

#-------------shared-items------------------#

#-------------shared-items------------------#
