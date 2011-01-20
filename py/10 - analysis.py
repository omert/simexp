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
from lasso import *



MM_file = "c:/temp/MM"
SS_file = "c:/temp/SS"

assert os.path.exists(MM_file)
f = open(MM_file,"rb")
(wids,t,M) = pickle.load(f)
f.close()
print "unpickling", M.shape


alpha=[chr(97+i) for i in range(26)]

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
    
    mms = "GraphPlot[{"
    
    sr = []
    for i in range(n):
        for j in range(i):
            sr.append((S[i][j],chr(97+i)+chr(97+j)))
            if S[i][j]>0.3:
                mms+=chr(97+i)+"->"+chr(97+j)+","
    sr.sort()
    res = ""
    for (x,ab) in sr:
        res += " "+ab
    print res
    
    mms=mms[:-1]
    mms+="},VertexLabeling->True]"
    #print mms

    for i in range(n):
        res = chr(97+i)+" "
        sr = []
        for j in range(n):
            sr.append((S[i][j],chr(97+j)))
        sr.sort(reverse=True)
        for (x,b) in sr:
            res += " "+b
        print res
    

#    plt.plot(ux,uy)
#    plt.plot(ux,[2/(1+exp(-.04*x))-1 for x in ux],'r')
#    plt.show()
    return S

def compute_S2(M):
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
    
    mms = "GraphPlot[{"
    
    sr = []
    for i in range(n):
        for j in range(i):
            sr.append((S[i][j],chr(97+i)+chr(97+j)))
            if S[i][j]>0.3:
                mms+=chr(97+i)+"->"+chr(97+j)+","
    sr.sort()
    res = ""
    for (x,ab) in sr:
        res += " "+ab
    print res
    
    mms=mms[:-1]
    mms+="},VertexLabeling->True]"
    #print mms

    for i in range(n):
        res = chr(97+i)+" "
        sr = []
        for j in range(n):
            sr.append((S[i][j],chr(97+j)))
        sr.sort(reverse=True)
        for (x,b) in sr:
            res += " "+b
        print res
    

#    plt.plot(ux,uy)
#    plt.plot(ux,[2/(1+exp(-.04*x))-1 for x in ux],'r')
#    plt.show()
    return S

    
    

def le2n(a):
    return ord(a)-97

def ridge_regression(X,Y,R):
    return  dot(linalg.inv(dot(X.T,X)+R*eye(X.shape[1])),dot(X.T,Y))


def without(li,i):
    return li[:i]+li[i+1:]

def train_test(Xtrain,Ytrain,Xtest,la,R):
    if la=="logistic":
        lr = LogisticRegression(Xtrain,Ytrain,Xtest,1.0/R)
        lr.train()
        return 2*lr.test_predictions()-1   
    if la=="ridge":
        wvec = ridge_regression(Xtrain,Ytrain,R)
    if la=="svm":
        wvec = simple_SVM(Xtrain,Ytrain,R)
    if la=="boosting":
        wvec = adaboost_feats(Xtrain,Ytrain,R)
    return dot(wvec,Xtest.T)

#see if each unlabeled example is more similar to positives or negatives
def learn(train,X,la="boosting",R=20):
    n = X.shape[0]
    lets, Y = zip(*train)
    llets = [le2n(i) for i in lets]
    y = {}
    unl = set(alpha)-set(lets)
    lunl = [le2n(i) for i in unl]
    if len(unl)>0:
        res = train_test(X[llets],Y,X[lunl],la,R)
        for i in range(len(lunl)):
            y[chr(97+lunl[i])]=res[i]
    for i in range(len(llets)):
        res = train_test(X[without(llets,i)],without(Y,i),X[llets[i]],la,R)
        y[chr(97+llets[i])]=res
    errs = 0
    sqerr  = 0.0
    for i in range(len(llets)):
        sqerr+=(y[lets[i]]-Y[i])**2
        if y[lets[i]]*Y[i]<=0:
            errs+=1. 
    m = len(llets)
    print "Err: ",errs/m,"\tSq err:",sqerr/m
    return (y,errs/m)


vowels = ['a','e','i','o','u']
cons = set(alpha)-set(vowels)-set(['y'])
tall = ['f','h','k','l','d','b','t']
low = ['p','q','g','y','j']

normal = set(alpha)-set(tall)-set(low)

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
X2 = zeros( (n,(n*(n-1))/2+1) ) 
for x in range(n):
    X2[x][0]=1.
    i=1
    for a in range(n):
        for b in range(a):
            X2[x][i]=sign(M[a][x][b])
            i+=1
