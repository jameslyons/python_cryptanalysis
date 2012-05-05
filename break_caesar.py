# this code cracks the caesar cipher
from ScoreText import ScoreText
from pycipher import Caesar

        
#ciphertext
ctext = 'YMJHFJXFWHNUMJWNXTSJTKYMJJFWQNJXYPSTBSFSIXNRUQJXYHNUMJWX'
score = ScoreText() # load our quadgram statistics

ptext = Caesar(1).decipher(ctext)
max_score = score.qgram(ptext)
max_key = 1

for i in range(2,26):
    ptext = Caesar(i).decipher(ctext)
    ptext_score = score.qgram(ptext)
    if ptext_score > max_score:
        max_score, max_key = ptext_score, i

ptext = Caesar(max_key).decipher(ctext)
print 'best candidate with key '+str(max_key)+':'
print ptext
