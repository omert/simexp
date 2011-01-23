# -*- coding: utf-8 -*-
"""
Created on Sat May 22 12:14:30 2010

@author: adum
"""

import os
import time, glob
import Tkinter
from PIL import Image, ImageTk
import urllib2, StringIO, shutil
from scipy.linalg import decomp

#compute the nearest PSD matrix of real symmetric x
def nearest_PSD(x):
    [T,U]=decomp.schur(x)
    return dot(dot(U,(T+abs(T))/2),U.T)

def uniqueify(lst): #remove duplicates
    res = []
    for i in range(len(lst)):
        if lst[i] not in res:
            res.append(lst[i])
    return res


def remove_comments(s):
    if type(s)==list:
        return [remove_comments(i) for i in s]
    if s.find("#")!=-1:
        return s[:s.index("#")].strip()
    return s.strip()

def save_matrix(M,filename):
    f = open(filename,"w")
    (m,n) = M.shape
    for i in range(m):
        for j in range(n):
            f.write(str(M[i][j])+" ")
        f.write("\n")
    f.close()

def my_run(st,dir = None):
    if dir != None:
        os.chdir(dir)
    if os.name == 'nt':
        pipe =os.popen(st+" 2>&1",'r')
    else:    
        pipe =os.popen("./"+st+" 2>&1",'r')
    text = pipe.read()
    sts = pipe.close()
    if sts:
            print "Exited with STATUS "+str(sts)+" on executing '"+st+"'"
    return text
    
def my_read(file):
    f = open(file,"r")
    st = f.read()
    f.close()
    return st

def my_write(file,contents):
    f = open(file,"w")
    st = f.write(contents)
    f.close()

def sub_col_mean(mat):
    (m,n)=mat.shape
    col_avg = [mat[:,j].sum()/m for j in range(n)]
    mat-=col_avg
    
def center_mat(mat):
    (m,n)=mat.shape
    row_avg = [mat[i].sum()/n for i in range(m)]
    col_avg = [mat[:,j].sum()/m for j in range(n)]
    tot = mat.sum()/(m*n)
    for i in range(m):
        for j in range(n):
            mat[i,j] = mat[i,j] + tot - row_avg[i] - col_avg[j]


def normalize(x,mag = 1.):
    r = sqrt(dot(x,x))
    if r!=0:
        x*= mag/r
    else:
        print "** [TOOLS] Alert: attempting to normalize 0 vector"

class SimpleDisplay( Tkinter.Frame ):
    def __init__( self, w = 500, h=1000 ):
        Tkinter.Frame.__init__( self )
        self.pack( expand = Tkinter.YES, fill = Tkinter.BOTH )
        self.master.title( "FaceX" )
        self.master.geometry( "+0+0" )

        self.base=""

        self.f2 = Tkinter.Frame(self)
        self.f2.pack(side= Tkinter.LEFT  , fill=Tkinter.Y)
        

#        self.thumbs_up = PhotoImage(file="c:/temp/thumbsup.gif")
#        self.thumbs_down = PhotoImage(file="c:/temp/thumbsdown.gif")
        
        self.back = "#%02x%02x%02x" % (255, 255, 255)

        # create Canvas component
        self.canvas = Tkinter.Canvas(self, width =w, height =h,relief =Tkinter.RIDGE, \
                             background = self.back, borderwidth =1)

      
        self.canvas.pack(side=Tkinter.RIGHT)
        self.canvas.create_line(w/2,0,w/2,h)
        self.w  = w
        self.h = h
        
    def go(self,imlist):
        w = self.w
        h= self.h
        self.imlist = imlist
        self.ims, u, v = zip(*imlist)
        minu = min(u)
        maxu = max(max(u),-minu)
        minu=-maxu
        minv = min(v)
        maxv = max(v)
        cx = (minu+maxu)/2
        cy = (minv+maxv)/2
        wx = (maxu-minu)*0.6 
        wy = (maxv-minv)*0.55
        
        for i in range(len(self.ims)):
            self.canvas.create_image(int(w/2 + ((u[i]-cx)*w)/wx/2),int(h/2+((v[i]-cy)*h)/wy/2),image=self.ims[i],tags=("id:"+str(i)))
        


