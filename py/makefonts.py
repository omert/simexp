# -*- coding: utf-8 -*-
"""
Created on Wed Oct 06 08:08:39 2010

@author: adum
"""

import tools, numpy
import random


coords = tools.my_read("c:/sim/tsp/fonts.txt").strip().splitlines()
M = []
for x in coords:
    (a,b,c)=x.split()
    M.append((float(a),float(b),float(c)))
    
print len(M)


def draw_fonts(f,title):
    res="<table width=300 border=1>"
    res+="<tr><td><u>"+title+"</u></td></tr>"
    for i in f:
        res+='<tr><td><font face="'+i+'">'+i+'</font></td></tr>\n'
    res+="</table>\n"
    return res

def font_dist(i,j):
#    if i==5:
#        return 0
#    if i>5:
#        i=i-1
    (a,b,c) = M[i]
    (d,e,f) = M[j]
    return (i-j)**2
    return ((a-d)**2 + (b-e)**2+(c-f)**2)


def TSPLIB_format():
    l = []
    n = 227
    for i in range(n):
        for j in range(i):
            l.append(font_dist(i,j))
    f = open("c:/sim/tsp/MyFonts.tsp","w")
    print >>f, """NAME: MyFonts
TYPE: TSP
COMMENT: Euclidean distances (in 3 dimensions) between 227 fonts in a huamn-measured distance metric 
DIMENSION: 227
EDGE_WEIGHT_TYPE: EXPLICIT
EDGE_WEIGHT_FORMAT: LOWER_ROW
EDGE_WEIGHT_SECTION"""
    k=0
    for i in range(1,n):
        for j in range(i):
            f.write(str(int(l[k])))
            f.write(" ")
            k += 1
        f.write("\n")
    print >>f, "EOF"
    f.close()


fonts = tools.my_read("c:/data/fonts/ids.txt").splitlines()
fonts2 = [i.split(".")[0] for i in fonts]
fonts2.sort()




TSPLIB_format()

tools.my_run("lkh MyFonts.par","c:/sim/tsp")

tour = tools.my_read("c:/sim/tsp/MyFonts.tour").strip().splitlines()
tour = tour[6:-2]
tour = [int(i)-1 for i in tour]
#real_tour = []
#for i in tour:
#    if i<5:
#        real_tour.append(i)
#    if i>5:
#        real_tour.append(i-1)
#tour=real_tour
print tour

fonts3 = []
for i in range(len(fonts2)):
    fonts3.append(fonts2[tour[i]])

s= "<html><head></head><body><table cellpadding=100><td>"

s+=draw_fonts(fonts2,"Alphabetical")
s+="</td><td>"
s+=draw_fonts(fonts3,"Human similarity")
s+="</td></table></body></html>\n"

tools.my_write("c:/sim/trees/fonts.html",s)


