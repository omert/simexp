# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 19:12:38 2010

@author: adum
"""

import sys
import os
import glob                     # needed for file globbing with wildcards
import tools, string

if len(sys.argv)==1:
    sys.argv.append(os.getcwd())
    
for d in sys.argv[1:]:
    if os.path.exists(d+'\\ids.txt'):
        continue
    os.chdir(d)
    lst = glob.glob('*.jpg')
    assert(len(lst)>0); #no jpegs in directory?
    tools.my_write(d+'\\ids.txt',string.join(lst,'\n'))
    print "Created "+d+'\\ids.txt, '+str(len(lst))+" distinct ids"

