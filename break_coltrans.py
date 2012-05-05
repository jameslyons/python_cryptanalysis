from ScoreText import ScoreText
from pycipher import ColTrans
import re
import random

score = ScoreText() # load the quadgram statistics
ctext = 'etlrstiiyemeetsisseokrxeocnasnekretwtteheethwhhfemroohaognogastmhgtytkroanicredrhlhidealheoetyhutpipswgarnhusatnfed'
ctext = 'The columnar transposition cipher is not the easiest of transposition ciphers to break, but there are statistical properties of language that can be exploited to recover the key. To greatly increase the security, a substitution cipher could be employed as well as the transposition.'
ctext = re.sub(r'[^A-Z]','',ctext.upper())
ctext = ColTrans('GERMAN').encipher(ctext)
print len(ctext)%6
# try keys in the range length=2 up to length=21
for L in range(2,22):
    key = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')[:L]
    ptext = ColTrans(''.join(key)).decipher(ctext)
    bestscore = score.trigram(ptext)
    bestkey = key[:]
    while 1:
        modified = False
        for i in xrange(0,10000):  
            key = bestkey[:]
            a = random.randint(0,L-1)
            b = random.randint(0,L-1)
            key[a],key[b] = key[b],key[a]
            ptext = ColTrans(''.join(key)).decipher(ctext)
            tempscore = score.trigram(ptext)
            if tempscore > bestscore:
                bestscore = tempscore
                bestkey = key[:]
                modified = True
        if not modified:
            break
    print str(bestscore),L,'key:',''.join(bestkey)
    print ColTrans(''.join(bestkey)).decipher(ctext)
