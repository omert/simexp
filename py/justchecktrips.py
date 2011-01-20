# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 14:38:53 2010

@author: adum
"""

import turk, time
import sys, glob
import tools, random, string

#sys.argv = ["","c:/sim/font_sample.config","c:/sim/sample.trips","c:/sim/sample.out"]

#print "Usage: checktrips.py"
#print "or"
#print "checktrips.py batch_id, where batch_id is the integer id of the batch"
#print "or"
#print "checktrips.py outfileloc"


if len(sys.argv)==2:
    label = sys.argv[1].strip()
else:
    label = str(turk.get_last_label())

if "\\" in label or "." in label or "/" in label:
    label=label.replace("/","\\")
    count = 0
    fname = ""
    for filename in glob.glob(turk.log_root+"/*.out_file_loc"):
        if tools.my_read(filename).strip().replace("/","\\")==label:
            fname = filename
            count += 1
    if count>1:
        print "Found more than one .out_file_loc file pointing to",label
        print "Exiting..."
        exit(0)
    if count==0:
        print "Couldn't find any .out_file_loc file pointing to",label
        print "Maybe try absolute path"
        exit(0)
    label = fname[fname.rindex("\\")+1:-13]
    print label
        

trips = tools.remove_comments(tools.my_read(turk.log_root+"/"+label+".trips").strip().split("\n"))
trips = [i.split() for i in trips]
trips = [(int(a),int(b),int(c)) for (a,b,c) in trips]



#label=None
turk.check_results(label,tools.my_read(turk.log_root+"/"+label+".out_file_loc").strip(),trips) 

