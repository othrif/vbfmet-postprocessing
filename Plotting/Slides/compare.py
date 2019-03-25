import pickle
import sys
def Merge(old,new,missing={}):
    total=0
    nSame=0
    for r,evts in old.iteritems():
        total+=len(evts)
        print 'Run: ',r,' ',len(evts)
        sys.stdout.flush()
        if r in new:
            evts.sort()
            new[r].sort()
            for e in evts:
                if e in new[r]:
                    nSame+=1

    return [total,nSame]

print 'Start'
sys.stdout.flush()
fr207 = open("r207Z.p","rb")
r207 = pickle.load(fr207)
print 'Loaded old'
sys.stdout.flush()
#fr21 = open("r21LooserNoLepDetaJet7040MjjMETNjTrigDphiNoPeriod.p","rb")
fr21 = open("r21Zee3018.p","rb")
r21 = pickle.load(fr21)
print 'Loaded new'
print 'Old!'
sys.stdout.flush()
runOld=r207[0]
#runOldVars=r207[1]
print 'New!'
runNew=r21[0]
#runNewVars=r21[1]
print 'Starting checks'
cutflow={}

cutflowRev={}
missing={}
for c,mp in runOld.iteritems():
    cutflow[c]=Merge(mp, runNew[c],missing)
    cutflowRev[c]=Merge( runNew[c],mp)
    #Merge

print 'fraction of 20.7 in 21'
for c,vals in cutflow.iteritems():
    f=0.0
    if vals[0]>0.0:
        f=vals[1]/float(vals[0])
    print c,' ',vals[0],vals[1],f

print ''
# reverse check
for c,vals in cutflowRev.iteritems():
    f=0.0
    if vals[0]>0.0:
        f=vals[1]/float(vals[0])
    print c,' ',vals[0],vals[1],f
    
