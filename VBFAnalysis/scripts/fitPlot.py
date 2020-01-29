#!/usr/bin/env python

# The input root files are the same as used for HistFitter

# Useful examples:
# fitPlot.py -i SumHF_BaselineCuts_ZeroPhoton_AllSyst_v26c.root --yieldTable -q --saveAs png --texTables --data --ratio
# fitPlot.py -c SumHF_BaselineCuts_ZeroPhoton_AllSyst_v26c.root,Rel207.root,SumHF_Nominal_v26.root --yieldTable -q --ratio --data --saveAs png --texTables

import os
import sys
import ROOT
import math
import pickle
import VBFAnalysis.ATLAS as ATLAS
import VBFAnalysis.Style as Style
from optparse import OptionParser
#import VBFAnalysis.systematics as vbf_syst
import HInvPlot.systematics as vbf_syst

import numpy as np

from collections import OrderedDict

def skipThis(key):
    toskip=False
    if "VBFHOther" in key: toskip=True
    if "VH125Old" in key:  toskip=True
    if "VBFH125Old" in key:  toskip=True
    if "ggFH125Old" in key:  toskip=True
    if "Z_strongmVBFFilt" in key:  toskip=True
    if "Wg_EWK" in key:  toskip=True
    if "Zg_EWK" in key:  toskip=True
    if "Zg_strong" in key:  toskip=True
    if "Wg_strong" in key:  toskip=True
    if "SinglePhoton" in key:  toskip=True
    if "VqqGam" in key:  toskip=True
    if "TTH125" in key:  toskip=True
    if "Ext" in key:  toskip=True
    if "Blind" in key:  toskip=True
    return toskip

def LoadPickleFiles(dir_name):

    if not os.path.exists(dir_name):
        print 'Pickle directory does not exist'
        sys.exit(0)
    fnames=[]
    for f in os.listdir(dir_name):
        if f.count('pickle'):
            fnames+=[dir_name.rstrip('/')+'/'+f]
        
    print 'Loaded post fit files:',fnames

    fpickles = []
    for f in fnames:
        fpickles+=[pickle.load(open(f,'rb'))]
    return fpickles
    
def addContent(hist, nbin, content, error):
    newE=math.sqrt(hist.GetBinError(nbin)**2+error**2)
    newC=hist.GetBinContent(nbin)+content
    hist.SetBinContent(nbin, newC)
    hist.SetBinError(nbin, newE)

def is_in_list(name, li):
    for l in li:
        if name in l: return True
    return False

class texTable(object):
    # This class is supposed to make the creating of tables simple

    # Dependencies: numpy
    # os+pdflatex for creating pdf output

    def __init__(self, npMat=None, arrayArray=None):
        if not (npMat is None):
            self.mat = npMat

        if not (arrayArray is None):
            self.mat = np.array(arrayArray)

        # NOTE mxn matrix: m rows
        self.rows = len(self.mat)
        self.colms = len(self.mat[0])

        self.rowNames = None
        self.colmNames = None

    def getTableString(self):
        cString = ("c|"*self.colms)[:-1]
        if self.rowNames:
            cString += "|c"
        tmp = 1
        tableString = '''\\begin{{table}}
\\centering
\\begin{{tabular}}{{{cs}}}
'''.format(cs=cString)
        if self.colmNames:
            for i, n in enumerate(self.colmNames):
                tableString += n + " & "
                if i == self.colms:
                    tableString = tableString[:-2]+"\\\\\n"
                    tableString += "\\hline\n"
        rowNameIndex = 0
        for i, e in enumerate(np.nditer(self.mat)):
            if self.rowNames and tmp == 1:
                tableString += self.rowNames[rowNameIndex] + " & "
                rowNameIndex += 1
            tableString += str(e) + " & "
            if tmp == self.colms:
                tmp = 1
                tableString = tableString[:-2]+"\\\\\n"
            else:
                tmp += 1
        tableString += '''\\end{tabular}
\\end{table}
'''
        return tableString

    def getStandaloneTable(self, big=False):
        tmpString = "\\documentclass{article}"
        if big:
            tmpString += '''\\usepackage[left=1cm, a0paper]{geometry}\n'''
        tmpString += "\\begin{document}\n"
        tmpString += self.getTableString()
        tmpString += "\\end{document}"
        return tmpString

    def setNames(self, rowNames=None, colmNames=None):
        if len(colmNames) == self.colms:  # This makes top left corner as empty
            colmNames.insert(0, " ")
        elif not(len(colmNames) == self.colms+1):
            print "WARNING: Not all colms have names"
            print len(colmNames),self.colms
        if not (len(rowNames) == self.rows):
            print "WARNING: Not all rows have names"
            print len(rowNames),self.rows
        self.rowNames = rowNames
        self.colmNames = colmNames

    def mirror(self):
        # Makes colms->rows and rows->colms
        newArrArr = []
        for a in range(self.colms):
            tmpArr = []
            for b in range(self.rows):
                tmpArr.append(self.mat[b][a])
            newArrArr.append(tmpArr)
        self.mat = np.array(newArrArr)
        self.rowNames, self.colmNames = self.colmNames, self.rowNames
        if self.rowNames:
            self.colmNames.insert(0, self.rowNames[0])
            self.rowNames.pop(0)
        self.rows, self.colms = self.colms, self.rows

    def createPDF(self, fileName="table", clean=False, big=False):
        # Needs pdflatex
        texName = fileName+".tex"
        if os.path.isfile(texName):
            print texName, "Already exists!"
            decision = raw_input("Are you sure you want to overwrite it?[y/n]")
            if not(decision == "y"):
                return
        texFile = open(texName, "w")
        texFile.write(self.getStandaloneTable(big))
        texFile.close()
        os.system("pdflatex -halt-on-error {}".format(texName))
        if clean:
            os.system("rm {a}.log {a}.tex {a}.aux".format(a=fileName))

    def isValid(self):
        pass

    def __str__(self):
        print "self.mat:\n", self.mat
        print "self.rowNames, self.colmNames:", self.rowNames, self.colmNames
        return "texTable"


