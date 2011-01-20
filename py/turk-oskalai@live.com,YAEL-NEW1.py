# -*- coding: utf-8 -*-
"""
Created on Sat May 22 14:39:14 2010

To see the ids of the 100 most popular people, check out:
http://65.215.1.20/faces/get_pic.py?tid=lfw_10322_13144_2194_10531_544_7615_12424_6244_8466_10483_244_6998_8853_4681_11600_6197_11311_2650_11546_11305_7350_1834_11657_2446_6100_1549_4731_7533_8041_7169_4504_715_4867_5606_7304_4959_4974_466_13027_9058_459_1686_6752_407_6179_7801_13132_7228_8087_11400_657_5204_12246_4795_9435_12814_8333_11865_816_5994_5554_5015_1007_3915_11126_12157_7084_694_12307_9528_5240_10108_8882_9896_3948_8222_3016_10030_12115_10553_8792_914_1809_9673_12705_6111_1210_6553_11241_6332_8080_6132_12730_5322_8458_11198_9408_9621_7186_5446
c:\vision\most_popular_100_ids_balanced.txt



@author: adum
"""

ce_root = "c:/vision"
turk_root = "c:/mturk/bin"
the_root = "c:/sim"
exp_root = the_root+"/turkexps"
log_root = exp_root+"/logs"
turk_log = log_root+"/turk.log"
input_template = exp_root+"/template.input"
question_template = exp_root+"/template.question"
properties_template = exp_root+"/template.properties"



batch_size = 50
reward = "0.15"

import tools
import time, urllib, urllib2
import xml.etree.ElementTree as etree
import os, shutil, string
import re
import monitor_workers
import random
from numpy import *
import datetime

def my_log(st):
    f = open(turk_log,"a")
    f.write("\n--------------------- "+str(datetime.datetime.now())+" ---------------------\n")
    print "--------------------- "+str(datetime.datetime.now())+" ---------------------"
    f.write(st)
    print st
    f.close()

def get_balance():
    text = tools.my_run("getbalance",turk_root).strip()
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
    return str(int(get_last_label())+1)

def load_hit_helper(label,input2, question2, properties2, comment):
    if comment!=None:
        fname = log_root+"/"+label+"_"+comment+".comment"
        tools.my_write(fname,"blah")
    st = "loadHITs -input "+input2+" -question "+question2+" -properties "+properties2+" -label "+label
    text = tools.my_run(st,turk_root)
    my_log("[LOAD HIT] "+st+"\nLABEL: "+label+"\n"+text)   
    shutil.move(turk_root+"/"+label+".success",log_root+"/"+label+".success")    
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



#buggy -- doesn't handle large files :(
def py_to_server(label="test",pycontents=None):
    if pycontents == None:
        pycontents = tools.my_read(exp_root+"/to_server.py")
    label=str(label)
    url = "http://65.215.1.20/faces/add_exp.py?"
    url += urllib.urlencode([("name",label),("contents",pycontents)])
    f=urllib2.urlopen(url)
    r = f.read().strip()
    assert r=="<html>SUCCESS</html>"
    return "http://65.215.1.20/faces/exps/"+label+".py"


def load_external_hit(url="http://65.215.1.20/faces/simp_sim1.py",pycontents=None,assignments=1,input="1",title="A nice HIT",description="Please help with our AI task",reward="0.15",duration=900,autoapproval=259200,approvalrate=95,height=500,keywords="image, similarity",numapproved=48,comment=None):    
    ell = locals()
    label = get_next_label()
    if url==None:
        assert False
        url = py_to_server(label,pycontents)
    input2 = log_root+"/"+label+".input"
    question2 = log_root+"/"+label+".question"
    properties2 = log_root+"/"+label+".properties"
    itmpl=tools.my_read(input_template)
    qtmpl=tools.my_read(question_template)
    ptmpl=tools.my_read(properties_template)
    st = string.Template(itmpl).substitute(ell)
    tools.my_write(input2,st)
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


def create_hits(trips_set,db,n):

    r = etree.Element("hitlist")
    for t in trips_set:
        head = etree.SubElement(r,"hit")
        etree.SubElement(head,"reward").text = reward
        etree.SubElement(head,"num_copies").text = str(n)
        etree.SubElement(head,"db_name").text = db
        data = etree.SubElement(head,"hit_data")
        for i in t:
            etree.SubElement(data,"triple").text = str(i)
    i = 1
    while True:
        fname = "c:/vision/hitset"+str(i)+".xml"
        if not os.path.exists(fname):
            break
        i+=1
    etree.ElementTree(r).write(fname)
    print "Created file: "+fname
    
#    f = open(block_list_xml,"w")
#    f.write("<blocklist>\n")
#    for wid in block_list+reject_list:
#        f.write("<workerID>"+wid+"</workerID>\n")
#    f.write("</blocklist>\n")
#    f.close()
#    print "Created file: "+block_list_xml

#    pipe =os.popen("ImageSimilarityMechanicalTurk.exe -create "+fname+" "+block_list_xml+" 2>&1",'r')
    text = tools.my_run("ImageSimilarityMechanicalTurk.exe -create "+fname,ce_root)
    print text

def check_hits():
    text2 = tools.my_run("ImageSimilarityMechanicalTurk.exe -check",ce_root)
    print text2
    m=re.search('(.*) out of (.*) are finished!',text2)
    assert m
    return m.group(1)==m.group(2)

