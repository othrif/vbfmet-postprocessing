#!/usr/bin/env python
import ROOT
import os
def writeMultiJet(Binning=0, year=2016, METCut=150, doDoubleRatio=False, singleHist=False):
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
        #multijets = [109., 130., 37., 34., 4., 91., 99., 42., 24., 0., 86.0] # MET>150 older non jet/etmiss resolution
        #multijets_statunc = [16.0,18.2,8.91,10.6,3.27,15.3,14.0,9.04,6.27,0.2,13.86]
        #multijets = [169.6, 151.2, 57.0, 31.4, 3.4, 125.1, 166.0, 72.5, 25.3, 2.6, 160.5] # MET>150
        #multijets_statunc = [43.1,36.7,12.1,10.4,2.8,22.6,28.0,17.1,9.3,2.6,26.5]
        multijets=[88.1, 102.9, 32.3, 21.3, 1.6, 69.5, 127.1, 35.7, 23.1, 0.0,56.4]
        multijets_statunc=[12.2, 13.2, 4.7, 5.3, 0.9, 7.0, 12.8, 5.2, 5.2, 0.2,11.1]
        if METCut>150:
            tmpmj=[88.1, 102.9, 32.3, 21.3, 1.6, 69.5, 127.1, 35.7, 23.1, 0.0, 56.4]
            tmpmj_statunc=[12.2, 13.2, 4.7, 5.3, 0.9, 7.0, 12.8, 5.2, 5.2, 0.2,11.1]
            #tmpmj = [169.6, 151.2, 57.0, 31.4, 3.4, 125.1, 166.0, 72.5, 25.3, 2.6, 160.5] # MET>150
            #tmpmj_statunc = [43.1,36.7,12.1,10.4,2.8,22.6,28.0,17.1,9.3,2.6,26.5]
            #tmpmj = [19.5, 32.0, 15.5, 11.0, 3.5, 9.0, 22.0, 10.0, 4.0, 2.0, 13.0]; multijets=[]  # MET>150
            #multijets = [79.2, 125.1, 51.2, 20.9, 2.7, 94.2, 118.0, 58.4, 13.6, 2.6, 108.3] # MET>150
            #multijets_statunc = [16.1,35.5,11.6,7.7,2.7,19.3,21.8,13.5,5.7,2.6,19.0]
            multijets=[]; multijets_statunc=[];
            MJSF=0.659
            if METCut==160: 
                MJSF=0.659
                #multijets = [66.6, 78.6, 28.7, 18.1, 1.5, 49.2, 79.6, 23.9, 21.0, 0., 27.0] # MET>150
                #multijets_statunc = [19.8,23.1,8.4,8.7,1.5,9.3,13.3,6.8,7.3,0.2,7.2]
            if METCut==165: 
                MJSF=0.5434
            if METCut==170:
                MJSF=0.4518
            if METCut==180:
                MJSF=0.659
            for i in range(0,len(tmpmj)):
                multijets+=[(MJSF)*tmpmj[i]] # MET>160... from scaling to low mjj
                multijets_statunc+=[(MJSF)*tmpmj_statunc[i]] # MET>160... from scaling to low mjj
    # MJ for other years
    if year==2017:
        if Binning==11:
            #multijets=[]; tmpmj = [191.3, 409.8, 102.7, 23.6, 8.5, 47.3, 101.2, 25.4, 5.8, 2.1, 55.5]
            #for i in tmpmj: multijets+=[(0.046/0.035)*i] # MET>150... from scaling to low mjj
            #multijets= [180., 169., 59., 28., 0., 61., 137., 75., 29., 0.0, 63.0]
            #multijets_statunc = [30.82,23.25,16.64,8.466,0.2,11.49,18.10,24.05,7.327,0.2,10.53] # older non-ggF
            #multijets= [169.6, 151.2, 57., 31.4, 3.4, 125.1, 166.1, 72.5, 25.3, 2.6, 160.5]
            #multijets_statunc = [43.1,36.7,12.1,10.4,2.8,22.6,28.0,17.1,9.3,2.6,26.5]
            multijets=[166.1, 194.1, 61.0, 40.2, 3.1, 131.1, 239.7, 67.3, 43.5, 0.0,188.5]
            multijets_statunc=[23.0, 24.9, 8.8, 10.0, 1.6, 13.2, 24.2, 9.9, 9.9, 0.2,31.2]
            tmpmj=[166.1, 194.1, 61.0, 40.2, 3.1, 131.1, 239.7, 67.3, 43.5, 0.0,188.5]
            tmpmj_statunc=[23.0, 24.9, 8.8, 10.0, 1.6, 13.2, 24.2, 9.9, 9.9, 0.2,31.2]
            if METCut>150:
                multijets=[]; multijets_statunc=[];
                MJSF=0.6991
                if METCut==160:
                    MJSF=0.6991
                    #multijets= [79., 125., 51., 20.8, 2.7, 94.2, 118., 58., 13.6, 2.6, 108.2]
                    #multijets_statunc = [16.1,35.5,11.6,7.7,2.7,19.2,21.8,13.5,5.7,2.6,19.0]
                elif METCut==165: 
                    MJSF=0.62322
                elif METCut==170: 
                    MJSF=0.540
                elif METCut==180: 
                    MJSF=0.659 # note computed
                for i in range(0,len(tmpmj)):
                    multijets+=[(MJSF)*tmpmj[i]] # MET>160... from scaling to low mjj
                    multijets_statunc+=[(MJSF)*tmpmj_statunc[i]] # MET>160... from scaling to low mjj
        else:
            print 'MJ is not defined for binning: ',Binning
    elif year==2018:
        if Binning==11:
            #multijets = [191.3, 409.8, 102.7, 23.6, 8.5, 47.3, 101.2, 25.4, 5.8, 2.1, 55.5] # MET>150... from scaling to low mjj
            #multijets = [142., 169., 48., 33., 0.0, 672., 122.0, 35.0, 25.0, 3.0, 108.0] # MET>150... from scaling to low mjj
            #multijets_statunc = [17.67,24.18,11.60,9.103,0.2,332.0,15.31,9.972,7.693,1.852,20.80] # older values
            #multijets = [176.8, 291.8, 54.0, 49.1, 2.95, 336., 144.7, 76.1, 68.7, 0.0, 331.0] # MET>150... from scaling to low mjj
            #multijets_statunc = [31.8,52.1,15.5,25.5,2.95,69.5,23.5,19.1,29.4,0.2,58.7]
            multijets=[210.7, 246.2, 77.3, 51.0, 3.9, 166.3, 304.0, 85.3, 55.2, 0.0, 331.0]
            multijets_stat=[29.2, 31.6, 11.2, 12.6, 2.1, 16.7, 30.6, 12.5, 12.5, 0.2, 58.7]
            tmpmj=[210.7, 246.2, 77.3, 51.0, 3.9, 166.3, 304.0, 85.3, 55.2, 0.0, 331.0]
            tmpmj_statunc=[29.2, 31.6, 11.2, 12.6, 2.1, 16.7, 30.6, 12.5, 12.5, 0.2, 58.7]
            if METCut>150:
                multijets=[]; multijets_statunc=[];
                MJSF=0.7655
                #multijets = [250., 120., 48.9, 25.3, 2.9, 260., 108., 44.3, 33.4, 0.0, 278.8] # MET>150... from scaling to low mjj
                #   multijets_statunc = [49.0,23.4,14.6,9.1,2.9,60.9,19.8,12.1,10.9,0.2,54.8]
                if METCut==160:
                    MJSF=0.7655
                elif METCut==165: 
                    MJSF=0.6634
                elif METCut==170:
                    MJSF=0.59065
                elif METCut==180:
                    MJSF=0.5 # not computed
                for i in range(0,len(tmpmj)):
                    multijets+=[(MJSF)*tmpmj[i]] # MET>160... from scaling to low mjj
                    multijets_statunc+=[(MJSF)*tmpmj_statunc[i]] # MET>160... from scaling to low mjj
        elif Binning==0:
            multijets = [400, 200, 200]
        elif Binning==6:
            multijets = [300.0, 135, 120.0, 70.0, 120.0, 120.0, 50.0]
        else:
            print 'MJ is not defined for binning: ',Binning

    if doDoubleRatio:
        multijets+=[300.0]
    a = 1
    f_multijet = ROOT.TFile("multijet.root", "recreate")    
    if not singleHist:
        for multijet in multijets:
            hist=None
            histClosUp=[]
            histClosDw=[]
            if doDoubleRatio and a==(len(multijets)):
                hist   = ROOT.TH1F("hmultijet_antiVBFSel_1Nom_AVBFCR1_obs_cuts", "hmultijet_VBFjetSel_1Nom_AVBFCR1_obs_cuts;;", 1, 0.5, 1.5)
                histUp = ROOT.TH1F("hmultijet_antiVBFSel_1MJUncHigh_AVBFCR1_obs_cuts", "hmultijet_VBFjetSel_1MJUncHigh_AVBFCR1_obs_cuts;;", 1, 0.5, 1.5)
                histDw = ROOT.TH1F("hmultijet_antiVBFSel_1MJUncLow_AVBFCR1_obs_cuts", "hmultijet_VBFjetSel_1MJUncLow_AVBFCR1_obs_cuts;;", 1, 0.5, 1.5)
                for yea in [2016, 2017, 2018]:
                    histClosUp +=[ ROOT.TH1F("hmultijet_antiVBFSel_1MJClos%sUncHigh_AVBFCR1_obs_cuts" %yea, "hmultijet_VBFjetSel_1MJClos%sUncHigh_AVBFCR1_obs_cuts;;" %yea, 1, 0.5, 1.5)]
                    histClosDw +=[ ROOT.TH1F("hmultijet_antiVBFSel_1MJClos%sUncLow_AVBFCR1_obs_cuts" %yea, "hmultijet_VBFjetSel_1MJClos%sUncLow_AVBFCR1_obs_cuts;;" %yea, 1, 0.5, 1.5) ]
            else:
                hist   = ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"Nom_SR"+str(a)+"_obs_cuts", "hmultijet_VBFjetSel_"+str(a)+"Nom_SR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
                histUp = ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"MJUncHigh_SR"+str(a)+"_obs_cuts", "hmultijet_VBFjetSel_"+str(a)+"MJUncHigh_SR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
                histDw = ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"MJUncLow_SR"+str(a)+"_obs_cuts", "hmultijet_VBFjetSel_"+str(a)+"MJUncLow_SR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
                for yea in [2016, 2017, 2018]:
                    histClosUp += [ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"MJClos%sUncHigh_SR" %yea+str(a)+"_obs_cuts", "hmultijet_VBFjetSel_"+str(a)+"MJClos%sUncHigh_SR" %yea+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)]
                    histClosDw += [ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"MJClos%sUncLow_SR" %yea+str(a)+"_obs_cuts", "hmultijet_VBFjetSel_"+str(a)+"MJClos%sUncLow_SR" %yea+str(a)+"_obs_cuts;;", 1, 0.5, 1.5) ]
            hist.SetBinContent(1,multijet)
            #hist.SetBinError(1,multijet*0.25)
            hist.SetBinError(1,multijets_statunc[a-1]) # stat uncertainty
            histUp.SetBinContent(1,multijet*1.387)
            histUp.SetBinError(1,0.0)
            histDw.SetBinContent(1,multijet/1.387)
            histDw.SetBinError(1,0.0)
            # setting the default value
            for itr in range(0,len(histClosUp)):
                histClosUp[itr].SetBinContent(1,multijet) 
                histClosUp[itr].SetBinError(1,0.0)
                histClosDw[itr].SetBinContent(1,multijet)
                histClosDw[itr].SetBinError(1,0.0)                    
            if  year==2016:
                histClosUp[0].SetBinContent(1,multijet*1.8) # set to 100%. total is 2813, so need 675/2813. this is not correlated.
                histClosDw[0].SetBinContent(1,multijet/1.8)
            if  year==2017:
                histUp.SetBinContent(1,multijet*1.189)
                histDw.SetBinContent(1,multijet/1.189)
                histClosUp[1].SetBinContent(1,multijet*1.47) # set to 100%. total is 2813, so need 421/2813. this is not correlated.
                histClosDw[1].SetBinContent(1,multijet/1.47)
            if  year==2018:
                histUp.SetBinContent(1,multijet*1.226)
                histDw.SetBinContent(1,multijet/1.226)
                histClosUp[2].SetBinContent(1,multijet*1.43) # set to 100%. total is 2813, so need 401/2813. this is not correlated.
                histClosDw[2].SetBinContent(1,multijet/1.43)
            hist.Write()
            histUp.Write()
            histDw.Write()
            for itr in range(0,len(histClosUp)):
                histClosUp[itr].Write()
                histClosDw[itr].Write()
            a += 1
    else: # write a single histogram
        histClosUp=[]
        histClosDw=[]
        a=89
        b=1
        nbins=len(multijets)*9
        hist   = ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"Nom_SR"+str(a)+"_obs_cuts", "hmultijet_VBFjetSel_"+str(a)+"Nom_SR"+str(a)+"_obs_cuts;;", nbins, 0.5, nbins+0.5)
        histUp = ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"MJUncHigh_SR"+str(a)+"_obs_cuts", "hmultijet_VBFjetSel_"+str(a)+"MJUncHigh_SR"+str(a)+"_obs_cuts;;", nbins, 0.5, nbins+0.5)
        histDw = ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"MJUncLow_SR"+str(a)+"_obs_cuts", "hmultijet_VBFjetSel_"+str(a)+"MJUncLow_SR"+str(a)+"_obs_cuts;;", nbins, 0.5, nbins+0.5)
        for yea in [2016, 2017, 2018]:
            histClosUp += [ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"MJClos%sUncHigh_SR" %yea+str(a)+"_obs_cuts", "hmultijet_VBFjetSel_"+str(a)+"MJClos%sUncHigh_SR" %yea+str(a)+"_obs_cuts;;", nbins, 0.5, nbins+0.5)]
            histClosDw += [ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"MJClos%sUncLow_SR" %yea+str(a)+"_obs_cuts", "hmultijet_VBFjetSel_"+str(a)+"MJClos%sUncLow_SR" %yea+str(a)+"_obs_cuts;;", nbins, 0.5, nbins+0.5) ]
        for multijet in multijets:
            print multijet
            hist.SetBinContent(a,multijet)
            hist.SetBinError(a,multijets_statunc[b-1]) # stat uncertainty
            histUp.SetBinContent(a,multijet*1.28)
            histUp.SetBinError(a,0.0)
            histDw.SetBinContent(a,multijet/1.28)
            histDw.SetBinError(a,0.0)
            # setting the default value
            for itr in range(0,len(histClosUp)):
                histClosUp[itr].SetBinContent(a,multijet) 
                histClosUp[itr].SetBinError(a,0.0)
                histClosDw[itr].SetBinContent(a,multijet)
                histClosDw[itr].SetBinError(a,0.0)                    
            if  year==2016:
                histClosUp[0].SetBinContent(a,multijet*1.8) # set to 100%. total is 2813, so need 675/2813. this is not correlated.
                histClosDw[0].SetBinContent(a,multijet/1.8)
            if  year==2017:
                histUp.SetBinContent(a,multijet*1.25) 
                histDw.SetBinContent(a,multijet/1.25)
                histClosUp[1].SetBinContent(a,multijet*1.5) # set to 100%. total is 2813, so need 421/2813. this is not correlated.
                histClosDw[1].SetBinContent(a,multijet/1.5)
            if  year==2018:
                histUp.SetBinContent(a,multijet*1.22)
                histDw.SetBinContent(a,multijet/1.22)
                histClosUp[2].SetBinContent(a,multijet*1.32) # set to 100%. total is 2813, so need 401/2813. this is not correlated.
                histClosDw[2].SetBinContent(a,multijet/1.32)

            a+=1
            b+=1
        # writing output
        hist.Write()
        histUp.Write()
        histDw.Write()
        for itr in range(0,len(histClosUp)):
            histClosUp[itr].Write()
            histClosDw[itr].Write()
    #f_multijet.Write()
    f_multijet.Close()
 
