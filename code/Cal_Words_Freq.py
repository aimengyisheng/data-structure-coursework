from collections import defaultdict
import os
class Cal_Words_Freq:
    def __init__(self,files):
        self.indexx ={}
        self.liss = {}
        stop_words=['a','about','after','all','also','always','am','an','and','any','are','at','be','been','being','but',
        'by','came','can','cannot','could','did','didnot','do','does','doesnot','doing','donnot','else','for','from','get' 
        ,'give','goes','going','had','happen','has','have','having','how','i','if','ill','in','into','is','it','its',
        'just','keep','let','like','made','make','many','may','me','mean','more','most','much','no','not','now','of',
        'only','or','our','really','say','see','some','something','take','tell','than','that','the','their','them','then'
        ,'they','thing','this','to','try','up','us','use','used','uses','very','want','was','way','we','what','when',
        'where','which','who','why','will','with','without','wont','you','your','youre','']
        for file in files:

            with open(file) as f:
                data = f.read()
                for i in '-,.:?"!\()0123456789\'':
                    data = data.replace(i, "")
                data = data.replace("<br />"," ")
                data = data.replace("/","")
                data = data + " "
                buf = ""

                for i in range(len(data)):
                    if (data[i] != " "):
                        buf += data[i].lower()
                    else:
                        if buf in stop_words:
                            buf = ""
                            pass
                        elif buf not in self.liss: 
                            self.liss[buf]=1
                        else:
                            self.liss[buf] += 1
                        buf = ""
    def getInv(self):
        
        return self.liss