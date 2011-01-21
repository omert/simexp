# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 14:38:53 2010

@author: adum
"""

import turk, time
import sys, glob
import tools, random, string, csv

commentfile = "comments.html"

#sys.argv = ["","c:/sim/font_sample.config","c:/sim/sample.trips","c:/sim/sample.out"]

#print "Usage: checktrips.py"
#print "or"
#print "checktrips.py batch_id, where batch_id is the integer id of the batch"

s = "<html><body>"

for filename in glob.glob(turk.log_root+"/*.results"):
    s+="<h2>"+filename[filename.rindex("\\")+1:-8]+"</h2>"
    print filename
    file = open(filename,"r")
    blah = csv.DictReader(file,delimiter='\t')
    c = []
    for r in blah:
        if 'Answer.comment' in r and r['Answer.comment']!=None and len(r['Answer.comment'])>2:
            c.append((len(r['Answer.comment']),r['Answer.comment']))
    c.sort()
    for (a,b) in c:
        s+=b+"<br>"
    file.close()

s+= "</body></html>"

tools.my_write(turk.log_root+"/"+commentfile,s)

print s
