# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 14:38:53 2010

@author: adum
"""

import turk, time
import sys
import tools, random, string

sys.argv = ["","c:/sim/font_sample.config","c:/sim/sample.trips","c:/sim/sample.out"]

def remove_comments(s):
    if type(s)==list:
        return [remove_comments(i) for i in s]
    if s.find("#")!=-1:
        return s[:s.index("#")].strip()
    return s.strip()

if len(sys.argv)!=4:
    print "Usage: runtrips.py config_file trips_file output_file"
    exit(1)

config = remove_comments(tools.my_read(sys.argv[1]).split("\n"))
trips = remove_comments(tools.my_read(sys.argv[2]).strip().split("\n"))

db = config[0]
payment = config[1]
assert float(payment)<0.9  #make sure we don't pay more than 90 cents/hit!
height = config[2]
comment = config[3]
instructions = string.join(config[4:],"\n")
if "%s" not in instructions:
    print "Instructions should have %s in them!"

inst_shortcut = turk.shortcut_to_server(instructions)



trips = [i.split() for i in trips]
#print trips
trips = [(int(a),int(b),int(c)) for (a,b,c) in trips]
datrips = [(a,b,c) if b<c else (a,c,b) for (a,b,c) in trips]
if len(datrips)<30:
    print "Too few triples.  Need at least 35."

t = turk.split_trips(datrips,40,10) #40 real triples and 10 fake ones

inp = ""
for r in t:
    inp += db
    for (a,b,c) in r:
        inp+="_"+str(a)+"_"+str(b)+"_"+str(c)
    inp+="\n"
    
print "Creating "+str(len(t))+" hits..."


label,t = turk.load_external_hit(url="http://65.215.1.20/faces/simp_sim4.py?instructions="+inst_shortcut,
                                 assignments=1,
                                 input=inp,
                                 title="Compare things to see which is most similar",
                                 description="Compare things and say which is more similar",
                                 reward=payment,
                                 duration=900,
                                 autoapproval=259200,
                                 approvalrate=95,
                                 height=height,
                                 keywords="image, similarity",
                                 numapproved=48,
                                 comment=comment)    

print "Waiting 2 minutes, label", label

time.sleep(120)



#label=None
turk.wait_til_done(label)


trips2,mis = turk.results2tripsplus(label)
bad_wids, really_bad_wids = turk.get_bad_wids(trips2)
print "bad wids",bad_wids
t = []
for (a,b,c,e,wid,hid) in trips2:
    if wid not in bad_wids:
        t.append((a,b,c,e))
random.shuffle(t)
t2 = []
for (a,b,c) in trips:
    found = False
    for i in range(len(t)):
        (x,y,z,e) = t[i]
        if x==a and (y==b and c==z or y==c and b==z):
            t2.append(t[i])
            t.pop(i)
            found = True
            break
    if found == False:
        #print "SHOOT!",(a,b,c)
        1

s = ""
for (a,b,c,e) in t2:
    s+=str(a)+" "+str(b)+" "+str(c)+" "+str(e)+"\n"
tools.my_write(sys.argv[3],s)
