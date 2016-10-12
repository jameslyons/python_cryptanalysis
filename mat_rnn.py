import numpy as np
from numpy import shape
from util import relu
import scipy.io as sio
from math import log
from sortedcontainers import SortedList
from copy import deepcopy

def a2i(ch):
    arr = {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7,'I':8,'J':9,'K':10,
       'L':11,'M':12,'N':13,'O':14,'P':15,'Q':16,'R':17,'S':18,'T':19,'U':20,
       'V':21,'W':22,'X':23,'Y':24,'Z':25,
       'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7,'i':8,'j':9,'k':10,
       'l':11,'m':12,'n':13,'o':14,'p':15,'q':16,'r':17,'s':18,'t':19,'u':20,
       'v':21,'w':22,'x':23,'y':24,'z':25}
    return arr[ch]

def i2a(i):
    i = i%26
    arr = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z')
    return arr[i]
                
# assumes uppercase A-Z, converts to 1-hot
def letter2onehot(inputstr):
    out = np.zeros((len(inputstr),26))
    for i in range(len(inputstr)):
        out[i,a2i(inputstr[i])] = 1.
    return out

def neighbours(str):
    ln = np.zeros((26,26))
    rn = np.zeros((26,26))
    onehot = letter2onehot(str)
    for i in range(26):
        for j in range(1,len(str)-1):
            if a2i(str[j]) == i:
                rn[i,:] += onehot[j+1,:]
                ln[i,:] += onehot[j-1,:]
                
    eln = np.zeros((1,26))
    for i in range(26):
        p = ln[i,:] / sum(ln[i,:] + 1e-10)
        eln[0,i] = -np.sum(p * np.log(p+1e-10))
    ern = np.zeros((1,26))
    for i in range(26):
        p = rn[i,:] / sum(rn[i,:] + 1e-10)
        ern[0,i] = -np.sum(p * np.log(p+1e-10))
    return eln,ern
    
from numpy.random import rand

monocounts = np.array([374061888.,70195826,138416451,169330528,529117365,95422055,91258980,216768975,
                       320410057,9613410,35373464,183996130,110504544,313720540,326627740,90376747,
                       4550166,277000841,294300210,390965105,117295780,46337161,79843664,8369915,75294515,4975847])
monodist = monocounts/np.sum(monocounts)

''' keep a top N list '''    
class Store:
    def __init__(self,N=10):
        self.store = SortedList()
        self.N = N
    
    def add(self,item):
        self.store.add(item)
        if len(self.store) > self.N: self.store.pop(0)

    def pop(self,i):
        self.store.pop(i)
        
    def __len__(self):
        return len(self.store)
        
    def __getitem__(self,i):
        return self.store[i]       
        
    def __str__(self):
        return str(self.store)

''' helper function, print just relevent parts of store '''
def printstore(store):
    for i in range(len(store)):
        print store[i][0],store[i][1]
        
