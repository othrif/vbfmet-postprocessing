import ROOT


f1= ROOT.TFile.Open('/tmp/corr.root')

can=f1.Get('CorrPlot')
c1= ROOT.TCanvas('table', 'table', 600, 850)
corr=None
for i in can.GetPad(0).GetListOfPrimitives():
    if i.GetName()=="correlation_matrix":
        corr=i.Clone()#can.Get(i.GetName())
c1.cd()
#corr.Draw()
keepThese=[]

pairMap={}
filterV=''
filterVN='k'
filterVN2='reno'
filterVN3='gamma'
for i in range(1,corr.GetNbinsX()+1):
    for j in range(1,corr.GetNbinsY()+1):
        if filterV!='' and not filterV in corr.GetXaxis().GetBinLabel(i):
            continue
        if filterVN!='' and (filterVN in corr.GetXaxis().GetBinLabel(i) or filterVN in corr.GetYaxis().GetBinLabel(j)):
            continue        
        if filterVN2!='' and (filterVN2 in corr.GetXaxis().GetBinLabel(i) or filterVN2 in corr.GetYaxis().GetBinLabel(j)):
            continue
        if filterVN3!='' and (filterVN3 in corr.GetXaxis().GetBinLabel(i) or filterVN3 in corr.GetYaxis().GetBinLabel(j)):
            continue                
        pairMap[corr.GetXaxis().GetBinLabel(i)+corr.GetYaxis().GetBinLabel(j)]=corr.GetBinContent(i,j)
        if i==(corr.GetNbinsY()+1-j):
            continue
        if corr.GetBinContent(i,j)==1.0:
            print i,j
        #print corr.GetBinContent(i,j)
        if abs(corr.GetBinContent(i,j))>0.2:
            myname1=corr.GetXaxis().GetBinLabel(i)
            myname2=corr.GetYaxis().GetBinLabel(j)
            if myname1 not in keepThese:
                keepThese+=[myname1]
            if myname2 not in keepThese:
                keepThese+=[myname2]
newPlot=ROOT.TH2F('cor2','cor2',len(keepThese),0.0,len(keepThese),len(keepThese),0.0,len(keepThese))
newPlot.SetStats(0)
ib=1
for i in keepThese:
    newPlot.GetXaxis().SetBinLabel(ib,i)
    newPlot.GetYaxis().SetBinLabel((len(keepThese)+1-ib),i)
    ib+=1
for i in range(1,newPlot.GetNbinsX()+1):
    for j in range(1,newPlot.GetNbinsY()+1):
        keyn=newPlot.GetXaxis().GetBinLabel(i)+newPlot.GetYaxis().GetBinLabel(j)
        if keyn in pairMap:
            v=pairMap[keyn]
            newPlot.SetBinContent(i,j,v)

c1.cd()
newPlot.Draw('colz')
print len(keepThese)
c1.Update()
#c1.WaitPrimitive()
raw_input('waiting')
