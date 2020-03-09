# Othmane Rifki
# usage: python calculateOTFYields.py <channel> <region>
# example: python calculateOTFYields.py Z_strong SR
# Valid channels: W_strong, Z_strong
# Valid regions: SR, CRW, CRZ

#!/usr/bin/env python

import os
import sys
import math
import subprocess
from ROOT import *
from array import array


debug = True
basePath = "./input/theoVariation"
outPath = "./output/theoVariation"

if not os.path.exists(outPath):
    os.makedirs(outPath)

channel = sys.argv[1]
region  = sys.argv[2]

print "\nRunning systs for channel:", channel, region

# up, down
# renofact, pdf, resum, ckkw

theoUncUp= {     "resum"        : [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
                 "ckkw"         : [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
                 }
theoUncDown= {   "resum"        : [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
                 "ckkw"         : [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
                 }

binItr ={}
binItr["resum"] = 0
binItr["ckkw"] = 0
listRegions=[region + "PhiLow", region + "PhiHigh", region + "Njet"]
if region == "Incl":
    listRegions=[region, region, region]
for reg in listRegions:
    if (debug): print reg

    varDict = {}  # varied samples ckkw, qsf

    # varied samples
    for key in ["qsf025", "qsf4", "ckkw15", "ckkw30"]:
        inFile = TFile.Open(basePath+"/theoVariation_"+channel+"_"+key+".root")
        outFile = TFile(outPath+"/variedYields_"+channel+"_"+reg+".root", "update")
        thisHist = inFile.Get("jj_mass_" + reg + "_nominal")
        if(len(thisHist.GetSumw2()) == 0):
            thisHist.Sumw2()
        varDict[key] = thisHist.Clone("h_" + key)
        varDict[key].SetDirectory(0)
        varDict[key].Write()
        inFile.Close()
        outFile.Close()

   ########################
    # Nominal
    ########################
    nbins    = 5
    mjj_bins = [0.,1.,1.5,2.,3.5]
    mjj_bins_xaxis = [0.8,1.,1.5,2.,3.5,5]
    mjj_incl = [0.8,1000]
    systs    = ["fac", "renorm", "both"]

    inFile   = TFile.Open(outPath+"/variedYields_"+channel+"_"+reg+".root")
    outFile  = TFile(outPath+"/reweight_"+channel+"_"+reg+".root", "recreate")

    yieldNom    = [0.,0.,0.,0.,0.]
    largestUp   = [1.,1.,1.,1.,1.]
    largestDown = [1.,1.,1.,1.,1.]
    err_yieldNom    = [0.,0.,0.,0.,0.]
    err_largestUp   = [0.,0.,0.,0.,0.]
    err_largestDown = [0.,0.,0.,0.,0.]
    yieldNomIncl = 0.
    largestUpIncl = 1.
    largestDownIncl = 1.
    err_yieldNomIncl = 0.
    err_largestUpIncl = 1.
    err_largestDownIncl = 1.


    ########################
    # qsf/ckkw variations
    ########################
    for wVar in ["resum", "ckkw"]:
        avgNormalization = 1./2
        qsfckkwYield = [0.,0.,0.,0.,0.]
        qsfckkwYieldSq = [0.,0.,0.,0.,0.]
        qsfckkwYieldIncl = 0.
        qsfckkwYieldSqIncl = 0.
        err_qsfckkwYield = [0.,0.,0.,0.,0.]
        err_qsfckkwYieldIncl = 0.
        if wVar == "resum":
            wList = ["qsf025", "qsf4"]
        elif wVar == "ckkw":
            wList = ["ckkw15", "ckkw30"]
        for i in wList:
            thisHist = inFile.Get("h_"+i)
            thisYield = [0.,0.,0.,0.,0.]
            err_thisYield = [0.,0.,0.,0.,0.]
            thisYieldIncl = 0.
            err_thisYieldIncl = 0.
            for iBin in range(thisHist.GetNbinsX()+1):
                binIndex = 0
                binCenter = thisHist.GetBinCenter(iBin+1)
                if binCenter < mjj_bins[0]:
                    continue
                while binIndex < 4:
                    if binCenter >= mjj_bins[binIndex] and binCenter < mjj_bins[binIndex+1] :
                        break
                    binIndex = binIndex + 1
                thisYield[binIndex] += thisHist.GetBinContent(iBin+1)
                thisYieldIncl += thisHist.GetBinContent(iBin+1)
                err_thisYield[binIndex] += thisHist.GetBinError(iBin+1)*thisHist.GetBinError(iBin+1)
                err_thisYieldIncl += thisHist.GetBinError(iBin+1)*thisHist.GetBinError(iBin+1)
            for j in range(nbins):
                qsfckkwYield[j]    += avgNormalization * thisYield[j]
                qsfckkwYieldSq[j]  += avgNormalization * thisYield[j] * thisYield[j]
                err_qsfckkwYield[j] = avgNormalization * math.sqrt(err_thisYield[binIndex])
            qsfckkwYieldIncl   += avgNormalization * thisYieldIncl
            qsfckkwYieldSqIncl += avgNormalization * thisYieldIncl * thisYieldIncl
            err_qsfckkwYieldIncl = avgNormalization * math.sqrt(err_thisYieldIncl)
        qsfckkw_up   = TH1F(wVar+"_up",   wVar+" up reweight",   nbins, array('d',mjj_bins_xaxis))
        qsfckkw_down = TH1F(wVar+"_down", wVar+" down reweight", nbins, array('d',mjj_bins_xaxis))
        qsfckkwError = [0.,0.,0.,0.,0.]
        tmp_qsfckkwVar=[0.,0.,0.,0.,0.]
        for i in range(nbins) :
            if(qsfckkwYield[i] == 0):
                if(debug): print " yield is zero for bin %i"%i
                continue
            qsfckkwError[i] = math.sqrt(qsfckkwYieldSq[i] - (qsfckkwYield[i] * qsfckkwYield[i]))
            tmp_qsfckkwVar[i] = qsfckkwError[i]/qsfckkwYield[i]
            if (debug):  print wVar+" variation in bin %i: %f %%" % (i, tmp_qsfckkwVar[i]*100)
            qsfckkw_up.SetBinContent(  i+1, 1 + tmp_qsfckkwVar[i])
            qsfckkw_down.SetBinContent(i+1, 1 - tmp_qsfckkwVar[i])
            qsfckkw_up.SetBinError(  i+1, err_qsfckkwYield[i])
            qsfckkw_down.SetBinError(i+1, err_qsfckkwYield[i])
            if binItr[wVar] < 10:
                theoUncUp[wVar][binItr[wVar]]   = 1 + tmp_qsfckkwVar[i]
                theoUncDown[wVar][binItr[wVar]] = 1 - tmp_qsfckkwVar[i]
                binItr[wVar] = binItr[wVar]+1
        qsfckkwErrorIncl = math.sqrt(qsfckkwYieldSqIncl - (qsfckkwYieldIncl * qsfckkwYieldIncl))
        theoUncUp[wVar][binItr[wVar]]   = 1 + qsfckkwErrorIncl/qsfckkwYieldIncl
        theoUncDown[wVar][binItr[wVar]] = 1 - qsfckkwErrorIncl/qsfckkwYieldIncl
        qsfckkw_up.Write()
        qsfckkw_down.Write()

inFile.Close()
outFile.Close()

if (debug): print "\n=====================\n"
for theo in theoUncUp:
    print region+"up="+theo+"_"+channel, ",".join([str('{0:.5g}'.format(x)) for x in theoUncUp[theo]])
print ""
for theo in theoUncDown:
    print region+"down="+theo+"_"+channel, ",".join([str('{0:.5g}'.format(x)) for x in theoUncDown[theo]])
