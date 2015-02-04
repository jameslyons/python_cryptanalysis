# usage: python break_fracmorse.py 'CIPHERTEXTMESSAGE'
# ideally you'll want 200 or so characters to reliably decrypt, shorter will often work but not as reliably.

import random
from ngram_score import ngram_score
import re
import sys
from pycipher import FracMorse

#ctext = FracMorse('PQRSTUVWXYZABCDEFGHIJKLMNO').encipher("He has not been returned to sea because of his affection for caregivers.The waitress pointed to the lunch menu, but the oldest living ex-major leaguer had no use for it")
fitness = ngram_score('fmorse_quadgrams.txt') # load our quadgram model

# helper function, converts an integer 0-25 into a character
def i2a(i): return 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[i%26]

# decipher a piece of text using the substitution cipher and a certain key    
def sub_decipher(text,key):
    invkey = [i2a(key.index(i)) for i in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
    ret = ''      
    for c in text:
        if c.isalpha(): ret += invkey[ord(c.upper())-ord('A')]
        else: ret += c
    return ret

# This code is just the simple substitution cipher cracking code, it works perfectly for fractionated morse as
# long as you use fractioned morse statistics instead of english statistics.
def break_simplesub(ctext,startkey=None):
    ''' perform hill-climbing with a single start. This function may have to be called many times
        to break a substitution cipher. '''
    # make sure ciphertext has all spacing/punc removed and is uppercase
    ctext = re.sub('[^A-Z]','',ctext.upper())
    parentkey,parentscore = startkey or list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'),-99e99
    if not startkey: random.shuffle(parentkey)
    parentscore = fitness.score(sub_decipher(ctext,parentkey))
    count = 0
    while count < 1000:
        a = random.randint(0,25)
        b = random.randint(0,25)
        child = parentkey[:]
        # swap two characters in the child
        child[a],child[b] = child[b],child[a]
        score = fitness.score(sub_decipher(ctext,child))
        # if the child was better, replace the parent with it
        if score > parentscore:
            parentscore, parentkey = score, child[:]
            count = 0 # reset the counter
        count += 1
    return parentscore, parentkey

ctext = sys.argv[1]
ctext = re.sub(r'[^A-Z ]','',ctext.upper())
maxscore, maxkey = break_simplesub(ctext,list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
print str(maxscore),'simplesub key:',''.join(maxkey), 'decrypt: ',sub_decipher(ctext,maxkey)
for i in range(1000):
    score, key = break_simplesub(ctext)
    if score > maxscore:
        maxscore,maxkey = score,key[:]
        print str(maxscore),'FractionatedMorse key:',''.join(maxkey), 'decrypt: ',FracMorse(maxkey).decipher(ctext)

