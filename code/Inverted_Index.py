from collections import defaultdict
import os
class Inverted_Index:
    def __init__(self,files):
        self.indexx ={}
        self.liss = defaultdict(list)
        for file in files:
            with open(file) as f:
                data = f.read()
                for i in '-,.:?"!\()0123456789\'':
                    data = data.replace(i, "")
                data = data.replace("<br />"," ")
                data = data.replace("/","")
                data = data + " "
                buf = ""
                flag = 0

                for i in range(len(data)):
                    if (data[i] != " "):
                        buf += data[i].lower()
                    else:
                        if buf == '':
                            pass
                        else:
                            for j in range(len(self.liss[buf])):
                                if self.liss[buf][j] != file:
                                    flag +=1
                                else:
                                    flag=0
                                    break
                            if flag == len(self.liss[buf]):
                                self.liss[buf].append(file)
                            flag = 0
                            buf = ""
        self.indexx = sorted(dict(self.liss).items())
    def getInv(self):
        return self.indexx