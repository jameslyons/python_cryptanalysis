# this code cracks the affine cipher
from ScoreText import ScoreText
from pycipher import Affine
        
#ciphertext
ctext = 'QUVNLAUVILZKVZZZVNHIVQUFSFZHWZQLQHQLJSNLAUVI'
score = ScoreText() # load quadgram statistics

ptext = Affine(1,1).decipher(ctext)
max_score = score.qgram(ptext)
max_key = (1,1)

# try all posiible keys, display the one with the highest fitness
for i in [1,3,5,7,9,11,15,17,19,21,23,25]:
    for j in range(0,25):
        ptext = Affine(i,j).decipher(ctext)
        ptext_score = score.qgram(ptext)
        # keep track of our best score so far
        if ptext_score > max_score: 
            max_score, max_key = ptext_score, (i,j)

ptext = Affine(*max_key).decipher(ctext)
print 'best candidate with key (a,b) = '+str(max_key)+':'
print ptext
