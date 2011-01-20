# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 23:52:53 2010

@author: adum
"""

import os
from manips import *
from boost_class import *
from numpy import *
import tkFileDialog
import Pmw
from data import *
import tkSimpleDialog
import types
import pickle    
from logistic_regression import *
from simple_SVM import *
from random import *


#
#
#d2 = Generic()
#d2.po = []
#d2.xscroll = 0
#d2.tags = []
#d2.req = []
#d2.po = []
#d2.ne = []
#d2.n = 26
#d2.un = range(26)
#d2.mf = 1
#d2.hf = 1
#d2.locs = ['c:/vision/calibrialpha/calibri-'+chr(97+i)+'.png' for i in range(26)]
#d2.locs
#d2.exc  = []
#d2.click_count = 0
#d2.autolearn  = 0
#d2.M = M5


im_height =  100 # The actual height of images
nh_param = 90 # The height of images for spacing
nw_param = 80 # The width of images for spacing


data_handle = 0

def safe_remove(li,x):
    if x in li:
        li.remove(x)

def load_image(file_name): 
    # check for resized file -- if exists use it otherwise create one
    thumb = file_name[:-4]+"_mythumb.ppm"
    if os.path.exists(thumb):
        try:
            im = Tkinter.PhotoImage(file=thumb)
        except:
            print "*** Couldn't load",thumb
        else:        
            if im.height()==im_height:
                return im
    im = Image.open(file_name)
    im = im.resize((im.size[0]*im_height/im.size[1],im_height))    
    try:
        im.save(thumb)
        print "Writing image file",thumb
    except:
        print "*** Couldn't save",thumb
    im2 = ImageTk.PhotoImage(im)    
    return im2
    
#class ScrolledImageStore(Tkinter.Frame):
#    def __init__(self, orient,w,h):
#        Tkinter.Frame.__init__(self, parent)
#        self.pack(expand=Tkinter.YES, fill=Tkinter.BOTH)                  
#        canv = Tkinter.Canvas(self, bg='black', relief=Tkinter.SUNKEN)
#        canv.config(width=w, height=h)                
#        canv.config(scrollregion=(0,0,300, 1000))         
#        canv.config(highlightthickness=0)                 
#
#        sbar = Tkinter.Scrollbar(self)
#        sbar.config(command=canv.yview)                   
#        canv.config(yscrollcommand=sbar.set)              
#        sbar.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)                     
#        canv.pack(side=Tkinter.LEFT, expand=Tkinter.YES, fill=Tkinter.BOTH)       
#
#        for i in range(10):
#            canv.create_text(150, 50+(i*100), text='spam'+str(i), fill='beige')
#        canv.bind('<Double-1>', self.onDoubleClick)       # set event handler
#        self.canvas = canv
#    def onDoubleClick(self, event):                  
#        print event.x, event.y
#        print self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
    
 

class StoreTagDlg(tkSimpleDialog.Dialog):
    def __init__(self, parent, li):
        self.li = li
        tkSimpleDialog.Dialog.__init__(self,parent,title="Tag")
    def body(self, master):    
        self.name = Pmw.ComboBox(master,dropdown=0,label_text="Tag name:",labelpos='nw',scrolledlist_items = self.li)
        self.name.pack()
        return self.name._entryWidget
    def apply(self):
        self.result = self.name.get()

class LoadTagDlg(tkSimpleDialog.Dialog):
    def __init__(self, parent, li):
        self.li = li
        assert(li!=[])
        tkSimpleDialog.Dialog.__init__(self,parent,title="Load tag")
    def body(self, master):    
        self.name = Pmw.ScrolledListBox(master,label_text="Tag name:",labelpos='nw',items = self.li, dblclickcommand=self.ok)
        self.name.setvalue(self.li[-1])
        self.name.pack()
        return self.name._listbox
    def apply(self):
        if self.name.getvalue()!=[]:
            self.result = self.name.getvalue()[0]


class ShowTagDlg(tkSimpleDialog.Dialog):
    def __init__(self, parent, li, li0, titl):
        self.li = li
        self.li0 = li0
        assert(li!=[])
        tkSimpleDialog.Dialog.__init__(self,parent,title=titl)
    def body(self, master):    
        self.names = Pmw.ScrolledListBox(master,label_text="Tags:",labelpos='nw',items = self.li)
        self.names.pack(side=Tkinter.LEFT)
        self.names._listbox.config(selectmode=Tkinter.MULTIPLE)
        self.names.setvalue(self.li0)        
        return self.names._listbox
    def apply(self):
        self.result = self.names.getvalue()




class ILearn(Tkinter.Frame, ):
    def __init__( self, master, data=None):
        print "Setting up ILearn..."
        self.master = master
        Tkinter.Frame.__init__(self,master)
        
        self.pack( expand = Tkinter.YES, fill = Tkinter.BOTH )
        self.master.title( "ILearn" )
        self.master.geometry( "+0+0" )

        self.base=""

        self.tag_region_width = 120
        self.tag_bar_width = 10

        window = Tkinter.Toplevel(self)
        # Get the screen's width and height.
        scrW = window.winfo_screenwidth()
        scrH = window.winfo_screenheight()
        w = scrW-20
        h= scrH-120
        self.h = h
        self.w = w
        self.nh = int(self.h/nh_param)-1
        self.nreg = self.nh
        self.ncols = (self.w-2*self.tag_region_width)/nw_param
        self.nunl = self.nh * self.ncols

        self.maxu=1
        self.minu=0


        self.f2 = Tkinter.Frame(self)
        self.f2.pack(side= Tkinter.TOP, fill=Tkinter.Y)

        Tkinter.Button(self.f2, bg="black",fg="white",text="Tag",command=self.store_tag_pos).pack(side=Tkinter.LEFT)
        Tkinter.Button(self.f2, bg="black",fg="white",text="Load Tag",command=self.load_tag_pos).pack(side=Tkinter.LEFT)

        self.counts_lab_po=Tkinter.Label(self.f2,text="",fg="red")
        self.counts_lab_po.pack(side=Tkinter.LEFT,padx=2)
        self.counts_lab_un=Tkinter.Label(self.f2,text="",fg="black")
        self.counts_lab_un.pack(side=Tkinter.LEFT,padx=2)
        self.counts_lab_ne=Tkinter.Label(self.f2,text="",fg="blue")
        self.counts_lab_ne.pack(side=Tkinter.LEFT,padx=2)

        Tkinter.Button(self.f2, bg="black",fg="white",text="Save Session",command=self.save,padx=0).pack(side=Tkinter.LEFT)
        loadbut = Tkinter.Button(self.f2, bg="black",fg="white",text="Load Session",command=self.load,padx=0)
        loadbut.pack(side=Tkinter.LEFT)
        Tkinter.Label(self.f2,text="").pack(side=Tkinter.LEFT,padx=10)
        Tkinter.Button(self.f2, bg="black",fg="white",text="Require tags",command=self.showtag,padx=0).pack(side=Tkinter.LEFT)
        Tkinter.Button(self.f2, bg="black",fg="white",text="Exclude tags",command=self.hidetag,padx=0).pack(side=Tkinter.LEFT)
        Tkinter.Button(self.f2, bg="black",fg="white",text="Delete tags",command=self.deltag,padx=0).pack(side=Tkinter.LEFT)
        
        
        Tkinter.Button(self.f2, bg="black",fg="white", text="Restart",command=self.restart).pack(side=Tkinter.LEFT)
        Tkinter.Button(self.f2, bg="yellow",fg="black", text="Learn",command=self.do_learn).pack(side=Tkinter.LEFT)
        Tkinter.Button(self.f2, bg="black",fg="white", text="CV",command=self.do_CV).pack(side=Tkinter.LEFT)
        
        Tkinter.Label(self.f2,text="").pack(side=Tkinter.LEFT,padx=10)
        
        self.click_count_lab=Tkinter.Label(self.f2,text="0")
        self.click_count_lab.pack(side=Tkinter.LEFT)

        self.autolearn = Tkinter.IntVar()
        Tkinter.Checkbutton(self.f2,text="Insta-learn",variable=self.autolearn).pack(side=Tkinter.LEFT)

        self.mf = Tkinter.IntVar()
        self.mf.set(1)
        self.mf_cb = Tkinter.Checkbutton(self.f2,text="Mach. feat.",variable=self.mf,state=Tkinter.DISABLED)
        self.mf_cb.pack(side=Tkinter.LEFT)

        self.hf = Tkinter.IntVar()
        self.hf.set(1)
        self.hf_cb=Tkinter.Checkbutton(self.f2,text="Human feat.",variable=self.hf,state=Tkinter.DISABLED)
        self.hf_cb.pack(side=Tkinter.LEFT)


        self.scale = Tkinter.Scale(self.f2, from_=1,to=1000,orient=Tkinter.HORIZONTAL)
        self.scale.pack(side=Tkinter.LEFT)
        self.scale.set(1000)

        self.learning_alg = Tkinter.StringVar()
        self.learning_alg.set("Boosting")
        Tkinter.OptionMenu(self.f2, self.learning_alg, "Linear SVM","Logistic regression","Boosting").pack(side=Tkinter.LEFT)
        
        self.click_count_lab=Tkinter.Label(self.f2,text="0")
        self.click_count_lab.pack(side=Tkinter.LEFT)

        Tkinter.Button(self.f2, bg="black",fg="white",text="Tag",command=self.store_tag_neg).pack(side=Tkinter.RIGHT)
        Tkinter.Button(self.f2, bg="black",fg="white",text="Load Tag",command=self.load_tag_neg).pack(side=Tkinter.RIGHT)



        self.back = "black"
        self.running = 0

        self.f3 = Tkinter.Frame(self)
        self.f3.pack(side=Tkinter.BOTTOM,fill=Tkinter.X)
        self.scrollbar = Tkinter.Scrollbar( self.f3, orient=Tkinter.HORIZONTAL )
        self.scrollbar.config( command = self.scroll )

        Tkinter.Button(self.f3, text="<<",command=self.LLLEFT).pack(side=Tkinter.LEFT)
        Tkinter.Button(self.f3, text=">>",command=self.RRRIGHT).pack(side=Tkinter.RIGHT)
        self.scrollbar.pack(fill=Tkinter.X,padx=self.tag_region_width-40)


        self.canvas = Tkinter.Canvas(self, width =w, height =h,relief =Tkinter.RIDGE, \
                             background = self.back, borderwidth =1)

      
        self.canvas.pack(side=Tkinter.BOTTOM)

        self.canvas.create_rectangle( 0,0, self.tag_region_width-self.tag_bar_width, self.h, tags = ("region","neg_region"), fill="red", outline="" )
        self.canvas.create_rectangle( self.tag_region_width-self.tag_bar_width, 0, self.tag_region_width, self.h, tags = ("bar","neg_bar"), fill="white", outline="" )


        self.canvas.create_rectangle( self.w-self.tag_region_width+self.tag_bar_width,0, self.w, self.h, tags = ("region","pos_region"), fill="blue", outline="" )
        self.canvas.create_rectangle( self.w-self.tag_region_width, 0, self.w-self.tag_region_width+self.tag_bar_width, self.h, tags = ("bar","pos_bar"), fill="white", outline="" )

        #create positive images
        x=int((self.tag_region_width-self.tag_bar_width)/2)
        for i in range(self.nreg):
            y = int((i+0.5)*float(self.h)/(self.nreg))
            self.canvas.create_image(x,y,tags=("im","pos:"+str(i))) #image =
        #create negative images
        x=self.w-int((self.tag_region_width-self.tag_bar_width)/2)
        for i in range(self.nreg):
            y = int((i+0.5)*float(self.h)/(self.nreg))
            self.canvas.create_image(x,y,tags=("im","neg:"+str(i))) #image =
        #create unlabeled images
        for i in range(self.nunl):
            a = i/self.nh
            b = i%self.nh
            x= int(self.tag_region_width + (a+1)*float(self.w-2*self.tag_region_width)/(self.ncols+1))
            y = int((b+0.5)*float(self.h)/(self.nh))
            self.canvas.create_image(x,y,tags=("im","unl:"+str(i))) #image =
        




    #    self.canvas.bind( "<B1-Motion>", self.move )

        # bind mouse dragging event to Canvas
#        self.canvas.bind( "<ButtonPress-1>", self.down )
#        self.canvas.bind( "<ButtonRelease-1>", self.up )
#        self.canvas.focus_set()

        master.bind("<Control-z>",self.load)
        master.bind("<Control-z>",self.undo)
        master.bind("<Control-l>",self.load)
        master.bind("<Control-s>",self.save)
        master.bind("<Return>",self.canvas_click)
        master.bind("<space>",self.canvas_click)
        self.canvas.tag_bind("region","<Button-1>",self.do_learn)
        self.canvas.tag_bind("bar","<ButtonPress-1>",self.grab_bar)
        self.canvas.tag_bind("bar","<ButtonRelease-1>",self.release_bar)
        self.canvas.tag_bind("im","<Button-1>",self.make_pos)
        self.canvas.tag_bind("im","<Button-3>",self.make_neg)
        self.canvas.tag_bind("im","<Enter>",self.over)
        self.canvas.tag_bind("im","<Leave>",self.out)



#start with z by default
        filename = "c:/temp/try1"
        print "Opening",filename  
        f=open(filename,"rb")
        data2=pickle.load(f)
#        data2=d2
        if hasattr(data2,"autolearn"):
            self.autolearn.set(data2.autolearn)
            self.mf.set(data2.mf)
            self.hf.set(data2.hf)
        f.close()
        print dir(data2)
        global data_handle
        data_handle = data2

        #print "tags",data2.tags
        self.go_start(data2)


#        self.go_start(data)
        self.focus_force()
        #self.canvas.after(100,self.tick)

    def LLLEFT(self):
        self.scroll("moveto","0")        
        
    def RRRIGHT(self):
        self.scroll("moveto","1")
        
    def scroll(self,x,y,z=None):
        cols = (len(self.data.un)+self.nh-1)/self.nh
        if cols==0:
            cols=1
            screen=0.95
        else:
            screen = min(float(self.ncols)/cols,0.95)
        if x=="moveto":
            y = float(y)
        else: 
            assert x=="scroll"
            a = self.scrollbar.get()[0]
            if z=="units":
                y = a+ int(y)*float(1)/cols
            else:
                assert z=="pages"
                y = a+ int(y)*float(self.ncols)/cols
        y=max(0,y)
        y = min(y,1.-screen)
        self.scrollbar.set(y,y+screen)
        self.data.xscroll = int(y*cols+0.000001)
        
        self.dispimages()
        
        
    def go_start(self,data):
        if data==None:
            data = Data()
            data.locs = []
            data.M= zeros((0,0))
# commented out 8/7/10
#           data.ids = []
            data.n = 0
        self.data = data
        self.n = self.data.n
        if not hasattr(data,"tags"):
            self.data.tags = []
            self.data.Mtag = []
        if not hasattr(data,"req"):
            self.data.req = []
            self.data.exc = []
        if not hasattr(data,"po"):
            self.data.po = []
            self.data.ne = []
            self.data.un = range(self.n)
            shuffle(self.data.un)
            
        if not hasattr(data,"click_count"):
            self.data.click_count = 0

        self.locs = data.locs
        self.X = normalize(array(data.M))
        if self.X.shape[1]==1256:
            self.hf.set(1)
            self.mf.set(1)
            self.mf_cb.config(state=Tkinter.NORMAL)
            self.hf_cb.config(state=Tkinter.NORMAL)
        else:
            print self.X.shape[1]
            if self.X.shape[1]==1001:
                self.mf.set(1)
                self.hf.set(0)
            else:
                self.hf.set(1)
                self.mf.set(0)
            self.mf_cb.config(state=Tkinter.DISABLED)
            self.hf_cb.config(state=Tkinter.DISABLED)
            
        print "Got",self.X.shape[1],"features."
        assert self.n == self.data.M.shape[0]
        
        
        #ids = vecs2dict.keys() #mix_list
#        u = lle_projected_data[:,0].tolist()
#        v = lle_projected_data[:,1].tolist()
        u = [random() for i in range(self.n)]
        v = [random() for i in range(self.n)]
        
        if self.n==0:
            minu=maxu=0
            minv=maxv=0
        else:
            minu = min(u)
            maxu = max(u)
            minv = min(v)
            maxv = max(v)
        if minv==maxv:
            maxv+=1
            minv-=1
        if minu==maxu:
            maxu+=1
            minu-=1
        cx = (minu+maxu)/2
        cy = (minv+maxv)/2
        wx = (maxu-minu)*0.50
        wy = (maxv-minv)*0.50

        
        self.u = u
        self.v = v

        self.over_what = False

        self.ims = []
        print "Loading/resizing",self.n,"images..."
        for i in range(self.n):
                self.ims.append(load_image(self.locs[i]))
        print "... done"
        #self.canvas.tag_bind(Tkinter.ALL,"<ButtonPress-1>",self.over)

        if not hasattr(data,"xscroll"):
            data.xscroll = 0
        self.scroll("moveto","0")
        self.dispimages()


    def restart(self):
        data = self.data
        data.req = []
        data.exc = []
        data.po = []
        data.ne = []
        data.un = range(self.n)
        data.click_count = 0
        shuffle(data.un)
        self.scroll("moveto","0")
        self.dispimages()

    def store_tag_pos(self):
        data = self.data
        if len(data.po)==0:
            print "No positives, returning"
            return
        d = StoreTagDlg(self,data.tags)
        tag = d.result
        if tag=="" or tag == None:
            return
        print "Storing tag", tag
        if tag in data.tags:
            idx = data.tags.index(tag)
            for i in range(data.Mtag.shape[0]):
                data.Mtag[i,idx]=0
        else:
            if len(data.tags)==0:
                idx = 0
                data.Mtag = zeros((self.n,1),dtype="uint8")
            else:
                idx = data.Mtag.shape[1]
                data.Mtag = c_[data.Mtag,zeros((self.n,1),dtype="uint8")]
            data.tags.append(tag)
        for i in data.po:
            data.Mtag[i,idx]=1

    def store_tag_neg(self):
        data = self.data
        if len(data.ne)==0:
            print "No negatives, returning"
            return
        d = StoreTagDlg(self,data.tags)
        tag = d.result
        if tag=="" or tag == None:
            return
        print "Storing tag", tag
        if tag in data.tags:
            idx = data.tags.index(tag)
            for i in range(data.Mtag.shape[0]):
                data.Mtag[i,idx]=0
        else:
            if len(data.tags)==0:
                idx = 0
                data.Mtag = zeros((self.n,1),dtype="uint8")
            else:
                idx = data.Mtag.shape[1]
                data.Mtag = c_[data.Mtag,zeros((self.n,1),dtype="uint8")]
            data.tags.append(tag)
        for i in data.ne:
            data.Mtag[i,idx]=1

    def load_tag_pos(self):
        data = self.data
        if data.tags==[]:
            return
        d = LoadTagDlg(self,data.tags)
        tag = d.result
        if tag=="" or tag==None or tag not in data.tags:
            return
        print "Loading tag",tag
        idx = data.tags.index(tag)
        data.un.extend(data.po)
        data.po=[]
        for i in range(self.n):
            if data.Mtag[i,idx]==1:
                safe_remove(self.data.ne,i)
                safe_remove(self.data.un,i)
                self.data.po.append(i)
        shuffle(self.data.po)
        self.remove_blanks()
        self.compute_hidden()
        self.scroll("scroll","0","units")
        self.dispimages()
        
    def load_tag_neg(self):
        data = self.data
        if data.tags==[]:
            return
        d = LoadTagDlg(self,data.tags)
        tag = d.result
        if tag=="" or tag==None or tag not in data.tags:
            return
        print "Loading tag",tag
        idx = data.tags.index(tag)
        data.un.extend(data.ne)
        data.ne=[]
        for i in range(self.n):
            if data.Mtag[i,idx]==1:
                safe_remove(self.data.po,i)
                safe_remove(self.data.un,i)
                self.data.ne.append(i)
        shuffle(self.data.ne)
        self.remove_blanks()
        self.compute_hidden()
        self.scroll("scroll","0","units")
        self.dispimages()
        
    def canvas_click(self,event):
    
        if len(self.canvas.gettags(Tkinter.CURRENT))==0:
            print "*** CANVAS CLICK ***"
            self.do_learn()
        
    def load(self, event = None):
        filename = tkFileDialog.askopenfilename()    
        if filename=="":
            return
        print "Opening",filename  
        f=open(filename,"rb")
        data2=pickle.load(f)
        if hasattr(data2,"autolearn"):
            self.autolearn.set(data2.autolearn)
            self.mf.set(data2.mf)
            self.hf.set(data2.hf)
        f.close()
#        print dir(data2)

        #print "tags",data2.tags
        self.go_start(data2)


    def save(self, event=None):
        data = self.data

        filename = tkFileDialog.asksaveasfilename()    
        if filename=="":
            return
        print "Saving as:",filename  
        f=open(filename,"wb")
        data.autolearn = self.autolearn.get()
        data.hf = self.hf.get()
        data.mf = self.mf.get()
        pickle.dump(data,f,-1)
        print dir(data)
        f.close()
        

    def showtag(self):
        data = self.data
        if len(data.tags)==0:
            return
        d = ShowTagDlg(self,data.tags,data.req,"Require tags")
        if d.result==None:
            return
        data.req = list(d.result)
        self.compute_hidden()
        self.scroll("scroll","0","units")
        self.dispimages()
                
    def hidetag(self):
        data = self.data
        if len(data.tags)==0:
            return
        d = ShowTagDlg(self,data.tags,data.exc,"Exclude tags")
        if d.result==None:
            return
        data.exc = list(d.result)
        self.compute_hidden()
        self.scroll("scroll","0","units")
        self.dispimages()

    def deltag(self):
        data = self.data
        if len(data.tags)==0:
            return
        d = ShowTagDlg(self,data.tags,[],"Delete tags")
        if d.result==None:
            return
        if d.result == []:
            return
        idx = []
        for j in range(len(data.tags)):
            if data.tags[j] not in d.result:
                idx.append(j)
        data.Mtag = data.Mtag[:,idx]
        for j in d.result:
            if j in data.exc:
                data.exc.remove(j)
            if j in data.req:
                data.req.remove(j)
            data.tags.remove(j)
        self.compute_hidden()
        self.scroll("scroll","0","units")
        self.dispimages()
                
    def compute_hidden(self):
        data = self.data
        for i in range(self.n):
            s = True
            for j in data.exc:
                if data.Mtag[i,data.tags.index(j)]==1:
                    s = False
                    break
            if s:
                for j in data.req:
                    if data.Mtag[i,data.tags.index(j)]==0:
                        s = False
                        break
            if s==False:
                if i in data.po:
                    data.po.remove(i)
                if i in data.ne:
                    data.ne.remove(i)
                if i in data.un:
                    data.un.remove(i)
            else:
                if i not in self.data.po and i not in self.data.ne and i not in self.data.un:
                    self.data.un.append(i)
    

    def over(self,event):
        self.canvas.lift(Tkinter.CURRENT)
        st = self.canvas.itemcget(Tkinter.CURRENT,"tag")
        m=re.search('im:(\\S*)',st,re.S)
        if not m:
            self.over_what = False
        else:
            self.over_what = int(m.group(1))
        
        
        
    def out(self,event):
        self.canvas.lower(Tkinter.CURRENT)
        self.canvas.lift(Tkinter.CURRENT,"bar")
        self.over_what = False
        
    def grab_bar(self, event):
        event.widget.bind("<Motion>",self.move_bar)
        self.canvas.itemconfigure (Tkinter.CURRENT, fill ="yellow")
        
    def move_bar(self, event):
#        self.master.config (cursor ="hand1")
               
        event.widget.coords(Tkinter.CURRENT,event.x-self.tag_bar_width/8,0,event.x-self.tag_bar_width/8+self.tag_bar_width/4,self.h)
        x = event.x
        a = (self.ncols+1)*float(x-self.tag_region_width)/(self.w-2*self.tag_region_width)-1
        if 'pos_bar' in self.canvas.gettags(Tkinter.CURRENT):
            a = int(a)
        else:
            a = int(a+0.999999999)
        for j in range(self.nh):
            self.canvas.lift("unl:"+str(j+a*self.nh))
        self.canvas.lift("bar")
    
    def undo(self, event):
        if hasattr(self,"last_tag"):
            1
            self.dispimages()
        if self.autolearn.get():
            self.do_learn()
        
    def release_bar(self, event):
        data = self.data
        event.widget.unbind("<Motion>")
        self.canvas.itemconfigure (Tkinter.CURRENT, fill ="white")
        ux = self.screenu(event.x)
        x = event.x
        a = (self.ncols+1)*float(x-self.tag_region_width)/(self.w-2*self.tag_region_width)-1
        if 'pos_bar' in self.canvas.gettags(Tkinter.CURRENT):
            event.x = self.w-self.tag_region_width+self.tag_bar_width/2
            event.widget.coords(Tkinter.CURRENT,event.x-self.tag_bar_width/2,0,event.x-self.tag_bar_width/2+self.tag_bar_width,self.h)            
            a = int(a+0.999999999)
        else:
            a = int(a+0.999999999)
            event.x = self.tag_region_width-self.tag_bar_width/2            
            event.widget.coords(Tkinter.CURRENT,event.x-self.tag_bar_width/2,0,event.x-self.tag_bar_width/2+self.tag_bar_width,self.h)            
        a += data.xscroll 
        assert 'bar' in self.canvas.gettags(Tkinter.CURRENT)

        self.click_inc()
        if len(data.un)==0:
            return
   
        assert 'bar' in self.canvas.gettags(Tkinter.CURRENT)
        if 'pos_bar' in self.canvas.gettags(Tkinter.CURRENT):
            data.ne = data.un[a*self.nh:]+data.ne
            data.un = data.un[:a*self.nh]
        else:
            data.po = data.un[:a*self.nh]+data.po
            data.un = data.un[a*self.nh:]
            
        self.scroll("scroll","0","units")

        self.dispimages()
        if self.autolearn.get() and (len(data.po)>0 and len(data.ne)>0):
            self.do_learn()


    def frac2screenx(self, f):
        return int(self.tag_region_width+60+int(f*(self.w-2*self.tag_region_width-120)))
        
    def screenx2frac(self, x):
        frac = float(x-self.tag_region_width-60)/(self.w-2*self.tag_region_width-120)
        if frac<0:
            return 0.
        if frac>1:
            return 1.
        return frac

    def screenu(self, x):
        frac = self.screenx2frac(x)
        ans = (self.maxu-self.minu)*frac+self.minu
        return ans
        

    def helper1(self,i):
        if i==-1:
            return ""
        return self.ims[i]

    def dispimages(self):
        data = self.data
        self.counts_lab_po.config(text=str(len(data.po)))
        self.counts_lab_ne.config(text=str(len(data.ne)))
        self.counts_lab_un.config(text=str(len(data.un)))
        #first display pos/neg
        for i in range(self.nreg):
            if i<len(data.po):
                self.canvas.itemconfigure("pos:"+str(i),image=self.helper1(data.po[i]))
            else:
                self.canvas.itemconfigure("pos:"+str(i),image="")
            if i<len(data.ne):
                self.canvas.itemconfigure("neg:"+str(i),image=self.helper1(data.ne[i]))
            else:
                self.canvas.itemconfigure("neg:"+str(i),image="")
        for i in range(self.nunl):
            a = i+data.xscroll*self.nh
            if a>=0 and a<len(data.un):
                self.canvas.itemconfigure("unl:"+str(i),image=self.helper1(data.un[a]))
            else:
                self.canvas.itemconfigure("unl:"+str(i),image="")
                
    
    def get_im_num( self ):
        st = self.canvas.itemcget(Tkinter.CURRENT,"tag")
        m=re.search('pos:(\\S*)',st,re.S)
        if m:
            st = int(m.group(1))
            if st<len(self.data.po):
                return self.data.po[st]
            else:
                return -1
        else:
            m=re.search('neg:(\\S*)',st,re.S)
            if m:
                st = int(m.group(1))
                if st<len(self.data.ne):
                    return self.data.ne[st]
                else:
                    return -1
            else:
                m=re.search('unl:(\\S*)',st,re.S)
                assert m
                st = int(m.group(1))+self.data.xscroll*self.nh
                if st<len(self.data.un):
                   return self.data.un[st]
                else:
                    return -1
    
    def click_inc(self):
        self.data.click_count+=1
        self.click_count_lab.config(text=str(self.data.click_count))
    
    def make_pos( self, event ):
        data = self.data
        if self.running==1:
            self.do_interrupt( event)
        print "HOHO pos"
        self.canvas.lift(Tkinter.CURRENT)

        st = self.get_im_num()
        print "on ",st
        if st==-1:
            return

        #self.last_tag=(st,self.data.pos[st],self.data.neg[st],self.data.unl[st],self.u[st])
        self.click_inc()
        
        if st in data.po:
            i = data.po.index(st)
            data.po[i]=-1
            data.un.append(st)
        else:
            data.po.insert(0,st)
            if st in data.un:
                i = data.un.index(st)
                data.un[i]=-1
                print "UNLABELED",i
            else:
                i = data.ne.index(st)
                data.ne[i]=-1
        self.canvas.lift(Tkinter.CURRENT)
        
        self.dispimages()
                    
        if self.autolearn.get():
            self.do_learn()
        


    def make_neg( self, event ):
        data = self.data
        if self.running==1:
            self.do_interrupt( event)
        print "HOHO neg"
        self.canvas.lift(Tkinter.CURRENT)

        st = self.get_im_num()
        print "on ",st
        if st==-1:
            return
        self.click_inc()
    
        #self.last_tag=(st,self.data.pos[st],self.data.neg[st],self.data.unl[st],self.u[st])
        if st in data.ne:
            i = data.ne.index(st)
            data.ne[i]=-1
            data.un.append(st)
        else:
            data.ne.insert(0,st)
            if st in data.un:
                i = data.un.index(st)
                data.un[i]=-1
            else:
                i = data.po.index(st)
                data.po[i]=-1
        self.canvas.lift(Tkinter.CURRENT)

        self.dispimages()
                    
        if self.autolearn.get():
            self.do_learn()


#
#    def do_interrupt( self, event ):
#        st = self.canvas.itemcget(Tkinter.CURRENT,"tag")
#        m=re.search('im:(\\S*)',st,re.S)
#        if not m:
#            return
#        self.running = 0
#        i = int(m.group(1))
#        print "GOTCHA:", i
#        wvec = self.ws[self.count-1]
#        print wvec
#        print dot(self.X[i],wvec)
    def remove_blanks(self): #remove all occurrences of -1
        self.data.po[:] = [i for i in self.data.po if i != -1]
        self.data.ne[:] = [i for i in self.data.ne if i != -1]
        self.data.un[:] = [i for i in self.data.un if i != -1]

    def help_learn( self, train, test ):
        data = self.data
        hf = self.hf.get()
        mf = self.mf.get()
        la = self.learning_alg.get()
        #print (mf,hf),"FEATURES",self.X.shape
        tmpY = [(i in data.po)*2-1. for i in train]             
        if (mf == hf) or self.X.shape[1]!=1256:
            if data.tags!=[]:
                print "Learning with tags!"
                tmpX = hstack([2*data.Mtag[train]-1.,self.X[train]])
            else:
                tmpX = self.X[train]
            self.R=self.scale.get()
            print "Learning, R=",self.R, la
            if la=="Logistic regression":
                if data.tags!=[]:
                    tstX = hstack([2*data.Mtag[test]-1.,self.X[test]])
                else:
                    tstX = self.X[test]
                print "Training:",tmpX.shape[0]                
                lr = LogisticRegression(tmpX,tmpY,tstX,1.0/self.R)
                lr.train()
                print "Testing:",tstX.shape[0]
                u=lr.test_predictions()
            else:
                if la=="Linear SVM":
                    wvec = simple_SVM(tmpX,tmpY,self.R)
                else:
                    assert la=="Boosting"
                    wvec = adaboost_feats(tmpX,tmpY,self.R)
                print sorted(abs(wvec),reverse=True)[:10]
                if data.tags!=[]:
                    tmpX = hstack([2*data.Mtag[test]-1.,self.X[test]])
                else:
                    tmpX = self.X[test]
                u= dot(tmpX,wvec)
            assert nan not in u
        else:
            a = 255
            b = 1255
            if hf==1:
                print "Human Features"
                assert mf==0
                rang = range(0,a)
                rang.append(b) # the all 1's col
            else:
                print "Machine Features"
                assert mf==1
                rang = range(a,b+1)
            if data.tags!=[]:
                print "Learning with tags"
                tmpX = hstack([2*data.Mtag[train]-1.,self.X[train,:][:,rang]])
            else:
                tmpX = self.X[train,:][:,rang]
            self.R=self.scale.get()
            print "Learning, R=",self.R,la
            if la=="Logistic regression":
                if data.tags!=[]:
                    tstX = hstack([2*data.Mtag[test]-1.,self.X[test,:][:,rang]])
                else:
                    tstX = self.X[test,:][:,rang]
                print "Training:",tmpX.shape[0]
                lr = LogisticRegression(tmpX,tmpY,tstX,1.0/self.R)
                lr.train()
                print "Testing:",tstX.shape[0]
                u=lr.test_predictions()
            else:
                if la=="Linear SVM":
                    wvec = simple_SVM(tmpX,tmpY,self.R)
                else:
                    assert la=="Boosting"
                    wvec = adaboost_feats(tmpX,tmpY,self.R)
                print sorted(abs(wvec),reverse=True)[:10]
                if data.tags!=[]:
                    tmpX = hstack([2*data.Mtag[test]-1.,self.X[test,:][:,rang]])
                else:
                    tmpX = self.X[test][:,rang]
                u= dot(tmpX,wvec)
        return u



    def do_learn( self, _=None):
        self.remove_blanks()
        if not hasattr(self,"data") or len(self.data.po)==0 or len(self.data.ne)==0:
            self.dispimages()
            return
        print "Learning..."
        data = self.data
        u = self.help_learn( sorted(data.po+data.ne),data.un )
        idxs = argsort(-u) 

        data.un = [data.un[idxs[i]] for i in range(len(idxs))]
        self.dispimages()
        
    def do_CV(self, waste=None):
        k=5
        data = self.data
        self.remove_blanks()
        idxs = array(data.po+data.ne)
        shuffle(idxs)
        tmpY = array([(i in data.po)*2-1. for i in idxs])             
        m = len(idxs)
        res = 0
        for i in range(k):
            a = m*i/k
            b = m*(i+1)/k
            train = range(0,a)+range(b,m)
            test = range(a,b)
            test_labels = self.help_learn( idxs[train], idxs[test] )
            res += dot(sign(test_labels),tmpY[test])
        res = float(res+m)/(2*m)
        print res
        
    def tick( self ):
        i= choice(self.canvas.find_withtag("im"))
        self.canvas.lift(i)
        if self.over_what!=False:
            self.canvas.lift("im:"+str(self.over_what))
        self.canvas.after(100,self.tick)




root =Tkinter.Tk()
root.title ("Interactive Learning Demo")

#datar = load_exp_combined()
#datar.locs = [id2loc_combined(id) for id in datar.ids]
#print "GOT", datar.n

#datar = Data()
##datar.ids, datar.locs, datar.M = load_keycard_samp(5000)
#datar.ids, datar.locs, datar.M, datar.tags, datar.Mtag = load_hybrid_samp(5000)
#datar.n = len(datar.locs)

#ILearn(root,datar).mainloop()

ILearn(root).pack()
root.mainloop()

#root.wait_window()


#param = svm_parameter(kernel_type = LINEAR, C = 10)
