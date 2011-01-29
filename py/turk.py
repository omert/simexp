# -*- coding: utf-8 -*-
"""
Created on Sat May 22 14:39:14 2010

To see the ids of the 100 most popular people, check out:
http://65.215.1.20/faces/get_pic.py?tid=lfw_10322_13144_2194_10531_544_7615_12424_6244_8466_10483_244_6998_8853_4681_11600_6197_11311_2650_11546_11305_7350_1834_11657_2446_6100_1549_4731_7533_8041_7169_4504_715_4867_5606_7304_4959_4974_466_13027_9058_459_1686_6752_407_6179_7801_13132_7228_8087_11400_657_5204_12246_4795_9435_12814_8333_11865_816_5994_5554_5015_1007_3915_11126_12157_7084_694_12307_9528_5240_10108_8882_9896_3948_8222_3016_10030_12115_10553_8792_914_1809_9673_12705_6111_1210_6553_11241_6332_8080_6132_12730_5322_8458_11198_9408_9621_7186_5446
c:\vision\most_popular_100_ids_balanced.txt



@author: adum
"""

import os, sys

ce_root = "c:/vision"
if os.name == 'nt':
    if os.path.exists("c:/mech-turk-tools-1.3.0/bin"):
        turk_root = "c:/mech-turk-tools-1.3.0/bin"
        the_root = "d:/sim/newgit/simexp"
    else:
        turk_root = "c:/mturk/bin"
        the_root = "c:/users/adum/simexp"
else:
    turk_root = "/home/tamuz/mturk/bin"
    the_root = "/home/tamuz/dev/simexp"
exp_root = the_root+"/turkexps"
log_root = exp_root+"/logs"
turk_log = log_root+"/turk.log"
input_template = exp_root+"/template.input"
question_template = exp_root+"/template.question"
properties_template = exp_root+"/template.properties"
recent_bad_work_file = exp_root+"/recent_bad_work.txt"


batch_size = 50
reward = "0.15"

import tools
import time, urllib, urllib2
import xml.etree.ElementTree as etree
import os, shutil, string, csv
import re
import monitor_workers
#from numpy import *
import random
import datetime



def create_rand_trips(num_data,num_trips):
    res = []
    s = ""
    while len(res)<num_trips:
        a=random.randrange(num_data)
        b=random.randrange(num_data)
        c=random.randrange(num_data)
        if b>c:
            (b,c)=(c,b)
        if a!=b and a!=c and b!=c and (a,b,c) not in res:
            res.append((a,b,c))
            s+=str(a)+" "+str(b)+" "+str(c)+"\n"
    return s.strip()

def my_log(st):
    f = open(turk_log,"a")
    f.write("\n--------------------- "+str(datetime.datetime.now())+" ---------------------\n")
    sys.stderr.write("--------------------- "+str(datetime.datetime.now())+" ---------------------")
    f.write(st)
    sys.stderr.write(st)
    f.close()

def get_balance():
    text = tools.my_run("getBalance",turk_root).strip()
    s = text.find("$")
    if s==-1:
        my_log("[BALANCE] getbalance\nCould not get balance: "+text)
        return -1
    else:
        b = float(text[s+1:])
        my_log("[BALANCE] getbalance\nGot balance of: "+str(b))
        return b

   
    
def get_last_label():
    last = False
    f = open(turk_log,"r")
    lines = f.readlines()
    f.close()
    for l in lines:
        if l[:7]=="LABEL: ":
            last = l.strip()[7:]
    return last if last else "-1"

def get_next_label():
    return str(int(get_last_label())+1+random.randrange(10000))

def load_hit_helper(label,input2, question2, properties2, comment):
    if comment!=None:
        fname = log_root+"/"+label+"_"+comment+".comment"
        tools.my_write(fname,"blah")
    st = "loadHITs -input "+input2+" -question "+question2+" -properties "+properties2+" -label "+label
    text = tools.my_run(st,turk_root)
    my_log("[LOAD HIT] "+st+"\nLABEL: "+label+"\n"+text)   
    shutil.move(turk_root+"/"+label+".success",log_root+"/"+label+".success")    
    #now find errors, try to reload 10 times
#    for i in range(10):
#        etxt = text.split("[ERROR] Error creating HIT ")[1:]
#        errors = [int(a[:a.find(" ")]) for a in etxt]
#        n = len(errors)
#        if n==0:
#            return (label,text)
#        for i in range(n):
#            print "...trying to fix ",etxt[i][:30]
#            input3=input2+"_temp.input"
#            s = tools.my_read(input2).splitlines()
#            s2 = [s[0]]+[s[i] for i in errors]
#            print "new inputs:",s2
#            s3 = string.join(s2,"\n")
#            tools.my_write(input3,s3)
#            st = "loadHITs -input "+input3+" -question "+question2+" -properties "+properties2+" -label "+label
#            text = tools.my_run(st,turk_root)
#            my_log("[LOAD HIT] "+st+"\nLABEL: "+label+"\n"+text)   
#            shutil.move(turk_root+"/"+label+".success",log_root+"/"+label+".success")    
#            
#            
#    for i in range(10):
#        print "*** FAILED TO LOAD ALL HITS!"
    return (label,text)



