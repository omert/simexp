# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 10:10:40 2011

@author: adum
"""

import tools
import os, csv

def create_info(dir):
    if dir[-1]!="/" and dir[-1]!="\\":
        dir+="/"
    assert not os.path.exists(dir+"info.csv")
    ids = tools.my_read(dir+"ids.txt").strip().splitlines()
    n = len(ids)
    print n,"ids."
    rs = []
    atts = [i for i in os.listdir(dir) if "." not in i]
    print "Attributes:",atts
    for i in range(n):
            r = { "id": i, "image": ids[i] }
            for att in atts:
                if att[:4]!="att_":
                    the_att="att_"+att
                else:
                    the_att = att
                if os.path.exists(dir+att+"/1/"+ids[i]):
                    r[the_att] = 1
                else:
                    if os.path.exists(dir+att+"/0/"+ids[i]):
                        r[the_att] = 0
                    else:
                        r[the_att] = -100
            rs.append(r)
    f=open(dir+"info.csv","wb")
    c = csv.DictWriter(f,sorted(rs[0].keys()))
    header = {}
    for k in rs[0].keys():
        header[k]=k
    c.writerow(header)
    c.writerows(rs)
    f.close()
    
#create_info("c:/data/flags")
#create_info("c:/data/calibrialpha")
#create_info("c:/data/neckties/neckties_small")
create_info("c:/data/newtiles")