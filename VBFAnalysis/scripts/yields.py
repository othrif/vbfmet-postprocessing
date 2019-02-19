import ROOT


regions=[
'VBFjetSel_1Nom_SR1_obs_cuts',
'VBFjetSel_2Nom_SR2_obs_cuts',
'VBFjetSel_3Nom_SR3_obs_cuts',

'VBFjetSel_1Nom_oneElePosCR1_obs_cuts',
'VBFjetSel_2Nom_oneElePosCR2_obs_cuts',
'VBFjetSel_3Nom_oneElePosCR3_obs_cuts',

'VBFjetSel_1Nom_oneEleNegCR1_obs_cuts',
'VBFjetSel_2Nom_oneEleNegCR2_obs_cuts',
'VBFjetSel_3Nom_oneEleNegCR3_obs_cuts',

'VBFjetSel_1Nom_oneElePosLowSigCR1_obs_cuts',
'VBFjetSel_2Nom_oneElePosLowSigCR2_obs_cuts',
'VBFjetSel_3Nom_oneElePosLowSigCR3_obs_cuts',

'VBFjetSel_1Nom_oneEleNegLowSigCR1_obs_cuts',
'VBFjetSel_2Nom_oneEleNegLowSigCR2_obs_cuts',
'VBFjetSel_3Nom_oneEleNegLowSigCR3_obs_cuts',

'VBFjetSel_1Nom_oneMuPosCR1_obs_cuts',
'VBFjetSel_2Nom_oneMuPosCR2_obs_cuts',
'VBFjetSel_3Nom_oneMuPosCR3_obs_cuts',

'VBFjetSel_1Nom_oneMuNegCR1_obs_cuts',
'VBFjetSel_2Nom_oneMuNegCR2_obs_cuts',
'VBFjetSel_3Nom_oneMuNegCR3_obs_cuts',

'VBFjetSel_1Nom_twoEleCR1_obs_cuts',
'VBFjetSel_2Nom_twoEleCR2_obs_cuts',
'VBFjetSel_3Nom_twoEleCR3_obs_cuts',

'VBFjetSel_1Nom_twoMuCR1_obs_cuts',
'VBFjetSel_2Nom_twoMuCR2_obs_cuts',
'VBFjetSel_3Nom_twoMuCR3_obs_cuts',]

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
f=ROOT.TFile.Open('SumHF_lepVeto.root')
#f=ROOT.TFile.Open('SumHF_BaselineCuts_ZeroPhoton_BaseLepVeto_AllSyst_v26c.root')
#f=ROOT.TFile.Open('SumHF_LooseCuts_ZeroPhoton_AllSyst_v26c.root')
#f=ROOT.TFile.Open('SumHF_LooseCuts_ZeroPhoton_AllSyst_v26c_FJVT.root')
#f=ROOT.TFile.Open('SumHF_nj2.root')
#f=ROOT.TFile.Open('SumHF_LooseCuts_ZeroPhoton_AllSyst_v26c_FixedLepTrig.root')
#f=ROOT.TFile.Open('SumHF.root')
SumList=[]
line='Region\t'
for s in samples:
    line+=s+'\t'
    SumList+=[0.0]
print line
nRegion=0
for r in regions:
    line =r+'\t'
    if nRegion==0:
        for su in range(0,len(SumList)):
            SumList[su]=0.0
    su=0
    for s in samples:
        histname=s+r
        if s=='hdata_':
            histname=s+'NONE_'+r[len('VBFjetSel_3Nom_'):]
            #print histname
        h=f.Get(histname)
        integral=0.0
        if h!=None:
            integral=h.Integral()
            line+='%0.2f\t' %integral
            SumList[su]+=integral
        else:
            line+='N/A\t' 
        su+=1
    print line
    nRegion+=1
    if nRegion==3:
        nRegion=0
        rline='Sum\t'
        for su in range(0,len(SumList)):
            rline+='%0.2f\t' %(SumList[su])
        print rline
print 'done'