class HistClass(object):
    '''Class to easily read out HistFitter input files'''
    Irfile=None #this has to be an open root file
    regDict=None
    nBins=None
    systs=[]
    onesided=False
    def __init__(self, hname,var=None):

        if HistClass.nBins==None:
            HistClass.nBins=HistClass.getNumberOfBins()
        if HistClass.regDict==None:
            HistClass.setRegDict()

        if var:
            self.hname=hname.replace(var,"cuts")
        else:
            self.hname=hname
            if not (hname.split("_")[-1]=="cuts"):
                self.hist=None
                return

        sp=self.hname.split("_")
        self.proc=sp[0][1:]
        if self.proc in ["W","Z"]:
            self.proc+="_"+sp[1]
        self.reg=sp[-3]
        self.mr=self.reg[-1]
        self.syst_HIGH_LOW=""
        if "NONE" in self.hname: # These are data hists
            self.syst="Nom"
        else:
            self.syst=self.hname[self.hname.find("VBFjetSel_")+11:self.hname.find("_"+self.reg)] #NOTE this only works for less than 10 bins. for more bins the "+11" has to change to +12
            if (self.hname[self.hname.find("VBFjetSel_")+10:self.hname.find("VBFjetSel_")+12]).isdigit():
                self.syst=self.hname[self.hname.find("VBFjetSel_")+12:self.hname.find("_"+self.reg)] #NOTE this only works for less than 10-99 bins. 
            if "Low" in self.syst:
                self.syst=self.syst.replace("Low","")
                self.syst_HIGH_LOW="Low"
            elif "High" in self.syst:
                self.syst=self.syst.replace("High","")
                self.syst_HIGH_LOW="High"
        if HistClass.regDict is not None:
            self.nbin=HistClass.regDict[self.reg]
        if var:
            self.hist=HistClass.Irfile.Get(hname)
        else:
            self.hist=HistClass.Irfile.Get(self.hname)
        if self.hist is None:
            print "Could not retrieve histogram!", self.hname, HistClass.Irfile

        if not(self.syst in HistClass.systs):
            HistClass.systs.append(self.syst)

    def getOtherVariation(self):
        #returns the name HistClass Obj for the up variation if this is the down variation and vice versa
        if self.syst_HIGH_LOW=="":
            print "This is not a systematic variation with up/down.", self.hname
            return
        for k,v in vbf_syst.systematics.getsystematicsOneSidedMap().iteritems():
            if self.syst in v:
                print "This is a one sided systematic can't get other variation!", self.hname
                return None
        opposite=""
        if self.syst_HIGH_LOW=="High": opposite="Low"
        elif self.syst_HIGH_LOW=="Low": opposite="High"
        else: print "WARNING! how can this happen?!"
        obj=HistClass(self.hname.replace(self.syst_HIGH_LOW, opposite, 1))
        return obj

    def getCentralHist(self):
        centralHist=HistClass.Irfile.Get(self.hname.replace(self.syst+self.syst_HIGH_LOW, "Nom"))
        return centralHist


    def isSystDict(self):
        for j in ["eleFakes", "multijet", "NONE", "Nom"]:
            if j in self.hname: return False
        return True

    def isBkg(self):
        if self.proc in ["Z_strong","W_strong","Z_EWK","W_EWK","ttbar","eleFakes","multijet","VV","VVV","QCDw"]:
            return True
        return False

    def isData(self):
        if self.proc=="data":
            return True
        return False


    def isSignal(self):
        if self.proc in ["VBFH125", "ggFH125", "VH125"]:
            return True
        return False

    def isTheoSyst(self):
        theoID=["CKKW", "PDF", "RESUM", "RENOFACT"]
        for Tid in theoID:
            if Tid in self.syst:
                return True
        return False

    def isExpSyst(self):
        if not(self.isTheoSyst()) and self.syst!="Nom":
            return True
        return False


    def __str__(self):
    # TODO: works only for bin 1 atm
        print "init with:",self.hname
        print "region:",self.reg,"# Process:",self.proc,"# Systematic:",self.syst, "# High/Low:",self.syst_HIGH_LOW
        if self.hist is not None:
            print "Content:",self.hist.GetBinContent(1),"+-",self.hist.GetBinError(1)
        print "signal:",self.isSignal()
        print "Bkg:",self.isBkg()
        print "Exp syst:",self.isExpSyst()
        print "Theo syst:",self.isTheoSyst()
        print "Nominal:",(self.syst=="Nom")
        return ""

    @classmethod
    def getHist(cls, proc="VBFH125", syst="Nom", reg="SR", mr="1", highLow=""):
        # Use this to create the histname for a specific hist
        hname="h"+proc+"_VBFjetSel_"+mr+syst+highLow+"_"+reg+mr+"_obs_cuts"
        obj=cls(hname)
        return obj

    @classmethod
    def getNumberOfBins(cls):
        nbins=0
        LOK=None
        for p in ["VBFH","Z_strong","W_strong","Z_EWK","W_EWK","ttbar","eleFakes","multijet","data"]:
            LOK=[k.GetName() for k in cls.Irfile.GetListOfKeys() if p in k.GetName()]
            if len(LOK)==0:
                continue
            else:
                break
        for k in LOK:
            for l in k.split("_"):
                if "Nom" in l:
                    if int(l.replace("Nom",""))>nbins:
                        nbins=int(l.replace("Nom",""))
        return nbins

    @classmethod
    def setRegDict(cls):
        if cls.Irfile is None:
            print "Set HistClass.Irfile first!"
            sys.ecit(0)
        else:
            cls.regDict=OrderedDict()
            if cls.nBins==None:
                cls.nBins=cls.getNumberOfBins()
            for n in range(1,cls.nBins+1):
                cls.regDict["SR{}".format(n)]=cls.nBins*8+n
                cls.regDict["oneMuNegCR{}".format(n)]=cls.nBins*4+n
                cls.regDict["oneMuPosCR{}".format(n)]=cls.nBins*5+n
                cls.regDict["oneEleNegCR{}".format(n)]=cls.nBins*2+n
                cls.regDict["oneElePosCR{}".format(n)]=cls.nBins*3+n
                cls.regDict["twoMuCR{}".format(n)]=cls.nBins*7+n
                cls.regDict["twoEleCR{}".format(n)]=cls.nBins*6+n
                cls.regDict["oneEleNegLowSigCR{}".format(n)]=n
                cls.regDict["oneElePosLowSigCR{}".format(n)]=cls.nBins+n

            cls.regionBins=OrderedDict()
            cls.regionBins["SR"]=[cls.regDict[k] for k in cls.regDict if "SR" in k]
            cls.regionBins["ZCRee"]=[cls.regDict[k] for k in cls.regDict if "twoEleCR" in k]
            cls.regionBins["ZCRmumu"]=[cls.regDict[k] for k in cls.regDict if "twoMuCR" in k]
            cls.regionBins["WCRep"]=[cls.regDict[k] for k in cls.regDict if "oneElePosCR" in k]
            cls.regionBins["WCRen"]=[cls.regDict[k] for k in cls.regDict if "oneEleNegCR" in k]
            cls.regionBins["WCRmup"]=[cls.regDict[k] for k in cls.regDict if "oneMuPosCR" in k]
            cls.regionBins["WCRmun"]=[cls.regDict[k] for k in cls.regDict if "oneMuNegCR" in k]
            cls.regionBins["lowsigWCRep"]=[cls.regDict[k] for k in cls.regDict if "oneElePosLowSigCR" in k]
            cls.regionBins["lowsigWCRen"]=[cls.regDict[k] for k in cls.regDict if "oneEleNegLowSigCR" in k]

            cls.regionBins["ZCRll"]=cls.regionBins["ZCRee"]+cls.regionBins["ZCRmumu"]
            cls.regionBins["WCRenu"]=cls.regionBins["WCRep"]+cls.regionBins["WCRen"]
            cls.regionBins["WCRmunu"]=cls.regionBins["WCRmup"]+cls.regionBins["WCRmun"]
            cls.regionBins["WCRlnu"]=cls.regionBins["WCRenu"]+cls.regionBins["WCRmunu"]
            cls.regionBins["lowsigWCRenu"]=cls.regionBins["lowsigWCRep"]+cls.regionBins["lowsigWCRen"]




def getBinsError(hist, bins):
    BE=0
    for bn in bins:
        if type(hist)==ROOT.TH1F:
            BE+=hist.GetBinError(bn) # FIXME squared or not?
        else:
            BE+=hist.GetErrorYhigh(bn-1)
    return BE

def getBinsYield(hist, bins):
    BC=0
    x1a=ROOT.Double()
    y1a=ROOT.Double()
    for bn in bins:
        if type(hist)==ROOT.TH1F:
            BC+=hist.GetBinContent(bn)
        else:
            hist.GetPoint(bn-1,x1a,y1a)
            BC+=y1a
    return BC

def removeLabel(leg, name):
    LOP=leg.GetListOfPrimitives()
    nothingWasRemoved=True
    for prim in LOP:
        if prim.GetLabel()==name:
            LOP.Remove(prim)
            nothingWasRemoved=False
    if nothingWasRemoved:
        print name, "was not found in labels and was not removed. List of labels:"
        for prim in LOP:
            print prim.GetLabel()

