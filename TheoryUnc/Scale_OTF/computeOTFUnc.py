#!/usr/bin/env python

# example: python computeOTFUnc.py Z_strong SR

import os
import sys
import math
import subprocess
from ROOT import *
from array import array
import numpy as np

debug = False
basePath = "./input/allregions_final"
outPath = "./output/allregions_final"

if not os.path.exists(outPath):
    os.makedirs(outPath)

channel = sys.argv[1]
region  = sys.argv[2]
doSmooth = True
doSeperate = False

nbins    = 5
mjj_bins_arr=np.array((0.8,1.,1.5,2.,3.5,5))


theoUncUp    = {"renofact":[1.0]*21, "pdf":[1.0]*21}
theoUncDown  = {"renofact":[1.0]*21, "pdf":[1.0]*21}
theoStatUp   = {"renofact":[1.0]*21, "pdf":[1.0]*21}
theoStatDown = {"renofact":[1.0]*21, "pdf":[1.0]*21}
if doSeperate:
    theoUncUp    = {"renofact":[1.0]*21, "pdf":[1.0]*21, "fac":[1.0]*21, "renorm":[1.0]*21, "both":[1.0]*21}
    theoUncDown  = {"renofact":[1.0]*21, "pdf":[1.0]*21, "fac":[1.0]*21, "renorm":[1.0]*21, "both":[1.0]*21}
    theoStatUp   = {"renofact":[1.0]*21, "pdf":[1.0]*21, "fac":[1.0]*21, "renorm":[1.0]*21, "both":[1.0]*21}
    theoStatDown = {"renofact":[1.0]*21, "pdf":[1.0]*21, "fac":[1.0]*21, "renorm":[1.0]*21, "both":[1.0]*21}




binItrScale = 0
binItrPDF = 0
binItr ={}

listRegions=[region + "PhiLow", region + "PhiHigh", region + "Njet", region + "METlow", region + "VRPhiHigh"]
#listRegions=[region + "Phi", region + "Phi", region + "Njet", region + "METlow"]
#listRegions=[region, region, region + "Njet"]
if region == "Incl":
    listRegions=[region, region, region]