def load_hit_from_files(input_file,question_file,properties_file,comment=None):
    label = get_next_label()
    input2 = log_root+"/"+label+".input"
    question2 = log_root+"/"+label+".question"
    properties2 = log_root+"/"+label+".properties"
    shutil.copyfile(input_file,input2)
    shutil.copyfile(question_file,question2)
    shutil.copyfile(properties_file,properties2)
    return load_hit_helper(label,input2,question2,properties2, comment)
    
def get_results(label = None):
    label = label or get_last_label()
    label = str(label)
    successfile = log_root+"/"+label+".success"
    resultsfile = log_root+"/"+label+".results"
    st = "getResults -successfile "+successfile+" -outputfile "+resultsfile
    text = tools.my_run(st,turk_root)
    my_log("[GET RESULTS] "+st+"\nLABEL: "+label+"\n"+text)   
    return text

def server_to_shortcut(label="test"):
    url="http://65.215.1.20/faces/add_shortcut.py?"+urllib.urlencode([("name",label)])
    f=tools.my_url_open(url)
    r = f.read().strip()
    return r

#buggy -- doesn't handle very large shortcuts :(
def shortcut_to_server(contents):
    url = "http://65.215.1.20/faces/add_shortcut.py?"
    url += urllib.urlencode([("contents",contents)])
    f=tools.my_url_open(url)
    r = f.read().strip()
    assert server_to_shortcut(r).strip().splitlines()==contents.strip().splitlines()
    return r


def input_shortcutifier(inp):
    ilist = inp.split("\n")
    for i in range(len(ilist)):
        if len(ilist[i])>200: #create shortcut
            r = shortcut_to_server(ilist[i])
            ilist[i]="shortCut"+r
    return string.join(ilist,'\n').strip()


def load_external_hit(url="http://65.215.1.20/faces/simp_sim3.py",assignments=1,input="1",title="A nice HIT",description="Please help with our AI task",reward="0.15",duration=900,autoapproval=259200,approvalrate=95,height=500,keywords="image, similarity",numapproved=48,comment=None):    
    ell = locals()
    label = get_next_label()
    input2 = log_root+"/"+label+".input"
    question2 = log_root+"/"+label+".question"
    properties2 = log_root+"/"+label+".properties"
    itmpl=tools.my_read(input_template)
    qtmpl=tools.my_read(question_template)
    ptmpl=tools.my_read(properties_template)
    st = string.Template(itmpl).substitute(ell)
    tools.my_write(input2,input_shortcutifier(st))
    st = string.Template(qtmpl).substitute(ell)
    tools.my_write(question2,st)
    st = string.Template(ptmpl).substitute(ell)
    tools.my_write(properties2,st)
    return load_hit_helper(label,input2,question2,properties2, comment)
    
#delete/expire the hits that were created!
def oops(label=None):
    if label==None:
        label=get_last_label()
    st = "deleteHits -successfile "+log_root+"/"+label+".success -force -approve -expire"
    text = tools.my_run(st,turk_root).strip()    
    my_log("[DELETE] "+st+"\n"+text+"\n")
    return text


def trips2mat(trips,n):
    res = zeros((n,n))
    for (x,y,z,wid) in trips:
        res[x][y] = res[x][y]-1
        res[x][z] = res[x][z]+1
        res[y][x] = res[y][x]-1
        res[z][x] = res[z][x]+1
    return res

def trips2mat3(trips,n):
    res = {}
    for (x,y,z,wid) in trips:
        t = (x,y,z)
        if t in res:
            res[t]=res[t]+1
        else:
            res[(x,z,y)]=0 # this makes sure that if (x,y,z) is in the hash so is (x,z,y)
            res[t]=1
#    for x in range(n):
#        for y in range(n):
#            for z in range(y):
#                if res[x][y][z]!=0 or res[x][z][y]!=0:
#                    a = res[x][y][z]
#                    b = res[x][z][y]
#                    res[x][y][z] = (a-b)/(a+b)
#                    res[x][z][y] = (b-a)/(a+b)
    return res

def downsample_trips(trips):
# changes all ids to {0,1,2,...,n}
# returns the trips, the map {}, and the list []
    res = []
    id_map = {}
    ids = []
    i=0
    for (x,y,z,wid) in trips:
        for v in [x,y,z]:
            if v not in ids:
                id_map[v]=i
                ids.append(v)
                i+=1
        res.append((id_map[x],id_map[y],id_map[z],wid))
    return (res,id_map,ids)
    