def make_legend(can):
    leg=can.BuildLegend(0.0,0.1,0.2,0.5)
    leg.SetBorderSize(0)
    leg.SetFillStyle (0)
    leg.SetTextFont(42)
    leg.SetTextSize(0.04)
    #leg.SetNColumns  (2)
    NameDict ={'ttbar':'Top+VV/VVV',
                   'Z_EWK':'EWK Z',
                   'W_EWK':'EWK W',
                   'Z_strong':'QCD Z',
                   'W_strong':'QCD W',
                   'signal':'Higgs',
                   'data':'Data',                   
                   'eleFakes':'e-fakes',
                   'multijet':'Multijet',
                   }
    for i in leg.GetListOfPrimitives():
        if i.GetLabel() not in ['signal','data']:
            i.GetObject().SetLineColor(i.GetObject().GetFillColor())
            i.GetObject().SetMarkerColor(i.GetObject().GetFillColor())
        if i.GetLabel() in NameDict:
            i.SetLabel(NameDict[i.GetLabel()])
    removeLabel(leg, 'dummy')
    removeLabel(leg, 'Others')
    nEntries=len(leg.GetListOfPrimitives())
    #leg.SetY1(0.9-nEntries*0.04)
    return leg


def get_THStack_sum(hstack):
        li = hstack.GetHists()
        tot_hist=None
        for i in li:
                if tot_hist==None:
                        tot_hist=i.Clone("Total_MC")
                else:
                        tot_hist.Add(i)
        return tot_hist


def make_yieldTable(regionDict, regionBinsDict, histDict, dataHist, nbins, makePDF=False):

    DataMC2=histDict["data"].Clone()
    DataMC2.Divide(histDict["bkgs"])

    DataMC=OrderedDict()
    for reg in regionBinsDict:
            DataMC[reg]=0
            if options.data: DataMC[reg]=(getBinsYield(histDict["data"], regionBinsDict[reg])/getBinsYield(histDict["bkgs"], regionBinsDict[reg]))

    arrArray=[]
    x1a=ROOT.Double()
    y1a=ROOT.Double()
    for hkey in histDict:
        tmpArr=[]
        for regkey in regionDict:
            #tmpArr.append(str(round(histDict[hkey].GetBinContent(regionDict[regkey]),2))+" $\\pm$ "+str(round(histDict[hkey].GetBinError(regionDict[regkey]),2)))
            yldvR=0.0
            if type(histDict[hkey])==ROOT.TH1F:
                yldvR=round(histDict[hkey].GetBinContent(regionDict[regkey]),2)
                yldeR=round(histDict[hkey].GetBinError(regionDict[regkey]),2)
            else:
                histDict[hkey].GetPoint(regionDict[regkey]-1,x1a,y1a)
                yldvR=round(y1a,2)
                ylde=histDict[hkey].GetErrorYhigh(regionDict[regkey]-1)
                yldeR=round(ylde,2)
            tmpArr.append(str(yldvR)+" +- "+str(yldeR))
        arrArray.append(tmpArr)
    arrArray.append([str(round(DataMC2.GetBinContent(dm),2))+" $\\pm$ "+str(round(DataMC2.GetBinError(dm),2)) for dm in [regionDict[i] for i in regionDict]])
    texTable1=texTable(arrayArray=arrArray)
    colmNames=[reg for reg in regionDict]
    rowNames=[hkey.replace("_"," ") for hkey in histDict]+["Data/MC"]
    texTable1.setNames(rowNames, colmNames)
    print texTable1.getTableString()
    print "\n###########\n"


    arrArray2=[]
    for hkey in histDict:
        tmpArr2=[]
        for regkey in regionBinsDict:
            var=getBinsYield(histDict[hkey], regionBinsDict[regkey])
            varE=getBinsError(histDict[hkey], regionBinsDict[regkey])
            tmpArr2.append(str(round(var,2))+" $\\pm$ "+str(round(varE,2)))
        arrArray2.append(tmpArr2)
    arrArray2.append([str(round(DataMC[f],3)) for f in DataMC])
    texTable2=texTable(arrayArray=arrArray2)
    colmNames2=[reg for reg in regionBinsDict]
    rowNames2=[hkey.replace("_"," ") for hkey in histDict]+["Data/MC"]
    texTable2.setNames(rowNames2, colmNames2)
    print texTable2.getTableString()
    print "\n###########\n"

    if makePDF:
        # texTable1.mirror()
        # texTable2.mirror()
        texTable1.createPDF(clean=True, fileName="yieldsAllRegions", big=True)
        texTable2.createPDF(clean=True, fileName="yieldsSummary", big=True)

    # Print transfer factors a=B_SR/B_CR
    B_WSR=(getBinsYield(histDict["W_strong"], regionBinsDict["SR"])+getBinsYield(histDict["W_EWK"], regionBinsDict["SR"]))
    B_WCR=(getBinsYield(histDict["W_strong"], regionBinsDict["WCRlnu"])+getBinsYield(histDict["W_EWK"], regionBinsDict["WCRlnu"]))
    B_ZSR=(getBinsYield(histDict["Z_strong"], regionBinsDict["SR"])+getBinsYield(histDict["Z_EWK"], regionBinsDict["SR"]))
    B_ZCR=(getBinsYield(histDict["Z_strong"], regionBinsDict["ZCRll"])+getBinsYield(histDict["Z_EWK"], regionBinsDict["ZCRll"]))

    try:
        aW=B_WSR/B_WCR
        aZ=B_ZSR/B_ZCR
        print "aW:",aW
        print "aZ:",aZ
    except:
        print "aW,aZ not defined. B_WCR, B_ZCR:",B_WCR, B_ZCR


    for i in range(1,nbins+1):
        tmpB_WCR=getBinsYield(histDict["W_strong"], [nbins*4+i,nbins*5+i,nbins*2+i,nbins*3+i])+getBinsYield(histDict["W_EWK"], [nbins*4+i,nbins*5+i,nbins*2+i,nbins*3+i])
        tmpB_WSR=getBinsYield(histDict["W_strong"], [8*nbins+i])+getBinsYield(histDict["W_EWK"], [8*nbins+i])
        tmpB_ZSR=(getBinsYield(histDict["Z_strong"], [8*nbins+i])+getBinsYield(histDict["Z_EWK"], [8*nbins+i]))
        tmpB_ZCR=(getBinsYield(histDict["Z_strong"], [6*nbins+i,7*nbins+i])+getBinsYield(histDict["Z_EWK"], [6*nbins+i,7*nbins+i]))
        try:
            print "aW{mr}=".format(mr=(i)),tmpB_WSR/tmpB_WCR
            print "aZ{mr}=".format(mr=(i)),tmpB_ZSR/tmpB_ZCR
        except:
            print "aW{mr}, aZ{mr} not defined. B_WCR, B_ZCR".format(mr=(i)),tmpB_WCR,tmpB_ZCR


def getNumberOfBins(rfileInput):
    tmpIrfile=ROOT.TFile(rfileInput)
    nbins=0
    LOK=None
    for p in ["VBFH","Z_strong","W_strong","Z_EWK","W_EWK","ttbar","eleFakes","multijet","data"]:
        LOK=[k.GetName() for k in tmpIrfile.GetListOfKeys() if p in k.GetName()]
        if len(LOK)==0:
            continue
        else:
            break
    for k in LOK:
        for l in k.split("_"):
            if "Nom" in l:
                if int(l.replace("Nom",""))>nbins:
                    nbins=int(l.replace("Nom",""))
    print "getNumberOfBins() detected {} bins".format(nbins)
    return nbins



