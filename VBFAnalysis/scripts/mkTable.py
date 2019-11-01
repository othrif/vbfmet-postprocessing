#!/usr/bin/env python
from optparse import OptionParser
import ROOT
import math
from array import *
from decimal import Decimal

def main(iFileName, oFileName, CutBin, nRegions):
    iFile=ROOT.TFile(iFileName)
    signal=["VBFH125","ggFH125","VH125"]
    bkgs=["W_EWK","Z_EWK","W_strong","Z_strong","ttbar","multijet"]
    Ws=["W_EWK","W_strong"]
    Wyield=0
    Zyield=0
    Zs=["Z_EWK","Z_strong"]

    hDict={}

#    nRegions = 9
    print hDict
    LOK=iFile.GetListOfKeys()
    for key in LOK:    #Generating dict with histos
        htemp=iFile.Get(key.GetName())
        if htemp.InheritsFrom('TH1'):
            hname=htemp.GetName()
            if not(("Nom" in hname) and ("_SR" in hname)): continue
            proc=(hname.split("_")[0])[1:]
            if proc in ["W","Z"]: proc+="_"+hname.split("_")[1]
            print hname
            if proc in Ws: Wyield += htemp.GetBinContent(CutBin)
            if proc in Zs: Zyield += htemp.GetBinContent(CutBin)
####################################################################
  #          if "SR1" in hname:
  #              try:
  #                  hDict[proc+"_SR1"].Add(htemp)
  #              except KeyError:
  #                  hDict[proc+"_SR1"]=htemp.Clone()
  #          elif "SR2" in hname:
  #              try:
  #                  hDict[proc+"_SR2"].Add(htemp)
  #              except KeyError:
  #                  hDict[proc+"_SR2"]=htemp.Clone()
  #          elif "SR3" in hname:
  #              try:
  #                  hDict[proc+"_SR3"].Add(htemp)
  #              except KeyError:
  #                  hDict[proc+"_SR3"]=htemp.Clone()
#########################################################
#Here I need to add the extra signal regions
            for i in range(nRegions):
                SRstring = "SR"+str(i+1)
                if SRstring in hname.split("_"):
                    try:
                        hDict[proc+"_"+SRstring].Add(htemp)
                        print "Adding to " + SRstring
                    except KeyError:
                        hDict[proc+"_"+SRstring]=htemp.Clone()
#    print hDict

#    Signal = [0.,0.,0.]
    Signal = [0.]*nRegions
#    Bckg = [0.,0.,0.]
    Bckg = [0.]*nRegions
    Wyields =  [0.]*nRegions
    Zyields =  [0.]*nRegions
    for h in hDict:  #Computing S and B in each region
        if (h.split("_")[0]) in signal:
            for nBin in range(0,nRegions):
                SRstr = "SR" + str(nBin+1)
                if h.split("_")[-1] == SRstr:
                    Signal[nBin] += hDict[h].GetBinContent(CutBin)
                    print h + "   content = " + str(hDict[h].GetBinContent(CutBin))
                    print "Adding to"  + SRstr
        else:
            proc = h.split("_")[0]
            if proc in ["W","Z"]:
                proc += "_"+h.split("_")[1]
#                print "Here a W or Z"
 #               print proc
            if proc in bkgs:
                for nBin in range(0,nRegions):
                    SRstr = "SR" + str(nBin+1)
                    if h.split("_")[-1] == SRstr:
                        Bckg[nBin] += hDict[h].GetBinContent(CutBin)
                        print h + "   content = " + str(hDict[h].GetBinContent(CutBin))
                        if proc in Ws: Wyields[nBin] += hDict[h].GetBinContent(CutBin)
                        elif proc in Zs: Zyields[nBin] += hDict[h].GetBinContent(CutBin)
    print Signal
    print Bckg
    print Wyields
    print Zyields

    sig = [s/math.sqrt(b) if b!=0 else -1 for s,b in zip(Signal,Bckg) ]
    print sig
    Stot = 0
    Btot = 0
    sigTot = 0
    for i in range(0,len(sig)):
        Stot += Signal[i]
        Btot += Bckg[i]
        sigTot += sig[i]*sig[i]
    sigTot = math.sqrt(sigTot)
    print "Total S = " + str(Stot)
    print "Total B = " + str(Btot)
    print "Total significance = " + str(sigTot)

    tableFile = open(oFileName,'w')
    tableFile.write(r"    & S   & W_{EWK}^{strong} & Z_{EWK}^{strong}  &   B &    S/B  &   S/$\sqrt(B)$ \\" +"\n")
    for i in range(0,nRegions):
        SRstr = "SR" + str(i+1)
#    tableFile.write("SR1 & "+str(round(Decimal(Signal[0]),2)) + " & "+str(round(Decimal(Bckg[0]),2)) + " & " + str(round(Decimal(Signal[0]/Bckg[0]),2)) + " & " + str(round(Decimal(Signal[0]/math.sqrt(Bckg[0])),2)) + "\\\\ \n")
        tableFile.write(SRstr +" & "+str(round(Decimal(str(Signal[i])),2))+ " & "+ str(round(Decimal(str(Wyields[i])),2))  +  " & " + str(round(Decimal(str(Zyields[i])),2))  + " & "+str(round(Decimal(str(Bckg[i])),2)) + " & " + str(round(Decimal(str(Signal[i]/Bckg[i]  if Btot!=Bckg[i] else -1 )),2)) + " & " + str(round(Decimal(str(sig[i])),2)) + "\\\\ \n")

    tableFile.write("Total signal = " + str(Stot) + "\n")
    tableFile.write("Total background = " + str(Btot) + "\n")
    tableFile.write("Total S/B = " + str( Stot/Btot if Btot!=0 else -1)+"\n")
    tableFile.write("Total significance = " + str(sigTot)+"\n")
    sigNj2 = 0
    bkgNj2 = 0
    for i in range(0,nRegions-1):
        sigNj2 += Signal[i]
        bkgNj2 += Bckg[i]
    tableFile.write("Njet==2  " +"  "+str(round(Decimal(str(sigNj2)),2))+ "  " + str(round(Decimal(str(bkgNj2)),2)) + "  " + str(round(Decimal(str(sigNj2/bkgNj2 )),2)) + "  " + "\n")
    tableFile.write("Njet==3,4" +"  "+str(round(Decimal(str(Signal[10])),2))+ "  "+ str(round(Decimal(str(Bckg[10])),2)) + "  " + str(round(Decimal(str(Signal[10]/Bckg[10])),2)) + "\n")


    tableFile.close()


if __name__=="__main__":
    p = OptionParser()
    p.add_option('-i', '--input', type='string', default="output.root", help='input file')
    p.add_option('-o', '--output', type='string', default="sigtable.txt", help='output file')
    p.add_option('-b', '--CutBin', type=int, default=1, help='Cut bin to be used')
    p.add_option('-n', '--nRegions', type=int, default=11, help='Number of signal regions')

    for option in p.option_list:
        if option.default != ("NO", "DEFAULT"):
            option.help += (" " if option.help else "") + "[default: %default]"

    (options, args) = p.parse_args()
    main(options.input, options.output,options.CutBin,options.nRegions)
