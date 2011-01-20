import tools, time
from PIL import Image

urlstring = "http://www.amazon.com/gp/search/ref=sr_hi_4?rh=n:228013,n:!468240,n:551240,n:13397641,n:324030011&bbn=324030011&sort=pmrank&ie=UTF8&qid=1286037602#/ref=sr_pg_4?rh=n%3A228013%2Cn%3A%21468240%2Cn%3A551240%2Cn%3A13397641%2Cn%3A324030011%2Cp_6%3AA3KN51DK5IJ2IF&page=pG&bbn=324030011&sort=pmrank&ie=UTF8&qid=1286037702"

a=tools.SimpleDisplay()

imgs2 = []
hout = '<html><head></head><frameset rows="200px'
for i in range(20):
    hout+=",200px"
hout+='">\n'
for p in range(24,40):
    url = urlstring.replace("pG",str(p))
    hout+="<frame src='"+url+"'>"
    
hout+="</frameset></html>"
tools.my_write("c:/temp/tiles/frameit3.html",hout)

