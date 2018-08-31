#!/usr/bin/env python
import ROOT

def writeMultiJet():
    multijets = [7.13, 2.24, 0.45]
    a = 1

    f_multijet = ROOT.TFile("multijet.root", "recreate")
    for multijet in multijets:
        hist = ROOT.TH1F("hmultijet_VBFjetSel_"+str(a)+"Nom_SR"+str(a)+"_obs_cuts", "hmultijet_VBFjetSel_"+str(a)+"Nom_SR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
        hist.SetBinContent(1,multijet)
        hist.Write()
        a += 1
    f_multijet.Write()
    f_multijet.Close()

def writeFakeEle():
    f_fakeele = ROOT.TFile("fakeele.root", "recreate")
    fakeelesp = [9, 9.7, 5]
    fakeelesm = [9, 9.7, 5]
    a = 1
    for fakeelep in fakeelesp:
        fakeelem = fakeelesm[a-1]
        histpLowSig = ROOT.TH1F("heleFakes_VBFjetSel_"+str(a)+"Nom_oneElePosLowSigCR"+str(a)+"_obs_cuts", "heleFakes_VBFjetSel_"+str(a)+"Nom_oneElePosLowSigCR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
        histmLowSig = ROOT.TH1F("heleFakes_VBFjetSel_"+str(a)+"Nom_oneEleNegLowSigCR"+str(a)+"_obs_cuts", "heleFakes_VBFjetSel_"+str(a)+"Nom_oneEleNegLowSigCR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
        histpLowSig.SetBinContent(1,fakeelep)
        histmLowSig.SetBinContent(1,fakeelem)
        histpLowSig.Write()
        histmLowSig.Write()
        histp = ROOT.TH1F("heleFakes_VBFjetSel_"+str(a)+"Nom_oneElePosCR"+str(a)+"_obs_cuts", "heleFakes_VBFjetSel_"+str(a)+"Nom_oneElePosCR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
        histm = ROOT.TH1F("heleFakes_VBFjetSel_"+str(a)+"Nom_oneEleNegCR"+str(a)+"_obs_cuts", "heleFakes_VBFjetSel_"+str(a)+"Nom_oneEleNegCR"+str(a)+"_obs_cuts;;", 1, 0.5, 1.5)
        histp.SetBinContent(1,1)
        histm.SetBinContent(1,1)
        histp.Write()
        histm.Write()
        a += 1
    f_fakeele.Write()
    f_fakeele.Close()