''' rnn class for solving substitution ciphers '''        
class rnn:
    def __init__(self,matname='C:\\Users\\james\\Documents\\MATLAB\\rnn_char\\savednn800small9B.mat'):
        mat_contents = sio.loadmat(matname)
        self.W1 = mat_contents['W1']
        self.W2 = mat_contents['W2']
        self.W3 = mat_contents['W3']
        self.WF = mat_contents['WF']
        self.b1 = mat_contents['b1']
        self.b2 = mat_contents['b2']
        self.b3 = mat_contents['b3']
        self.I = np.shape(self.W1)[0]
        self.H = np.shape(self.WF)[0]
        self.O = np.shape(self.W3)[1]

    ''' do the feedforward prediction of a piece of data'''   
    def predict(self,input):
        L = np.shape(input)[0]
        #output = np.zeros((L,self.O))

        a1 = relu(np.dot(input,self.W1) + self.b1)
        a2 = np.zeros((L,self.H))
        a2prev = np.zeros((1,self.H))        
        for i in range(L):
            a2[i,:] = relu(np.dot(a1[i,:],self.W2) + np.dot(a2prev,self.WF) + self.b2)
            a2prev = a2[i,:]
        out = np.exp(np.dot(a2,self.W3) + self.b3)
        output = out.T / (np.sum(out,1)+ 3.5e-15)
        return output.T

    ''' should give identical results as predict, except uses predict1step'''
    def predict1(self,input):
        L = np.shape(input)[0]
        output = np.zeros((L,self.O))
        a2 = np.zeros((1,self.H))
        for i in range(len(input)):
            output[i,:],a2 = self.predict1step(input[i,:],a2)
        return output    
            
    ''' given a2prev predict one step into future '''
    def predict1step(self,input,a2prev):
        a1 = relu(np.dot(input,self.W1) + self.b1)
        a2 = relu(np.dot(a1,self.W2) + np.dot(a2prev,self.WF) + self.b2)
        out = np.exp(np.dot(a2,self.W3) + self.b3)
        output = out.T / (np.sum(out,1)+ 3.5e-15)
        return output.T, a2        
    
    ''' given a vector of probabilities, pull a sample from the distribution '''    
    def sampleletter(self,distribution):
        dist = np.cumsum(distribution)
        point = rand()
        for i in range(len(distribution)):
            if point < dist[i]: 
                return i
    
    ''' solve a substitution cipher, return top N candidates in a list '''
    def solve(self,ciphertext,key={},N=200):
        alph = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        input = self.str2in(ciphertext)

        store = Store(N)
        key = {} # key is sometimes not empty?
        if ciphertext[0] in key: 
            c = key[ciphertext[0]]
            store.add((log(monodist[a2i(c)]),c,np.zeros((1,self.H)),deepcopy(key)))
        else: 
            unused = alph - set(key.values())
            for c in unused:
                key[ciphertext[0]] = c
                store.add((log(monodist[a2i(c)]),c,np.zeros((1,self.H)),deepcopy(key)))

        for i in range(1,len(ciphertext)):
            prevstore = store
            store = Store(N)
            if len(key) > len(set(ciphertext[:i])): print 'BAD3',key,i,ciphertext
            for j in range(len(prevstore)):
                score,text,a2prev,key = prevstore[j]
                feat = input[:i,:]
                feat[:,:26] = letter2onehot(text)
                pred,a2prev = self.predict1step(feat[-1,:],a2prev[:])
                if ciphertext[i] in key: 
                    c = key[ciphertext[i]]
                    store.add((score+log(pred[0,a2i(c)]), text + c, a2prev[:], deepcopy(key)))
                else: 
                    unused = alph - set(key.values())
                    for c in unused:
                        key[ciphertext[i]] = c
                        store.add((score+log(pred[0,a2i(c)]), text + c, a2prev[:], deepcopy(key)))
        ret = []
        for i in range(len(store)):
            ret.append((store[i][0],store[i][1]))
        return ret
        
    ''' return the likelyhood of a string given the rnn model '''
    def prob(self,str):
        feat = self.str2in(str)
        probs = self.predict(feat)
        prob = 0
        for i in range(len(str)-1):
            prob = prob + np.log(probs[i,a2i(str[i+1])])
        return prob            
    
    ''' build the feature vector for a string '''
    def str2in(self,str):
        onehot = letter2onehot(str)
        freq = np.mean(onehot,0)
        eln,ern = neighbours(str)
        f0 = onehot
        temp = np.dot(onehot,freq)
        f1 = np.append(temp[1:],0)
        f2 = np.append(temp[2:],(0,0))
        f3 = np.append(temp[3:],(0,0,0))
        
        temp = np.dot(onehot,eln.T)
        f4 = np.append(temp[1:],0)
        f5 = np.append(temp[2:],(0,0))
        f6 = np.append(temp[3:],(0,0,0))

        temp = np.dot(onehot,ern.T)
        f7 = np.append(temp[1:],0)
        f8 = np.append(temp[2:],(0,0))
        f9 = np.append(temp[3:],(0,0,0))      
        
        temp = np.vstack((f1,f2,f3,f4,f5,f6,f7,f8,f9))
        feat = np.concatenate((f0,temp.T),1)
        return feat
