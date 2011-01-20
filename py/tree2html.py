import sys, tools

htmlfile = "c:/sim/tree9d.html"
dataroot = "c:/data"


if len(sys.argv)!=4:
    print "Usage: tree2html.py file.tree9 database aspectratio"
    print "Creates a file called file.html"
    exit(0)
    
db = sys.argv[2]
aspectratio = sys.argv[3]

infile = sys.argv[1]
outfile = sys.argv[1].replace(".tree9",".html")

s = '<html><head>\n<script language="JavaScript">\n'
s+='var aspectratio = '+aspectratio+';\n'
s+='var datab = "'+db+'";\n'

def list_to_str(lst):
    res = "["
    for i in lst:
        if type(i)==list:
            res+=list_to_str(i)
        else:
            res+=str(i)
        res+=","
    if res[-1]==",":
        return res[:-1] + "]"
    return res+"]"
    
tree = []
inf = tools.my_read(infile).splitlines()
for line in inf:
    (a,b) = line.split(":")
    tree.append([a.split(),b.split()])
    
s+='var tree = '+list_to_str(tree)+";\n"
s+='var ids = ['
ids = tools.my_read(dataroot+"/"+db+"/ids.txt").splitlines()
for i in ids:
    s+='"'+i+'",'
s=s[:-1]
s+='];\n'

s+= '</script></head>\n'
s+= tools.my_read(htmlfile)
tools.my_write(outfile,s)