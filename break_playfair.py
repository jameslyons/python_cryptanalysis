from ScoreText import ScoreText
from pycipher import Playfair
import random
import math

#ctext = 'XZOGQRWVQWNROKCOAELBXZWGEQYLGDRZXYZRQAEKLRHDUMNUXYXSXYEMXEHDGNXZYNTZONYELBEUGYSCOREUSWTZRLRYBYCOLZYLEMWNSXFBUSDBORBZCYLQEDMHQRWVQWAEDPGDPOYHORXZINNYWPXZGROKCOLCCOCYTZUEUIICERLEVHMVQWLNWPRYXHGNMLEKLRHDUYSUCYRAWPUYECRYRYXHGNBLUYSCCOUYOHRYUMNUXYXSXYEMXEHDGN'
ctext = 'pdflakmygubxxsulrqractavefbkrykggfmkrqcxqzksdpcfvnormqbnryhmzmskkmseeflwebgrilxbrysrdlboislzmsprcfmrawosoxpmwonxsxcfcdrpdpnmiczefceaphdkrmgakqaplfricfbobznafmiooramlenoclrykcprpdiuolmkxarabrszcfxbclskclprhmaqmpfcea'
scoreText = ScoreText()

def modify_key(parent):
    i = random.randint(0,4)
    child = parent[:]
    if i == 0: #swap 2 rows
        a,b = random.randint(1,4),random.randint(1,4)
        child[5*a:5*a+4] = parent[5*b:5*b+4] 
        child[5*b:5*b+4] = parent[5*a:5*a+4]
    elif i == 1: #swap 2 cols
        a,b = random.randint(1,4),random.randint(1,4)
        child[a::5] = parent[b::5] 
        child[b::5] = parent[a::5]
    else:
        a,b = random.randint(1,24),random.randint(1,24)
        child[a] = parent[b]
        child[b] = parent[a]      
    return child
        
        

parent = list('BCDEFGHIKLMNOPQRSTUVWXYZ')
random.shuffle(parent)
parent = ['A']+parent
pf = Playfair(parent)
parentscore = scoreText.qgram(pf.decipher(ctext))

bestkey = parent[:]
bestscore = parentscore

T = 20
while T >= 0:
    for i in xrange(50000):
        child = modify_key(parent)   
        pf = Playfair(child)
        childscore = scoreText.qgram(pf.decipher(ctext))
        dF = childscore - parentscore
        if dF >= 0:
            parentscore,parent = childscore,child[:]
        elif T > 0:
            prob = math.exp(dF/T)
            if prob > random.random():
                parentscore,parent = childscore,child[:]
        if parentscore > bestscore:
            bestscore,bestkey = parentscore,parent[:]        
    print T,bestscore,parentscore,''.join(bestkey)
    T = T-1


pf = Playfair(bestkey)
print 'best key: '+''.join(bestkey)
print 'plaintext: '+pf.decipher(ctext)