#for each letter, is it more similar to a than b is similar to a (for each a,b)
X3 = zeros( (n,(n*(n-1))/2) ) 
for x in range(n):
    i=0
    for a in range(n):
        for b in range(a):
            X3[x][i]=M[a][x][b]
            i+=1
    
#tools.save_matrix(X1,"c:/matlab/X1.txt")
#tools.save_matrix(X2,"c:/matlab/X2.txt")
#tools.save_matrix(X3,"c:/matlab/X3.txt")


def load_letter(c,color="black",size=100):
    im = Image.open("C:/vision/calibrialpha/calibri-"+c+".png")
    im = im.resize(((im.size[0]*size)/im.size[1],size))
    
    ## now make the white invisible 
    im = im.convert('RGBA')
    source = im.split()                 # split the image into layers
    mask = im.point(lambda i: i < 255)  # kluge
    if color=="blue":
        source[2].paste(im.point(lambda i: 255 if i<100 else 0))
    if color=="green":
        source[1].paste(im.point(lambda i: 255 if i<100 else 0))
    if color=="red":
        source[0].paste(im.point(lambda i: 255 if i<100 else 0))
    source[3].paste(mask)               # put mask into the alpha channel
    im = Image.merge(im.mode, source)   # build a new multiband image
    ##
    return ImageTk.PhotoImage(im)



def letter_display(train,test):
    sd = tools.SimpleDisplay()
    imlist=[]
    t = {}
    for (a,y) in train:
        t[a]=y
    for i in range(26):
        c = chr(i+97)
        if c in test:
            imlist.append((load_letter(c,color="blue"),test[c],i*100))
        if c in t:
            imlist.append((load_letter(c,color="black",size=50),t[c],i*100))
    sd.go(imlist)
    sd.mainloop()


XX = hstack([X1,X3])



tools.sub_col_mean(XX)

res = []
errs = []
ys= []
zzz = alpha
random.shuffle(zzz)



if os.path.exists(SS_file):
    f = open(SS_file,"rb")
    print "unpickling"
    S = pickle.load(f)
    f.close()
else:
    S = 2*compute_S(M)-1
    f = open(SS_file,"wb")
    print "pickling"
    pickle.dump(S,f,-1)
    f.close()






def to_train_test(pos,neg):
    return [(i,1.) for i in pos]+[(i,-1.) for i in neg]

tryme1 = ['w', 'p', 'b', 'f', 'v', 'm', 't', 'd', 'n', 'z', 'r' ,'l']

tryme2 = ['a','e','o','c','q','b','p','d','s','g']


tt = to_train_test(['a','b','c','d','e','f','g'],['t','u','v','w','x','y','z'])
#alphabet order:
#tt = [(chr(97+i),i-14) for i in range(26)]
#scrabble points!:
#tt = [('e',1),('a',1),('i',1),('o',1),('n',1),('r',1),('t',1),('l',1),('s',1),('u',1),('d',2),('g',2),('b',3),('c',3),('m',3),('p',3),('f',4),('h',4),('v',4),('w',4),('y',4),('k',5),('j',8),('x',8),('q',10),('z',10)]
#tt = [(x,y-2) for (x,y) in tt]
#Letter frequency:
#tt=[('a', 0.63339999999999996), ('b', -0.7016), ('c', -0.44359999999999999), ('d', -0.14939999999999998), ('e', 1.5404), ('f', -0.5544), ('g', -0.59699999999999998), ('h', 0.21880000000000011), ('i', 0.39319999999999999), ('j', -0.96940000000000004), ('k', -0.84560000000000002), ('l', -0.19499999999999995), ('m', -0.51879999999999993), ('n', 0.34979999999999989), ('o', 0.50139999999999985), ('p', -0.61419999999999997), ('q', -0.98099999999999998), ('r', 0.19740000000000002), ('s', 0.26540000000000008), ('t', 0.81119999999999992), ('u', -0.44840000000000002), ('v', -0.8044), ('w', -0.52800000000000002), ('x', -0.96999999999999997), ('y', -0.60519999999999996), ('z', -0.98519999999999996)]
#random set:
#r = alpha[:]
#random.shuffle(r)
#tt = to_train_test(r[:14],r[14:])
tt = to_train_test(tall,set(alpha)-set(tall))
for t in [0.0001,0.001,0.01,0.1,1,10,100,1000,10000]:    
    (y,err) = learn(tt,hstack([ S]),"ridge",t)
    res.append(sorted([(y[i],i) for i in y]))
    errs.append(err)
    ys.append(y.copy())
print errs
i = argmin(errs)
print i
print res[i]
letter_display(tt,ys[i])