def score_trips(trips):
    new_trips, id_map, ids = downsample_trips(trips)
    n = len(ids)
    print "# ids",n
    c = {}
    for (x,y,z,wid) in trips:
        if wid not in c:
            c[wid]=1
        else:
            c[wid]+=1
    M3 = trips2mat3(trips,n)
    h3 = {}
    h4 = {}
    for i in c:
        h3[i]=0
        h4[i] = []
    for (x,y,z,wid) in trips:
        h3[wid]+=(M3[(x,y,z)]-1.-M3[(x,z,y)])/(c[wid]*(M3[(x,y,z)]-1.+M3[(x,z,y)]))
        h4[wid].append((M3[(x,y,z)]-1.-M3[(x,z,y)])/((M3[(x,y,z)]-1.+M3[(x,z,y)])))
    return (c,h3,h4)
    
def split_trips(target_trips,batch_size,gold_size):
    ids = {}
    for (a,b,c) in target_trips:
#        if a==b or a==c or b==c:
#            print "Warning: do not support (x,x,y) trips!!!"
        ids[a]=ids[b]=ids[c]=0
    ids = ids.keys()
    #first split the triples into groups of roughly equal size=batch_size
    n = len(target_trips)
    m = (n+batch_size-1)/batch_size # number of hits
    batch_size2 = (n+m-1)/m # max number comparisons per hit
    x =target_trips[:]
    for i in range(len(x)):
        (a,b,c) = x[i]
        if b>c:
            x[i]=(a,c,b)
    counts = {}
    for t in x:
        if t not in counts:
            counts[t]=0
        counts[t]+=1
    mymax = max(counts.values())
    if mymax>m:
        print "Invalid triples.  I am creatinging",m,"hits but I have ",mymax,"occurences of a triple."        
        assert False
    random.shuffle(x)
    res = [ [] for i in range(m) ]
    while x:
        a = x.pop()
        while True:
            i = random.randint(0,m-1)
            if a not in res[i]:
                if len(res[i])==batch_size2:
                    x.append(res[i].pop(random.randint(0,len(res[i])-1)))
                res[i].append(a)
                break
    for i in range(m):
        l = batch_size-len(res[i])
        for j in range(l):
            res[i].append(random.choice(target_trips))
    #fill in each hit with gold_size obvious comparisons of the form (x,x,y)
    for i in range(m):
        while len(res[i])<gold_size+batch_size:
            random.shuffle(ids)
            res[i].append((ids[0],ids[0],ids[1]))
    return res

#helper for results2trips:
def match(c,l):
    n = len(c)
    if n*5!=len(l)*3: 
        print "* Mismatch in length"
        print n, len(l)
        return False
    cd  = {}
    for i in range(n/3):
        r = []
        for j in range(3):
            r.append(int(c[3*i+j]))
        r = tuple(r)
        (u,v,w)=r
        if v>w:
            r = (u,w,v) 
        if r in cd:
            cd[r]+=1
        else:
            cd[r]=1
    for i in range(n/3):        
        r = []
        for j in range(3):
            r.append(int(l[5*i+j]))
        r = tuple(r)
        (u,v,w)=r
        if v>w:
            r = (u,w,v)            
        if r not in cd or cd[r]==0:
            print c,l
            print r
            print "* Mismatch in answer"
            return False
        cd[r]-=1
    return True

def results2tripsplus(label = None):
    label = label or get_last_label()
    file = open(log_root+"/"+label+".results","r")
    blah = csv.DictReader(file,delimiter='\t')
    trips = []
    mismatch = []
    for r in blah:
        wid = r['workerid']
        hid = r['hitid']
        challenge = r['annotation']
        if challenge[:8] == "shortCut":
            challenge = server_to_shortcut(challenge[8:])
        challenge = challenge.split("_")
        if 'Answer.res' in r and r['Answer.res']!=None and r['Answer.res']!="":
            li = r['Answer.res'].split("_")
    #        if len(r['Answer.comment']>10):
    #            print r['Answer.comment']
            if challenge[0]!=li[0]:
                print "REALLY STRANGE: challenge database mismatch:",challenge[0],li[0]
                print challenge
                print li
                mismatch.append(r['hitid'])
            else:
                if match(challenge[1:],li[1:]):
                    n = (len(li)-1)/5
                    li2 = [tuple(li[5*i+1:5*i+6]) for i in range(n)]
                    li3 = [((a,b,c,e) if d=='0' else (a,c,b,e)) for (a,b,c,d,e) in li2]
                    trips += [(int(a),int(b),int(c),int(e)*0.001,wid,hid) for (a,b,c,e) in li3]
                else:
                    mismatch.append(r['hitid'])
    file.close()
    return trips, mismatch


