from ScoreText import ScoreText
from pycipher import Autokey
import re

score = ScoreText() # load the quadgram statistics
ctext = 'WHDAVUIGLFLMFSVSKMSGZMJVZSGLVZKOTUIIXJIITEBXZIMYUMLZIKPYTAVBIHEBBBTKIANWSJXTEDHNEKILEIIFYIOVPSWGKLIAFHCQIIIARFYIIBBSEFVPIHXUGKCMMMOIIEPLIOVPSWAHBJEVSVUYSRGHUGGLRDKAIZEMSLLIAMWVYUVBIHRVGEAGRDKXUGKCMM'
ctext = re.sub(r'[^A-Z]','',ctext.upper())

# try keys in the range length=1 up to length=21
for L in range(1,22):
    key = L*['A'] # start with a key consisting entirely of 'A's
    ptext = Autokey(''.join(key)).decipher(ctext)
    bestscore = score.qgram(ptext)
    bestkey = key[:]
    while 1:
        modified = False
        for i in range(0,len(key)):  
            key = bestkey[:]
            for k in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                key[i] = k;
                ptext = Autokey(''.join(key)).decipher(ctext)
                tempscore = score.qgram(ptext)
                if tempscore > bestscore:
                    bestscore = tempscore
                    bestkey = key[:]
                    modified = True
        if not modified:
            break
    print str(bestscore),L,'key:',''.join(bestkey)
    print Autokey(''.join(bestkey)).decipher(ctext)