def main(options):
    if options.quite:
        ROOT.gROOT.SetBatch(True)

    nbins=getNumberOfBins(options.input)

    ATLAS.Style()

    can=ROOT.TCanvas("c","c",1000,600)

    if options.ratio:
        can.Divide(1,2)
        can.cd(1)
        ROOT.gPad.SetBottomMargin(0)
        ROOT.gPad.SetRightMargin(0.1)
        ROOT.gPad.SetPad(0,0.3,1,1)
        ROOT.gPad.SetLogy()
        can.cd(2)
        ROOT.gPad.SetTopMargin(0)
        ROOT.gPad.SetBottomMargin(0.35)
        ROOT.gPad.SetRightMargin(0.1)
        ROOT.gPad.SetPad(0,0,1,0.3)
        can.cd(1)
    else:
        can.SetLogy()


    dummyHist=ROOT.TH1F("dummy","",9*nbins,0,9*nbins)
    dummyHist.SetStats(0)


    hDict=OrderedDict()
    histNames=["signal", "W_strong", "Z_strong", "W_EWK", "Z_EWK", "eleFakes", "ttbar", "multijet", "Others"] # This order determines the order in which the hists are stacked


    regDict=OrderedDict()
    for n in range(1,nbins+1):
        regDict["SR{}".format(n)]=nbins*8+n
        regDict["oneMuNegCR{}".format(n)]=nbins*4+n
        regDict["oneMuPosCR{}".format(n)]=nbins*5+n
        regDict["oneEleNegCR{}".format(n)]=nbins*2+n
        regDict["oneElePosCR{}".format(n)]=nbins*3+n
        regDict["twoMuCR{}".format(n)]=nbins*7+n
        regDict["twoEleCR{}".format(n)]=nbins*6+n
        regDict["oneEleNegLowSigCR{}".format(n)]=n
        regDict["oneElePosLowSigCR{}".format(n)]=nbins+n


    regionBins=OrderedDict()
    regionBins["SR"]=[regDict[k] for k in regDict if "SR" in k]
    regionBins["ZCRee"]=[regDict[k] for k in regDict if "twoEleCR" in k]
    regionBins["ZCRmumu"]=[regDict[k] for k in regDict if "twoMuCR" in k]
    regionBins["WCRep"]=[regDict[k] for k in regDict if "oneElePosCR" in k]
    regionBins["WCRen"]=[regDict[k] for k in regDict if "oneEleNegCR" in k]
    regionBins["WCRmup"]=[regDict[k] for k in regDict if "oneMuPosCR" in k]
    regionBins["WCRmun"]=[regDict[k] for k in regDict if "oneMuNegCR" in k]
    regionBins["lowsigWCRep"]=[regDict[k] for k in regDict if "oneElePosLowSigCR" in k]
    regionBins["lowsigWCRen"]=[regDict[k] for k in regDict if "oneEleNegLowSigCR" in k]

    regionBins["ZCRll"]=regionBins["ZCRee"]+regionBins["ZCRmumu"]
    regionBins["WCRenu"]=regionBins["WCRep"]+regionBins["WCRen"]
    regionBins["WCRmunu"]=regionBins["WCRmup"]+regionBins["WCRmun"]
    regionBins["WCRlnu"]=regionBins["WCRenu"]+regionBins["WCRmunu"]
    regionBins["lowsigWCRenu"]=regionBins["lowsigWCRep"]+regionBins["lowsigWCRen"]

    #setting dummyHist
    for k in regDict:
        dummyHist.GetXaxis().SetBinLabel(regDict[k],k)
    dummyHist.SetMaximum(2000)
    dummyHist.SetMinimum(1)
    dummyHist.GetYaxis().SetTitle("Events")
    dummyHist.Draw()

    hists=[]
    for hname in histNames[::-1]:
        hists.append(ROOT.TH1F(hname,hname,nbins*9,0,nbins*9))
        hDict[hname]=hists[-1]
        hDict[hname].Sumw2()
    data=ROOT.TH1F("data","data",nbins*9,0,nbins*9)
    hDict["data"]=data


    #Styles
    Style.setStyles(data,[1,0,2,0,0,1,20,1.2])
    Style.setStyles(hDict["signal"],[2,2,3,0,0,0,0,0])
    Style.setStyles(hDict["Z_strong"],[1,1,1,46,1001,0,0,0])
    Style.setStyles(hDict["Z_EWK"],[1,1,1,8,1001,0,0,0])
    Style.setStyles(hDict["W_strong"],[1,1,1,9,1001,0,0,0])
    Style.setStyles(hDict["W_EWK"],[1,1,1,5,1001,0,0,0])
    Style.setStyles(hDict["ttbar"],[1,1,1,0,1001,0,0,0])
    Style.setStyles(hDict["eleFakes"],[1,1,1,11,1001,0,0,0])
    Style.setStyles(hDict["multijet"],[1,1,1,12,1001,0,0,0])
    Style.setStyles(hDict["Others"],[1,1,1,2,1001,0,0,0])

    # loop over all hists in input file and add their content to the right hist
    rfile=ROOT.TFile(options.input)
    LOK=rfile.GetListOfKeys()
    HistClass.Irfile=rfile
    HistClass.regDict=regDict


    hnames=[i.GetName() for i in LOK if ("Nom" in i.GetName() or "NONE" in i.GetName())]
    for key in hnames:
        # NOTE here you can specify hisotgrams which should be skipped
        if skipThis(key): continue
        histObj=HistClass(key)
        if not histObj.hist: continue
        if histObj.isSignal():
            addContent(hDict["signal"], histObj.nbin, histObj.hist.GetBinContent(options.nBin), histObj.hist.GetBinError(options.nBin))
        elif histObj.proc in histNames+["data"]:
            addContent(hDict[histObj.proc], histObj.nbin, histObj.hist.GetBinContent(options.nBin), histObj.hist.GetBinError(options.nBin))
        else:
            if not key.count('hQCDw_'):
                print key, "could not be identified correctly! BinContent will be added to Others"
                addContent(hDict["Others"], histObj.nbin, histObj.hist.GetBinContent(options.nBin), histObj.hist.GetBinError(options.nBin))

    postFitPickles=None
    if options.postFitPickleDir!=None:
        hist_array_keys = [i.GetName() for i in hists]
        postFitPickles = LoadPickleFiles(options.postFitPickleDir)
        for fpickle in postFitPickles: # example Fitted_events_VH125_VBFjetSel_2
            pickle_region_names = fpickle['names'] # these are the CR and SR names as entered. just a description of the entries
            for pickle_key in fpickle.keys():
                if not ('Fitted_events_' in pickle_key): # only process the fitted events here
                    continue
                #if ('Fitted_events_VBFH' in pickle_key): # skip signal
                #    continue
                pickle_key_remFit = pickle_key[len('Fitted_events_'):]
                m=0
                for i in hist_array_keys:
                    if i in pickle_key_remFit:
                        break
                    m+=1
                if m>=len(hists):
                    print 'Post fit - could not find (fine if signal): ',pickle_key
                    continue
                histToSet = hists[m]
                #print 'check',regDict['oneEleNegCR1'] #+'_cuts' need to strip '_cuts'
                ireg=0
                for iname in pickle_region_names:
                    #print "Setting: ",iname,pickle_key
                    histToSet.SetBinContent(regDict[iname.rstrip('_cuts')],fpickle[pickle_key][ireg])
                    ireg+=1
                
    #defining bkg hist
    bkgsList=["Z_strong","Z_EWK","W_EWK","W_strong","ttbar","eleFakes","multijet"]+["Others"]
    bkgs=ROOT.TH1F("bkgs","bkgs",nbins*9,0,nbins*9)
    hDict["bkgs"]=bkgs
    hDict["bkgsStat"]=bkgs.Clone() # this has the bkg mc stat uncertainty
    for bkg in bkgsList:
        hDict["bkgs"].Add(hDict[bkg])
        hDict["bkgsStat"].Add(hDict[bkg])
    # Set the MC stat uncertainties to 0 in the systematics plot
    if not options.show_mc_stat_err:
        for i in range(0,hDict["bkgs"].GetNbinsX()):
            hDict["bkgs"].SetBinError(i,0.0)

    hStack=ROOT.THStack()
    for h in hists:
        hStack.Add(h)

    if not options.unBlindSR:
        # totalMC=get_THStack_sum(hStack)
        for SRbin in regionBins["SR"]:
            hDict["data"].SetBinContent(SRbin,bkgs.GetBinContent(SRbin))

    dummyHist.SetMaximum(hStack.GetMaximum()*1.4)
    hStack.Draw("samehist")
    if options.data: data.Draw("Esame")

    # print the stat uncertainties:
    if options.show_mc_stat_err:
        regionsList=[
        'gamma_stat_oneEleNegLowSigCRX_obs_cuts_bin_0',
        'gamma_stat_oneElePosLowSigCRX_obs_cuts_bin_0',
        'gamma_stat_oneEleNegCRX_obs_cuts_bin_0',
        'gamma_stat_oneElePosCRX_obs_cuts_bin_0',
        'gamma_stat_oneMuNegCRX_obs_cuts_bin_0',
        'gamma_stat_oneMuPosCRX_obs_cuts_bin_0',
        'gamma_stat_twoEleCRX_obs_cuts_bin_0',
        'gamma_stat_twoMuCRX_obs_cuts_bin_0',
        'gamma_stat_SRX_obs_cuts_bin_0',    
        ]
        regionItr=0
        print 'syst data_fraction mc_fraction'
        writeLine=''
        for i in range(1,hDict["bkgs"].GetNbinsX()+1):
            if (i-1)%11==0 and i!=1:
                regionItr+=1
            binVal=((i)%11)
            if binVal==0:
                binVal=11
            nameGamma = regionsList[regionItr].replace('X_','%s_' %(binVal))
            total_bin_err = math.sqrt((data.GetBinError(i))**2+(hDict["bkgs"].GetBinError(i))**2)
            print 'bin: ',i,nameGamma,' %0.3f %0.3f' %((data.GetBinError(i)/total_bin_err),(hDict["bkgs"].GetBinError(i)/total_bin_err))
            writeLine+=nameGamma+' %0.3f %0.3f\n' %((data.GetBinError(i)/total_bin_err),(hDict["bkgs"].GetBinError(i)/total_bin_err))
        statFil=open('statunc.txt','w')
        statFil.write(writeLine)
        statFil.close()

    systHist=hDict["bkgs"]
    systHistAsym = ROOT.TGraphAsymmErrors(systHist)
    hDict["bkgsAsymErr"] = systHistAsym

    # collect the one-sided systematics
    mysystOneSided = vbf_syst.systematics('OneSided')
    one_sided_list = []
    for s in mysystOneSided.getsystematicsList():
        s_lift=s
        if s_lift.count('__1up'):
            s_lift=s[:-5]
        one_sided_list+=[s_lift]

    for i in range(0,systHist.GetNbinsX()):
        systHistAsym.SetPointEXhigh(i-1,systHist.GetXaxis().GetBinWidth(i)/2.0)
        systHistAsym.SetPointEXlow(i-1,systHist.GetXaxis().GetBinWidth(i)/2.0)
        
    if not options.syst=="":
        tmpSys=vbf_syst.systematics(options.syst)
        print "Calculating systematic variations for %s systematics. This could take a while..."%options.syst
        totSystStackDict={}#This contains the total sum of hists of bkgs for a certain sytematic and region
        systVariationDict={} # This will contain the variation from the central value for each bin
        binVariationHigh2={}
        binVariationLow2={}

        # Filling the totSystStackDict
        for b in range(1,len(regDict)+1):
            binVariationLow2[b]=0
            binVariationHigh2[b]=0

        num_syst_hist=0
        num_syst_hist_skipped=0
        histKeys=[i.GetName() for i in rfile.GetListOfKeys()]
        print "process          reg              systematic              diff/central                 diff                  variation                     central"
        for k in histKeys:
            if "theoFactors" in k or "NONEBlind" in k: continue
            tmpHist=HistClass(k)

            # check if this is a one sided systematic
            if tmpHist.syst in one_sided_list:
                tmpHist.onesided=True

            # Check that this is not a sample to be skipped
            if skipThis(k): continue
                
            if not(options.syst=="All"):
                if not(is_in_list(tmpHist.syst, tmpSys.getsystematicsList())):
                    if options.debug or (num_syst_hist_skipped%10000)==0:
                        print "skipping:",tmpHist.syst,k,tmpHist.proc,' nSyst skipped: ',num_syst_hist_skipped
                        sys.stdout.flush()
                    num_syst_hist_skipped+=1
                    continue

            if not(tmpHist.isSystDict()): continue
            if tmpHist.isSignal(): continue # FIXME revisit this. decide if we want the signal uncertainties added?
            if options.debug or (num_syst_hist%1200)==0:
                print 'This is a systematic: ',k,' This is syst number: ',num_syst_hist
                sys.stdout.flush()
            num_syst_hist+=1
                
            systName=tmpHist.syst+"_"+tmpHist.syst_HIGH_LOW
            centralHist=rfile.Get(k.replace(tmpHist.syst+tmpHist.syst_HIGH_LOW, "Nom"))
            centralValue=centralHist.GetBinContent(options.nBin)
            # centralValue=hDict[tmpHist.proc].GetBinContent(tmpHist.nbin)
            diff=tmpHist.hist.GetBinContent(options.nBin)-centralValue

            if "R" in tmpHist.reg:
                rat="nan"
                if centralValue!=0: rat=diff/centralValue

                #print '{0:<10}'.format(tmpHist.proc), '{0:<20}'.format(tmpHist.reg), '{0:<20}'.format(systName), "\t",'{0:<15}'.format(str(rat)), "\t",'{0:<15}'.format(str(diff)),"\t",'{0:<15}'.format(str(tmpHist.hist.GetBinContent(options.nBin))),"$\\pm$",'{0:<15}'.format(str(tmpHist.hist.GetBinError(options.nBin))),"\t",'{0:<15}'.format(str(centralValue)),"$\\pm$",'{0:<15}'.format(str(centralHist.GetBinError(options.nBin)))

            if diff>0:
                binVariationHigh2[tmpHist.nbin]+=diff**2
            else:
                binVariationLow2[tmpHist.nbin]+=diff**2
            #add the other for one-sided systematics
            if tmpHist.onesided:
                if diff>0:
                    binVariationLow2[tmpHist.nbin]+=diff**2
                else:
                    binVariationHigh2[tmpHist.nbin]+=diff**2

        x1a=ROOT.Double()
        y1a=ROOT.Double()
        for b in range(1,len(regDict)+1):
            lowVariation=math.sqrt(binVariationLow2[b])
            highVariation=math.sqrt(binVariationHigh2[b])
            systHistAsym.GetPoint(b-1,x1a,y1a)
            print "bin, lowVariation, highVariation:",b, lowVariation, highVariation,' central value: ',y1a
            systVariationDict[b]=(lowVariation+highVariation)/2.
            systHist.SetBinError(b, math.sqrt(systVariationDict[b]**2+systHist.GetBinError(b)**2))
            # asymmetric unc.
            ey_high=systHistAsym.GetErrorYhigh(b-1)
            new_e = ROOT.Double(math.sqrt(ey_high*ey_high+highVariation*highVariation))
            systHistAsym.SetPointEYhigh(b-1,new_e)
            ey_low=systHistAsym.GetErrorYlow(b-1)
            new_e = ROOT.Double(math.sqrt(ey_low*ey_low+lowVariation*lowVariation))
            systHistAsym.SetPointEYlow(b-1,new_e)
            
        systHist.SetTitle("Systematics")
        print "Done!"
    else:
        systHist.SetTitle("MC stat")

    # adding the post fit errors. these should include the mc stat uncertainties
    if postFitPickles!=None:
        for fpickle in postFitPickles: # example Fitted_events_VH125_VBFjetSel_2
            pickle_region_names = fpickle['names'] # these are the CR and SR names as entered. just a description of the entries
            for pickle_key in fpickle.keys():
                if not ('Fitted_err_' in pickle_key): # only process the fitted events here
                    continue
                pickle_key_remFit = pickle_key[len('Fitted_err_'):]
                m=0
                for i in hist_array_keys:
                    if i in pickle_key_remFit:
                        break
                    m+=1
                if m>=len(hists):
                    print 'Post fit syst band - could not find (fine if signal): ',pickle_key
                    continue
                histToSet = hists[m]
                ireg=0
                #print fpickle[pickle_key]
                for iname in pickle_region_names:
                    ey_low=systHistAsym.GetErrorYlow(regDict[iname.rstrip('_cuts')]-1)
                    ey_new = fpickle[pickle_key][ireg]
                    e_new = math.sqrt(ey_low*ey_low+ey_new*ey_new)
                    #print 'e_new:',e_new
                    systHistAsym.SetPointEYlow(regDict[iname.rstrip('_cuts')]-1,e_new)
                    systHistAsym.SetPointEYhigh(regDict[iname.rstrip('_cuts')]-1,e_new)
                    ireg+=1
        
    ROOT.gStyle.SetErrorX(0.5)
    fillStyle = 3004 # was 3018
    Style.setStyles(systHist,[0,0,0,1,fillStyle,0,0,0])
    Style.setStyles(hDict["bkgsStat"],[0,0,0,1,fillStyle,0,0,0])
    Style.setStyles(hDict["bkgsAsymErr"],[0,0,0,1,fillStyle,0,0,0])
    #systHist.Draw("same e2") # smooths the errors assuming they are symmetric
    systHistAsym.Draw("same e2")

    print "Systematics found:",HistClass.systs

    if options.yieldTable:
        make_yieldTable(regDict, regionBins, hDict, data, nbins, options.texTables)

    leg=make_legend(ROOT.gPad)
    leg.Draw()

    texts = ATLAS.getATLASLabels(can, 0.2, 0.86, options.lumi, selkey="")

    for text in texts:
        text.Draw()

    if options.ratio:
        can.cd(2)
        rHist=data.Clone("ratioHist")
        rbkgs = hDict["bkgsStat"].Clone()
        if options.show_mc_stat_err or options.postFitPickleDir!=None: # removing mc stat unc.
            for i in range(0,rbkgs.GetNbinsX()+1):
                rbkgs.SetBinError(i,0.0)
        
        rHist.Divide(rbkgs)
        rHist.GetYaxis().SetTitle("Data/MC")
        rHist.GetYaxis().SetTitleOffset(.35)
        rHist.GetYaxis().SetTitleSize(0.1)
        rHist.GetYaxis().CenterTitle()

        for k in regDict:
            rHist.GetXaxis().SetBinLabel(regDict[k],k)
        rHist.GetXaxis().SetLabelSize(0.1)
        rHist.GetYaxis().SetLabelSize(0.1)

        line1=data.Clone("line1")
        for i in range(1,line1.GetNbinsX()+1):
            line1.SetBinContent(i,1)
        Style.setLineAttr(line1,2,2,3)

        rHist.Draw()
        line1.Draw("histsame")
        if options.show_mc_stat_err or options.syst!="" or options.postFitPickleDir!=None:
            if options.show_mc_stat_err:
                bkgs = hDict["bkgsStat"].Clone() # this only holds the MC stat uncertainty
            for i in range(0,rbkgs.GetNbinsX()+1):
                rbkgs.SetBinContent(i,1.0)
                e1 = 0.0;
                if bkgs.GetBinContent(i)!=0.0:
                    e1=bkgs.GetBinError(i)/bkgs.GetBinContent(i)
                rbkgs.SetBinError(i,e1)

            # load the asymmetric
            systHistAsymRatio = systHistAsym.Clone()
            x1=ROOT.Double()
            y1=ROOT.Double()
            for j in range(1,bkgs.GetNbinsX()+1):
                # Set Y value to 1
                systHistAsymRatio.GetPoint(j-1,x1,y1)
                systHistAsymRatio.SetPoint(j-1,x1,1.0)
                val=bkgs.GetBinContent(j)
                eyu=systHistAsym.GetErrorYhigh   (j-1)/val
                eyd=systHistAsym.GetErrorYlow    (j-1)/val
                systHistAsymRatio.SetPointEYhigh(j-1,eyu)
                systHistAsymRatio.SetPointEYlow (j-1,eyd)

            #rbkgs.Draw('same e2') # divides (up-down)/2 for symmetric unc.
            systHistAsymRatio.Draw('same e2')
            rHist.Draw('same')
            line1.Draw("histsame")
                
        can.GetPad(2).RedrawAxis()
        can.GetPad(2).Modified()
        can.GetPad(2).Update()
        can.cd(1)

    ROOT.gPad.RedrawAxis()
    ROOT.gPad.Modified()
    ROOT.gPad.Update()

    can.cd(1)
    blindStr=""
    if not options.unBlindSR:
        blindStr=", SR blinded"
    namingScheme="Pre-Fit"
    if options.postFitPickleDir!=None:
        namingScheme="Post-Fit"
    preFitLabel=ROOT.TLatex(.5,.86,namingScheme+blindStr)
    preFitLabel.SetNDC()
    preFitLabel.SetTextFont(72)
    preFitLabel.SetTextSize(0.055)
    preFitLabel.SetTextAlign(11)    
    preFitLabel.SetTextColor(ROOT.kBlack)
    preFitLabel.Draw()

    can.Modified()
    can.Update()

    if not options.quite:
        raw_input("Press Enter to continue")
    if options.saveAs:
        can.SaveAs("preFit."+options.saveAs)

    rfile.Close()