#returns a random regular bipartite graph with m nodes on left,
#n nodes on right, and degree d on the left.  If n | dm then the degree on
#the right is exactly n/(md) otherwise it's as close as possible
def reg_bipartite(m,n,d):
    x = range(n)
    random.shuffle(x)
    x=x[:(m*d)%n]
    x += range(n)*((m*d)/n)
    random.shuffle(x)
    res = [ [] for i in range(m) ]
    while x:
        a = x.pop()
        while True:
            i = random.randint(0,m)
            if a not in res[i]:
                if len(res[i])==d:
                    x.append(res[i].pop(random.randint(0,len(res[i]))))
                res[i].append(a)
                break
    return res

def my_url_open(url):
    for i in range(40):
        try:
            f=urllib2.urlopen(url)
            return f
        except:
            print "Retry",i,": Error reading url",url[:90]
            time.sleep(3)
    return None

def my_open_img(file_or_url,height=None,whiteout=False):
    if file_or_url[:4]=="http":
        img = my_url_open(file_or_url).read()
        im = Image.open(StringIO.StringIO(img))
    else:
        im = Image.open(file_or_url)
    try:
        if height!=None:
            im = im.resize(((im.size[0]*height)/im.size[1],height))
        if whiteout:
        ## now make the white invisible (if you want!)
            im = im.convert('RGBA')
            source = im.split()                 # split the image into layers
            mask = im.point(lambda i: i < 240)  # kluge
            source[3].paste(mask)               # put mask into the alpha channel
            im = Image.merge(im.mode, source)   # build a new multiband image

        im.verify()
    except:
        print "*** Error verifying image",file_or_url

    return ImageTk.PhotoImage(im)
    
def my_open_img2(file_or_url,height=None,whiteout=False):
    if file_or_url[:4]=="http":
        img = my_url_open(file_or_url).read()
        im = Image.open(StringIO.StringIO(img))
    else:
        im = Image.open(file_or_url)
    try:
        if height!=None:
            im = im.resize(((im.size[0]*height)/im.size[1],height))
        if whiteout:
        ## now make the white invisible (if you want!)
            im = im.convert('RGBA')
            source = im.split()                 # split the image into layers
            mask = im.point(lambda i: i < 240)  # kluge
            source[3].paste(mask)               # put mask into the alpha channel
            im = Image.merge(im.mode, source)   # build a new multiband image

        im.verify()
    except:
        print "*** Error verifying image",file_or_url

    return im
#not working:!
def flatten(l):
    if isinstance(l,list):
        return sum(map(flatten,l))
    else:
        return l

def print_timing(func):    
    def wrapper(*arg):
        t1 = time.time()
        res = func(*arg)
        t2 = time.time()
        print '%s took %0.1f secs' % (func.func_name, t2-t1)
        return res
    return wrapper # declare the @ decorator just before the function, invokes print_timing()

@print_timing
#this routine shows how we time routines
def test_timing(n = 10):
    time.sleep(n)
    
def copy_all_images(root,dest):
    lst = glob.glob(root+'\\*.jpg')
    lst += glob.glob(root+'\\*.jpg')
    lst += glob.glob(root+'\\*\\*.jpg')
    lst += glob.glob(root+'\\*\\*\\*.jpg')
    lst += glob.glob(root+'\\*\\*\\*\\*.jpg')
    lst += glob.glob(root+'\\*\\*\\*\\*\\*.jpg')
    for t in lst:
        fname = t.split("\\")[-1]
        shutil.copyfile(t,dest+"\\"+fname)
    print lst
    
def count_unique_guys(filename):
    f = my_read(filename).splitlines()
    a=[]
    for l in f:
        if ":" in l:
            a+= l.split(":")[1].split()
    b = {}
    for i in a:
        if i in b:
            b[i]+=1
        else:
            b[i]=1
    return b           
    
def uniqueify(lst):
    a = []
    for b in lst:
        if b not in a:
            a.append(b)
    return a
    
def my_save_web_image(url,filename):
   f = open(filename,"wb") 
   f.write(my_url_open(url).read())
   f.close()
