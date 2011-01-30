"""
a=create_rand_trips(1181,1000)
tools.my_write("c:/users/adum/simexp/turkexps/neckties/random_multi_times/2.trips",a)
c:\users\adum\simexp\py\runtrips_multiple_times.py  C:\Users\adum\simexp\turkexps\neckties\random_multi_times\neckties_multi_times.config C:\Users\adum\simexp\turkexps\neckties\random_multi_times\2.trips C:\Users\adum\simexp\turkexps\neckties\random_multi_times\2.trips.out
get_agreement("c:/users/adum/simexp/turkexps/neckties/random_multi_times/2.trips.out")

a=create_rand_trips(433,1000)
tools.my_write("c:/users/adum/simexp/turkexps/newtiles/random_multi_times/2.trips",a)
c:\users\adum\simexp\py\runtrips_multiple_times.py  C:\Users\adum\simexp\turkexps\newtiles\random_multi_times\newtiles_multi_times.config C:\Users\adum\simexp\turkexps\newtiles\random_multi_times\2.trips C:\Users\adum\simexp\turkexps\newtiles\random_multi_times\2.trips.out
get_agreement("c:/users/adum/simexp/turkexps/newtiles/random_multi_times/2.trips.out")

a=create_rand_trips(26,1000)
c:\users\adum\simexp\py\runtrips_multiple_times.py  C:\Users\adum\simexp\turkexps\calibrialpha\random_multi_times\calibrialpha_multi_times.config C:\Users\adum\simexp\turkexps\calibrialpha\random_multi_times\1.trips C:\Users\adum\simexp\turkexps\calibrialpha\random_multi_times\1.trips.out
get_agreement("c:/users/adum/simexp/turkexps/calibrialpha/random_multi_times/1.trips.out")


"""


import tools, numpy as np
import scipy.stats.morestats

def get_agreement(filename):
    s = tools.my_read(filename).strip().splitlines()
    trips = {}
    for l in s:
        (a,b,c,e) = l.split()
        a = int(a)
        b = int(b)
        c = int(c)
        tb = min(b,c)
        tc = max(b,c)
        if b<c:
            y = 1
        else:
            y = 0
        if (a,tb,tc) not in trips:
            trips[(a,tb,tc)]=[0,0]
        trips[(a,tb,tc)][y]=trips[(a,tb,tc)][y]+1
    v = trips.values()
    data = []
    for (a,b) in v:
        if(a+b>1):
            data.append( (a*(a-1.)+b*(b-1.))/((a+b)*(a+b-1.))) # double count agreement and disagreement pairs
    r =scipy.stats.morestats.bayes_mvs(data, 0.95)[0]
    print "Mean",r[0], "  95% confidence interval",r[1]
    print "This corresponds to a signal of ", 0.5+np.sqrt(r[0]/2.-1/4.)
    return r[0]
