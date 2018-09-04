import ROOT
import subprocess
import pickle

l = open('/tmp/files.txt','r')

#for i in `cat /tmp/files.txt`; do rucio list-file-replicas --pfns --protocol root --rse MWT2_UC_LOCALGROUPDISK  $i/ ; done &> /tmp/all.txt
myMap = {}
n=0
for ite in l:

    i=ite.rstrip('\n')
    print 'File:',i

    stdout=None
    returnCode = -10
    while returnCode!=0:
    #proc = subprocess.Popen(['/bin/bash'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    #stdout,error = proc.communicate('rucio list-file-replicas --pfns --protocol root --rse MWT2_UC_LOCALGROUPDISK  '+i+'/')
        proc = subprocess.Popen(['/bin/bash'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        stdout = proc.communicate('rucio list-file-replicas --pfns --protocol root --rse MWT2_UC_LOCALGROUPDISK  '+i+'/')
    #stdout = proc.communicate('rucio list-file-replicas --pfns --protocol root --rse MWT2_UC_LOCALGROUPDISK  '+i+'/')
    
        print stdout
        print 'Return note: ',proc.returncode
        returnCode=proc.returncode
    #print "ERROR: ",error
    files=[]
    for f in stdout:
        if f !=None:
            print '   Files',f
            allF = f.split('\n')
            for a in allF:
                if len(a.strip())>1:
                    files+=[a.strip()]
    myMap[i]=files
    n+=1
    #if n>5:
    #    break
print myMap


pickle.dump( myMap, open( "myMap.p", "wb" ) )
print 'done'
