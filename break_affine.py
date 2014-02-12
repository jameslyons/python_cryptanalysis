# this code cracks the affine cipher
import re
from ngram_score import ngram_score
fitness = ngram_score('quadgrams.txt') # load our quadgram statistics
from pycipher import Affine
        
def break_affine(ctext):
    # make sure ciphertext has all spacing/punc removed and is uppercase
    ctext = re.sub('[^A-Z]','',ctext.upper())
    # try all posiible keys, return the one with the highest fitness
    scores = []
    for i in [1,3,5,7,9,11,15,17,19,21,23,25]:
        scores.extend([(fitness.score(Affine(i,j).decipher(ctext)),(i,j)) for j in range(0,25)])
    return max(scores)
    
# example ciphertext
ctext = 'QUVNLAUVILZKVZZZVNHIVQUFSFZHWZQLQHQLJSNLAUVI'
max_key = break_affine(ctext)

print 'best candidate with key (a,b) = '+str(max_key[1])+':'
print Affine(max_key[1][0],max_key[1][1]).decipher(ctext)