def compareMain(options):
    if options.quite:
        ROOT.gROOT.SetBatch(True)
    openRfiles={}
    for i,rfile in enumerate(options.compare.split(",")):
        openRfiles[i]=ROOT.TFile(rfile)

    ATLAS.Style()

    mjjBins=None
    # loop over all hists in input file and add their content to the right hist
    histDict={}
    for i in openRfiles:
        print "loading",openRfiles[i].GetName()
        histDict[i]={"bkg":None}
        if options.data:
            histDict[i]["data"]=None
            histDict[i]["data/MC"]=None
        HistClass.Irfile=openRfiles[i]
        if mjjBins is None:
            mjjBins=HistClass.getNumberOfBins()# This should be 3 in normal analysis
        LOK=openRfiles[i].GetListOfKeys()

        hnames=[j.GetName() for j in LOK if ("Nom" in j.GetName() or "NONE" in j.GetName())]
        for key in hnames:
            # NOTE here you can specify hisotgrams which should be skipped
            if "VBFHOther" in key: continue
            if "Ext" in key: continue
            if "Blind" in key: continue
            histObj=HistClass(key)
            if not histObj.hist: continue

            if histObj.isBkg():
                try:
                    addContent(histDict[i]["bkg"], histObj.nbin, histObj.hist.GetBinContent(options.nBin), histObj.hist.GetBinError(options.nBin))
                except:
                    histDict[i]["bkg"]=ROOT.TH1F("bkg{}".format(i),"",9*mjjBins,0,9*mjjBins)
                    addContent(histDict[i]["bkg"], histObj.nbin, histObj.hist.GetBinContent(options.nBin), histObj.hist.GetBinError(options.nBin))
            elif histObj.isData() and options.data:
                try:
                    addContent(histDict[i]["data"], histObj.nbin, histObj.hist.GetBinContent(options.nBin), histObj.hist.GetBinError(options.nBin))
                except:
                    histDict[i]["data"]=ROOT.TH1F("data{}".format(i),"",9*mjjBins,0,9*mjjBins)
                    addContent(histDict[i]["data"], histObj.nbin, histObj.hist.GetBinContent(options.nBin), histObj.hist.GetBinError(options.nBin))

        if options.data:
            histDict[i]["data/MC"]=histDict[i]["data"].Clone("data/MC{}".format(i))
            histDict[i]["data/MC"].Divide(histDict[i]["bkg"])

        for k in histDict:
            for r in histDict[k]:
                try:
                    histDict[k][r].SetLineColor(k+1)
                    histDict[k][r].SetLineWidth(3)
                except:
                    print r,"not found",openRfiles[k].GetName()

    c1=ROOT.TCanvas("c1","c2",1600,1200)

    dummyHist=ROOT.TH1F("dummy","",9*mjjBins,0,9*mjjBins)
    dummyHist.SetStats(0)
    for k in HistClass.regDict:
        dummyHist.GetXaxis().SetBinLabel(HistClass.regDict[k],k)

    for p in histDict[0]:
        colmNames=[k for k in HistClass.regDict]
        rowNames=[openRfiles[l].GetName().replace("_"," ") for l in openRfiles]

        if options.yieldTable:
            # Table 1: Explicit
            rowVals=[]
            for r in openRfiles:
                colmVals=[]
                for n in colmNames:
                    tmpStr=""
                    tmpStr+="{:.2f}".format(histDict[r][p].GetBinContent(HistClass.regDict[n]))
                    tmpStr+=" $\\pm$ "
                    tmpStr+="{:.2f}".format(histDict[r][p].GetBinError(HistClass.regDict[n]))
                    colmVals.append(tmpStr)
                rowVals.append(colmVals)
            if options.ratio:
                for nFile in histDict:
                    if nFile==0: continue
                    ratioH=histDict[0][p].Clone("ratioH{}".format(nFile))
                    ratioH.Divide(histDict[nFile][p])
                    ratioColm=[]
                    for n in colmNames:
                        tmpStr=""
                        tmpStr+="{:.2f}".format(ratioH.GetBinContent(HistClass.regDict[n]))
                        # tmpStr+=" +- "
                        # tmpStr+="{:.2f}".format(ratioH.GetBinError(HistClass.regDict[n])) #NOTE I dont think showing error in this makes sense because the events are often the same.
                        ratioColm.append(tmpStr)
                    rowVals.append(ratioColm)
                    rowNames.append((openRfiles[0].GetName()+"/"+openRfiles[nFile].GetName()).replace("_"," "))

            texTableObj1=texTable(arrayArray=rowVals)
            texTableObj1.setNames(rowNames, colmNames)

                # Table 2: Summary
            colmNames2=[k for k in HistClass.regionBins]
            rowNames2=[openRfiles[l].GetName().replace("_"," ") for l in openRfiles]
            rowVals=[]
            tmpForRatio=[]
            for r in openRfiles:
                colmVals=[]
                tmpForRatioVals=[]
                for n in colmNames2:
                    var=getBinsYield(histDict[r][p], HistClass.regionBins[n])
                    varE=getBinsError(histDict[r][p], HistClass.regionBins[n])
                    if p=="data/MC":
                        var=var/len(HistClass.regionBins[n])
                        varE=varE/len(HistClass.regionBins[n])
                    tmpForRatioVals.append(var)
                    colmVals.append(str(round(var,2))+" $\\pm$ "+str(round(varE,2)))
                tmpForRatio.append(tmpForRatioVals)
                rowVals.append(colmVals)
            if options.ratio and not(p=="data/MC"): #TODO add this also for data/MC summary table
                for nFile in histDict:
                    if nFile==0: continue
                    ratioH=histDict[0][p].Clone("ratioH{}".format(nFile))
                    ratioH.Divide(histDict[nFile][p])
                    ratioColm=[]
                    for n in range(len(rowVals[0])):
                        tmpStr="{:.2f}".format(tmpForRatio[0][n]/tmpForRatio[nFile][n])
                        ratioColm.append(tmpStr)
                    rowVals.append(ratioColm)
                    rowNames2.append((openRfiles[0].GetName()+"/"+openRfiles[nFile].GetName()).replace("_"," "))

            texTableObj2=texTable(arrayArray=rowVals)
            texTableObj2.setNames(rowNames2, colmNames2)

            # texTableObj.mirror()
            print "############ {} ###########\n".format(p)
            print "\nExplicit:\n"
            print texTableObj1.getTableString()
            print "\nSummary:\n"
            print texTableObj2.getTableString()
            # texTableObj.getStandaloneTable()
            if options.texTables:
                texTableObj1.createPDF(clean=True, fileName=("table_{}".format(p)).replace("/","_"), big=True)
                texTableObj2.createPDF(clean=True, fileName=("summaryTable_{}".format(p)).replace("/","_"), big=True)
            print "\n##########################\n"



        dummyHist.SetTitle(str(p))
        if p=="data/MC":
            c1.SetLogy(0)
            dummyHist.SetMaximum(3)
            dummyHist.SetMinimum(0)
            dummyHist.GetYaxis().SetTitle("Data/MC")
            line1=dummyHist.Clone("line1")
            for i in range(1,line1.GetNbinsX()+1):
                line1.SetBinContent(i,1)
            Style.setLineAttr(line1,2,2,3)
            dummyHist.Draw()
            line1.Draw("histsame")
        else:
            c1.SetLogy()
            dummyHist.SetMaximum(2000)
            dummyHist.SetMinimum(1)
            dummyHist.GetYaxis().SetTitle("{} Events".format(str(p)))
            dummyHist.Draw()

        legX=0.2
        legY=0.9
        leg=ROOT.TLegend(legX,legY-len(histDict)*0.05,legX+0.3,legY)
        
        for k in histDict:
            entry_name =openRfiles[k].GetName()
            #print 'entry_name: ',entry_name
            #if entry_name in NameDict:
            #    entry_name=NameDict[entry_name]
            leg.AddEntry(histDict[k][p],entry_name,"l")
            histDict[k][p].Draw("Ehistsame")
        texts = ATLAS.getATLASLabels(c1, 0.54, 0.78, options.lumi, selkey="")
        for text in texts:
            text.Draw()
        leg.Draw()
        c1.RedrawAxis()
        c1.Modified()
        c1.Update()
        if not options.quite:
            raw_input("Press Enter to continue")
        if options.saveAs:
            c1.SaveAs(("preFitCompare{}".format(p)+"."+options.saveAs).replace("/","_"))


