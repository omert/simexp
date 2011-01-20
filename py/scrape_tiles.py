import tools, time
from PIL import Image

urlstring = "http://www.amazon.com/gp/search/ref=sr_hi_4?rh=n%3A228013%2Cn%3A%21468240%2Cn%3A551240%2Cn%3A13397641%2Cn%3A324030011&bbn=324030011&ie=UTF8&qid=1286030645#/ref=sr_pg_2?rh=n%3A228013%2Cn%3A%21468240%2Cn%3A551240%2Cn%3A13397641%2Cn%3A324030011%2Cp_6%3AA2PHD1PQGLN1MQ&page=pG&bbn=324030011&sort=pmrank&ie=UTF8&qid=1286031509"


s=""
for i in range(163):
    s+=str(i)+"_"
    
    
print s
exit(0)

imgs2 = []
for p in range(2,4):
    url = urlstring.replace("pG",str(p))
    print url
    html = tools.my_url_open(url).read()
    #print html
    imgs = html.split("AA160_.jpg")
    
    for im in imgs[:-1]:
        if im.rfind("http:")!=-1:
            imgs2.append(im[im.rfind("http:"):]+"AA160_.jpg")
    
    st = "<html>"
    for i in imgs2:
        st+="<img src='"+i+"'>\n "
    tools.my_write('c:/temp/tiles/massive2.html',st)
    
    print "Page ",p,"got ",len(imgs2),"images"
    time.sleep(2)

