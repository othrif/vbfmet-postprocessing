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


debug = False
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
    mjj_bins = [0.8,1.,1.5,2.,3.5]
    mjj_bins_xaxis = [0.8,1.,1.5,2.,3.5,5]
    mjj_incl = [0.8,1000]

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
            if (debug):  print "Systematic: ", i
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
                #print (binIndex, binCenter, thisHist.GetBinContent(iBin+1), thisHist.GetBinError(iBin+1), 100*thisHist.GetBinError(iBin+1)/thisHist.GetBinContent(iBin+1))
                thisYield[binIndex] += thisHist.GetBinContent(iBin+1)
                thisYieldIncl += thisHist.GetBinContent(iBin+1)
                err_thisYield[binIndex] += thisHist.GetBinError(iBin+1)*thisHist.GetBinError(iBin+1)
                err_thisYieldIncl += thisHist.GetBinError(iBin+1)*thisHist.GetBinError(iBin+1)
            for j in range(nbins):
                if (debug):  print "REBINNED: ", j, thisYield[j], math.sqrt(err_thisYield[j])
                qsfckkwYield[j]    += avgNormalization * thisYield[j]  # mu
                qsfckkwYieldSq[j]  += avgNormalization * thisYield[j] * thisYield[j]
                err_qsfckkwYield[j] += avgNormalization * avgNormalization * err_thisYield[j]
            qsfckkwYieldIncl   += avgNormalization * thisYieldIncl
            qsfckkwYieldSqIncl += avgNormalization * thisYieldIncl * thisYieldIncl
            err_qsfckkwYieldIncl += avgNormalization * avgNormalization * err_thisYieldIncl
        qsfckkw_up   = TH1F(wVar+"_up",   wVar+" up reweight",   nbins, array('d',mjj_bins_xaxis))
        qsfckkw_down = TH1F(wVar+"_down", wVar+" down reweight", nbins, array('d',mjj_bins_xaxis))
        qsfckkwError = [0.,0.,0.,0.,0.]
        tmp_qsfckkwVar=[0.,0.,0.,0.,0.]
        tmp_qsfckkwErr=[0.,0.,0.,0.,0.]
        for i in range(nbins) :
            if(qsfckkwYield[i] == 0):
                if(debug): print " yield is zero for bin %i"%i
                continue
            qsfckkwError[i] = math.sqrt(qsfckkwYieldSq[i] - (qsfckkwYield[i] * qsfckkwYield[i]))  # sigma
            A = qsfckkwError[i]
            dA = math.sqrt(err_qsfckkwYield[i])
            B = qsfckkwYield[i]
            dB = math.sqrt(err_qsfckkwYield[i])
            tmp_qsfckkwVar[i] = A/B
            tmp_qsfckkwErr[i] =  A/B*math.sqrt( math.pow(dA/A,2)+ math.pow(dB/B,2))
            if (debug):  print " >>>> ", i, "A = ", A, " +- ", dA, ", B = ", B, " +- ", dB
            if (debug):  print " >>>> RATIO: ", i, tmp_qsfckkwVar[i] ," +- ", tmp_qsfckkwErr[i]
            if (debug):  print wVar+" variation in bin %i: %f %%" % (i, tmp_qsfckkwVar[i]*100)
            qsfckkw_up.SetBinContent(  i+1, 1 + tmp_qsfckkwVar[i])
            qsfckkw_down.SetBinContent(i+1, 1 - tmp_qsfckkwVar[i])
            qsfckkw_up.SetBinError(  i+1, tmp_qsfckkwErr[i])
            qsfckkw_down.SetBinError(i+1, tmp_qsfckkwErr[i])
            if binItr[wVar] < 10:
                theoUncUp[wVar][binItr[wVar]]   = 1 + tmp_qsfckkwVar[i]
                theoUncDown[wVar][binItr[wVar]] = 1 - tmp_qsfckkwVar[i]
                binItr[wVar] = binItr[wVar]+1

            qsfckkwErrorIncl = math.sqrt(qsfckkwYieldSqIncl - (qsfckkwYieldIncl * qsfckkwYieldIncl))  # sigma
            A = qsfckkwErrorIncl
            dA = math.sqrt(err_qsfckkwYieldIncl)
            B = qsfckkwYieldIncl
            dB = math.sqrt(err_qsfckkwYieldIncl)
            tmp_qsfckkwVarIncl = A/B
            tmp_qsfckkwErrIncl =  A/B*math.sqrt( math.pow(dA/A,2)+ math.pow(dB/B,2))

        theoUncUp[wVar][binItr[wVar]]   = 1 + tmp_qsfckkwVarIncl
        theoUncDown[wVar][binItr[wVar]] = 1 - tmp_qsfckkwVarIncl
        if "Njet" in reg:
            njet_up   = TH1F(wVar+"_1bin_Njet_up",   wVar+" 1 bin up reweight",   1, 3,4)
            njet_down = TH1F(wVar+"_1bin_Njet_down", wVar+" 1 bin down reweight", 1, 3,4)
            njet_up.SetBinContent(  1, 1 + tmp_qsfckkwVarIncl)
            njet_down.SetBinContent(1, 1 - tmp_qsfckkwVarIncl)
            njet_up.SetBinError(  1, tmp_qsfckkwErrIncl)
            njet_down.SetBinError(1, tmp_qsfckkwErrIncl)
            njet_up.Write()
            njet_down.Write()
            if (debug):  print " >>>> Inclusive: ", tmp_qsfckkwVarIncl ," +- ", tmp_qsfckkwErrIncl

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