def writeFakeEle(Binning=0, year=2016, doDoubleRatio=False, singleHist=False):

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
        #fakeelesp = [8.3, 11.1, 6.7, 4.0, 1.9, 8.3, 11.1, 6.7, 4.0, 1.9, 9.1]
        #fakeelesm = [8.3, 11.1, 6.7, 4.0, 1.9, 8.3, 11.1, 6.7, 4.0, 1.9, 9.1] # met>150 numbers
        fakeelesp = [8.4, 11.0, 6.6, 3.9, 1.9, 8.4, 11.0, 6.6, 3.9, 1.9, 7.0]
        fakeelesm = [8.4, 11.0, 6.6, 3.9, 1.9, 8.4, 11.0, 6.6, 3.9, 1.9, 7.0]

    if doDoubleRatio:
        fakeelesp+=[12.5]
        fakeelesm+=[12.5]
    a = 1
    if not singleHist:
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
    else: # write out a single histogram
        nbins=len(fakeelesp)*9
        binshift=len(fakeelesp)
        a=1
        histp = ROOT.TH1F("heleFakes_VBFjetSel_"+str(a)+"Nom_SR"+str(a)+"_obs_cuts", "heleFakes_VBFjetSel_"+str(a)+"Nom_SR"+str(a)+"_obs_cuts;;", nbins, 0.5, nbins+0.5)
        histm = ROOT.TH1F("heleFakes_VBFjetSel_"+str(a)+"Nom_SR"+str(a)+"_obs_cuts", "heleFakes_VBFjetSel_"+str(a)+"Nom_SR"+str(a)+"_obs_cuts;;", nbins, 0.5, nbins+0.5) 

        for fakeelep in fakeelesp:
            fakeelem = fakeelesm[a-1]
            histp.SetBinContent(a+binshift*3,1)
            histm.SetBinContent(a+binshift*2,1)
            a += 1
        histp.Write()
        histm.Write()
    #f_fakeele.Write()
    f_fakeele.Close()
#writeMultiJet(11, 2016, 150)
#writeMultiJet(11, 2016, 170)
#os.chdir('../v34D')
#writeMultiJet(11, 2017, 150)
#os.chdir('../v34E')
#writeMultiJet(11, 2018, 150)
#writeFakeEle(11,  2018)
