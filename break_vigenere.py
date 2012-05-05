from ScoreText import ScoreText
from pycipher import Vigenere
import re

score = ScoreText() # load the quadgram statistics
ctext = 'vptnvffuntshtarptymjwzirappljmhhqvsubwlzzygvtyitarptyiougxiuydtgzhhvvmumshwkzgstfmekvmpkswdgbilvjljmglmjfqwioiivknulvvfemioiemojtywdsajtwmtcgluysdsumfbieugmvalvxkjduetukatymvkqzhvqvgvptytjwwldyeevquhlulwpkt'
ctext = re.sub(r'[^A-Z]','',ctext.upper()) #remove spacing and punctuation

# try keys in the range length=1 up to length=21
for L in range(1,22):
    key = L*['A'] # start with a key consisting entirely of 'A's
    ptext = Vigenere(''.join(key)).decipher(ctext)
    bestscore = score.qgram(ptext)
    bestkey = key[:]
    while 1:
        modified = False
        for i in range(0,len(key)):  
            key = bestkey[:]
            for k in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                key[i] = k;
                ptext = Vigenere(''.join(key)).decipher(ctext)
                tempscore = score.qgram(ptext)
                if tempscore > bestscore:
                    bestscore = tempscore
                    bestkey = key[:]
                    modified = True
        if not modified:
            break
    print str(bestscore),L,'key:',''.join(bestkey)
    print '    ',Vigenere(''.join(bestkey)).decipher(ctext)