def plotVar(options):
    if options.quite:
        ROOT.gROOT.SetBatch(True)
    # ATLAS.Style()
    opt=options.plot.split(",")
    var=opt[0]
    reg=opt[1]
    mjjBins=opt[2].split("_")

    rfile=ROOT.TFile(options.input)

    bkgDict={}
    sigDict={}

    HistClass.Irfile=rfile

    hnames=[j.GetName() for j in rfile.GetListOfKeys() if (("Nom" in j.GetName() or "NONE" in j.GetName()) and var in j.GetName() and reg in j.GetName()) ]
    for h in hnames:
        hObj=HistClass(h, var)
        if not (hObj.mr in mjjBins):
            continue

        if hObj.isSignal():
            key=hObj.proc
            try:
                sigDict[key].Add(hObj.hist)
            except:
                sigDict[key]=hObj.hist.Clone(key)
                sigDict[key].SetTitle(key)
                Style.setStyles(sigDict[key], Style.styleDict[key])
        signal=ROOT.THStack()
        for h in sorted(sigDict.values()): #TODO this sorting does not work. implement lambda
            signal.Add(h)

        if hObj.isBkg():
            key=hObj.proc
            if not ("W" in key or "Z" in key):
                key="Others"
            try:
                bkgDict[key].Add(hObj.hist)
            except:
                bkgDict[key]=hObj.hist.Clone(key)
                bkgDict[key].SetTitle(key)
                Style.setStyles(bkgDict[key], Style.styleDict[key])
                
        bkg=ROOT.THStack()
        for h in sorted(bkgDict.values()): #TODO this sorting does not work. implement lambda
            bkg.Add(h)


        if hObj.isData():
            key=hObj.proc
            try:
                dataH.Add(hObj.hist)
            except:
                dataH=hObj.hist.Clone(key)
                dataH.SetTitle(key)
                Style.setStyles(dataH, Style.styleDict[key])

    if not(options.unBlindSR) and reg=="SR":
        tmpBKG=get_THStack_sum(bkg)
        dataH=tmpBKG.Clone("data blinded")
        dataH.SetTitle("data blinded")
        Style.setStyles(dataH, Style.styleDict["data"])

    can=ROOT.TCanvas("c1","c1",1600,1000)
    if options.ratio:
        can.Divide(1,2)
        can.cd(1)
        ROOT.gPad.SetBottomMargin(0)
        ROOT.gPad.SetRightMargin(0.1)
        ROOT.gPad.SetPad(0,0.3,1,1)
        can.cd(2)
        ROOT.gPad.SetTopMargin(0)
        ROOT.gPad.SetBottomMargin(0.35)
        ROOT.gPad.SetRightMargin(0.1)
        ROOT.gPad.SetPad(0,0,1,0.3)
        can.cd(1)

    bkg.Draw("hist")
    signal.Draw("Psame")
    if options.data:
        dataH.Draw("PEsame")

    bkg.GetXaxis().SetTitle(var)
    bkg.GetYaxis().SetTitle("Entries")
    bkg.SetTitle(reg+" "+",".join(mjjBins))

    ROOT.gPad.BuildLegend(0.7,0.7,0.9,0.9)

    texts = ATLAS.getATLASLabels(can, 0.4, 0.78, options.lumi, selkey="")
    for text in texts:
        text.Draw()

    blindStr=""
    if not options.unBlindSR and reg=="SR":
        blindStr=", SR blinded"
    preFitLabel=ROOT.TLatex(.7,.6,"Pre-Fit"+blindStr)
    preFitLabel.SetNDC()
    preFitLabel.SetTextFont(72)
    preFitLabel.SetTextSize(0.055)
    preFitLabel.SetTextAlign(11)    
    preFitLabel.SetTextColor(ROOT.kBlack)
    preFitLabel.Draw()

    if options.ratio:
        can.cd(2)
        rHist=dataH.Clone("ratioHist")
        rHist.Divide(get_THStack_sum(bkg))
        rHist.GetYaxis().SetTitle("Data/MC")
        rHist.GetXaxis().SetTitle(var)
        rHist.GetYaxis().SetTitleOffset(.35)
        rHist.GetYaxis().SetTitleSize(0.1)
        rHist.GetXaxis().SetTitleOffset(.85)
        rHist.GetXaxis().SetTitleSize(0.1)
        rHist.GetYaxis().CenterTitle()
        rHist.GetXaxis().SetLabelSize(0.1)
        rHist.GetYaxis().SetLabelSize(0.1)
        line1=dataH.Clone("line1")
        for i in range(1,line1.GetNbinsX()+1):
            line1.SetBinContent(i,1)
        Style.setLineAttr(line1,2,2,3)
        rHist.SetTitle("")
        rHist.SetStats(0)
        rHist.Draw()
        line1.Draw("histsame")
        can.GetPad(2).RedrawAxis()
        can.GetPad(2).Modified()
        can.GetPad(2).Update()
        can.cd(1)

    ROOT.gPad.RedrawAxis()
    ROOT.gPad.Modified()
    ROOT.gPad.Update()

    can.Modified()
    can.Update()

    if not options.quite:
        raw_input("Press Enter to continue")
    if options.saveAs:
        can.SaveAs(options.plot.replace(",","_")+"."+options.saveAs)
    del can

