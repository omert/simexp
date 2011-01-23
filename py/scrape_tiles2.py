import tools, time, csv, os, sys
from PIL import Image

#urlstring = "http://www.amazon.com/s?ie=UTF8&rh=n%3A324030011%2Cp_6%3AA2U9N7C8EXZMY6&page=pG"
urlstring = "http://www.amazon.com/s?ie=UTF8&rh=n%3A324030011&page=pG"

s=""
for i in range(163):
    s+=str(i)+"_"
    
    
#print s

def scrape_amazon_page(html):
    imgs = html.split("AA160_.jpg")
    results = []
    for i in range(len(imgs)-1):
        try:
            res = {}
            im = imgs[i]
            nxt = imgs[i+1]
            if im.rfind("http:")==-1:
                print "YO1"
                continue
            aaa = im.rfind("http:")
            res['image_url'] = im[aaa:]+"AA160_.jpg";
            aaa = im[:aaa].rfind("http:")
            bbb = aaa+im[aaa:].find('"')
            res['orig_url'] = im[aaa:bbb]
            res['ASIN']=res['orig_url'][-10:]
            res['url'] = 'http://www.amazon.com/dp/'+res['ASIN']
            res['image']=res['ASIN']+".jpg"
            aaa=nxt.find('<br clear="all" />')
            if aaa==-1: 
                print "YO2"
                continue
            bbb=aaa+nxt[aaa:].find("</a>")
            if bbb==-1: 
                print "YO3"
                continue
            res['name'] = nxt[aaa+18:bbb]
            aaa = aaa+nxt[aaa:].find("<span>$")+7
            if aaa==-1:
                print "YO6"            
                continue
            bbb = aaa+nxt[aaa:].find("</span>")
            if bbb==-1: 
                print "YO7"
                continue
            res['att_price'] = float(nxt[aaa:bbb].replace(",",""))
            results.append(res)
        except:
            pass
    return results


for p in range(326,328): 
    allresults = []
    url = urlstring.replace("pG",str(p))
    #print url
    html = tools.my_url_open(url).read()
    allresults=scrape_amazon_page(html)
    print "results page",p, len(allresults), len(allresults)/24., len(tools.uniqueify(allresults))
  
    i=0
    ar2 = []
    for r in allresults:
        i=i+1
        imfname = "c:/temp/tiles2/"+r['ASIN']+".jpg"
        if not os.path.exists(imfname):
            try:
                print "Scraping object",i,"page",p,(p-1)*24+i
                html = tools.my_url_open(r['url']).read()
                r['att_glass']=1 if 'Glass Tiles</a>' in html else 0
                r['att_ceramic']=1 if 'Ceramic Tiles</a>' in html else 0
                r['att_stone']=1 if 'Stone Tiles</a>' in html else 0
                r['att_limestone']=1 if 'Limestone Tiles</a>' in html else 0
                r['att_marble']=1 if 'Marble Tiles</a>' in html else 0
                r['bestsellers_string']=""
                r['att_bestsellerrank'] = -1
                if "<b>Amazon Bestsellers Rank:</b>" in html:
                    aaa = html.find("<b>Amazon Bestsellers Rank:</b>")
                    bbb = aaa+html[aaa:].find("(")
                    r['bestsellers_string'] = html[aaa+33:bbb].strip()
                    r['att_bestsellerrank'] = int(r['bestsellers_string'][1:r["bestsellers_string"].find(" ")].replace(",",""))
                tools.my_save_web_image(r['image_url'],imfname)
                ar2.append(r)
            except:
                print "EXCEPTION",sys.exc_info()[0]
                print r
    if len(ar2)==0:
        continue
    
    fname = "c:/temp/tiles2/info.csv"
    if os.path.exists(fname):
        print "FILE EXISTS, APPENDING"
        f=open(fname,"ab")
        c = csv.DictWriter(f,sorted(ar2[0].keys()))
    else:
        print "CREATING FILE"
        f=open(fname,"wb")
        c = csv.DictWriter(f,sorted(ar2[0].keys()))
        header = {}
        for k in ar2[0].keys():
            header[k]=k
        c.writerow(header)
    c.writerows(ar2)
    f.close()