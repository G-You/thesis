import pickle
import jieba
import regex as re

'''
# Chinese
data = pickle.load(open("chn_dyads.p","rb"))
shared = pickle.load(open("shared_items.p","rb"))
success = pickle.load(open("game_success.p","rb"))
'''


data = pickle.load(open("eng_dyads.p","rb"))
shared = pickle.load(open("eng_shared_items.p","rb"))
success = pickle.load(open("eng_game_success.p","rb"))


chn_f = open("chn_ref_list.txt","r+")
eng_f = open("eng_ref_list.txt","r+")
chn_noun = chn_f.read().split()
eng_noun = eng_f.read().split()

f = open("eng_align_score.txt","w+")
i = 1
occur = 0
bi_occur = 0
noun_flag = 0
prev_item = {}
prev_bi = {}

def get_bigram(l):
    if (len(l)<2):
        return ([])
    else:
        bi_list = []
        for i in range(len(l)-1):
            bi_list.append(str(l[i])+"_"+str(l[i+1]))
        return (bi_list)

for dyad in data:
    trial_num = 1
    for trial in dyad: 
        bi_occur = 0        
        occur = 0
        noun_flag = 0
        interrupt = 0
        f.write(str(i)+"\t")
        pair = list(set(trial["person"]))
        p1 = pair[0]
        p2 = "person2"
        prev_item = {}
        prev_item[p1] = []
        prev_item[p2] = []
        prev_bi = {}
        prev_bi[p1] = []
        prev_bi[p2] = []
        turnno = 0
        for turn in trial["product"]:
#            for item in jieba.lcut_for_search(turn):   #chinese
            for item in turn.split():
                if (trial["person"][turnno]==p1):
                    if item in prev_item[p2]: #alignment
                        occur += 1
                else:
                    if item in prev_item[p1]: #alignment
                        occur += 1
                if item in eng_noun or item in chn_noun: #ref
                    noun_flag = 1
            if (trial["person"][turnno]==p1):
                prev_item[p1] = prev_item[p1] + turn.split()
            else:
                prev_item[p2] = prev_item[p2] + turn.split()
            for bi in get_bigram(turn.split()):
                if (trial["person"][turnno]==p1):
                    if bi in prev_bi[p2]: #alignment
                        bi_occur += 1
                        print(p1+"   "+bi)
                else:
                    if bi in prev_bi[p1]: #alignment
                        bi_occur += 1
                        print(p1+"   "+bi)
            if (trial["person"][turnno]==p1):
                prev_bi[p1] = prev_bi[p1] + get_bigram(turn.split())
            else:
                prev_bi[p2] = prev_bi[p2] + get_bigram(turn.split())

            turnno += 1

        for p in trial["process"]:  #turn-taking
            simul = re.findall(r"⊆[^▅⊇]+⊇",p)
            interrupt += len(simul)

        words = len(set(prev_item[p1] + prev_item[p2]))
        bi_words = len(set(prev_bi[p1] + prev_bi[p2]))

        f.write(str(trial_num)+"\t"+str(occur)+"\t"+str(words)+"\t"+str(bi_occur)+"\t"+str(bi_words)+"\t"+str(noun_flag)+"\t"+str(interrupt)+"\t"+str(success[i-1][trial_num-1])+"\t\n")
        trial_num += 1
    i += 1

        
