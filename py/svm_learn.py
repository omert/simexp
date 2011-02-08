#learn with svm_light

data_file = "c:/temp/to_svm.txt"
model_file = "c:/temp/svm_model.txt"
pred_file = "c:/temp/svm_pred.txt"


import tools
import csv
import glob
import numpy as np

def create_data(dir,att,info_file,fit_file,data_file):
    x = tools.my_read(fit_file).strip().splitlines()
    x = [[float(zz) for zz in z.split()] for z in x]
    m = len(x)
    d = len(x[0])
    
    f = open(info_file,"r")
    csvr = csv.DictReader(f)
    y = [int(r[att]) for r in csvr]
    f.close()
    st = ""
    for i in range(m):
        if y[i]!=-100:
            if y[i]==1:
                st+="+1"
            else: #translate 0 to -1
                st+="-1" 
            for j in range(d):
                st+=" "+str(j+1)+":"+str(x[i][j])
            st+=" # "+str(i)
            st+="\n"
    st = st.strip()
    tools.my_write(data_file,st)   
    return (x,y)

def read_model(model_file):
    d = tools.my_read(model_file).strip().splitlines()
    assert(d[9][-20:].strip()=="port vectors plus 1")
    num_vectors = int(d[9].split()[0])-1
    thresh = float(d[10].split()[0])
    #print num_vectors, thresh
    alphas = np.array([[float(t.split()[0]) for t in d[11:]]])
    #print len(alphas)
    svs = np.array([[float(t.split(":")[1]) for t in r.strip().split()[1:-2]] for r in d[11:]])
    w = np.dot(alphas,svs)
    return w, thresh 
    
def classify(dir,att,info_file=None,fit_file = None):
    global model_file, data_file,pred_file
    if dir[-1]!="/" and dir[-1]!="\\":
        dir+="/"
    if info_file==None:
        info_file = dir+"info.csv"
    if fit_file==None:
        fit_file = glob.glob(dir+"*fit.txt")[0]
                
    (x,y) = create_data(dir,att,info_file,fit_file,data_file)
    st2= tools.my_run("c:/users/adum/simexp/svmlight/svm_learn.exe -x 1 "+data_file+" "+model_file)
    w, thresh = read_model(model_file)
    print st2
    print thresh
    res = [r[0] for r in np.dot(x,w.T)-thresh]
    res2 = [(res[i],chr(65+i)) for i in range(26)]
    res2.sort()
    print res2
    st3= tools.my_run("c:/users/adum/simexp/svmlight/svm_classify.exe "+data_file+" "+model_file+" "+pred_file)    
    print st3

classify("c:/users/adum/simexp/data/flags","att_stripes")
classify("c:/users/adum/simexp/data/calibrialpha","att_tall")
#classify("c:/users/adum/simexp/data/calibrialpha","att_vowels")
#classify("c:/users/adum/simexp/data/calibrialpha","att_ee")
#classify("c:/users/adum/simexp/data/neckties","att_many_colors")
#classify("c:/users/adum/simexp/data/neckties","att_bow_or_neck")
#classify("c:/users/adum/simexp/data/newtiles","att_ornate")
#read_model(model_file)