def reject_work(wids,label=None):
    label = label or get_last_label()
    file = open(log_root+"/"+label+".results","r")
    blah = csv.DictReader(file,delimiter='\t')
    aids = []
    for r in blah:
        wid = r['workerid']
        if wid in wids:
            aids.append(r['assignmentid'])       
    file.close()
    ttext = ""
    for aid in aids:
        st = "rejectWork -assignment "+aid+' -force'
        text = tools.my_run(st,turk_root).strip()    
        my_log("[REJECT WORK]"+st+text+"\n")
        ttext+=st+"\n"+text+"\n"
    return ttext


def redo_work(wids=[],hitids=[],label=None):
    label = label or get_last_label()
    file = open(log_root+"/"+label+".results","r")
    blah = csv.DictReader(file,delimiter='\t')
    st = "hitid\thittypeid\n"
    for r in blah:
        wid = r['workerid']
        if r['hitid'] in hitids:
            st+=r['hitid']+"\t"+r['hittypeid']+"\n"
            hitids.remove(r['hitid'])
        else:
            if wid in wids:
                st+=r['hihttp://www.mturk.com/mturk/preview?groupId=1DS91QNJYJ9DKY1BZYKGZ13YD5OGVLtid']+"\t"+r['hittypeid']+"\n"
        
    file.close()
    sfname = log_root+"/"+label+"_temp.success"
    tools.my_write(sfname,st)
    st = "extendHITs -assignments 1 -hours 24 -successfile " + sfname
    text = tools.my_run(st,turk_root).strip()    
    my_log("[EXTEND_HITS]"+st+text+"\n")
    return st+"\n"+text+"\n"


def get_bad_wids(tripsplus):
    widscores = {}
    for (x,y,z,e,wid,hid) in tripsplus:
        if wid not in widscores:
            widscores[wid]=(0,0)
        (a,b) = widscores[wid]
        if x==y:
            widscores[wid]=(a+1,b)
        if x==z:
            assert x!=y
            widscores[wid]=(a,b+1)
    bad_wids = []
    really_bad_wids = []
    for wid in widscores:
        s=widscores[wid][1]*1.0/(widscores[wid][0]+widscores[wid][1])
#        widscores[wid]=s
        if s>0.11:
            bad_wids.append(wid)
        if s>0.25:
            really_bad_wids.append(wid)
#    print widscores
#    global v
#    v= widscores.values()
    if len(really_bad_wids)>0:
        f = open(recent_bad_work_file,"a")
        for wid in really_bad_wids:
            hids = []
            for (x,y,z,e,wid2,hid) in tripsplus:
                if wid2==wid:
                    if hid not in hids:
                        hids.append(hid)
                        f.write(wid+"\t"+hid+"\n");
        f.close()
    return bad_wids, really_bad_wids

    
    

def check_results(label=None,outfile=None,init_trips=None):
    g = get_results(label)
    trips,mis = results2tripsplus(label)
    bad_wids, really_bad_wids = get_bad_wids(trips)
    print len(bad_wids),"bad workers and ",len(really_bad_wids),"really bad workers"
    amdone= (g.find("100%")!=-1)
    if amdone:
        hitids = {}
        for i in mis:
            hitids[i]=0
        for (a,b,c,e,wid,hid) in trips:
            hitids[hid]=0
        for (a,b,c,e,wid,hid) in trips:
            if wid not in bad_wids:
                hitids[hid]+=1
        redo = []
        for hid in hitids:
            if hitids[hid]==0:
                redo.append(hid)
#        if len(redo)>0:
#            amdone = False
#            print "About to redo",len(redo),"hits."
#            print "You have 10 seconds to kill job"
#            time.sleep(10)
#            redo_work(hitids = redo,label = label)
    if outfile!=None:
        assert init_trips!=None
        t = []
        for (a,b,c,e,wid,hid) in trips:
            if wid not in bad_wids and a!=b and a!=c:
                t.append((a,b,c,e))
        random.shuffle(t)
        t2 = []
        
        s = ""
        for (a,b,c,e) in t:
            s+=str(a)+" "+str(b)+" "+str(c)+" "+str(e)+"\n"
        tools.my_write(outfile,s)

    return amdone, really_bad_wids

def check_til_done(label=None,out_file=None,init_trips=None):
    s=120
    print "Getting results."
    while True:
        done, really_bad_wids = check_results(label,out_file,init_trips)
        if done:
            break
        print "Not done. Waiting ",int(s/60)," minutes...."
        time.sleep(s)
        s+=60
        print "Getting results."
    if len(really_bad_wids)>0:
        reject_work(really_bad_wids,label)


#g = get_results()
