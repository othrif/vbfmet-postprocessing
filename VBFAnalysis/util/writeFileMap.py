import ROOT
import subprocess
import pickle
import sys
import argparse
import sys

parser = argparse.ArgumentParser( description = "get total Nevent to weight samples", add_help=True , fromfile_prefix_chars='@')
parser.add_argument( "-l", "--list", type = str, dest = "filelist", default = "filteredSherpa.txt", help = "text file with list of datasets" )
parser.add_argument( "-o", "--output", type = str, dest = "output", default = "myMap.p", help = "output file name" )
parser.add_argument( "-s", "--site", type = str, dest = "site", default = "MWT2_UC_LOCALGROUPDISK", help = "grid site: MWT2_UC_LOCALGROUPDISK or DESY-HH_LOCALGROUPDISK" )
args, unknown = parser.parse_known_args()

l = open(args.filelist)

#for i in `cat /tmp/files.txt`; do rucio list-file-replicas --pfns --protocol root --rse MWT2_UC_LOCALGROUPDISK  $i/ ; done &> /tmp/all.txt
myMap = {}
n=0
for ite in l:

    if ite.count('#'):
        continue

    i=ite.rstrip('\n')
    print 'File:',i.strip()
    sys.stdout.flush()

    if i.strip()=='':
        continue

    stdout=None
    returnCode = -10
    while returnCode!=0:
    #proc = subprocess.Popen(['/bin/bash'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    #stdout,error = proc.communicate('rucio list-file-replicas --pfns --protocol root --rse MWT2_UC_LOCALGROUPDISK  '+i+'/')
        proc = subprocess.Popen(['/bin/bash'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        if args.site=="None":
            stdout = proc.communicate('rucio list-file-replicas --pfns --protocol root  '+i.strip()+'/')
        else:
            stdout = proc.communicate('rucio list-file-replicas --pfns --protocol root --rse  '+args.site+' '+i.strip()+'/')
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

    ikey=i
    if i.count('346600'):
        ikey = 'user.schae.v37Syst.346600.invSig.e7613_s3126_r9364_p3895_MiniNtuple.root'
    myMap[ikey]=files
    n+=1
    #if n>5:
    #    break
print myMap


pickle.dump( myMap, open(args.output, "wb" ) )
print 'done'
