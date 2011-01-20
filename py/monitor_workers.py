# -*- coding: utf-8 -*-
"""
Created on Sat May 22 09:59:55 2010

@author: adum
"""

wid_score_file = "c:/mturk/wid_score_file.txt"
wid_score_bak = "c:/mturk/.wid_score_file.bak"
block_reason = '"Work too low quality -- did not match others work"'
mturk_bin_dir = "c:/mturk/bin"

import pickle
import os
import tools

# The monitor maintains the list of assignments that each worker has completed,
# along with a "good score" and a "bad score" for each worker.  The idea
# is that every time a worker does something good, we increment the
# good score, and everytime they do something bad, we increment the
# bad score
class Monitor:
    wid_scores = {}  # wid_scores[wid][assignmentid]=score
    ignore_list = [] # list of people to ignore
    good_list = []   # list of really good workers
    reject_buffer = []   # list of (wid,assignmentID) to reject when flushed
    block_buffer = []    # list of people to block when flushed
    bonus_buffer = {}    # bonuses that we plan to give later
        

def load_monitor(fname = wid_score_file):
    if os.path.exists(fname):
        f = open(fname)
        monitor = pickle.load(f)
        f.close()
        return monitor
    else:
        print "unable to find file!"
        
        
def save_monitor(m):
    i = 0
    while os.path.exists(wid_score_bak+str(i)):
        i+=1
    os.rename(wid_score_file,wid_score_bak+str(i))
    f = open(wid_score_file,'w')
    pickle.dump(m, f)#, pickle.HIGHEST_PROTOCOL)
    f.close()

def add_assignments(li): 
    #li is (wid,assignmentID,score) or a list of them
    monitor = load_monitor()
    if type(li) is not list:
        li = [li]
    for (wid,assignmentID,score) in li:
        if wid not in monitor.wid_scores:
            monitor.wid_scores[wid] = {}
        d = monitor.wid_scores[wid]
        d[assignmentID] = score
    save_monitor()

def get_scores(wid,monitor=None):
    if monitor == None:
        monitor = load_monitor()
    if wid not in monitor.wid_scores:
        return (0,0,0)
    v = monitor.wid_scores[wid].values()
    a = sum([i for i in v if i>0])
    b = -sum([i for i in v if i<0])
    return (len(v),a,b)

def ignore_list():
    return load_monitor().ignore_list
    
def flush():
    monitor = load_monitor()
    print "swish..."
    blocked = 0
    failed = []
    while monitor.block_buffer:
        wid = monitor.block_buffer.pop()
        res = tools.my_run(mturk_bin_dir+"/blockWorker -workerid "+wid+" -reason "+block_reason,mturk_bin_dir) 
        if ('Blocked '+wid) in res:
            blocked+=1
        else:
            print "Failed to block:",wid
            print "*"+res
            failed.append(wid)
    monitor.block_buffer = failed
    if blocked>0:
        print "Blocked "+str(blocked)+" workers"
    save_monitor(monitor)
