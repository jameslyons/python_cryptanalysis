from pycipher.util import ngram_freq
import re
import json
import sys
try:
    f = open(sys.argv[1],'r')
except IndexError:
    print "getstats requires 1 argument: a large text file from which to build statistics"
    exit()
except IOError:
    print "could not open file: "+sys.argv[1]
    exit()
    
text = ''.join(f.readlines()).upper()
f.close()  

text = re.sub(r'[^A-Z]','',text) # remove all punctuation
print "number of chars: "+str(len(text))
print "You will typically want > 3 million chars for accurate quadgram stats."
fjson = open('ngrams.json','w')

print 'building monograms ...'
monograms = ngram_freq(text,N=1,log=True)
print 'building bigrams ...'
bigrams = ngram_freq(text,N=2,log=True)
print 'building trigrams ...'
trigrams = ngram_freq(text,N=3,log=True)
print 'building qgrams ...'
qgrams = ngram_freq(text,N=4,log=True)
# write everything to file
json.dump((monograms,bigrams,trigrams,qgrams), fjson)

fjson.close()      
print 'n-gram extraction successfully completed.'