if __name__=='__main__':
    p = OptionParser()

    p.add_option('-i', '--input', type='string', help='input file. Created from plotEvent.py')
    p.add_option('-c', '--compare', type='string', help='Compare any number of input files. Does not support --syst atm. example: --compare rfile1.root,rfile2.root')

    p.add_option('--lumi', type='float', default=139, help='Defines the integrated luminosity shown in the label')
    p.add_option('--nBin', type='int', default=1, help='Defines which bin is plotted')
    p.add_option('-s', '--syst', type='string', default="", help='NEEDS FIXING. defines the systematics that are plotted. -s all <- will plot all available systematics. Otherwise give a key to the dict in systematics.py')# FIXME
    p.add_option('-d', '--data', action='store_true', help='Draw data')
    p.add_option('--unBlindSR', action='store_true', help='Unblinds the SR bins')
    p.add_option('--debug', action='store_true', help='Print in debug mode')    
    p.add_option('-r', '--ratio', action='store_true', help='Draw data/MC ratio in case of -i and adds ratios to tables for both -i and -c')
    p.add_option('--yieldTable', action='store_true', help='Produces yield table')
    p.add_option('--saveAs', type='string', help='Saves the canvas in a given format. example argument: pdf')
    p.add_option('-q', '--quite', action='store_true', help='activates Batch mode')
    p.add_option('--texTables', action='store_true', help='Saves tables as pdf. Only works together with --yieldTable')
    p.add_option('--postFitPickleDir', type='string', default=None, help='Directory of post fit yields pickle files. expects the files end in .pickle')    
    p.add_option('--show-mc-stat-err', action='store_true',  dest='show_mc_stat_err', help='Shows the MC stat uncertainties separately from the data ratio error')    
    p.add_option('--plot', default='', help='Plots a variable in a certain region. HFInputAlg.cxx produces these plots with the --doPlot flag . Only works with -i and not with -c. example: jj_mass,SR,1_2_3')

    for option in p.option_list:
        if option.default != ("NO", "DEFAULT"):
            option.help += (" " if option.help else "") + "[default: %default]"

    (options, args) = p.parse_args()
    if options.compare and options.input:
        print "Only give either --input or --compare!"
        sys.exit(0)
    if options.compare:
        compareMain(options)
    elif options.input:
        if options.plot:
            plotVar(options)
        else:
            main(options)
    else:
        print "Please give either --input or --compare!"
