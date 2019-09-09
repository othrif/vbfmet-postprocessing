import ROOT
import math
import sys
regions=[
'VBFjetSel_XNom_SRX_obs_cuts',
'VBFjetSel_XNom_twoEleCRX_obs_cuts',
'VBFjetSel_XNom_twoMuCRX_obs_cuts',
'VBFjetSel_XNom_oneElePosCRX_obs_cuts',
'VBFjetSel_XNom_oneEleNegCRX_obs_cuts',
'VBFjetSel_XNom_oneMuPosCRX_obs_cuts',
'VBFjetSel_XNom_oneMuNegCRX_obs_cuts',
'VBFjetSel_XNom_oneElePosLowSigCRX_obs_cuts',
'VBFjetSel_XNom_oneEleNegLowSigCRX_obs_cuts',
]

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

samplesPrint =['Samples','VBFH125',
          'ggFH125',
          'VH125',
          'Z QCD',
          'Z EWK',
          'W QCD',
          'W EWK',
          'ttbar',
          'QCD',
          'eleFakes',
          'multijet',
          'data',
          'total bkg','data/bkg'
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
#f=ROOT.TFile.Open('SumHF_BaselineCuts_ZeroPhoton_BaseLepVeto_AllSyst_v26c_DPhiFix.root')
#f=ROOT.TFile.Open('SumHF_BaselineCuts_ZeroPhoton_AllSyst_v26c_DPhiFix.root')
#f=ROOT.TFile.Open('SumHF_LooseCuts_ZeroPhoton_SystAll_Extension_DPhijjMjjBinningNjetBinDilepTrig_v26c_DPhiFix.root')
#f=ROOT.TFile.Open('SumHF_LooseCuts_ZeroPhoton_AllSyst_Madgraph_v26c_DPhiFix.root')
#f=ROOT.TFile.Open('SumHF_LooseCuts_ZeroPhoton_AllSyst_v26c_DPhiFix.root')
#f=ROOT.TFile.Open('SumHF_BaselineCuts_ZeroPhoton_AllSyst_Extension_v26c_DPhiFix.root')
#f=ROOT.TFile.Open('SumHF_BaselineCuts_ZeroPhoton_AllSyst_v26c_DPhiFix.root')
#f=ROOT.TFile.Open('SumHF_LooseCuts_ZeroPhoton_AllSyst_Extension_v26c_DPhiFix.root')
#f=ROOT.TFile.Open('SumHF_LooseCuts_ZeroPhoton_NominalOnly_Extension_DPhijjMjjBinningNjetBinDilepTrig_v26c_DPhiFix.root')
#f=ROOT.TFile.Open('/home/schae/testarea/HInv/runLoosev26Syst/SumHF_LooseCuts_ZeroPhoton_NominalOnly_Extension_DPhijjMjjBinningNjetBin_v26c_DPhiFix_QCDEst_J400.root')
#f=ROOT.TFile.Open('SumHF_BaselineCuts_ZeroPhoton_AllSyst_v26c_DPhiFix_J400.root')
#f=ROOT.TFile.Open('SumHF_BaselineCuts_ZeroPhoton_Nominal_v26c_DPhiFix_J400_XSSig.root')
#f=ROOT.TFile.Open('SumHF_BaselineCuts_ZeroPhoton_AllSyst_Extension_v26c_DPhiFix_J400_XSSig.root')
#f=ROOT.TFile.Open('SumHF_BaselineCuts_ZeroPhoton_AllSyst_v26c_DPhiFix_J400.root')
#f=ROOT.TFile.Open('SumHF_BaselineCuts_ZeroPhoton_AllSyst_v26c_DPhiFix.root')
#f=ROOT.TFile.Open('SumHF_LooseCuts_ZeroPhoton_Syst_Extension_DPhijjMjjBinningNjetBinDilepTrig_v26c_DPhiFixQCDEst_J400_XSSig_METTenac.root')
#f=ROOT.TFile.Open('SumHF_LooseCuts_ZeroPhoton_Syst_Extension_DPhijjMjjBinningNjetBinDilepTrig_v26c_DPhiFixQCDEst_J400_XSSig_METMuonTrigOR.root')
#f=ROOT.TFile.Open('SumHF_BaselineCuts_ZeroPhoton_AllSyst_v26c_DPhiFix_J400_XSSig.root')
#f=ROOT.TFile.Open('SumHF_LooseCuts_ZeroPhoton_Syst_Extension_DPhijjMjjBinningNjetBinDilepTrig_v26c_DPhiFixQCDEst_J400_XSSig_METMuonTrigOR_BaseLep.root')
#f=ROOT.TFile.Open('SumHF_delete.root')
#f=ROOT.TFile.Open('SumHF_LooseCuts_ZeroPhoton_Syst_7binMETTenac_v26c_DPhiFixQCDEst_J400_XSSig_TopFix_TrigFix.root')
#f=ROOT.TFile.Open('/home/schae/testarea/HInv/runLoosev26/SumHF_LooseCuts_ZeroPhoton_Syst_7binMET_v26c_DPhiFixQCDEst_J400_XSSig_final.root')
#f=ROOT.TFile.Open('SumHF_LooseCuts_ZeroPhoton_Syst_7binMET_v26c_DPhiFixQCDEst_J400_XSSig_updateXESF_doPlot.root')
#f=ROOT.TFile.Open('SumHF_LooseCuts_ZeroPhoton_Syst_7binMET_v26c_DPhiFixQCDEst_J400_XSSig_updateXESF_UpdateMETSF_doPlot.root')
#f=ROOT.TFile.Open('SumHF_LooseCuts_ZeroPhoton_Syst_7binMET_v26c_DPhiFixQCDEst_J400_XSSig_updateXESF_Tenac_UpdateMETSF_METTrig.root')
#f=ROOT.TFile.Open('SumHF_LooseCuts_ZeroPhoton_Syst_7binMET_v26c_DPhiFixQCDEst_J400_XSSig_updateXESF_Tenac_UpdateMETSF.root')
#f=ROOT.TFile.Open('SumHF_LooseCuts_ZeroPhoton_Syst_7binMET_v26c_DPhiFixQCDEst_J400_XSSig_updateXESF_Tenac_UpdateMETSF_lepMETTrig.root')
#f=ROOT.TFile.Open('SumHF_LooseCuts_ZeroPhoton_Nominal_r207Ana_UpdateMETSF.root')
#f=ROOT.TFile.Open('SumHF_BaselineCuts_ZeroPhoton_AllSyst_Extension_v26c_DPhiFix_J400_XSSig_badTrig.root')
#f=ROOT.TFile.Open('Sum_NominalOnly_QG.root')
#f=ROOT.TFile.Open('SumHF_LooseCuts_ZeroPhoton_Syst_7binMET_v26c_DPhiFixQCDEst_J400_XSSig_updateXESF_UpdateMETSF.root')
#f=ROOT.TFile.Open('SumHF_NoTrigSFbutLepTrig.root')
#f=ROOT.TFile.Open('SumHF_NoTrigSF.root')
#f=ROOT.TFile.Open('SumHF_LooseCuts_ZeroPhoton_Syst_7binMET_v26c_DPhiFixQCDEst_J400_XSSig_updateXESF_UpdateMETSF.root')
#f=ROOT.TFile.Open('SumHF_nobveto.root')
#f=ROOT.TFile.Open('SumHF_bveto.root')
#f=ROOT.TFile.Open('SumHF_bveto_MuonMETOnly.root')
#f=ROOT.TFile.Open('SumHF_bveto_MuonMETOR.root')
#f=ROOT.TFile.Open('/tmp/Sum_NominalOnly_noQGBins.root')
#f=ROOT.TFile.Open('/tmp/Sum_NominalOnly_QG.root')
#f=ROOT.TFile.Open('SumHF_tmva.root')
#f=ROOT.TFile.Open('SumHF_tmva_11var.root')
#f=ROOT.TFile.Open('SumHF_tmva_11var_mjj800SoftDPhi2.root')
#f=ROOT.TFile.Open('SumHF_tmva_11var_mjj900.root')
#f=ROOT.TFile.Open('SumHF_tmva_11vartest4.root')
f=ROOT.TFile.Open('SumHF_v26_var9_metTenacT5.root')
#f=ROOT.TFile.Open('SumHF_BaselineCuts_ZeroPhoton_Nominal_r207Ana_UpdateMETSF.root')
#f=ROOT.TFile.Open('SumHF_BaselineCuts_ZeroPhoton_AllSyst_v26c_DPhiFix_J400.root')
#f=ROOT.TFile.Open('SumHF_BaselineCuts_ZeroPhoton_AllSyst_Extension_v26c_DPhiFix_J400.root')#
#f=ROOT.TFile.Open('SumHF_LooseCuts_ZeroPhoton_Syst_Extension_DPhijjMjjBinningNjetBinDilepTrig_v26c_DPhiFixQCDEst_J400_SigXS.root')
#f=ROOT.TFile.Open('SumHF_LooseCuts_ZeroPhoton_Syst_Extension_DPhijjMjjBinningNjetBinDilepTrig_v26c_DPhiFix_QCDEst.root')
#f=ROOT.TFile.Open('SumHF_LooseCuts_ZeroPhoton_Syst_Extension_DPhijjMjjBinningNjetBin_v26c_DPhiFixQCDEst_J400_SigXS.root')
#f=ROOT.TFile.Open('SumHF_LooseCuts_ZeroPhoton_Syst_Extension_DPhijjMjjBinningNjetBin_v26c_DPhiFixQCDEst_J400_XSSig.root')
#f=ROOT.TFile.Open('SumHF_LooseCuts_ZeroPhoton_Syst_Extension_DPhijjMjjBinningNjetBinDilepTrig_v26c_DPhiFixQCDEst_J400_XSSig.root')
#f=ROOT.TFile.Open('SumHF_LooseCuts_ZeroPhoton_Syst_Extension_DPhijjMjjBinningNjetBinDilepTrig_v26c_DPhiFixQCDEst_J400.root')
#f=ROOT.TFile.Open('SumHF_LooseCuts_ZeroPhoton_NominalOnly_Extension_LooseLepDilepTrig_v26c_DPhiFix.root')
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

region_cf=[]
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
                if s=='hVBFH125_' or s=='hggFH125_' or s=='hVH125_':
                    line+=''
                elif s!='hdata_':
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
        if lineData<1.0:
            lineData=1.0
        if lineBkg<1.0:
            lineBkg=1.0
        line +='%0.3f +/- %0.3f\t' %(lineData/lineBkg, math.sqrt(1./lineData+bkgFracErr**2)*(lineData/lineBkg))
        print line
        nRegion+=1
        if nRegion==sTot:
            nRegion=0
            totalData=0
            totalBkg=0
            totalBkgErr=0
            rline='Sum\t'
            sreg=['Region']
            if r.count('twoEle'):  sreg=['Zee']
            elif r.count('twoMu'):  sreg=['Zmm']
            elif r.count('oneEleNegLowSigC'):  sreg=['WenminusLowMetSig']
            elif r.count('oneElePosLowSigC'):  sreg=['WenplusLowMetSig']
            elif r.count('oneEleNeg'):  sreg=['Wenminus']
            elif r.count('oneElePos'):  sreg=['Wenplus']
            elif r.count('oneMuNeg'):  sreg=['Wmnminus']
            elif r.count('oneMuPos'):  sreg=['Wmnplus']
            elif r.count('_SR'):  sreg=['SR']
            for su in range(0,len(SumList)):
                sreg+=[SumList[su]]
                #rline+='%0.2f\t' %(SumList[su])
                rline+='%0.2f +/- %0.2f\t' %(SumList[su],math.sqrt(SumErrList[su]))
                if samples[su]=='hVBFH125_' or samples[su]=='hggFH125_' or samples[su]=='hVH125_':
                    pass
                elif samples[su]!='hdata_':
                    totalBkg+=SumList[su]
                    totalBkgErr+=SumErrList[su]
                else:
                    totalData=SumList[su]
            sreg+=[totalBkg]
            region_cf+=[sreg]            
            #bkgFracErr
            totalBkgFracErr = math.sqrt(totalBkgErr)/totalBkg
            rline+='%0.3f\t%0.3f +/- %0.3f\t' %(totalBkgFracErr, totalData/totalBkg, math.sqrt(totalBkgFracErr**2+1./totalData)*(totalData/totalBkg))
            print rline
print 'done'

print ''
print '\\resizebox{\\textwidth}{!}{ '
print '\\begin{tabular}{l|ccccccccc}'
cline=''
for b in range(0,len(region_cf[0])+1):
    cline=samplesPrint[b]+'\t& '
    for r in range(0,len(region_cf)):
    #for b in range(0,len(samples)+2):
        extra=''
        if b==0:
            cline+='%s\t& ' %(region_cf[r][b])
            extra='\\hline\\hline'
        elif b>=len(region_cf[0]):
            cline+='%0.3f\t& ' %(region_cf[r][b-2]/region_cf[r][b-1] )
        elif b==len(region_cf[0])-2:# data
            cline+='%0.0f\t& ' %(region_cf[r][b])
        else:
            cline+='%0.1f\t& ' %(region_cf[r][b] )
            if b==len(region_cf[0])-3:# mj
                extra='\\hline\\hline'
            if b==len(region_cf[0])-1:# total bkg
                extra='\\hline'
    print cline.rstrip().rstrip('&')+'\\\\'+extra
    cline=''
print '\\end{tabular}'
print '}'
sys.exit(0)
# Collect systematics
tobj = f.GetListOfKeys()
mye=ROOT.Double(0.0)
for sample in samples:
    for i in tobj:
    
        vname=i.GetName()
        #print vname
        #if vname.count('VBFjetSel') and vname.count('_SR1_obs_cuts') and vname.count(sample):
        if vname.count('VBFjetSel') and vname.count('_oneEleNegLowSigCR3_') and vname.count(sample):
            h=f.Get(vname)
            intBkg=h.IntegralAndError(0,1001,mye)
            #print '%0.2f ' %(intBkg)+vname 
            print '%0.2f +/- %0.2f ' %(intBkg,mye)+vname 
