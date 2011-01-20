# -*- coding: utf-8 -*-
"""
Created on Sat May 22 12:14:30 2010

@author: adum
"""

import os
import time

def my_run(st,dir = None):
    if dir != None:
        os.chdir(dir)
    pipe =os.popen(st+" 2>&1",'r')
    text = pipe.read()
    sts = pipe.close()
    if sts:
            print "Exited with STATUS "+str(sts)+" on executing '"+st+"'"
    return text
    
def my_read(file):
    f = open(file,"r")
    st = f.read()
    f.close()
    return st

def my_write(file,contents):
    f = open(file,"w")
    st = f.write(contents)
    f.close()

def sub_col_mean(mat):
    (m,n)=mat.shape
    col_avg = [mat[:,j].sum()/m for j in range(n)]
    mat-=col_avg
    
def center_mat(mat):
    (m,n)=mat.shape
    row_avg = [mat[i].sum()/n for i in range(m)]
    col_avg = [mat[:,j].sum()/m for j in range(n)]
    tot = mat.sum()/(m*n)
    for i in range(m):
        for j in range(n):
            mat[i,j] = mat[i,j] + tot - row_avg[i] - col_avg[j]


def normalize(x,mag = 1.):
    r = sqrt(dot(x,x))
    if r!=0:
        x*= mag/r
    else:
        print "** [TOOLS] Alert: attempting to normalize 0 vector"


def flatten(l):
    if isinstance(l,list):
        return sum(map(flatten,l))
    else:
        return l


def print_timing(func):    
    def wrapper(*arg):
        t1 = time.time()
        res = func(*arg)
        t2 = time.time()
        print '%s took %0.1f secs' % (func.func_name, t2-t1)
        return res
    return wrapper # declare the @ decorator just before the function, invokes print_timing()

@print_timing
#this routine shows how we time routines
def test_timing(n = 10):
    time.sleep(n)