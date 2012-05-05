import json
import re

class ScoreText(object):
    def __init__(self):
        fl = open('ngrams.json','rb')
        data = json.load(fl)
        self.monogr = data[0]
        self.bigr = data[1]
        self.trigr = data[2]
        self.qgr = data[3]
        fl.close()

    def monogram(self,text):
        score = 0
        for i in text:
            if i in self.monogr: score += self.monogr[i]
            else: score += self.monogr['floor']
        return score  
        
    def bigram(self,text):
        score = 0
        for i in xrange(len(text)-1):
            if text[i:i+2] in self.bigr: score += self.bigr[text[i:i+2]]
            else: score += self.bigr['floor']
        return score  

    def trigram(self,text):
        score = 0
        for i in xrange(len(text)-2):
            if text[i:i+3] in self.trigr: score += self.trigr[text[i:i+3]]
            else: score += self.trigr['floor']            
        return score   

    def qgram(self,text):
        score = 0
        qgr = self.qgr.__getitem__
        for i in xrange(len(text)-3):
            if text[i:i+4] in self.qgr: score += qgr(text[i:i+4])
            else: score += qgr('floor')          
        return score
       
