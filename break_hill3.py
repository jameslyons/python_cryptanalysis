# this code breaks 3by3 hill ciphers fairly efficiently. 

from itertools import product
from ngram_score import ngram_score
L2I = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ",range(26)))
I2L = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
import sys
preamble = sys.argv[1]
ctext = sys.argv[2]
  
def hill3decipher(ctext,key):
    if len(ctext)%3==1:
        ctext = ctext + 'XX'
    elif len(ctext)%3==2:
        ctext = ctext + 'X'
    ptext = ""
    for i in range(0,len(ctext),3):
        ptext += I2L[(key[0]*L2I[ctext[i]] + key[1]*L2I[ctext[i+1]] + key[2]*L2I[ctext[i+2]])%26] + \
                 I2L[(key[3]*L2I[ctext[i]] + key[4]*L2I[ctext[i+1]] + key[5]*L2I[ctext[i+2]])%26] + \
                 I2L[(key[6]*L2I[ctext[i]] + key[7]*L2I[ctext[i+1]] + key[8]*L2I[ctext[i+2]])%26]        
    return ptext        
    
# keep a list of the N best things we have seen, discard anything else
# the list may be greater than N, and unsorted. Call finalise() before accessing
# to guarantee correct length and sorted order.
class nbest(object):
    def __init__(self,N=1000):
        self.store = []
        self.N = N
        
    def add(self,item):
        self.store.append(item)
        if len(self.store): self.finalise()
        
    def finalise(self):
        self.store.sort(reverse=True)
        self.store = self.store[:self.N]   
    
    def __getitem__(self,k):
        return self.store[k]

    def __len__(self):
        return len(self.store)


import re
# this is the second feynman cipher, no known decryption
ctext ='XUKEXWSLZJUAXUNKIGWFSOZRAWURORKXAOSLHROBXBTKCMUWDVPTFBLMKEFVWMUXTVTWUIDDJVZKBRMCWOIWYDXMLUFPVSHAGSVWUFWORCWUIDUJCNVTTBERTUNOJUZHVTWKORSVRZSVVFSQXOCMUWPYTRLGBMCYPOJCLRIYTVFCCMUWUFPOXCNMCIWMSKPXEDLYIQKDJWIWCJUMVRCJUMVRKXWURKPSEEIWZVXULEIOETOOFWKBIUXPXUGOWLFPWUSCH'
ctext = re.sub('[^A-Z]','',ctext.upper())

mono = ngram_score('monograms.txt')
bi = ngram_score('bigrams.txt')
quad = ngram_score('quadgrams.txt')

N = 20
rec = nbest(N)
for seq in product(range(26),repeat=3):
    if seq[0]%2 == 0 and seq[1]%2 == 0 and seq[2]%2 == 0:
        continue
    if seq[0]%13 == 0 and seq[1]%13 == 0 and seq[2]%13 == 0:
        continue        
    seq2 = (seq[0],seq[1],seq[2],1,1,1,1,1,1)
    txt = hill3decipher(ctext,seq2)
    score = 0
    for i in range(0,len(txt),3):
        score += mono.score(txt[i])
    rec.add((score,seq2))   

rec.finalise()
rec2 = nbest(N)
for j in range(N):
  for seq in product(range(26),repeat=3):
    if seq[0]%2 == 0 and seq[1]%2 == 0 and seq[2]%2 == 0:
        continue
    if seq[0]%13 == 0 and seq[1]%13 == 0 and seq[2]%13 == 0:
        continue        
    seq2 = (rec[j][1][0],rec[j][1][1],rec[j][1][2],seq[0],seq[1],seq[2],1,1,1)
    txt = hill3decipher(ctext,seq2)
    score = 0
    for i in range(0,len(txt),3):
        score += bi.score(txt[i:i+2])
    rec2.add((score,seq2))   

rec2.finalise()
rec3 = nbest(N)
for j in range(N):
    for seq in product(range(26),repeat=3):
        seq2 = (rec2[j][1][0],rec2[j][1][1],rec2[j][1][2],rec2[j][1][3],rec2[j][1][4],rec2[j][1][5],seq[0],seq[1],seq[2])
        da = (seq2[0]*seq2[4]*seq2[8] + seq2[1]*seq2[5]*seq2[6] + seq2[2]*seq2[3]*seq2[7]) - (seq2[2]*seq2[4]*seq2[6] + seq2[1]*seq2[3]*seq2[8] + seq2[0]*seq2[5]*seq2[7])
        if da % 2 == 0 or da % 13 ==0:
            continue
        txt = hill3decipher(ctext,seq2)
        score = quad.score(txt)
        rec3.add((score,seq2)) 

rec3.finalise()
for j in range(10):
    print rec3[j],preamble, hill3decipher(ctext,rec3[j][1])
    sys.stdout.flush()

