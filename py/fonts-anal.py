# -*- coding: utf-8 -*-
"""
Created on Wed Sep 22 23:30:10 2010

@author: adum
"""

import tools, turk, csv
from numpy import *
import matplotlib.pyplot as plt
import Tkinter
from PIL import Image, ImageTk
import random

#trip_file = "c:/sim/turkexps/fonts/fonts1.out"
trip_file = "c:/sim/fonts10000.out"

ids = []
id_locs = tools.my_read("c:/matlab/fonts/ids.txt").strip().split("\n")

txt = tools.my_read(trip_file).strip().split("\n")
txt2 = [l.split() for l in txt]
trips = [(int(l[0]),int(l[1]),int(l[2])) for l in txt2]
for t in trips:
    for i in t:
        if i not in ids:
            ids.append(i)

trips2 = [ (ids.index(a),ids.index(b),ids.index(c)) for (a,b,c) in trips]

n = len(ids)
print n




class Generic:
   pass


class PCA( Tkinter.Frame ):
    def __init__( self, data, (com1,com2)=(0,1) ):
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
        w=1500
        h=1000
        self.canvas = Tkinter.Canvas(self, width =w, height =h,relief =Tkinter.RIDGE, \
                             background = self.back, borderwidth =1)

      
        self.canvas.pack(side=Tkinter.RIGHT)
    
    #    self.canvas.bind( "<B1-Motion>", self.move )

        # bind mouse dragging event to Canvas
#        self.canvas.bind( "<ButtonPress-1>", self.down )
#        self.canvas.bind( "<ButtonRelease-1>", self.up )
#        self.canvas.focus_set()


#       self.canvas.create_oval( x1, y1, x2, y2, tag = "node", fill="white" )

#        u = lle_projected_data[:,0].tolist()
#        v = lle_projected_data[:,1].tolist()
        u = data.Vh[com1]
        v = data.Vh[com2]
        
        minu = min(u)
        maxu = max(u)
        minv = min(v)
        maxv = max(v)
        cx = (minu+maxu)/2
        cy = (minv+maxv)/2
        wx = (maxu-minu)*0.6 
        wy = (maxv-minv)*0.6

        self.ims = []
        
        for i in range(0,data.n):
           # print ids[i]
            im = tools.my_open_img(data.img_src[i],height=146,whiteout=False)
          
            
            self.ims.append(im)
            #print len(self.ims)
            self.canvas.create_image(int(w/2 + ((u[i]-cx)*w)/wx/2),int(h/2+((v[i]-cy)*h)/wy/2),image=self.ims[-1],tags=("id:"+str(i)))
        self.canvas.bind("<Motion>",self.go)
        self.canvas.after(100,self.tick)


    def go( self, event ):
        #print "HOHO"
        self.canvas.lower(Tkinter.CURRENT)
        
    def tick( self ):
        i= random.choice(self.canvas.find_withtag(Tkinter.ALL))
        self.canvas.lift(i)
        self.canvas.after(100,self.tick)

        
        
def go_PCA(com1=0,com2=1):
    data = Generic()
    data.n = n
    data.img_src = [ "C:/matlab/fonts/"+id_locs[ids[i]]  for i in range(data.n) ]
    data.M = zeros((data.n,data.n))
    for (a,b,c) in trips2:
        data.M[a,b]-=1
        data.M[a,c]+=1
        data.M[b,a]-=1
        data.M[c,a]+=1        
    tools.center_mat(data.M)
    [data.U,data.sss,data.Vh]=linalg.svd(data.M.T)
    PCA(data,(com1,com2)).mainloop()

go_PCA()