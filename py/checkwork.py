# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 14:38:53 2010

@author: adum
"""

import turk, time
import sys, glob
import tools, random, string, csv


s = "<html><body>"

def check_work(date = None):

    for filename in glob.glob(turk.log_root+"/*.results"):
        s+="<h2>"+filename[filename.rindex("\\")+1:-8]+"</h2>"
        print filename
        file = open(filename,"r")
        blah = csv.DictReader(file,delimiter='\t')
        c = []
        for r in blah:
            if 'Answer.res' in r and r['Answer.res']!=None and r['Answer.res']!="":
    
    if 'Answer.comment' in r and r['Answer.comment']!=None and len(r['Answer.comment'])>2:
                c.append((len(r['Answer.comment']),r['Answer.comment']))
        c.sort()
        for (a,b) in c:
            s+=b+"<br>"
        file.close()

s+= "</body></html>"

tools.my_write(turk.log_root+"/"+commentfile,s)


