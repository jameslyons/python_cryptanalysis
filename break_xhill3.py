from itertools import product
from ngram_score import ngram_score
L2I = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ",range(26)))
I2L = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
import sys
ctext = 'hwduyfsfqdxnx nx ymj fwy tk gwjfpnsl htijx fsi hnumjwx. bmjs fyyjruynsl yt hwfhp f mnqq hnumjw, kwjvzjshd fsfqdxnx bnqq gj uwfhynhfqqd zxjqjxx'
  
def hill3decipher(ctext,key,key2):
    if len(ctext)%3==1:
        ctext = ctext + 'XX'
    elif len(ctext)%3==2:
        ctext = ctext + 'X'
    ptext = ""
    for i in range(0,len(ctext),3):
        ptext += I2L[(key[0]*L2I[ctext[i]] + key[1]*L2I[ctext[i+1]] + key[2]*L2I[ctext[i+2]] + key2[0])%26]
        ptext += I2L[(key[3]*L2I[ctext[i]] + key[4]*L2I[ctext[i+1]] + key[5]*L2I[ctext[i+2]] + key2[1])%26]
        ptext += I2L[(key[6]*L2I[ctext[i]] + key[7]*L2I[ctext[i+1]] + key[8]*L2I[ctext[i+2]] + key2[2])%26]        
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
        if len(self.store)>2*N: self.finalise()
        
    def finalise(self):
        self.store.sort(reverse=True)
        self.store = self.store[:self.N]   
    
    def __getitem__(self,k):
        return self.store[k]

    def __len__(self):
        return len(self.store)


import re
#ctext ='XUKEXWSLZJUAXUNKIGWFSOZRAWURORKXAOSLHROBXBTKCMUWDVPTFBLMKEFVWMUXTVTWUIDDJVZKBRMCWOIWYDXMLUFPVSHAGSVWUFWORCWUIDUJCNVTTBERTUNOJUZHVTWKORSVRZSVVFSQXOCMUWPYTRLGBMCYPOJCLRIYTVFCCMUWUFPOXCNMCIWMSKPXEDLYIQKDJWIWCJUMVRCJUMVRKXWURKPSEEIWZVXULEIOETOOFWKBIUXPXUGOWLFPWUSCH'
ctext = re.sub('[^A-Z]','',ctext.upper())

mono = ngram_score('monograms.txt')
bi = ngram_score('bigrams.txt')
quad = ngram_score('quadgrams.txt')

N = 100
rec = nbest(N)
for seq in product(range(26),repeat=4):
    if seq[0]%2 == 0 and seq[1]%2 == 0 and seq[2]%2 == 0:
        continue
    if seq[0]%13 == 0 and seq[1]%13 == 0 and seq[2]%13 == 0:
        continue        
    seq2 = (seq[0],seq[1],seq[2],1,1,1,1,1,1)
    txt = hill3decipher(ctext,seq2,(seq[3],0,0))
    score = 0
    for i in range(0,len(txt),3):
        score += mono.score(txt[i])
    rec.add((score,seq2,(seq[3],0,0)))   
rec.finalise()
print 'stage 1 complete...'
rec2 = nbest(N)
for j in range(N):
  print j,
  sys.stdout.flush()
  for seq in product(range(26),repeat=4):
    if seq[0]%2 == 0 and seq[1]%2 == 0 and seq[2]%2 == 0:
        continue
    if seq[0]%13 == 0 and seq[1]%13 == 0 and seq[2]%13 == 0:
        continue        
    seq2 = (rec[j][1][0],rec[j][1][1],rec[j][1][2],seq[0],seq[1],seq[2],1,1,1)
    txt = hill3decipher(ctext,seq2,(rec[j][2][0],seq[3],0))
    score = 0
    for i in range(0,len(txt),3):
        score += bi.score(txt[i:i+2])
    rec2.add((score,seq2,(rec[j][2][0],seq[3],0)))   
print 'stage 2 complete.'
rec2.finalise()
rec3 = nbest(N)
for j in range(N):
    print j,
    sys.stdout.flush()
    for seq in product(range(26),repeat=4):
        seq2 = (rec2[j][1][0],rec2[j][1][1],rec2[j][1][2],rec2[j][1][3],rec2[j][1][4],rec2[j][1][5],seq[0],seq[1],seq[2])
        da = (seq2[0]*seq2[4]*seq2[8] + seq2[1]*seq2[5]*seq2[6] + seq2[2]*seq2[3]*seq2[7]) - (seq2[2]*seq2[4]*seq2[6] + seq2[1]*seq2[3]*seq2[8] + seq2[0]*seq2[5]*seq2[7])
        if da % 2 != 0 and da % 13 !=0:
            txt = hill3decipher(ctext,seq2,(rec2[j][2][0],rec2[j][2][1],seq[3]))
            score = quad.score(txt)
            rec3.add((score,seq2,(rec2[j][2][0],rec2[j][2][1],seq[3]))) 
        # also try other permutation
        seq2 = (seq[0],seq[1],seq[2],rec2[j][1][0],rec2[j][1][1],rec2[j][1][2],rec2[j][1][3],rec2[j][1][4],rec2[j][1][5])
        da = (seq2[0]*seq2[4]*seq2[8] + seq2[1]*seq2[5]*seq2[6] + seq2[2]*seq2[3]*seq2[7]) - (seq2[2]*seq2[4]*seq2[6] + seq2[1]*seq2[3]*seq2[8] + seq2[0]*seq2[5]*seq2[7])
        if da % 2 != 0 and da % 13 !=0:
            txt = hill3decipher(ctext,seq2,(seq[3],rec2[j][2][0],rec2[j][2][1]))
            score = quad.score(txt)
            rec3.add((score,seq2,(seq[3],rec2[j][2][0],rec2[j][2][1]))) 
        
rec3.finalise()
print 'stage 3 complete.'

for j in range(10):
    print rec3[j], hill3decipher(ctext,rec3[j][1],rec3[j][2])


