import ROOT
import subprocess
import pickle

l = open('extra.txt','r')
#l = open('extra_v15.txt','r')

#for i in `cat /tmp/files.txt`; do rucio list-file-replicas --pfns --protocol root --rse MWT2_UC_LOCALGROUPDISK  $i/ ; done &> /tmp/all.txt
myMap = {}
n=0
for ite in l:

    if ite.count ('#'):
        continue
    i=ite.rstrip('\n')
    print 'File:',i

    stdout=None
    returnCode = -10
    #while returnCode!=0:
    #proc = subprocess.Popen(['/bin/bash'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    #stdout,error = proc.communicate('rucio list-file-replicas --pfns --protocol root --rse MWT2_UC_LOCALGROUPDISK  '+i+'/')
    proc = subprocess.Popen(['/bin/bash'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout = proc.communicate('ls  '+i+'/*root*')
    #stdout = proc.communicate('rucio list-file-replicas --pfns --protocol root --rse MWT2_UC_LOCALGROUPDISK  '+i+'/')
    
        #print stdout
        #print 'Return note: ',proc.returncode
        #returnCode=proc.returncode
    #print "ERROR: ",error
    files=[]
    for f in stdout:
        if f !=None:
            print '   Files',f
            allF = f.split('\n')
            for a in allF:
                if len(a.strip())>1:
                    files+=[a.strip()]
    ikey = i
    ikey = (ikey.rstrip('/'))[ikey.rfind('/')+1:]
    if i.count('361515'):
        ikey = 'user.othrif.v07.361515.Sherpa_221_NNPDF30NNLO_Wtaunu_MAXHTPTV70_140_BFilter.e5340_s3126_r9364_p3575_MiniNtuple.root'
    elif i.count('361516'):
        ikey = 'user.othrif.v07.361516.Sherpa_221_NNPDF30NNLO_Wtaunu_MAXHTPTV70_140_BFilter.e5340_s3126_r9364_p3575_MiniNtuple.root'
    elif i.count('361517'):
        ikey = 'user.othrif.v07.361517.Sherpa_221_NNPDF30NNLO_Wtaunu_MAXHTPTV70_140_BFilter.e5340_s3126_r9364_p3575_MiniNtuple.root'
    elif i.count('361518'):
        ikey = 'user.othrif.v07.361518.Sherpa_221_NNPDF30NNLO_Wtaunu_MAXHTPTV70_140_BFilter.e5340_s3126_r9364_p3575_MiniNtuple.root'
    elif i.count('361519'):
        ikey = 'user.othrif.v07.361519.Sherpa_221_NNPDF30NNLO_Wtaunu_MAXHTPTV70_140_BFilter.e5340_s3126_r9364_p3575_MiniNtuple.root'
    myMap[ikey]=files
    n+=1
    #if n>5:
    #    break
print myMap

# merging two maps
if True:
    oldMap = pickle.load( open( 'mapOld.p', "rb" ) )
    for i,k in oldMap.iteritems():
        if len(k)>0:
            if i not in myMap:
                myMap[i]=k
            else:
                print 'not replacing: ',i, myMap[i]
        else:
            print 'empty: ' ,i
    print myMap

pickle.dump( myMap, open( "myMap.p", "wb" ) )
print 'done'
