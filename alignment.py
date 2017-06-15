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
noun_flag = 0

for dyad in data:
    trial_num = 1
    for trial in dyad:         
        occur = 0
        noun_flag = 0
        interrupt = 0
        f.write(str(i)+"\t")
        for turn in trial["product"]:
#            for item in jieba.lcut_for_search(turn):   #chinese
            for item in turn.split():
                if item in shared[i-1]: #alignment
                    occur += 1
                if item in eng_noun or item in chn_noun: #ref
                    noun_flag = 1
        for p in trial["process"]:  #turn-taking
            simul = re.findall(r"⊆[^▅⊇]+⊇",p)
            interrupt += len(simul)

        f.write(str(trial_num)+"\t"+str(occur)+"\t"+str(noun_flag)+"\t"+str(interrupt)+"\t"+str(success[i-1][trial_num-1])+"\t\n")
        trial_num += 1
    i += 1

        
