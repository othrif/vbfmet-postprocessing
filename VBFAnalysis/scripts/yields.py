import ROOT
import math

regions=[
'VBFjetSel_XNom_SRX_obs_cuts',
'VBFjetSel_XNom_oneElePosCRX_obs_cuts',
'VBFjetSel_XNom_oneEleNegCRX_obs_cuts',
'VBFjetSel_XNom_oneElePosLowSigCRX_obs_cuts',
'VBFjetSel_XNom_oneEleNegLowSigCRX_obs_cuts',
'VBFjetSel_XNom_oneMuPosCRX_obs_cuts',
'VBFjetSel_XNom_oneMuNegCRX_obs_cuts',
'VBFjetSel_XNom_twoEleCRX_obs_cuts',
'VBFjetSel_XNom_twoMuCRX_obs_cuts',]

#hdata_NONE_twoEleCR3_obs_cuts
samples =['hVBFH125_',
          'hggFH125_',
          'hVH125_',
          'hZ_strong_',
          'hZ_EWK_',
          'hW_strong_',
          'hW_EWK_',
          'httbar_',
          'hQCDw_',
          'heleFakes_',
          'hmultijet_',
          'hdata_',
]

#f=ROOT.TFile.Open('SumHF_BaselineCuts_ZeroPhotonAllSyst_v26New.root')
#f=ROOT.TFile.Open('SumHF_noMET.root')
#f=ROOT.TFile.Open('SumHF_lepVeto.root')
#f=ROOT.TFile.Open('SumHF_BaselineCuts_ZeroPhoton_BaseLepVeto_AllSyst_v26c.root')
#f=ROOT.TFile.Open('SumHF_BaselineCuts_ZeroPhoton_BaseLepVeto_AllSyst_Madgraph_v26c.root')
#f=ROOT.TFile.Open('SumHF_BaselineCuts_ZeroPhotonAllSyst_Madgraph_v26New.root')
#f=ROOT.TFile.Open('SumHF_LooseCuts_ZeroPhoton_AllSyst_v26c.root')
#f=ROOT.TFile.Open('SumHF_LooseCuts_ZeroPhoton_NominalOnly_LooseLepZonly_v26c.root')
#f=ROOT.TFile.Open('SumHF_LooseCuts_ZeroPhoton_NominalOnly_DPhijjMjjBinningNjetBin_v26c.root')
#f=ROOT.TFile.Open('SumHF_LooseCuts_ZeroPhoton_NominalOnly_LooseLepDilepTrig_v26c.root')
f=ROOT.TFile.Open('SumHF_BaselineCuts_ZeroPhoton_BaseLepVeto_AllSyst_v26c_DPhiFix.root')
#f=ROOT.TFile.Open('SumHF_LooseCuts_ZeroPhoton_NominalOnly_NjetBin_v26c.root')
#f=ROOT.TFile.Open('SumHF_LooseCuts_ZeroPhoton_NominalOnly_LowMETBin_v26c.root')
#f=ROOT.TFile.Open('SumHF_LooseCuts_ZeroPhoton_NominalOnly_LooseLep_v26c.root')
#f=ROOT.TFile.Open('SumHF_LooseCuts_ZeroPhoton_NominalOnly_TenaciousMET_v26c.root')
#f=ROOT.TFile.Open('SumHF_LooseCuts_ZeroPhoton_AllSyst_Madgraph_v26c.root')
#f=ROOT.TFile.Open('SumHF_LooseCuts_ZeroPhoton_AllSyst_v26c_FJVT.root')
#f=ROOT.TFile.Open('SumHF_nj2.root')
#f=ROOT.TFile.Open('SumHF_LooseCuts_ZeroPhoton_AllSyst_v26c_FixedLepTrig.root')
#f=ROOT.TFile.Open('SumHF.root')
SumList=[]
SumErrList=[]
line='Region\t'
for s in samples:
    line+=s+'\t'
    SumList+=[0.0]
    SumErrList+=[0.0]
print line

bins=[1,2,3,4,5,6,7,8,9]
nRegion=0
sTot=0
for bin_num in bins:
    r=regions[0].replace('X','%s' %bin_num)
    histname=samples[0]+r
    h=f.Get(histname)
    if not h:
        sTot=bin_num-1
        break
for rmy in regions:
    if nRegion==0:
        for su in range(0,len(SumList)):
            SumList[su]=0.0
            SumErrList[su]=0.0
    for bin_num in bins:
        r=rmy.replace('X','%s' %bin_num)
        if bin_num<=sTot:
            line =r+'\t'
        else:
            continue
        su=0
        lineBkgErr=0.0
        lineBkg=0.0
        lineData=0.0
        for s in samples:
            histname=s+r
            if s=='hdata_':
                histname=s+'NONE_'+r[len('VBFjetSel_3Nom_'):]
                #print histname
            h=f.Get(histname)
            integral=0.0

            if h!=None:
                e = ROOT.Double(0.0)
                integral=h.IntegralAndError(0,1001,e)
                line+='%0.2f +/- %0.2f\t' %(integral,e)
                #line+='%0.2f\t' %(integral)
                SumList[su]+=integral
                SumErrList[su]+=e**2
                if s!='hdata_':
                    lineBkgErr+=e**2
                    lineBkg+=integral
                else:
                    lineData=integral
            else:
                line+='N/A\t'
            su+=1

        # add stat/MC and data/MC
        bkgFracErr= math.sqrt(lineBkgErr)/lineBkg
        line +='%0.3f\t' %(bkgFracErr)
        #line +='%0.2f\t' %(lineData/lineBkg)
        line +='%0.3f +/- %0.3f\t' %(lineData/lineBkg, math.sqrt(1./lineData+bkgFracErr**2)*(lineData/lineBkg))
        print line
        nRegion+=1
        if nRegion==sTot:
            nRegion=0
            totalData=0
            totalBkg=0
            totalBkgErr=0
            rline='Sum\t'
            for su in range(0,len(SumList)):
                #rline+='%0.2f\t' %(SumList[su])
                rline+='%0.2f +/- %0.2f\t' %(SumList[su],math.sqrt(SumErrList[su]))
                if samples[su]!='hdata_':
                    totalBkg+=SumList[su]
                    totalBkgErr+=SumErrList[su]
                else:
                    totalData=SumList[su]
            
            #bkgFracErr
            totalBkgFracErr = math.sqrt(totalBkgErr)/totalBkg
            rline+='%0.3f\t%0.3f +/- %0.3f\t' %(totalBkgFracErr, totalData/totalBkg, math.sqrt(totalBkgFracErr**2+1./totalData)*(totalData/totalBkg))
            print rline
print 'done'