for ireg,reg in enumerate(listRegions):
    variationDict = {"nominal"     : "jj_mass_" + reg + "_nominal",
                     "fac_up"      : "scales/jj_mass_" + reg + "_fac_up",
                     "fac_down"    : "scales/jj_mass_" + reg + "_fac_down",
                     "renorm_up"   : "scales/jj_mass_" + reg + "_renorm_up",
                     "renorm_down" : "scales/jj_mass_" + reg + "_renorm_down",
                     "both_up"     : "scales/jj_mass_" + reg + "_both_up",
                     "both_down"   : "scales/jj_mass_" + reg + "_both_down"}

    pdfString = "PDF/jj_mass_" + reg + "_pdf"

    histDict = {} # scale variations
    pdfDict = {}  # pdf variations
    varDict = {}  # varied samples ckkw, qsf

    inFile = TFile.Open(basePath+"/theoVariation_"+channel+".root")
    outFile = TFile(outPath+"/variedYields_"+channel+"_"+reg+".root", "recreate")

    # Scale variations
    for scale in variationDict:
        thisHist = inFile.Get(variationDict[scale])
        if(len(thisHist.GetSumw2()) == 0):
            thisHist.Sumw2()
        histDict[scale] = thisHist.Clone("h_" + scale)
        histDict[scale]=histDict[scale].Rebin(nbins,"h_"+scale,mjj_bins_arr)
        histDict[scale].SetDirectory(0)
        histDict[scale].Write()

    # PDF variations
    for i in range(100):
        thisHist = inFile.Get(pdfString + "%i"%i)
        if(len(thisHist.GetSumw2()) == 0):
            thisHist.Sumw2()
        pdfDict[i] = thisHist.Clone("h_pdf%i"%i)
        pdfDict[i]=pdfDict[i].Rebin(nbins,"h_pdf"+str(i),mjj_bins_arr)
        pdfDict[i].SetDirectory(0)
        pdfDict[i].Write()
    inFile.Close()
    outFile.Close()

    inFile   = TFile.Open(outPath+"/variedYields_"+channel+"_"+reg+".root")
    outFile  = TFile(outPath+"/reweight_"+channel+"_"+reg+".root", "recreate")

    nomHist = inFile.Get("h_nominal")

    ########################
    # Scale variations
    ########################
    systs    = ["fac", "renorm", "both"]
    largestUp   = [1.,1.,1.,1.,1.]
    largestDown = [1.,1.,1.,1.,1.]
    err_largestUp   = [0.,0.,0.,0.,0.]
    err_largestDown = [0.,0.,0.,0.,0.]
    for syst in systs :
        upHist = inFile.Get("h_" + syst + "_up")
        downHist = inFile.Get("h_" + syst + "_down")
        reweight_up = upHist.Clone(syst + "_up")
        reweight_down = downHist.Clone(syst + "_down")
        reweight_up.Divide(upHist,nomHist,1.0,1.0,"B");
        reweight_down.Divide(downHist,nomHist,1.0,1.0,"B");
        if doSmooth:
            reweight_up.Smooth()
            reweight_down.Smooth()
        reweight_up.Write()
        reweight_down.Write()

        for i in range(nomHist.GetNbinsX()):
            variationUp = reweight_up.GetBinContent(i+1)
            variationDown = reweight_down.GetBinContent(i+1)
            err_variationUp = reweight_up.GetBinError(i+1)
            err_variationDown = reweight_down.GetBinError(i+1)
            if(math.fabs(variationUp-1) > math.fabs(largestUp[i]-1)):
                largestUp[i] = variationUp
                err_largestUp[i] = err_variationUp
            if(math.fabs(variationDown-1) > math.fabs(largestDown[i]-1)):
                largestDown[i] = variationDown
                err_largestDown[i] = err_variationDown
            if doSeperate:
                cfix=0
                if ireg == 0: # PhiLow
                    cfix=0
                if ireg == 1: # PhiHigh
                    cfix=5
                if ireg == 2: # Njet
                    cfix=10
                if ireg == 3: # MET
                    cfix=13
                if ireg == 4: # VR
                    cfix=16
                if ireg<2 or ireg==4: # PhiLow or PhiHigh
                    theoUncUp[syst][i+cfix] = reweight_up.GetBinContent(i+1)
                    theoUncDown[syst][i+cfix] = reweight_down.GetBinContent(i+1)
                    theoStatUp[syst][i+cfix] = reweight_up.GetBinError(i+1)
                    theoStatDown[syst][i+cfix] = reweight_down.GetBinError(i+1)
                elif ireg>1 and i>1:
                    theoUncUp[syst][i+cfix-2] = reweight_up.GetBinContent(i+1-2)
                    theoUncDown[syst][i+cfix-2] = reweight_down.GetBinContent(i+1-2)
                    theoStatUp[syst][i+cfix-2] = reweight_up.GetBinError(i+1-2)
                    theoStatDown[syst][i+cfix-2] = reweight_down.GetBinError(i+1-2)

    envelope_up = nomHist.Clone("envelope_up")
    envelope_down = nomHist.Clone("envelope_down")
    for i in range(nomHist.GetNbinsX()):
        envelope_up.SetBinContent(i+1, largestUp[i])
        envelope_up.SetBinError(i+1, err_largestUp[i])
        envelope_down.SetBinContent(i+1, largestDown[i])
        envelope_down.SetBinError(i+1, err_largestDown[i])
        cfix=0
        if ireg == 0: # PhiLow
            cfix=0
        if ireg == 1: # PhiHigh
            cfix=5
        if ireg == 2: # Njet
            cfix=10
        if ireg == 3: # MET
            cfix=13
        if ireg == 4: # VR
            cfix=16
        if ireg<2 or ireg==4: # PhiLow or PhiHigh or VRPhiHigh
            theoUncUp["renofact"][i+cfix] = envelope_up.GetBinContent(i+1)
            theoUncDown["renofact"][i+cfix] = envelope_down.GetBinContent(i+1)
            theoStatUp["renofact"][i+cfix] = envelope_up.GetBinError(i+1)
            theoStatDown["renofact"][i+cfix] = envelope_down.GetBinError(i+1)
        elif ireg>1 and i>1:
            theoUncUp["renofact"][i+cfix-2] = envelope_up.GetBinContent(i+1-2)
            theoUncDown["renofact"][i+cfix-2] = envelope_down.GetBinContent(i+1-2)
            theoStatUp["renofact"][i+cfix-2] = envelope_up.GetBinError(i+1)
            theoStatDown["renofact"][i+cfix-2] = envelope_down.GetBinError(i+1)
    envelope_up.Write()
    envelope_down.Write()

    ########################
    # PDF variations
    ########################
    avgNormalization = 1./100
    pdfHist = nomHist.Clone()
    for i in range(100):
        thisHist = inFile.Get("h_pdf%i"%i)
        pdfHist.Add(thisHist)
    pdfHist.Scale(avgNormalization)
    pdf_up   = nomHist.Clone("pdf_up")
    pdf_down = nomHist.Clone("pdf_down")
    for i in range(nomHist.GetNbinsX()):
        pdf_up.SetBinContent(  i+1, 1 + pdfHist.GetBinError(i+1)/pdfHist.GetBinContent(i+1))
        pdf_down.SetBinContent(i+1, 1 - pdfHist.GetBinError(i+1)/pdfHist.GetBinContent(i+1))
        pdf_up.SetBinError(  i+1, pdfHist.GetBinError(i+1))
        pdf_down.SetBinError(i+1, pdfHist.GetBinError(i+1))
        cfix=0
        if ireg == 0: # PhiLow
            cfix=0
        if ireg == 1: # PhiHigh
            cfix=5
        if ireg == 2: # Njet
            cfix=10
        if ireg == 3: # MET
            cfix=13
        if ireg == 4: # VR
            cfix=16
        if ireg<2 or ireg==4: # PhiLow or PhiHigh
            theoUncUp["pdf"][i+cfix] = pdf_up.GetBinContent(i+1)
            theoUncDown["pdf"][i+cfix] = pdf_down.GetBinContent(i+1)
            theoStatUp["pdf"][i+cfix] = pdf_up.GetBinError(i+1)
            theoStatDown["pdf"][i+cfix] = pdf_down.GetBinError(i+1)
        elif ireg>1 and i>1:
            theoUncUp["pdf"][i+cfix-2] = pdf_up.GetBinContent(i+1-2)
            theoUncDown["pdf"][i+cfix-2] = pdf_down.GetBinContent(i+1-2)
            theoStatUp["pdf"][i+cfix-2] = pdf_up.GetBinError(i+1-2)
            theoStatDown["pdf"][i+cfix-2] = pdf_down.GetBinError(i+1-2)
    if doSmooth:
        pdf_up.Smooth()
        pdf_down.Smooth()
    pdf_up.Write()
    pdf_down.Write()

inFile.Close()
outFile.Close()

print "\n\n=====================\n"
for theo in theoUncUp:
    print region+"up="+theo+"_"+channel, ",".join([str('{0:.5g}'.format(x)) for x in theoUncUp[theo]])
print ""
for theo in theoUncDown:
    print region+"down="+theo+"_"+channel, ",".join([str('{0:.5g}'.format(x)) for x in theoUncDown[theo]])
'''
print "\n\n=====================\n"
for theo in theoStatUp:
    print region+"upSTAT="+theo+"_"+channel, ",".join([str('{0:.5g}'.format(x)) for x in theoStatUp[theo]])
print ""
for theo in theoStatDown:
    print region+"downSTAT="+theo+"_"+channel, ",".join([str('{0:.5g}'.format(x)) for x in theoStatDown[theo]])
    '''
