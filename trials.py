import xlrd
import pickle

book = xlrd.open_workbook("EngCleanedData.xlsx")
sh = book.sheet_by_index(0)
dyads = []
trials = []
turns = {"person":[],"product":[],"process":[]}	#product & process

for rx in range(1,sh.nrows):
    if (sh.row(rx)[0].value=="New"):
        if (trials!=[]):
            dyads.append(trials)
        trials = []
        turns = {"person":[],"product":[],"process":[]}	
    else:
        text = sh.row(rx)[1].value
        if isinstance(text, float):
            if (turns!={"person":[],"product":[],"process":[]}):
                trials.append(turns)
                turns = {"person":[],"product":[],"process":[]}
        else:
            turns["person"].append(sh.row(rx)[0].value)
            turns["product"].append(text)
            turns["process"].append(sh.row(rx)[2].value)

dyads.append(trials)

pickle.dump(dyads,open("eng_dyads.p","wb"))
        
