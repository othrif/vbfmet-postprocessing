#!/usr/bin/env python
import ROOT
import os
def writeMultiJet(Binning=0, year=2016, METCut=150, doDoubleRatio=False):
    multijets = [7.13, 2.24, 0.45]
    #multijets = [3.0, 0.5, 0.1]
    #multijets = [58.+3.0, 28.0+0.5, 26.0+0.1]
    if Binning==-1:
        multijets = [31.0, 14.5, 13.0, 30.0, 14.0, 13.0]
    if Binning==1:
        multijets = [3.0, 0.5, 0.1, 112.] 
    if Binning==2:
        multijets = [58.0, 27.5, 25.0, 5.0]
    if Binning==3:
        multijets = [3.0, 0.5, 0.1, 58.0, 27.0, 25.0]
    if Binning==4:
        multijets = [58.0, 27.5, 25.0, 4.0, 0.5, 0.5]
    if Binning==5:
        multijets = [31.0, 14.5, 13.0, 30.0, 14.0, 13.0]
    if Binning==6:
        multijets = [30.0, 13.5, 12.0, 29.0, 12.0, 12.0]
        multijets += [5.0]
    if Binning==7:
        multijets = [30.0, 13.5, 30.0, 13.5, 12.0, 29.0, 12.0, 12.0]
        multijets += [5.0]
    if Binning==8:
        multijets = [30.0, 13.5, 30.0, 13.5, 12.0, 29.0, 12.0, 12.0]
        multijets += [5.0]
    if Binning==9:
        multijets = [30.0, 13.5, 30.0, 13.5, 12.0, 29.0, 12.0, 12.0]
    if Binning==10:
        multijets = [30.0, 13.5, 30.0, 13.5, 12.0, 29.0, 10.0, 10.0, 2.0, 2.0]
        multijets += [5.0]
    if Binning==11:
        #multijets = [19.5, 32.0, 15.5, 11.0, 3.5, 9.0, 22.0, 10.0, 4.0, 2.0, 13.0] # MET>150
        multijets = [109., 130., 37., 34., 4., 91., 99., 42., 24., 0., 86.0] # MET>150
        multijets_statunc = [16.0,18.2,8.91,10.6,3.27,15.3,14.0,9.04,6.27,0.2,13.86]
        if METCut>150:
            tmpmj = [19.5, 32.0, 15.5, 11.0, 3.5, 9.0, 22.0, 10.0, 4.0, 2.0, 13.0]; multijets=[]  # MET>150
            if METCut==160: 
                for i in tmpmj: multijets+=[(0.84085024)*i] # MET>160... from scaling to low mjj
            if METCut==165: 
                for i in tmpmj: multijets+=[(0.76158444)*i] # MET>165... from scaling to low mjj
            if METCut==170: 
                for i in tmpmj: multijets+=[(0.70803802)*i] # MET>170... from scaling to low mjj
            if METCut==180: 
                for i in tmpmj: multijets+=[(0.53423362)*i] # MET>180... from scaling to low mjj
    # MJ for other years
    if year==2017:
        if Binning==11:
            #multijets=[]; tmpmj = [191.3, 409.8, 102.7, 23.6, 8.5, 47.3, 101.2, 25.4, 5.8, 2.1, 55.5]
            #for i in tmpmj: multijets+=[(0.046/0.035)*i] # MET>150... from scaling to low mjj
            multijets= [180., 169., 59., 28., 0., 61., 137., 75., 29., 0.0, 63.0]
            multijets_statunc = [30.82,23.25,16.64,8.466,0.2,11.49,18.10,24.05,7.327,0.2,10.53]
            if METCut==160: 
                for i in tmpmj: multijets+=[(0.84085024)*(0.046/0.035)*i] # MET>160... from scaling to low mjj                
            if METCut==165: 
                for i in tmpmj: multijets+=[(0.76158444)*(0.046/0.035)*i] # MET>165... from scaling to low mjj                
            if METCut==170: 
                for i in tmpmj: multijets+=[(0.70803802)*(0.046/0.035)*i] # MET>170... from scaling to low mjj                
            if METCut==180: 
                for i in tmpmj: multijets+=[(0.53423362)*(0.046/0.035)*i] # MET>180... from scaling to low mjj                
        else:
            print 'MJ is not defined for binning: ',Binning
    elif year==2018:
        if Binning==11:
            #multijets = [191.3, 409.8, 102.7, 23.6, 8.5, 47.3, 101.2, 25.4, 5.8, 2.1, 55.5] # MET>150... from scaling to low mjj
            multijets = [142., 169., 48., 33., 0.0, 672., 122.0, 35.0, 25.0, 3.0, 108.0] # MET>150... from scaling to low mjj
            multijets_statunc = [17.67,24.18,11.60,9.103,0.2,332.0,15.31,9.972,7.693,1.852,20.80]
            if METCut>150:
                tmpmj = [191.3, 409.8, 102.7, 23.6, 8.5, 47.3, 101.2, 25.4, 5.8, 2.1, 55.5]; multijets=[] # MET>150... from scaling to low mjj
                if METCut==160: 
                    for i in tmpmj: multijets+=[(0.84085024)*i] # MET>160... from scaling to low mjj
                if METCut==165: 
                    for i in tmpmj: multijets+=[(0.76158444)*i] # MET>165... from scaling to low mjj
                if METCut==170: 
                    for i in tmpmj: multijets+=[(0.70803802)*i] # MET>170... from scaling to low mjj
                if METCut==180: 
                    for i in tmpmj: multijets+=[(0.53423362)*i] # MET>180... from scaling to low mjj
        elif Binning==0:
            multijets = [400, 200, 200]
        elif Binning==6:
            multijets = [300.0, 135, 120.0, 70.0, 120.0, 120.0, 50.0]
        else:
            print 'MJ is not defined for binning: ',Binning

    if doDoubleRatio:
        multijets+=[300.0]
    a = 1
    histClosUp=None
    histClosDw=None
    f_multijet = ROOT.TFile("multijet.root", "recreate")    
    for multijet in multijets:
        hist=None
        if doDoubleRatio and a==(len(multijets)):
            hist   = ROOT.TH1F("hmultijet_antiVBFSel_1Nom_AVBFCR1_obs_cuts", "hmultijet_VBFjetSel_1Nom_AVBFCR1_obs_cuts;;", 1, 0.5, 1.5)
            histUp = ROOT.TH1F("hmultijet_antiVBFSel_1MJUncHigh_AVBFCR1_obs_cuts", "hmultijet_VBFjetSel_1MJUncHigh_AVBFCR1_obs_cuts;;", 1, 0.5, 1.5)
            histDw = ROOT.TH1F("hmultijet_antiVBFSel_1MJUncLow_AVBFCR1_obs_cuts", "hmultijet_VBFjetSel_1MJUncLow_AVBFCR1_obs_cuts;;", 1, 0.5, 1.5)
            histClosUp = ROOT.TH1F("hmultijet_antiVBFSel_1MJClos%sUncHigh_AVBFCR1_obs_cuts" %year, "hmultijet_VBFjetSel_1MJClos%sUncHigh_AVBFCR1_obs_cuts;;" %year, 1, 0.5, 1.5)
            histClosDw = ROOT.TH1F("hmultijet_antiVBFSel_1MJClos%sUncLow_AVBFCR1_obs_cuts" %year, "hmultijet_VBFjetSel_1MJClos%sUncLow_AVBFCR1_obs_cuts;;" %year, 1, 0.5, 1.5)            
        else:
            hist   = ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"Nom_SR"+str(a)+"_obs_cuts", "hmultijet_VBFjetSel_"+str(a)+"Nom_SR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
            histUp = ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"MJUncHigh_SR"+str(a)+"_obs_cuts", "hmultijet_VBFjetSel_"+str(a)+"MJUncHigh_SR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
            histDw = ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"MJUncLow_SR"+str(a)+"_obs_cuts", "hmultijet_VBFjetSel_"+str(a)+"MJUncLow_SR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
            histClosUp = ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"MJClos%sUncHigh_SR"+str(a)+"_obs_cuts" %year, "hmultijet_VBFjetSel_"+str(a)+"MJClos%sUncHigh_SR"+str(a)+"_obs_cuts;;" %year, 1, 0.5, 1.5)
            histClosDw = ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"MJClos%sUncLow_SR"+str(a)+"_obs_cuts" %year, "hmultijet_VBFjetSel_"+str(a)+"MJClos%sUncLow_SR"+str(a)+"_obs_cuts;;" %year, 1, 0.5, 1.5) 
        hist.SetBinContent(1,multijet)
        #hist.SetBinError(1,multijet*0.25)
        hist.SetBinError(1,multijets_statunc[a-1]) # stat uncertainty
        histUp.SetBinContent(1,multijet*1.25)
        histUp.SetBinError(1,0.0)
        histDw.SetBinContent(1,multijet/1.25)
        histDw.SetBinError(1,0.0)
        histClosUp.SetBinContent(1,multijet/1.23) # set to 100%. total is 2813, so need 675/2813. this is not correlated.
        histClosUp.SetBinError(1,0.0)
        histClosDw.SetBinContent(1,multijet*1.23)
        histClosDw.SetBinError(1,0.0)        
        if  year==2017:
            histUp.SetBinContent(1,multijet*1.61) 
            histUp.SetBinError(1,0.0)
            histDw.SetBinContent(1,multijet/1.61)
            histDw.SetBinError(1,0.0)    
            histClosUp.SetBinContent(1,multijet*1.15) # set to 100%. total is 2813, so need 421/2813. this is not correlated.
            histClosUp.SetBinError(1,0.0)
            histClosDw.SetBinContent(1,multijet/1.15)
            histClosDw.SetBinError(1,0.0)
        if  year==2018:
            histUp.SetBinContent(1,multijet*1.56)
            histUp.SetBinError(1,0.0)
            histDw.SetBinContent(1,multijet/1.56)
            histDw.SetBinError(1,0.0)
            histClosUp.SetBinContent(1,multijet*1.14) # set to 100%. total is 2813, so need 401/2813. this is not correlated.
            histClosUp.SetBinError(1,0.0)
            histClosDw.SetBinContent(1,multijet/1.14)
            histClosDw.SetBinError(1,0.0)
        hist.Write()
        histUp.Write()
        histDw.Write()
        histClosUp.Write()
        histClosDw.Write()        
        a += 1
    f_multijet.Write()
    f_multijet.Close()
 
