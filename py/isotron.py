# -*- coding: utf-8 -*-
"""
Created on Fri May 14 16:29:01 2010

@author: adum
"""
# outputs a list of (x,y) pairs
import random
import bisect
from numpy import *
from scipy.linalg import decomp


#compute the nearest PSD matrix of real symmetric x
def nearest_PSD(x):
    [T,U]=decomp.schur(x)
    return dot(dot(U,(T+abs(T))/2),U.T)

def pav(y):
    # don't even try to understand the code for this routine
    if y==[]:
        return []
    n = len(y)
    b = [1]*n
    prev = y[0]
    prevn = 1
    for i in range(1,n):
        while (y[i] if b[i]==1 else b[i-1])*prevn<prev*b[i]:
            b[i-1] = prev+ (y[i] if b[i]==1 else b[i-1])
            b[i]+= prevn
            if b[i]>i:
                break
            else:
                prevn=b[i-b[i]]
                prev = y[i-b[i]] if prevn==1 else b[i-b[i]-1]
        prevn = b[i]
        prev = y[i] if b[i]==1 else b[i-1]
    i = n-1
    while i>=0:
        if b[i]==1:
            b[i]=y[i]
            i-=1
        else:
            c = b[i]
            d = b[i-1]/b[i]
            for j in range(c):
                b[i-j]=d
            i-=int(c)
    return array(b)

def Lipschitz_pav(x,y,L):
    return L*x-pav(L*x-pav(y))
    

def lin_xyz(x,y,z):
    #evaluate the piecewise continuous linear function defined by x,y pairs at z
    i = bisect.bisect_left(x,z)
    if i==0:
        return y[0]
    if i>=len(y):
        return y[-1]
    delta = x[i]-x[i-1]
    if delta==0 or z==x[i]:
        return y[i]
    return (y[i]*(z-x[i-1])+y[i-1]*(x[i]-z))/delta

def isotron(x,y,its): #its is num iterations
    #output w,ux,uy
    n, d = x.shape
    w = zeros(d)
    for it in range(its):
        #print w
        #compute ux,uy
        z = zip(dot(x,w),-y,range(n))  #-y: important trick makes sure ties are handled properly
        z.sort()
        ux,sy,pi = zip(*z)
        sy = -array(sy)
        uy = pav(sy)
        for (truey,yhat,i) in zip(sy,uy,pi):
            w += (truey-yhat) * x[i] 
    z = zip(dot(x,w),-y,range(n))  
    z.sort()
    ux,sy,pi = zip(*z)
    ux = array(ux)
    uy = -array(sy)
    uy = pav(uy)
    return (w,array(ux),uy)

def triples_dot(x,w):
    d = w.shape[0]
    n = len(x)
    res = zeros(n)
    for i in range(n):
        (a,b,c) = x[i]
        res[i] = w[a,b]-w[a,c]
    return res
        
def triples_add(w,(a,b,c),k):
    w[a,b]+=k/2.
    w[b,a]+=k/2.
    w[a,c]-=k/2.
    w[c,a]-=k/2.


#below, x represents a bunch of triples (a,b,c) meaning a is more similar to b than c
def triples_isotron(x,L,its,xtest=None): #its is num iterations, L i Lipschitz param
    #output w,ux,uy
    d=max([max(t) for t in x])+1
    n = len(x)
    x = x+[(a,c,b) for (a,b,c) in x]
    y = array([1.]*n+[0.]*n)
    n *= 2
    w = zeros((d,d))
    for it in range(its):
        #print "Iteration ",it
        #compute ux,uy
        z = zip(triples_dot(x,w),-y,range(n))  #-y: important trick makes sure ties are handled properly
        z.sort()
        ux,sy,pi = zip(*z)
        ux = array(ux)
        sy = -array(sy)
        uy = Lipschitz_pav(ux,sy,L)
        c = 0.
        for (truey,yhat,i) in zip(sy,uy,pi):
            triples_add(w,x[i],truey-yhat)
            c+=(truey-yhat)**2
        if xtest!=None:
            m = len(xtest)
            test_dot = triples_dot(xtest,w)
            test_c = 0.
            for i in range(m):
                test_c+=(lin_xyz(ux,uy,test_dot[i])-1)**2
            print "It",it,"train, test sq error =",c/n,test_c/m
        else:
            print "It",it,"train sq error =",c/n
        w = nearest_PSD(w)
    z = zip(triples_dot(x,w),-y,range(n))  
    z.sort()
    ux,sy,pi = zip(*z)
    ux = array(ux)
    uy = -array(sy)
    uy = Lipschitz_pav(ux,uy,L)
    return (w,array(ux),uy)
    

def sigma(x):
    return 1./(1.+exp(-x))

#below, x represents a bunch of triples (a,b,c) meaning a is more similar to b than c
def triples_sigmoid_isotron(x,eta,its,xtest=None): #its is num iterations, eta is step size
    #output w,ux,uy
    d=max([max(t) for t in x])+1
    n = len(x)
    w = zeros((d,d))
    for it in range(its):
        #print "Iteration ",it            
        train_dot = triples_dot(x,w)
        c=0.
        for i in range(n):
            yhat = sigma(train_dot[i])
            triples_add(w,x[i],eta*(1-yhat))
            c+=(1-yhat)**2
        if xtest!=None:
            m = len(xtest)
            test_dot = triples_dot(xtest,w)
            test_c = 0.
            for i in range(m):
                test_c+=(sigma(test_dot[i])-1)**2
            print "It",it,"train, test sq error =",c/n,test_c/m, max(diag(w))
        else:
            print "It",it,"train sq error =",c/n
        w = nearest_PSD(w)
    return w
    
    
