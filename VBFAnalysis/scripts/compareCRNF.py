import math

def averageNF(s1,s2):
    b1=s1.strip().rstrip('\t')
    b1list=b1.split('$\\pm$')
    v1=float(b1list[0].strip())
    e1=float(b1list[1].strip())
    b2=s2.strip().rstrip('\t')
    b2list=b2.split('$\\pm$')
    v2=float(b2list[0].strip())
    e2=float(b2list[1].strip())

    v=(v2*e1+v1*e2)/(e1+e2)
    e=v*1./math.sqrt(1./(e1/v1)**2+1./(e2/v2)**2)
    print v,e
    return [v,e]

def averageNFList(s1,s2):
    v1=s1[0]
    v2=s2[0]
    e1=s1[1]
    e2=s2[1]
    v=(v2*e1+v1*e2)/(e1+e2)
    e=v*1./math.sqrt(1./(e1/v1)**2+1./(e2/v2)**2)
    print v,e
    return [v,e]

def ratioNF(s1,s2):
    b1=s1.strip().rstrip('\t')
    b1list=b1.split('$\\pm$')
    v1=float(b1list[0].strip())
    e1=float(b1list[1].strip())
    b2=s2.strip().rstrip('\t')
    b2list=b2.split('$\\pm$')
    v2=float(b2list[0].strip())
    e2=float(b2list[1].strip())

    v=v1/v2
    e=v*math.sqrt((e1/v1)**2+(e2/v2)**2)
    print 'ratio: ',v,e
    return [v,e]

def ratioNFValues(a1,a2,s):
    v1=a1[0]
    e1=a1[1]
    v2=a2[0]
    e2=a2[1]
    v=v1/v2
    e=v*math.sqrt((e1/v1)**2+(e2/v2)**2)
    print s,'ratio: %0.3f +/- %0.3f'%(v,e)
    #return v,e

#fil = open('/Users/schae/testarea/HInvNov/my_syst.txt','r')
fil = open('vr.txt')

combine={}
combine[1]=6
combine[2]=7
combine[3]=8
combine[4]=9
combine[5]=10
binmap={}

for line in fil:
    shortline = line.rstrip('\n').strip()
    shortline_list = shortline.split('&')
    nbin = int(shortline_list[0].strip())
    
    binmap[nbin]=shortline_list[1:]
    print binmap[nbin]

x=0
DPHIzee={}
DPHIzmm={}
DPHIwe={}
DPHIwm={}
zll={}
we={}
wm={}
for i in range(1,11):
    zll[i]=averageNF(binmap[i][0],binmap[i][1])
    we[i]=averageNF(binmap[i][4],binmap[i][5])
    wm[i]=averageNF(binmap[i][2],binmap[i][3])

for i in range(1,6):
    DPHIzee[i]=averageNF(binmap[i][0],binmap[i+5][0])
    DPHIzmm[i]=averageNF(binmap[i][1],binmap[i+5][1])
for i in range(1,6):
    DPHIwe[i]=averageNFList(we[i],we[i+5])
    DPHIwm[i]=averageNFList(wm[i],wm[i+5])
mjjbins={}
mjjbins[1]='0.8-1.0 TeV: '
mjjbins[2]='1.0-1.5 TeV: '
mjjbins[3]='1.5-2.0 TeV: '
mjjbins[4]='2.0-3.5 TeV: '
mjjbins[5]='3.5-    TeV: '
print 'Zll'
for i in range(1,6):
    #print zll[i],zll[i+5]
    ratioNFValues(zll[i],zll[i+5],mjjbins[i])
print 'Wmunu'
for i in range(1,6):
    ratioNFValues(wm[i],wm[i+5],mjjbins[i])
print 'Wenu'
for i in range(1,6):
    #print we[i],we[i+5]
    ratioNFValues(we[i],we[i+5],mjjbins[i])
print 'Zee/Zmm'
for i in range(1,6):
    #print we[i],we[i+5]
    ratioNFValues(DPHIzee[i],DPHIzmm[i],mjjbins[i])
print 'Wen/Wmn'
for i in range(1,6):
    #print we[i],we[i+5]
    ratioNFValues(DPHIwe[i],DPHIwm[i],mjjbins[i])