def writeFakeEle(Binning=0, year=2016, doDoubleRatio=False):

    f_fakeele = ROOT.TFile("fakeele.root", "recreate")
    fakeelesp = [10.7, 11.6, 5.0]
    fakeelesm = [10.7, 11.6, 5.0]
    if Binning==1:
        fakeelesp += [9.3]
        fakeelesm += [9.3]
    if Binning==2:
        fakeelesp += [5.3]
        fakeelesm += [5.3]
    if Binning>2 or Binning==-1:
        fakeelesp = [10.4, 10.0, 5.3, 14.5, 14.2, 6.2]
        fakeelesm = [10.4, 10.0, 5.3, 14.5, 14.2, 6.2]
    if Binning==6:
        fakeelesp += [5.3]
        fakeelesm += [5.3]
    if Binning==7:
        fakeelesp = [10.4, 10.0, 10.4, 10.0, 5.3, 14.5, 14.2, 6.2,5.3]
        fakeelesm = [10.4, 10.0, 10.4, 10.0, 5.3, 14.5, 14.2, 6.2,5.3]
    if Binning==8:
        fakeelesp = [10.4, 10.0, 10.4, 10.0, 5.3, 14.5, 14.2, 6.2,5.3]
        fakeelesm = [10.4, 10.0, 10.4, 10.0, 5.3, 14.5, 14.2, 6.2,5.3]
    if Binning==9:
        fakeelesp = [10.4, 10.0, 10.4, 10.0, 5.3, 14.5, 14.2, 6.2]
        fakeelesm = [10.4, 10.0, 10.4, 10.0, 5.3, 14.5, 14.2, 6.2]
    if Binning==10:
        fakeelesp = [10.4, 10.0, 10.4, 10.0, 5.3, 14.5, 14.2, 6.2, 14.2, 6.2 ,5.3]
        fakeelesm = [10.4, 10.0, 10.4, 10.0, 5.3, 14.5, 14.2, 6.2, 14.2, 6.2, 5.3]
    if Binning==11: # set for all years
        fakeelesp = [8.3, 11.1, 6.7, 4.0, 1.9, 8.3, 11.1, 6.7, 4.0, 1.9, 9.1]
        fakeelesm = [8.3, 11.1, 6.7, 4.0, 1.9, 8.3, 11.1, 6.7, 4.0, 1.9, 9.1]

    if doDoubleRatio:
        fakeelesp+=[12.5]
        fakeelesm+=[12.5]
    a = 1
    for fakeelep in fakeelesp:
        fakeelem = fakeelesm[a-1]
        histpLowSig=None
        histmLowSig=None
        if doDoubleRatio and a==(len(fakeelesp)):
            histpLowSig = ROOT.TH1F("heleFakes_antiVBFSel_1Nom_oneElePosLowSigCR1_obs_cuts", "heleFakes_antiVBFSel_1Nom_oneElePosLowSigCR1_obs_cuts;;", 1, 0.5, 1.5)
            histmLowSig = ROOT.TH1F("heleFakes_antiVBFSel_1Nom_oneEleNegLowSigCR1_obs_cuts", "heleFakes_antiVBFSel_1Nom_oneEleNegLowSigCR1_obs_cuts;;", 1, 0.5, 1.5)
        else:
            histpLowSig = ROOT.TH1F("heleFakes_VBFjetSel_"+str(a)+"Nom_oneElePosLowSigCR"+str(a)+"_obs_cuts", "heleFakes_VBFjetSel_"+str(a)+"Nom_oneElePosLowSigCR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
            histmLowSig = ROOT.TH1F("heleFakes_VBFjetSel_"+str(a)+"Nom_oneEleNegLowSigCR"+str(a)+"_obs_cuts", "heleFakes_VBFjetSel_"+str(a)+"Nom_oneEleNegLowSigCR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
        histpLowSig.SetBinContent(1,fakeelep)
        histmLowSig.SetBinContent(1,fakeelem)
        histpLowSig.Write()
        histmLowSig.Write()
        histm=None
        histp=None
        if doDoubleRatio and a==(len(fakeelesp)):
            histp = ROOT.TH1F("heleFakes_antiVBFSel_1Nom_oneElePosACR1_obs_cuts", "heleFakes_antiVBFSel_1Nom_oneElePosACR1_obs_cuts;;", 1, 0.5, 1.5)
            histm = ROOT.TH1F("heleFakes_antiVBFSel_1Nom_oneEleNegACR1_obs_cuts", "heleFakes_antiVBFSel_1Nom_oneEleNegACR1_obs_cuts;;", 1, 0.5, 1.5)
        else:
            histp = ROOT.TH1F("heleFakes_VBFjetSel_"+str(a)+"Nom_oneElePosCR"+str(a)+"_obs_cuts", "heleFakes_VBFjetSel_"+str(a)+"Nom_oneElePosCR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
            histm = ROOT.TH1F("heleFakes_VBFjetSel_"+str(a)+"Nom_oneEleNegCR"+str(a)+"_obs_cuts", "heleFakes_VBFjetSel_"+str(a)+"Nom_oneEleNegCR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5) 
        histp.SetBinContent(1,1)
        histm.SetBinContent(1,1)
        histp.Write()
        histm.Write()
        a += 1
    f_fakeele.Write()
    f_fakeele.Close()
#writeMultiJet(11, 2016, 150)
#os.chdir('../v34D')
#writeMultiJet(11, 2017, 150)
#os.chdir('../v34E')
#writeMultiJet(11, 2018, 150)
#writeFakeEle(11,  2018)
