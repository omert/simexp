import tools, time
from PIL import Image
import re
from urllib import urlretrieve

urlstring = "http://www.lifeprint.com/asl101/gifs-animated/"
html = tools.my_url_open(urlstring).read()
lst= re.findall('href.*</a>',html)
lst2 = [i[6:i.rindex('"')] for i in lst]
lst3 = [i[i.rindex('"')+2:-4] for i in lst]
#for i in range(len(lst2)):
#    urlretrieve("http://www.lifeprint.com/asl101/gifs-animated/"+lst2[i],"c:/data/signs/"+lst3[i]+".gif")