@tools.print_timing
def wait_hit(max_time=1e21):
    t = time.time()
    delay = 30 
    while time.time()-t<max_time:
        if delay+time.time()-t>max_time:
            delay = max_time - (time.time()-t)
        time.sleep(delay)
        delay *=1.5
        pipe =os.popen("ImageSimilarityMechanicalTurk.exe -check 2>&1",'r')
        text2 = pipe.readlines()
        print text2
        sts2 = pipe.close()
        print sts2
        m=re.search('(.*) out of (.*) are finished!',text2[-1])
        assert m
        print text2[-1]
        if m.group(1)==m.group(2):
            return True
    return False
    
def xml2trips(xml_files,ignore_list = "default"):
    if ignore_list=="default":
        ignore_list=monitor_workers.ignore_list()
    if type(xml_files) is not list:
        xml_files = [xml_files]
    res = []
    ignored = 0
    for xml_file in xml_files:
        a = etree.parse(xml_file)
        b = a.find("hit_data")
        trips = []
        if not b:
            print "COULD NOT FIND hit_data"
            return
        for i in b.findall("triple"):
            trips.append(eval(i.text))
        b = a.find("answer")
        if not b:
            print "COULD NOT FIND answer"
            return   
        n = len(trips)
        for i in b.findall("assignment"):
            wid = i.find("workerID").text
            if wid in ignore_list:
                ignored+=1
                #print "Ignoring: ",wid
                continue
            li = eval(i.find("annotation").text)
            assert len(li)==n
            for k in range(n):
                (x,y,z) = trips[k]
                if li[k]:
                    res.append((x,y,z,wid))
                else:
                    res.append((x,z,y,wid))
    if ignored>0:
        print "Ignored ",ignored," assignments."
    return res
    
def xml2comments(xml_files,cheaters=0):
    #cheaters = 0 gets all comments, cheaters = -1 means no cheaters,
    # and cheaters = 1 means only cheaters
    if type(xml_files) is not list:
        xml_files = [xml_files]
    res = []
    ignored = 0
    for xml_file in xml_files:
        a = etree.parse(xml_file)
        b = a.find("answer")
        if not b:
            print "COULD NOT FIND answer"
            return   
        for i in b.findall("assignment"):
            wid = i.find("workerID").text

            if (cheaters==-1 and wid in monitor_workers.ignore_list()) or (cheaters==1 and wid not in monitor_workers.ignore_list()):
                ignored+=1
                #print "Ignoring: ",wid
                continue
            li = i.find("comment").text
            if li:
                li = li.strip()
                if li:
                    res.append((wid,li))
    if ignored>0:
        print "Ignored ",ignored," assignments."
    return res
    


def latest_trips(root=ce_root+"/workspace"):
    i=0
    while os.path.exists(root+"/Batch_%05d" % i):
        i+=1
    i-=1
    return batch_i(i,root)

def batch_i(i,root=ce_root+"/workspace"):
    res = []
    j = 0
    while os.path.exists(root+"/Batch_%05d/HIT_%05d.xml" % (i,j)):
        j+=1
    return [root+"/Batch_%05d/HIT_%05d.xml" % (i,k) for k in range(j)]


def load_idmap(filename="c:/vision/exp_000_test/idids.txt"):
    li=[eval(i) for i in open(filename).readlines()]
    res = {}
    a=0
    for i in li:
        if i not in res:
            res[i]=a
            a = a+1
    return res

def load_mapid(filename="c:/vision/exp_000_test/idids.txt"):
    return [eval(i) for i in open(filename).readlines()]



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
    
#-----------------------------------------
# Start Trip Magic
#-----------------------------------------
#This routine creates a bunch of triples. The idea is that some things are 
#tested on multiple workers.

base_threshold = 5 # if each trip is happening 4 times then we don't need to duplicate,
duplicity_m = 15 #otherwise, make sure each hit has duplicity_n queries, each running on
duplicity_k = 8 #duplicity_k HITs
assert duplicity_m < batch_size



def start_trip_magic(trips,db,n):
    random.shuffle(trips)
    ntrips = len(trips)
    if n>=base_threshold:
        bs = batch_size
        trips+=trips[:(bs-(ntrips%bs))%bs] #make an even multiple of bs trips
        ntrips = len(trips)
        assert ntrips%bs==0
        k = ntrips/bs
        #just break trips into blocks of batch_size
        trips_set = [ trips[i*bs:(i+1)*bs] for i in range(k) ]
    else:
        m = duplicity_m
        k = duplicity_k
        N = batch_size
        r = int(math.ceil(k*1.0/n))
        A = int(math.ceil(ntrips*1.0/(N-m*(1-1./r))))
        I = int(math.ceil(m*A*1.0)/r)
        assert I<ntrips
        #repeat the first I trips in about r HITs each
        repset = trips[:I]
        repset_leftovers = []
        trips_set = [ [] for i in range(A) ]
        for i in range(m):
            for j in range(A):
                success = False
                count = 0
                while not success:
                    for k in range(len(repset)):
                        if repset[k] not in trips_set[j] or count ==20:
                            trips_set[j].append(repset[k])
                            repset_leftovers.append(repset.pop(k))
                            success = True
                            break
                    if not success:
                        random.shuffle(repset_leftovers)
                        repset+=repset_leftovers
                        repset_leftovers=[]
                        count += 1
        for j in range(A):
            assert len(trips_set[j])==m
            while(len(trips_set[j])<N):
                if len(trips)==0:
                    trips += repset+repset_leftovers
                trips_set[j].append(trips.pop())
            random.shuffle(trips_set[j])
    return trips_set
    #turk_tools.create_hits(trips_set,db,n)

#get_balance()
