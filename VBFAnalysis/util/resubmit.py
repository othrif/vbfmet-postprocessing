#from  VBFAnalysis import systematics
import VBFAnalysis.systematics

sys = VBFAnalysis.systematics.systematics("All")
systList = sys.getsystematicsList()

#for i in systList:
#    print i

# read syst
systFiles = open('failSyst.txt','r')
myList=[]
for f in systFiles:
    syst='Nominal'
    for s in systList:
        if f.count(s):
            syst = s
            break
    myList+=[[f,s]]
print myList

#files
fListVec=[]
fList = open('lauchList.txt','r')
for f in fList:
    fListVec+=[f]

print fListVec

fout = open('writeOut.txt','w')
for i in range(0,len(fListVec)):
    line = myList[i][1]+' '+fListVec[i]
    fout.write(line)
fout.close()
#testSyst/VBFAnalysisCondorSub
