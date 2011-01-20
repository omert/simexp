# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 14:38:53 2010

@author: adum
"""

import turk, time
import sys
import tools, random, string, shutil

#sys.argv = ["","c:/sim/font_sample.config","c:/sim/sample.trips","c:/sim/sample.out"]

if len(sys.argv)!=4 and len(sys.argv)!=3:
    print "Usage: runtrips.py config_file trips_file output_file"
    print " or"
    print "Usage: runtrips.py config_file trips_file"
    print "in which case the output file is trips_file.out"
    exit(1)

if len(sys.argv)==3:
    (a,b,c) = sys.argv[2].rpartition(".")
    if b=="":
        sys.argv.append(sys.argv[2]+".out")
    else:
        sys.argv.append(a+".out")
    print "outfile "+sys.argv[-1]

config = tools.remove_comments(tools.my_read(sys.argv[1]).split("\n"))
trips = tools.remove_comments(tools.my_read(sys.argv[2]).strip().split("\n"))

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


tools.my_write(turk.log_root++"/"+label+".out_file_loc",sys.argv[3])
shutil.copy(sys.argv[2],turk.log_root++"/"+label+".trips")
shutil.copy(sys.argv[1],turk.log_root++"/"+label+".config2")


print "**** The ID of this batch is ",label

print "Waiting 2 minutes"

time.sleep(120)



#label=None
turk.check_til_done(label,sys.argv[3],trips) #outfile

