import tools, time
from PIL import Image

urlstring = "http://www.amazon.com/s/qid=1285958507/ref=sr_pg_pG?ie=UTF8&sort=-price&keywords=ties&bbn=1036592&rh=k%3Aties%2Cn%3A1036592%2Cn%3A%211036682%2Cp_6%3AA32FQKBE4XLKI7&page=pG"

a=tools.SimpleDisplay()

imgs2 = []
for p in range(66):
    html = tools.my_url_open(urlstring.replace("pG",str(p))).read()
    imgs = html.split("190,246_.jpg")
    
    for im in imgs[:-1]:
        if im.rfind("http:")!=-1:
            imgs2.append(im[im.rfind("http:"):]+"190,246_.jpg")
    
    st = "<html>"
    for i in imgs2:
        st+="<img src='"+i+"'>\n "
    tools.my_write('c:/temp/ties/massive2.html',st)
    
    print "Page ",p,"got ",len(imgs2),"images"
    time.sleep(2)

