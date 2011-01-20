import tools, time
from PIL import Image
import re
from urllib import urlretrieve

def get_gogh_urls():

    urlstring = "http://www.vangoghgallery.com/catalog/Painting/"
    html = tools.my_url_open(urlstring).read()
    lst= re.findall('catalog/Painting/.*?html',html)
    return lst
    
lst=tools.uniqueify(get_gogh_urls())
lst2=[i[17:] for i in lst]
ref_urls = ["http://www.vangoghgallery.com/catalog/Painting/"+i for i in lst2]
img_urls = []
for i in ref_urls:
    html = tools.my_url_open(i).read()
    s = re.findall("image/.*?/.*?.jpg",html)
    assert len(s)==2 and s[0]==s[1]
    print i
    img_urls.append("http://www.vangoghgallery.com/catalog/"+s[0])



#lst2 = [i[6:-1] for i in lst]
#lst4 = []
#for i in lst2:
#    html = tools.my_url_open("http://flower-dictionary.com/"+i).read()
#    lst3=re.findall("/uploads/flowers/.*?.jpg",html)    
#    if len(lst3)!=1:
#        print "SHOOT:",i,len(lst3)
#    lst4+=lst3
#lst2b = [i[:-4] for i in lst2]
#lst5 = [i[17:] for i in lst4]
#
#n = len(lst5)
#
#names = []
#nums = []
#
#for i in range(n):
#    if lst5[i] not in lst5[:i]:
#        nums.append(lst5[i])
#        names.append(lst2b[i])
#
#for i in range(len(names)):
#    urlretrieve("http://flower-dictionary.com/images/uploads/flowers/"+nums[i],"c:/data/flowers/"+names[i]+".jpg")
1