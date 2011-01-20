import tools, turk, csv, random
from numpy import *
import matplotlib.pyplot as plt
import Tkinter
from PIL import Image, ImageTk
import os
import pickle
import isotron

from boost_class import *
from logistic_regression import *
from simple_SVM import *




MM_file = "c:/temp/MM"

assert os.path.exists(MM_file)
f = open(MM_file,"rb")
(wids,t,M) = pickle.load(f)
f.close()
print "unpickling", M.shape


def to_in(i,j):
    a = max(i,j)
    b = min(i,j)
    return (a*(a+1))/2+b


def compute_S(M):
    n = 26
    
    m = 2*(26*26*27)/2
    X = zeros((m,(n*(n+1))/2))
    Y = zeros(m)
    
    
    r = 0
    for i in range(n):
        for j in range(n):
            for k in range(j+1):
                X[r][to_in(i,j)]=1.
                X[r][to_in(i,k)]=-1.
                Y[r] = M[i][j][k]
                r+=1
                X[r][to_in(i,j)]=-1.
                X[r][to_in(i,k)]=1.
                Y[r] = M[i][k][j]
                r+=1
    
    (w,ux,uy)=isotron.isotron(X,Y,30)
    haty = [isotron.lin_xyz(ux,uy,dot(w,x)) for x in X]
    
    print "Our squared error:",sum([(haty[i]-Y[i])**2 for i in range(m)])/(1.*m)
    print "0's squared error:",sum([(Y[i])**2 for i in range(m)])/(1.*m)
    
    S = zeros((n,n))
    a = max(w)
    b = min(w)
    
    for i in range(n):
        for j in range(n):
            S[i][j]=(w[to_in(i,j)]-b)/(a-b)
    
    sr = []
    for i in range(n):
        for j in range(i):
            sr.append((S[i][j],chr(97+i)+chr(97+j)))
    sr.sort()
    res = ""
    for (x,ab) in sr:
        res += " "+ab
    print res
    return S
#plt.plot(ux,uy)
#plt.plot(ux,[2/(1+exp(-.04*x))-1 for x in ux],'r')
#plt.show()

def alpha():
    return [chr(97+i) for i in range(26)]
    
def alpha_c(li):
    return set(alpha())-set(li)

def le2n(a):
    return ord(a)-97

#see if each unlabeled example is more similar to positives or negatives
def learn(pos,neg,X,la="boosting",R=20):
    assert len(pos)>1 and len(neg)>1
    n = X.shape[0]
    lpos = [le2n(i) for i in pos]
    lneg = [le2n(i) for i in neg]
    Y = zeros(len(lpos)+len(lneg))
    for i in range(len(lpos)):
        Y[i]=1.
    for i in range(len(lneg)):
        Y[i+len(lpos)]=-1.
    y = {}
    unl = set(alpha())-set(pos)-set(neg)
    if len(unl)>0:
        if la=="svm":
            wvec = simple_SVM(X[lpos+lneg],Y,R)
            for i in unl:
                y[i]=dot(wvec,X[le2n(i)])
        if la=="boosting":
            wvec = adaboost_feats(X[lpos+lneg],Y,R)
            for i in unl:
                y[i]=dot(wvec,X[le2n(i)])
        if la=="logistic":
            lr = LogisticRegression(X[lpos+lneg],Y,X[[le2n(i) for i in unl]],1.0/R)
            lr.train()
            u=lr.test_predictions()
            i=0
            for a in unl:
                y[a] = 2*u[i]-1
                i+=1
                
    for i in pos:
        lpos2 = lpos[:]
        lpos2.remove(le2n(i))
        if la=="boosting":
            wvec = adaboost_feats(X[lpos2+lneg],Y[1:],R)
            y[i]=dot(wvec,X[le2n(i)])
        if la=="svm":
            wvec = simple_SVM(X[lpos2+lneg],Y[1:],R)
            y[i]=dot(wvec,X[le2n(i)])
        if la=="logistic":
            lr = LogisticRegression(X[lpos2+lneg],Y[1:],X[[le2n(i)]],1.0/R)
            lr.train()
            y[i]=2*lr.test_predictions()[0]-1

    for i in neg:
        lneg2 = lneg[:]
        lneg2.remove(le2n(i))
        if la=="svm":
            wvec = simple_SVM(X[lpos+lneg2],Y[:-1],R)
            y[i]=dot(wvec,X[le2n(i)])      
        if la=="boosting":
            wvec = adaboost_feats(X[lpos+lneg2],Y[:-1],R)
            y[i]=dot(wvec,X[le2n(i)])      
        if la=="logistic":
            lr = LogisticRegression(X[lpos+lneg2],Y[:-1],X[[le2n(i)]],1.0/R)
            lr.train()
            y[i]=2*lr.test_predictions()[0]-1

    errs = 0
    sqerr  = 0.0
    for i in pos:
        sqerr+=(y[i]-1)**2
        if y[i]<0:
            errs+=1.
    for i in neg:
        sqerr+=(y[i]+1)**2
        if y[i]>=0:
            errs+=1.
    m = len(pos)+len(neg)
    print "Err: ",errs/m,"\tSq err:",sqerr/m
    return (y,errs/m)
    
vowels = ['a','e','i','o','u']
cons = alpha_c(vowels)
tall = ['f','h','k','l','d','b']
low = ['p','q','g','y','j']

normal = set(alpha())-set(tall)-set(low)

n = M.shape[0]

#for each letter, is it more similar to a or b (for each a,b)
X1 = zeros( (n,(n*(n-1))/2) ) 
for x in range(n):
    i=0
    for a in range(n):
        for b in range(a):
            X1[x][i]=M[x][a][b]
            i+=1

#for each letter, is it more similar to a than b is similar to a (for each a,b)
X2 = zeros( (n,(n*(n-1))/2) ) 
for x in range(n):
    i=0
    for a in range(n):
        for b in range(a):
            X2[x][i]=sign(M[a][x][b])
            i+=1
res = []
errs = []
zzz = alpha()
random.shuffle(zzz)

for t in [1,2,10,500]:    
    (y,err) = learn(['a','b','c','d','e','f','g','h','i','j'],['p','q','r','s','t','u','v','w','x','y','z'],X2,"boosting",2*t)
    res.append(sorted([(y[i],i) for i in y]))
    errs.append(err)
print errs
print res[-1]