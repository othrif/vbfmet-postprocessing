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
import math
import copy
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
    if not options.ph_ana:
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

def Scale(hist, nbins, nf):
    x1a=ROOT.Double()
    y1a=ROOT.Double()
    for nbin in nbins:
        if type(hist)==ROOT.TH1F:
            v=hist.GetBinContent(nbin)
            hist.SetBinContent(nbin,v*nf)
        else:
            hist.GetPoint(nbin-1,x1a,y1a)
            hist.SetPoint(nbin-1,x1a,y1a*nf)

def getNF(histDict, nbins, signalKeys=[], NFOnly=False):
    sigV=0.0
    sigE=0.0
    bkgV=0.0
    bkgE=0.0
    dataV=getBinsYield(histDict["data"], nbins)
    
    for hkey,hist in histDict.iteritems():
        if hkey=="signal":
            continue
        if hkey in signalKeys:
            sigV+=getBinsYield(histDict[hkey], nbins)
            sigE+=(getBinsError(histDict[hkey], nbins))**2
        elif hkey in ["Z_strong","W_strong","Z_EWK","W_EWK","Zg_strong","Wg_strong","Zg_EWK","Wg_EWK","ttbar","eleFakes","muoFakes","multijet"]:
            bkgV+=getBinsYield(histDict[hkey], nbins)
            bkgE+=(getBinsError(histDict[hkey], nbins))**2
    nf=(dataV-bkgV)
    nferr=0
    if sigV>0.0 and dataV>0.0:
        nf=(dataV-bkgV)/sigV
        nferr = nf*math.sqrt((dataV+bkgE)/(dataV**2)+sigE/(sigV**2))
    if NFOnly:
        return nf
    return '%0.2f +/- %0.2f' %(nf,nferr)
def getDataMC(histDict, nbins):
    bkgV=0.0
    bkgE=0.0
    dataV=getBinsYield(histDict["data"], nbins)
    
    for hkey,hist in histDict.iteritems():
        if hkey=="signal":
            continue
        if hkey in ["Z_strong","W_strong","Z_EWK","W_EWK","Zg_strong","Wg_strong","Zg_EWK","Wg_EWK","ttbar","eleFakes","muoFakes","multijet"]:
            bkgV+=getBinsYield(histDict[hkey], nbins)
            bkgE+=(getBinsError(histDict[hkey], nbins))**2
    nf=dataV
    nferr=0
    if bkgV>0:
        nf=(dataV/bkgV)
        nferr = nf*math.sqrt(1.0/(dataV)+bkgE/(bkgV**2))
    return '%0.2f +/- %0.2f' %(nf,nferr)
    
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
        titleKeys={'SR':'SR',
                       'WCRenu':'W$\\rightarrow$e$\\nu$ CR',
                       'WCRmunu':'W$\\rightarrow\\mu\\nu$ CR',
                       'lowsigWCRen':'Fake-#it{e} CR',
                       'fakeMu':'Fake-#it{#mu} CR',                       
                       'WCRlnu':'W$\\rightarrow\\ell\\nu$ CR',
                       'ZCRll':'Z$\\rightarrow\\ell\\ell$ CR',
                       }
        NameDict ={'ttbar':'Top$+$#it{VV}/#it{VVV}',
                       'eleFakes':'#it{e}-fakes',
                       'muoFakes':'#it{#mu}-fakes',
                   'Z_EWK':'#it{Z} EWK',
                   'W_EWK':'#it{W} EWK',
                   'Z_strong':'#it{Z} strong',
                   'W_strong':'#it{W} strong',
                   'Zg_EWK':'#it{Z+#gamma} EWK',
                   'Wg_EWK':'#it{W+#gamma} EWK',
                   'Zg_strong':'#it{Z+#gamma} strong',
                   'Wg_strong':'#it{W+#gamma} strong',                   
                   'signal':'#it{H}(#it{B}_{inv} = %0.2f)' %(options.hscale),
                   'data':'Data',
                   'bkgs':'Total Bkg',
                   'multijet':'Multijet',
                   }
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
                if n in titleKeys:
                    tableString += titleKeys[n] + " & "
                else:
                    tableString += n + " & "                    
                if i == self.colms:
                    if tableString[:-2] in titleKeys:
                        tableString = titleKeys[tableString[:-2]]+"\\\\\n"
                    else:
                        tableString = tableString[:-2]+"\\\\\n"
                    tableString += "\\hline\n"
        rowNameIndex = 0
        for i, e in enumerate(np.nditer(self.mat)):
            if self.rowNames and tmp == 1:
                if self.rowNames[rowNameIndex] in NameDict:
                    tableString += NameDict[self.rowNames[rowNameIndex]] + " & "
                else:
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
        if self.proc in ["W","Z","Zg","Wg"]:
            self.proc+="_"+sp[1]
        self.reg=sp[-3]
        self.mr=self.reg[-1]
        if (self.reg[-2]).isdigit():
            self.mr=self.reg[-2]+self.reg[-1]
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
        if self.hist and var and False:
            maxNbin=self.hist.GetNbinsX()
            self.hist.SetBinContent(maxNbin,self.hist.GetBinContent(maxNbin)+self.hist.GetBinContent(maxNbin+1))
            self.hist.SetBinError(maxNbin,math.sqrt((self.hist.GetBinError(maxNbin))**2+(self.hist.GetBinContent(maxNbin+1))**2))
            self.hist.SetBinContent(1,self.hist.GetBinContent(0)+self.hist.GetBinContent(1))
            self.hist.SetBinError(1,math.sqrt((self.hist.GetBinError(0))**2+(self.hist.GetBinContent(1))**2))
            self.hist.SetBinContent(0,0)
            self.hist.SetBinError(0,0)
            self.hist.SetBinContent(maxNbin,0)
            self.hist.SetBinError(maxNbin,0)
        if self.hist is None:
            print "Could not retrieve histogram!", self.hname, HistClass.Irfile
        #else:
        #    print 'Hist: ',self.hname
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
        for j in ["eleFakes", "muoFakes", "multijet", "NONE", "Nom"]:
            if j in self.hname: return False
        return True

    def isBkg(self):
        if self.proc in ["Z_strong","W_strong","Z_EWK","W_EWK","Zg_strong","Wg_strong","Zg_EWK","Wg_EWK","ttbar","eleFakes","muoFakes","multijet","VV","VVV","QCDw"]:
            return True
        return False

    def isData(self):
        if self.proc=="data":
            return True
        return False


    def isSignal(self):
        if self.proc in ["VBFH125", "ggFH125", "VH125",'VBFHgam125']:
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
        mysamples=["VBFH","Z_strong","W_strong","Z_EWK","W_EWK","ttbar","eleFakes","multijet","data"]
        if options.fakeMu:
            mysamples=["VBFH","Z_strong","W_strong","Z_EWK","W_EWK","ttbar","eleFakes","muoFakes","multijet","data"]
        elif options.ph_ana:
            mysamples=["VBFH","Z_strong","W_strong","Z_EWK","W_EWK","Zg_strong","Wg_strong","Zg_EWK","Wg_EWK","ttbar","data"]
        for p in mysamples:
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
                if options.ph_ana:
                    cls.regDict["SR{}".format(n)]=cls.nBins*3+n
                    cls.regDict["oneMuCR{}".format(n)]=cls.nBins+n
                    cls.regDict["oneEleCR{}".format(n)]=n
                    cls.regDict["twoLepCR{}".format(n)]=cls.nBins*2+n                    
                elif options.combinePlusMinus:
                    cls.regDict["SR{}".format(n)]=cls.nBins*4+n
                    cls.regDict["oneMuCR{}".format(n)]=cls.nBins*2+n
                    cls.regDict["oneEleCR{}".format(n)]=cls.nBins+n
                    cls.regDict["twoLepCR{}".format(n)]=cls.nBins*3+n
                    cls.regDict["oneEleLowSigCR{}".format(n)]=n
                    if options.fakeMu:
                        cls.regDict["SR{}".format(n)]=cls.nBins*5+n
                        cls.regDict["oneMuCR{}".format(n)]=cls.nBins*3+n
                        cls.regDict["oneEleCR{}".format(n)]=cls.nBins*2+n
                        cls.regDict["twoLepCR{}".format(n)]=cls.nBins*4+n
                        cls.regDict["oneEleLowSigCR{}".format(n)]=cls.nBins+n
                        cls.regDict["oneMuMTCR{}".format(n)]=n                        
                else:
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
            if options.ph_ana:
                cls.regionBins["SR"]=[cls.regDict[k] for k in cls.regDict if "SR" in k]
                cls.regionBins["ZCRll"]=[cls.regDict[k] for k in cls.regDict if "twoLepCR" in k]
                cls.regionBins["WCRenu"]=[cls.regDict[k] for k in cls.regDict if "oneEleCR" in k]
                cls.regionBins["WCRmunu"]=[cls.regDict[k] for k in cls.regDict if "oneMuCR" in k]                
            elif options.combinePlusMinus:
                cls.regionBins["SR"]=[cls.regDict[k] for k in cls.regDict if "SR" in k]
                cls.regionBins["ZCRll"]=[cls.regDict[k] for k in cls.regDict if "twoLepCR" in k]
                cls.regionBins["WCRenu"]=[cls.regDict[k] for k in cls.regDict if "oneEleCR" in k]
                cls.regionBins["WCRmunu"]=[cls.regDict[k] for k in cls.regDict if "oneMuCR" in k]
                cls.regionBins["lowsigWCRen"]=[cls.regDict[k] for k in cls.regDict if "oneEleLowSigCR" in k]
                if options.fakeMu:
                    cls.regionBins["fakeMu"]=[cls.regDict[k] for k in cls.regDict if "oneMuMTCR" in k]
                #cls.regionBins["WCRlnu"]=cls.regionBins["WCRenu"]+cls.regionBins["WCRmunu"]
                #cls.regionBins["lowsigWCRenu"]=cls.regionBins["lowsigWCRen"]
            else:
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
                #cls.regionBins["WCRlnu"]=cls.regionBins["WCRenu"]+cls.regionBins["WCRmunu"]
                cls.regionBins["lowsigWCRenu"]=cls.regionBins["lowsigWCRep"]+cls.regionBins["lowsigWCRen"]

def getBinsError(hist, bins):
    BE=0
    for bn in bins:
        if type(hist)==ROOT.TH1F:
            BE+=(hist.GetBinError(bn))**2 # FIXME squared or not?
        else:
            BE+=(hist.GetErrorYhigh(bn-1))**2
    return math.sqrt(BE)

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

def make_legend(can,poskeys=[0.845,0.09,0.991,0.87],ncolumns=1):#[0.0,0.04,0.155,0.6]
    leg=can.BuildLegend(poskeys[0],poskeys[1],poskeys[2],poskeys[3])
    leg.SetBorderSize(0)
    leg.SetFillStyle (0)
    leg.SetTextFont(42)
    leg.SetNColumns(ncolumns)
    leg.SetTextSize(0.05)
    legNew=leg.Clone()
    legNew.Clear()
    #leg.SetNColumns  (2)
    NameDict ={'ttbar':'Other',#'Top+#it{VV}/#it{VVV}',
                   'eleFakes':'#it{e}-fakes',
                   'muoFakes':'#it{#mu}-fakes',                   
                   'Z_EWK':'#it{Z} EWK',
                   'EWK W':'#it{W} EWK',
                   'W_EWK':'#it{W} EWK',
                   'Z_strong':'#it{Z} strong',
                   'W_strong':'#it{W} strong',
                   'Zg_EWK':'#it{Z+#gamma} EWK',                   
                   'Wg_EWK':'#it{W+#gamma} EWK',
                   'Zg_strong':'#it{Z+#gamma} strong',
                   'Wg_strong':'#it{W+#gamma} strong',
                   'signal':'#it{H}(#it{B}_{inv} = %0.2f)' %options.hscale,
                   'data':'Data',
                   'bkgs':'Uncertainty',
                   'multijet':'Multijet',
                   }
    if options.postFitPickleDir:
        NameDict['bkgs']='Uncertainty'
    
    if not options.scaleSig:
        NameDict['signal']='#it{H}(#it{B}_{inv} = %0.2f)' %(options.hscale)
    listInputs=[]
    legOrder=[]
    for i in leg.GetListOfPrimitives():
        
        if i.GetLabel().strip() in NameDict and  NameDict[i.GetLabel().strip()] in listInputs:
            removeLabel(leg, i.GetLabel())
            continue
            #print 'lab: ',i.GetLabel()
        else:
            if i.GetLabel().strip() in NameDict:
                listInputs+=[NameDict[i.GetLabel().strip()]]
        if i.GetLabel() not in ['signal','data']:
            i.GetObject().SetLineColor(i.GetObject().GetFillColor())
            i.GetObject().SetMarkerColor(i.GetObject().GetFillColor())
        if i.GetLabel() in NameDict:
            i.SetLabel(NameDict[i.GetLabel()])
        if 'Unc' in i.GetLabel().strip():
            i.GetObject().SetMarkerSize(0)
            i.GetObject().SetLineWidth(0)
            i.GetObject().SetMarkerColor(0)

    if not options.fakeMu:
        removeLabel(leg, 'dummy')
        removeLabel(leg, 'Others')
        removeLabel(leg, 'multijet')
        removeLabel(leg, 'W_EWK')
        removeLabel(leg, 'eleFakes')

    for i in leg.GetListOfPrimitives():
        print 'leg: ',i.GetLabel(),i.GetObject()
        legOrder+=[[i.GetLabel(),i.GetObject()]]
        
    for en in legOrder:
        if en[0]=='Data':
            legNew.AddEntry(en[1],en[0])
            break
    for en in legOrder:
        if 'Unc' in en[0]:
            legNew.AddEntry(en[1],en[0])
            break
    for ita in range(0,len(legOrder)):
        it=len(legOrder)-ita-1
        if 'Data' in legOrder[it][0]:
            continue
        if 'Unc' in legOrder[it][0]:
            continue
        if '#it{H}' in legOrder[it][0]:
            continue
        legNew.AddEntry(legOrder[it][1],legOrder[it][0])
    for en in legOrder:
        if '#it{H}' in en[0]:
            en[1].SetMarkerColor(en[1].GetLineColor())
            legNew.AddEntry(en[1],en[0])
            break
        
    nEntries=len(leg.GetListOfPrimitives())
    #leg.SetY1(0.9-nEntries*0.04)
    leg.Clear()
    return legNew


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
    if options.postFitPickleDir!=None:
        for i in range(1,DataMC2.GetNbinsX()+1):
            DataMC2.SetBinError(i,0.0)
    DataMC2.Divide(histDict["bkgs"])

    DataMC=OrderedDict()
    for reg in regionBinsDict:
        DataMC[reg]=0
        if getBinsYield(histDict["bkgs"], regionBinsDict[reg])>0.0:
            if options.data: DataMC[reg]=(getBinsYield(histDict["data"], regionBinsDict[reg])/getBinsYield(histDict["bkgs"], regionBinsDict[reg]))
        else:
            if options.data: DataMC[reg]=(0.0)
    altArray=[]                
    arrArray=[]
    x1a=ROOT.Double()
    y1a=ROOT.Double()
    for hkey in histDict:
        tmpArr=[]
        tmpAltArr=[]
        for regkey in regionDict:
            #tmpArr.append(str(round(histDict[hkey].GetBinContent(regionDict[regkey]),2))+" $\\pm$ "+str(round(histDict[hkey].GetBinError(regionDict[regkey]),2)))
            yldvR=0.0
            if type(histDict[hkey])==ROOT.TH1F:
                yldvR=(round(histDict[hkey].GetBinContent(regionDict[regkey]),1))
                yldeR=(round(histDict[hkey].GetBinError(regionDict[regkey]),1))
            else:
                histDict[hkey].GetPoint(regionDict[regkey]-1,x1a,y1a)
                yldvR=(round(y1a,1))
                ylde=histDict[hkey].GetErrorYhigh(regionDict[regkey]-1)
                yldeR=(round(ylde,1))
            tmpArr.append(" $%0.0f\\pm$ %0.0f"%(yldvR,yldeR))
            if not (hkey=='bkgs' or hkey.count('bkgsAsymErr')):
                if regkey.count('SR'):
                    tmpAltArr.append(" $%0.0f\\pm$ %0.0f"%(yldvR,yldeR))
        arrArray.append(tmpArr)
        if len(tmpAltArr)>0:
            altArray.append(tmpAltArr)
    arrArray.append([" $%0.2f\\pm$ %0.2f"%((round(DataMC2.GetBinContent(dm),2)),round(DataMC2.GetBinError(dm),2)) for dm in [regionDict[i] for i in regionDict]])
    tmpAltArr=[]
    for i in regionDict:
        if i.count('SR'):
            dm=regionDict[i]
            tmpAltArr.append("$%0.2f\\pm$ %0.2f"%((round(DataMC2.GetBinContent(dm),2)),(round(DataMC2.GetBinError(dm),2))) )
    altArray.append(tmpAltArr)
    texTable1=texTable(arrayArray=arrArray)
    colmNames=[reg for reg in regionDict]
    rowNames=[hkey.replace("_"," ") for hkey in histDict]+["Data/Bkg"]
    texTable1.setNames(rowNames, colmNames)
    print texTable1.getTableString()
    print "\n###########\n"


    arrArray2=[]
    for hkey in histDict:
        tmpArr2=[]
        for regkey in regionBinsDict:
            var=getBinsYield(histDict[hkey], regionBinsDict[regkey])
            varE=getBinsError(histDict[hkey], regionBinsDict[regkey])
            tmpArr2.append("$%0.0f\\pm$ %0.0f" %((round(var,2)),(round(varE,2))))
        arrArray2.append(tmpArr2)
    arrArray2.append([str(round(DataMC[f],3)) for f in DataMC])
    texTable2=texTable(arrayArray=arrArray2)
    colmNames2=[reg for reg in regionBinsDict]
    rowNames2=[hkey.replace("_"," ") for hkey in histDict]+["Data/Bkg"]
    texTable2.setNames(rowNames2, colmNames2)
    print texTable2.getTableString()
    print "\n###########\n"

    texTable3=texTable(arrayArray=altArray)
    colmNames=[]
    for reg in regionDict:
        if reg.count('SR'):
            colmNames+=[reg]
    rowNames=[]
    for hkey in histDict:
        if not (hkey.count('bkgsStat') or hkey.count('bkgsAsymErr')):
            rowNames+=[hkey.replace("_"," ")]
    rowNames+=["Data/Bkg"]
    texTable3.setNames(rowNames, colmNames)
    print texTable3.getTableString()
    print "\n###########\n"
    
    if makePDF:
        # texTable1.mirror()
        # texTable2.mirror()
        texTable1.createPDF(clean=True, fileName="yieldsAllRegions", big=True)
        texTable2.createPDF(clean=True, fileName="yieldsSummary", big=True)

    # Print transfer factors a=B_SR/B_CR
    B_WSR=(getBinsYield(histDict["W_strong"], regionBinsDict["SR"])+getBinsYield(histDict["W_EWK"], regionBinsDict["SR"]))
    B_WCR=(getBinsYield(histDict["W_strong"], regionBinsDict["WCRenu"])+getBinsYield(histDict["W_EWK"], regionBinsDict["WCRenu"])+getBinsYield(histDict["W_strong"], regionBinsDict["WCRmunu"])+getBinsYield(histDict["W_EWK"], regionBinsDict["WCRmunu"]))
    B_ZSR=(getBinsYield(histDict["Z_strong"], regionBinsDict["SR"])+getBinsYield(histDict["Z_EWK"], regionBinsDict["SR"]))
    B_ZCR=(getBinsYield(histDict["Z_strong"], regionBinsDict["ZCRll"])+getBinsYield(histDict["Z_EWK"], regionBinsDict["ZCRll"]))

    try:
        aW=B_WSR/B_WCR
        aZ=B_ZSR/B_ZCR
        print "aW:",aW
        print "aZ:",aZ
    except:
        print "aW,aZ not defined. B_WCR, B_ZCR:",B_WCR, B_ZCR
    doCRScaling=True
    for i in range(1,nbins+1):
        tmpNF_fake_ele_neg = getNF(histDict,[i],["eleFakes"])
        tmpNF_fake_ele_pos = getNF(histDict,[nbins+i],["eleFakes"])
        tmpNF_fake_ele = getNF(histDict,[i,nbins+i],["eleFakes"],True)
        if doCRScaling:
            Scale(histDict["eleFakes"],[nbins*2+i,nbins*3+i], tmpNF_fake_ele)
        tmpNF_WCR = getNF(histDict,[nbins*4+i,nbins*5+i,nbins*2+i,nbins*3+i],["W_strong","W_EWK"])
        tmpNF_ZCR = getNF(histDict,[6*nbins+i,7*nbins+i],["Z_strong","Z_EWK"])
        tmpB_WCR=getBinsYield(histDict["W_strong"], [nbins*4+i,nbins*5+i,nbins*2+i,nbins*3+i])+getBinsYield(histDict["W_EWK"], [nbins*4+i,nbins*5+i,nbins*2+i,nbins*3+i])
        tmpB_WSR=getBinsYield(histDict["W_strong"], [8*nbins+i])+getBinsYield(histDict["W_EWK"], [8*nbins+i])
        tmpB_ZSR=(getBinsYield(histDict["Z_strong"], [8*nbins+i])+getBinsYield(histDict["Z_EWK"], [8*nbins+i]))
        tmpB_ZCR=(getBinsYield(histDict["Z_strong"], [6*nbins+i,7*nbins+i])+getBinsYield(histDict["Z_EWK"], [6*nbins+i,7*nbins+i]))
        try:
            print "wNF{mr}=".format(mr=(i)),tmpNF_WCR," zNF: ",tmpNF_ZCR," FakeEleNeg: ",tmpNF_fake_ele_neg," FakeElePos: ",tmpNF_fake_ele_pos," FakeELe: ",tmpNF_fake_ele
            print "aW{mr}=".format(mr=(i)),tmpB_WSR/tmpB_WCR
            print "aZ{mr}=".format(mr=(i)),tmpB_ZSR/tmpB_ZCR
        except:
            print "aW{mr}, aZ{mr} not defined. B_WCR, B_ZCR".format(mr=(i)),tmpB_WCR,tmpB_ZCR,tmpNF_WCR

    print 'reduced kZ,kW'
    for i in range(1,nbins/2+1):
        tmpNF_fake_ele = getNF(histDict,[i,nbins+i,i+5,nbins+i+5],["eleFakes"])
        tmpNF_WCR = getNF(histDict,[nbins*4+i,nbins*5+i,nbins*2+i,nbins*3+i, nbins*4+i+5,nbins*5+i+5,nbins*2+i+5,nbins*3+i+5],["W_strong","W_EWK"])
        tmpNF_ZCR = getNF(histDict,[6*nbins+i,7*nbins+i,6*nbins+i+5,7*nbins+i+5],["Z_strong","Z_EWK"])
        tmpNF_WCRv = getNF(histDict,[nbins*4+i,nbins*5+i,nbins*2+i,nbins*3+i, nbins*4+i+5,nbins*5+i+5,nbins*2+i+5,nbins*3+i+5],["W_strong","W_EWK"],True)
        tmpNF_ZCRv = getNF(histDict,[6*nbins+i,7*nbins+i,6*nbins+i+5,7*nbins+i+5],["Z_strong","Z_EWK"],True)        
        if doCRScaling:
            Scale(histDict["Z_strong"],[nbins*8+i,nbins*8+i+5], tmpNF_ZCRv)
            Scale(histDict["Z_EWK"],[nbins*8+i,nbins*8+i+5], tmpNF_ZCRv)
            Scale(histDict["W_strong"],[nbins*8+i,nbins*8+i+5], tmpNF_WCRv)
            Scale(histDict["W_EWK"],[nbins*8+i,nbins*8+i+5], tmpNF_WCRv)
            
        tmpNF_SR1=getDataMC(histDict, [nbins*8+i])
        tmpNF_SR2=getDataMC(histDict, [nbins*8+i+5])
        try:
            print "wNF{mr}=".format(mr=(i+5)),tmpNF_WCR," zNF: ",tmpNF_ZCR," FakeELe: ",tmpNF_fake_ele,' SR: ',tmpNF_SR1,' SR5bin: ',tmpNF_SR2
        except:
            print "aW{mr}, aZ{mr} not defined. B_WCR, B_ZCR".format(mr=(i+5)),tmpB_WCR,tmpB_ZCR,tmpNF_WCR

def getNumberOfBins(rfileInput):
    tmpIrfile=ROOT.TFile(rfileInput)
    nbins=0
    LOK=None
    for p in ["VBFH","Z_strong","W_strong","Z_EWK","W_EWK","ttbar","eleFakes","muoFakes","multijet","Zg_strong","Wg_strong","Zg_EWK","Wg_EWK","data"]:
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
    byNum=9
    if options.ph_ana:
        byNum=4
    elif options.combinePlusMinus:
        byNum=5
        if options.fakeMu:
            byNum=6
    if options.ratio:
        can.Divide(1,2)
        can.cd(1)
        ROOT.gPad.SetBottomMargin(0)
        ROOT.gPad.SetRightMargin(0.16)
        ROOT.gPad.SetLeftMargin(0.1)
        ROOT.gPad.SetPad(0,0.3,1,1)
        if not options.ph_ana:
            ROOT.gPad.SetLogy()
        can.cd(2)
        ROOT.gPad.SetTopMargin(0)
        ROOT.gPad.SetBottomMargin(0.35)
        ROOT.gPad.SetLeftMargin(0.1)
        ROOT.gPad.SetRightMargin(0.16)
        ROOT.gPad.SetPad(0,0,1,0.3)
        can.cd(1)
    else:
        can.SetLogy()


    dummyHist=ROOT.TH1F("dummy","",byNum*nbins,0,byNum*nbins)
    dummyHist.SetStats(0)


    hDict=OrderedDict()
    hDictSig=OrderedDict()
    histNames=[]
    histNamesSig=[]
    totbkg=ROOT.TH1F("totbkg","",byNum*nbins,0,byNum*nbins)
    totbkg.SetStats(0)
    if options.stack_signal:
       histNames=["signal"]
    else:
        histNamesSig+=["signal"]#,"VBFH125","ggFH125","VH125","VBFHgam125"]
    histNames+=["W_strong", "W_EWK", "Z_strong", "Z_EWK", "eleFakes", "ttbar", "multijet"] # This order determines the order in which the hists are stacked , "Others"
    if options.fakeMu:
        histNames+=["W_strong", "W_EWK", "Z_strong", "Z_EWK", "eleFakes","muoFakes", "ttbar", "multijet"] # This order determines the order in which the hists are stacked , "Others"
    if options.ph_ana:
        histNames=["Z_strong","Z_EWK","W_EWK","W_strong","ttbar","Zg_strong","Zg_EWK","Wg_EWK","Wg_strong"] 

    regDict=OrderedDict()
    for n in range(1,nbins+1):
        if options.ph_ana:
            regDict["SR{}".format(n)]=nbins*3+n
            regDict["oneMuCR{}".format(n)]=nbins+n
            regDict["oneEleCR{}".format(n)]=n
            regDict["twoLepCR{}".format(n)]=nbins*2+n            
        elif options.combinePlusMinus:
            #if not options.cronly:
            regDict["SR{}".format(n)]=nbins*4+n
            regDict["oneMuCR{}".format(n)]=nbins*2+n
            regDict["oneEleCR{}".format(n)]=nbins+n
            regDict["twoLepCR{}".format(n)]=nbins*3+n
            regDict["oneEleLowSigCR{}".format(n)]=n
            if options.fakeMu:
                regDict["SR{}".format(n)]=nbins*5+n
                regDict["oneMuCR{}".format(n)]=nbins*3+n
                regDict["oneEleCR{}".format(n)]=nbins*2+n
                regDict["twoLepCR{}".format(n)]=nbins*4+n
                regDict["oneEleLowSigCR{}".format(n)]=nbins+n
                regDict["oneMuMTCR{}".format(n)]=n                
        else:
            #if not options.cronly:
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
    byNum=9

    if options.ph_ana:
        byNum=4
        regionBins["SR"]=[regDict[k] for k in regDict if "SR" in k]
        regionBins["ZCRll"]=[regDict[k] for k in regDict if "twoLepCR" in k]
        regionBins["WCRenu"]=[regDict[k] for k in regDict if "oneEleCR" in k]
        regionBins["WCRmunu"]=[regDict[k] for k in regDict if "oneMuCR" in k]
        regionBins["WCRlnu"]=regionBins["WCRenu"]+regionBins["WCRmunu"]
    elif options.combinePlusMinus:
        byNum=5
        regionBins["SR"]=[regDict[k] for k in regDict if "SR" in k]
        regionBins["ZCRll"]=[regDict[k] for k in regDict if "twoLepCR" in k]
        regionBins["WCRenu"]=[regDict[k] for k in regDict if "oneEleCR" in k]
        regionBins["WCRmunu"]=[regDict[k] for k in regDict if "oneMuCR" in k]
        regionBins["WCRlnu"]=regionBins["WCRenu"]+regionBins["WCRmunu"]
        regionBins["lowsigWCRen"]=[regDict[k] for k in regDict if "oneEleLowSigCR" in k]
        if options.fakeMu:
            byNum=6
            regionBins["fakeMu"]=[regDict[k] for k in regDict if "oneMuMTCR" in k]
        #regionBins["lowsigWCRenu"]=regionBins["lowsigWCRen"]
    else:
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
    dummyHist.GetYaxis().SetTitle("Events / Bin")
    dummyHist.GetYaxis().SetTitleSize(1.4*dummyHist.GetYaxis().GetTitleSize())
    dummyHist.GetYaxis().SetTitleOffset(0.45*dummyHist.GetYaxis().GetTitleOffset())    
    dummyHist.GetYaxis().SetRangeUser(1.001,2000)
    if options.ph_ana:
        dummyHist.GetYaxis().SetRangeUser(0.5,180.0)
    #dummyHist.GetYaxis().SetRangeUser(1.73,5000)
    if options.cronly:
        dummyHist.GetXaxis().SetRangeUser(0,44)
    dummyHist.Draw()

    hists=[]
    histsSig=[]
    for hname in histNames[::-1]:
        hists.append(ROOT.TH1F(hname,hname,nbins*byNum,0,nbins*byNum))
        hDict[hname]=hists[-1]
        hDict[hname].Sumw2()
    for hname in histNamesSig:
        histsSig.append(ROOT.TH1F(hname,hname,nbins*byNum,0,nbins*byNum))
        hDictSig[hname]=histsSig[-1]
        hDictSig[hname].Sumw2()
    data=ROOT.TH1F("data","data",nbins*byNum,0,nbins*byNum)
    hDict["data"]=data

    #Styles
    Style.setStyles(data,[1,0,2,0,0,1,20,1.2])
    if options.stack_signal:
        Style.setStyles(hDict["signal"],[2,2,3,0,0,0,0,0])
    else:
        Style.setStyles(hDictSig["signal"],[2,2,3,0,0,0,0,0])

    #Style.setStyles(hDict["Z_strong"],[1,1,1,46,1001,0,0,0])
    #Style.setStyles(hDict["Z_EWK"],[1,1,1,8,1001,0,0,0])
    #Style.setStyles(hDict["W_strong"],[1,1,1,9,1001,0,0,0])
    #Style.setStyles(hDict["W_EWK"],[1,1,1,5,1001,0,0,0])
    #Style.setStyles(hDict["ttbar"],[1,1,1,0,1001,0,0,0])
    #Style.setStyles(hDict["eleFakes"],[1,1,1,11,1001,0,0,0])
    #Style.setStyles(hDict["multijet"],[1,1,1,12,1001,0,0,0])
    if options.ph_ana:
        Style.setStyles(hDict["Zg_strong"],Style.styleDict["Z_strong"])
        Style.setStyles(hDict["Zg_EWK"],Style.styleDict["Z_EWK"])
        Style.setStyles(hDict["Wg_strong"],Style.styleDict["W_strong"])
        Style.setStyles(hDict["Wg_EWK"],Style.styleDict["W_EWK"])
    Style.setStyles(hDict["Z_strong"],Style.styleDict["Z_strong"])
    Style.setStyles(hDict["Z_EWK"],Style.styleDict["Z_EWK"])
    Style.setStyles(hDict["W_strong"],Style.styleDict["W_strong"])
    Style.setStyles(hDict["W_EWK"],Style.styleDict["W_EWK"])    
    Style.setStyles(hDict["ttbar"],Style.styleDict["ttbar"])
    if not options.ph_ana:
        Style.setStyles(hDict["eleFakes"],Style.styleDict["eleFakes"])
    if options.fakeMu:
        Style.setStyles(hDict["muoFakes"],Style.styleDict["muoFakes"])
    if "multijet" in hDict:
        Style.setStyles(hDict["multijet"],Style.styleDict["multijet"])
    if "Others" in hDict:
        Style.setStyles(hDict["Others"],[1,1,1,2,1001,0,0,0])

    # loop over all hists in input file and add their content to the right hist
    rfile=ROOT.TFile(options.input)
    LOK=rfile.GetListOfKeys()
    HistClass.Irfile=rfile
    HistClass.regDict=regDict

    region_keys = regDict.keys()
    hnames=[i.GetName() for i in LOK if ("Nom" in i.GetName() or "NONE" in i.GetName())]
    for key in hnames:
        # NOTE here you can specify hisotgrams which should be skipped
        if skipThis(key): continue
        # if the plots are not to shown, then skip
        checkRegion=False
        for rkey in region_keys:
            if rkey in key:
                checkRegion=True
                break
        if not checkRegion:
            continue

        histObj=HistClass(key)
        
        if not histObj.hist: continue
        if histObj.isSignal():
            if options.stack_signal:
                addContent(hDict["signal"], histObj.nbin, histObj.hist.GetBinContent(options.nBin), histObj.hist.GetBinError(options.nBin))
            else:
                addContent(hDictSig["signal"], histObj.nbin, histObj.hist.GetBinContent(options.nBin), histObj.hist.GetBinError(options.nBin))                
        elif histObj.proc in histNames+["data"]:
            addContent(hDict[histObj.proc], histObj.nbin, histObj.hist.GetBinContent(options.nBin), histObj.hist.GetBinError(options.nBin))
        else:
            if not (key.count('hQCDw_') or key.count('hVBFH')): # look for non H125 masses
                print key, "could not be identified correctly! BinContent will be added to Others"
                if "Others" in hDict:
                    addContent(hDict["Others"], histObj.nbin, histObj.hist.GetBinContent(options.nBin), histObj.hist.GetBinError(options.nBin))

    postFitPickles=None
    if options.postFitPickleDir!=None:
        if options.scaleSig:
            for ib in range(0,hDictSig["signal"].GetNbinsX()+1):
                hDictSig["signal"].SetBinContent(ib,0.0)
                hDictSig["signal"].SetBinError(ib,0.0)
        hist_array_keys = [i.GetName() for i in hists]
        postFitPickles = LoadPickleFiles(options.postFitPickleDir)
        for fpickle in postFitPickles: # example Fitted_events_VH125_VBFjetSel_2
            pickle_region_names = fpickle['names'] # these are the CR and SR names as entered. just a description of the entries
            print 'pickle_region_names:',pickle_region_names
            print 'pickle_region_names:',pickle_region_names,fpickle['TOTAL_FITTED_bkg_events']
            print 'pickle_region_names:',pickle_region_names,' %0.0f $\\pm$ %0.0f' %(fpickle['TOTAL_FITTED_bkg_events'][0],fpickle['TOTAL_FITTED_bkg_events_err'][0] )#
            # set the total bkg to its fitted values
            ireg=0
            pickle_region_namestmp=copy.deepcopy(pickle_region_names)
            if options.cronly and options.combinePlusMinus:
                pickle_region_namestmp=pickle_region_namestmp[1:]
            for iname in pickle_region_namestmp:
                if iname.rstrip('_cuts') in regDict and  'TOTAL_FITTED_bkg_events' in fpickle and ireg<len(fpickle['TOTAL_FITTED_bkg_events']):
                    totbkg.SetBinContent(regDict[iname.rstrip('_cuts')],fpickle['TOTAL_FITTED_bkg_events'][ireg])
                    totbkg.SetBinError  (regDict[iname.rstrip('_cuts')],fpickle['TOTAL_FITTED_bkg_events_err'][ireg])
                else:
                    print 'ERROR missing region: ',iname
                ireg+=1
            # set the signal and bkg individually
            for pickle_key in fpickle.keys():
                print pickle_key,fpickle[pickle_key][0]#['TOTAL_FITTED_bkg_events'],'+/-',fpickle[pickle_key]['TOTAL_FITTED_bkg_events_err']
                isError=False
                if  ('Fitted_events_' in pickle_key): # only process the fitted events here
                    pickle_key_remFit = pickle_key[len('Fitted_events_'):]
                elif  ('Fitted_err_' in pickle_key): # only process the fitted events here
                    pickle_key_remFit = pickle_key[len('Fitted_err_'):]
                    isError=True
                else:
                    continue
                #if ('Fitted_events_VBFH' in pickle_key): # skip signal
                #    continue
                if ('Fitted_err_' in pickle_key and 'H125' in pickle_key) and options.stack_signal: # skip signal
                    if pickle_key_remFit[:pickle_key_remFit.find('_')] in ['VBFH125','VH125','ggFH125','VBFHgam125']:
                         if 'signal' in hDict:
                            ireg=0
                            for iname in pickle_region_names:
                                if isError:
                                    print 'SIGGE',ireg,pickle_key,pickle_key_remFit[:pickle_key_remFit.find('_')],fpickle[pickle_key][ireg]                                    
                                    e1=hDict['signal'].GetBinError(regDict[iname.rstrip('_cuts')])
                                    if not options.show_mc_stat_err:
                                        hDict['signal'].SetBinError(regDict[iname.rstrip('_cuts')],math.sqrt((fpickle[pickle_key][ireg])**2+e1**2))
                                ireg+=1
                if pickle_key_remFit.find('_')>0 and options.scaleSig:
                    if pickle_key_remFit[:pickle_key_remFit.find('_')] in ['VBFH125','VH125','ggFH125','VBFHgam125']:
                        if 'signal' in hDictSig:
                            ireg=0
                            for iname in pickle_region_names:
                                if not isError:
                                    print 'SIGGV',ireg,pickle_key,pickle_key_remFit[:pickle_key_remFit.find('_')],fpickle[pickle_key][ireg]
                                    hDictSig['signal'].SetBinContent(regDict[iname.rstrip('_cuts')],fpickle[pickle_key][ireg]+hDictSig['signal'].GetBinContent(regDict[iname.rstrip('_cuts')]))
                                else:
                                    print 'SIGGE',ireg,pickle_key,pickle_key_remFit[:pickle_key_remFit.find('_')],fpickle[pickle_key][ireg]                                    
                                    e1=hDictSig['signal'].GetBinError(regDict[iname.rstrip('_cuts')])
                                    if not options.show_mc_stat_err:
                                        hDictSig['signal'].SetBinError(regDict[iname.rstrip('_cuts')],math.sqrt((fpickle[pickle_key][ireg])**2+e1**2))
                                ireg+=1
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
                    if isError:
                        #print pickle_key,fpickle[pickle_key][ireg]
                        totalErrStatSyst = math.sqrt((fpickle[pickle_key][ireg])**2+(histToSet.GetBinError(regDict[iname.rstrip('_cuts')]))**2)
                        if not options.show_mc_stat_err:
                            histToSet.SetBinError(regDict[iname.rstrip('_cuts')],totalErrStatSyst)
                    else:
			#print "Get bin content ",histToSet.GetBinContent(regDict[iname.rstrip('_cuts')])
			#print "Set bin content ",fpickle[pickle_key][ireg]
                        histToSet.SetBinContent(regDict[iname.rstrip('_cuts')],fpickle[pickle_key][ireg])
                    ireg+=1
                
    #defining bkg hist
    bkgsList=["Z_strong","Z_EWK","W_EWK","W_strong","eleFakes","ttbar","multijet"] #+["Others"]
    if options.fakeMu:
        bkgsList=["Z_strong","Z_EWK","W_EWK","W_strong","eleFakes","muoFakes","ttbar","multijet"] #+["Others"]
    if options.ph_ana:
        bkgsList=["Z_strong","Z_EWK","W_EWK","W_strong","ttbar","Zg_strong","Zg_EWK","Wg_EWK","Wg_strong"] #+["Others"]        
    bkgs=ROOT.TH1F("bkgs","bkgs",nbins*byNum,0,nbins*byNum)
    hDict["bkgs"]=bkgs
    hDict["bkgsStat"]=bkgs.Clone() # this has the bkg mc stat uncertainty
    for bkg in bkgsList:
        hDict["bkgs"].Add(hDict[bkg])
        hDict["bkgsStat"].Add(hDict[bkg])
    # Set the MC stat uncertainties to 0 in the systematics plot
    if not options.show_mc_stat_err and postFitPickles!=None:
        for i in range(0,hDict["bkgs"].GetNbinsX()):
            hDict["bkgs"].SetBinError(i,0.0)

    hStack=ROOT.THStack()
    for h in hists:
        hStack.Add(h)

    if not options.unBlindSR:
        # totalMC=get_THStack_sum(hStack)
        for SRbin in regionBins["SR"]:
            hDict["data"].SetBinContent(SRbin,bkgs.GetBinContent(SRbin))

    if not options.ph_ana:
        dummyHist.SetMaximum(hStack.GetMaximum()*3.4)
    hStack.Draw("samehist")
    if options.data: data.Draw("Esame")
    if options.stack_signal:
        for ib in range(1,hDict["signal"].GetNbinsX()+1):
            hDict["signal"].SetBinContent(ib,options.hscale*hDict["signal"].GetBinContent(ib))
    else:
        hDictSig["signal"].Scale(options.hscale)
    print 'scaling signal to %0.2f' %(options.hscale)
    if not options.stack_signal:
        hDictSig["signal"].Draw('HISTsame')
    # print the stat uncertainties:
    if options.show_mc_stat_err:
        if options.combinePlusMinus:
            regionsList=[]
            if options.fakeMu:
                regionsList=['gamma_stat_oneMuMTCRX_obs_cuts_bin_0',]
            regionsList+=[
            'gamma_stat_oneEleLowSigCRX_obs_cuts_bin_0',
            'gamma_stat_oneEleCRX_obs_cuts_bin_0',
            'gamma_stat_oneMuCRX_obs_cuts_bin_0',
            'gamma_stat_twoLepCRX_obs_cuts_bin_0',
            'gamma_stat_SRX_obs_cuts_bin_0',    
            ]
        else:
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
            #print 'bin: ',i,nameGamma,' %0.3f %0.3f' %((data.GetBinError(i)/total_bin_err),(hDict["bkgs"].GetBinError(i)/total_bin_err)) #can uncomment to print to command line
            writeLine+=nameGamma+' %0.3f %0.3f\n' %((data.GetBinError(i)/total_bin_err),(hDict["bkgs"].GetBinError(i)/total_bin_err))
        statFil=open('statunc.txt','w')
        statFil.write(writeLine)
        statFil.close()

    systHist=hDict["bkgs"]
    systHist.SetName('bkgsCopy')
    systHistAsym = ROOT.TGraphAsymmErrors(systHist)
    if postFitPickles!=None:
        systHistAsym = ROOT.TGraphAsymmErrors(totbkg)
        systHistAsym.SetName('bkgs')
        totbkg.SetName('bkgs')
        totbkg.SetTitle('bkgs')
        for i in range(1,55):
            print totbkg.GetBinContent(i),totbkg.GetBinError(i)
        hDict["bkgs"]=totbkg.Clone()
        hDict["bkgsStat"]=totbkg.Clone()
        bkgs=totbkg.Clone()
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

            if options.combinePlusMinus:
                if 'oneElePosCR' in k:
                    continue
                elif 'oneEleNegCR' in k:
                    continue
                elif 'oneEleNegLowSigCR' in k:
                    continue
                elif 'oneElePosLowSigCR' in k:
                    continue
                elif 'oneMuNegCR' in k:
                    continue
                elif 'oneMuPosCR' in k:
                    continue                
                elif 'twoMuCR' in k:
                    continue
                elif 'twoEleCR' in k:
                    continue
            if "theoFactors" in k or "NONEBlind" in k: continue
            tmpHist=HistClass(k)

            # check if this is a one sided systematic
            for sy in tmpHist.systs:
                if sy in one_sided_list:
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
    #if postFitPickles!=None:
    #    for fpickle in postFitPickles: # example Fitted_events_VH125_VBFjetSel_2
    #        pickle_region_names = fpickle['names'] # these are the CR and SR names as entered. just a description of the entries
    #        for pickle_key in fpickle.keys():
    #            if not ('Fitted_err_' in pickle_key): # only process the fitted events here
    #                continue
    #            pickle_key_remFit = pickle_key[len('Fitted_err_'):]
    #            m=0
    #            for i in hist_array_keys:
    #                if i in pickle_key_remFit:
    #                    break
    #                m+=1
    #            if m>=len(hists):
    #                print 'Post fit syst band - could not find (fine if signal): ',pickle_key
    #                continue
    #            histToSet = hists[m]
    #            ireg=0
    #            #print fpickle[pickle_key]
    #            for iname in pickle_region_names:
    #                ey_low=systHistAsym.GetErrorYlow(regDict[iname.rstrip('_cuts')]-1)
    #                ey_new = fpickle[pickle_key][ireg]
    #                e_new = math.sqrt(ey_low*ey_low+ey_new*ey_new)
    #                #print 'e_new:',e_new
    #                if not options.show_mc_stat_err:
    #                    systHistAsym.SetPointEYlow(regDict[iname.rstrip('_cuts')]-1,e_new)
    #                    systHistAsym.SetPointEYhigh(regDict[iname.rstrip('_cuts')]-1,e_new)
    #                ireg+=1
        
    ROOT.gStyle.SetErrorX(0.5)
    #fillStyle = 3345 #3004 # was 3018
    fillStyle = 3004 # was 3018
    ROOT.gStyle.SetHatchesLineWidth(1)
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

    texts = ATLAS.getATLASLabels(can, 0.125, 0.86, options.lumi, selkey="",preliminary=options.preliminary)

    for text in texts:
        text.Draw()

    if options.ratio:
        can.cd(2)
        rHist=data.Clone("ratioHist")
        rbkgs = hDict["bkgsStat"].Clone()
        if (not options.show_mc_stat_err and options.postFitPickleDir!=None): # removing mc stat unc.
            for i in range(0,rbkgs.GetNbinsX()+1):
                #print 'stats are set to zero!'
                rbkgs.SetBinError(i,0.0)
        
        rHist.Divide(rbkgs)
        rHist.GetYaxis().SetTitle("Data / Bkg")
        rHist.GetYaxis().SetTitleOffset(.3)
        rHist.GetYaxis().SetTitleSize(0.145)
        rHist.GetYaxis().CenterTitle()

	#Set x axis labels
        for k in regDict:
	    if options.combinePlusMinus:
	        index=k.find('R')
                rHist.GetXaxis().SetBinLabel(regDict[k],k[index+1::])
	        rHist.GetXaxis().LabelsOption('h')
	    else:
                rHist.GetXaxis().SetBinLabel(regDict[k],k)
        rHist.GetXaxis().SetLabelSize(0.1)
        rHist.GetYaxis().SetLabelSize(0.1)
	
        line1=data.Clone("line1")
        for i in range(1,line1.GetNbinsX()+1):
            line1.SetBinContent(i,1)
        Style.setLineAttr(line1,1,2,1)

        if options.cronly:
            rHist.GetXaxis().SetRangeUser(0,44)
        rHist.GetYaxis().SetRangeUser(0.801,1.1999)
        if options.ph_ana:
            rHist.GetYaxis().SetRangeUser(0.001,1.9999)            
        rHist.Draw()
        line1.Draw("histsame")
        val=0
        if options.show_mc_stat_err or options.syst!="" or options.postFitPickleDir!=None:
            if options.show_mc_stat_err and options.postFitPickleDir==None: # the post fit already has the MC stat uncertainties included
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
                if val==0:#AMANDA - hack for bkgonly fits, final bin (99) is empty
                    print "bin ",i," has no content"
                    val=0.00001
                eyu=systHistAsym.GetErrorYhigh   (j-1)/val
                eyd=systHistAsym.GetErrorYlow    (j-1)/val
                systHistAsymRatio.SetPointEYhigh(j-1,eyu)
                systHistAsymRatio.SetPointEYlow (j-1,eyd)

            #rbkgs.Draw('same e2') # divides (up-down)/2 for symmetric unc.
            systHistAsymRatio.Draw('same e2')
            line1.Draw("histsame")
            rHist.Draw('same')
            
            
        can.GetPad(2).RedrawAxis()
        can.GetPad(2).Modified()
        can.GetPad(2).Update()
        can.cd(1)
    can.cd(1)
    ROOT.gPad.RedrawAxis()
    ROOT.gPad.Modified()
    ROOT.gPad.Update()

    #can.cd(1)
    blindStr=""
    if not options.unBlindSR:
        blindStr=", SR blinded"
    if options.cronly:
        blindStr=", CR only"
    namingScheme="Pre-fit"
    if options.postFitPickleDir!=None:
        namingScheme="Post-fit"

    preFitLabel=ROOT.TLatex(.43,.86,namingScheme+blindStr)
    preFitLabel.SetNDC()
    preFitLabel.SetTextFont(72)
    preFitLabel.SetTextSize(0.055)
    preFitLabel.SetTextAlign(11)    
    preFitLabel.SetTextColor(ROOT.kBlack)
    preFitLabel.Draw()

    can.Modified()
    can.Update()

    #Draw region boxes under axis to clarify plot
    can.cd()
    labelTxt = ROOT.TLatex()
    labelTxt.SetTextAlign(11)

    nameMap={#'FakeE':'#it{W}_{#it{e#nu}}^{low} CR',#Fake-#it{e} CR
              #   'Wenu':'#it{W}_{#it{e#nu}}^{high} CR',##it{W}#rightarrow#it{e#nu} CR
              'FakeE':'Fake-#it{e} CR',#Fake-#it{e} CR
              'FakeM':'Fake-#it{#mu} CR',#Fake-#it{e} CR
                 'Wenu':'#it{W}_{#it{e#nu}} CR',##it{W}#rightarrow#it{e#nu} CR
                 'Wmunu':'#it{W}_{#it{#mu#nu}} CR', ##it{W}#rightarrow#it{#mu#nu}
                 'Zll':'#it{Z}_{#it{ll}} CR',##it{Z}#rightarrow#it{ll}
                 }
    yvallab=0.0345
    shift=0.01
    newShift=-0.06
    if options.ph_ana:
        nameMap={#'FakeE':'#it{W}_{#it{e#nu}}^{low} CR',#Fake-#it{e} CR
              #   'Wenu':'#it{W}_{#it{e#nu}}^{high} CR',##it{W}#rightarrow#it{e#nu} CR
              'FakeE':'Fake-#it{e} CR',#Fake-#it{e} CR
              'FakeM':'Fake-#it{#mu} CR',#Fake-#it{e} CR
                 'Wenu':'#it{W}_{#it{e#nu}}^{#it{#gamma}} CR',##it{W}#rightarrow#it{e#nu} CR
                 'Wmunu':'#it{W}_{#it{#mu#nu}}^{#it{#gamma}} CR', ##it{W}#rightarrow#it{#mu#nu}
                 'Zll':'#it{Z}_{#it{ll}}^{#it{#gamma}} CR',##it{Z}#rightarrow#it{ll}
                 }
        
        shift=0.01
        newShift=-0.06
        line0=ROOT.TLine(0.162+newShift-0.002,0.02,0.162+newShift-0.002,0.11)
        line0.Draw()
        labelTxt.DrawLatex(0.20+shift+0.005+newShift,yvallab,nameMap['Wenu'])
        line2=ROOT.TLine(0.347+newShift-0.002,0.02,0.347+newShift-0.002,0.11)
        line2.Draw()
        labelTxt.DrawLatex(0.39+shift+0.005+newShift,yvallab,nameMap['Wmunu'])
        line3=ROOT.TLine(0.531+newShift-0.001,0.02,0.531+newShift-0.001,0.11)
        line3.Draw()
        labelTxt.DrawLatex(0.58+shift+newShift,yvallab,nameMap['Zll'])
        line4=ROOT.TLine(0.715+newShift,0.02,0.715+newShift,0.11)
        line4.Draw()        
        labelTxt.DrawLatex(0.79+newShift,yvallab,"SR")
        line5=ROOT.TLine(0.9+newShift,0.02,0.9+newShift,0.11)
        line5.Draw()
        hline=ROOT.TLine(0.16+newShift,0.08,0.9+newShift,0.08)
        hline.Draw()
        hline0=ROOT.TLine(0.16+newShift,0.02,0.9+newShift,0.02)
        hline0.Draw()
    elif not options.cronly:
        if options.combinePlusMinus:
            labelTxt.SetTextSize(0.04)
        line00=ROOT.TLine(0.16+newShift,0.02,0.16+newShift,0.11)
        line00.Draw()
        labelTxt.DrawLatex(0.19+shift-0.01+newShift,yvallab,nameMap['FakeE'])
        line0=ROOT.TLine(0.31+newShift-0.002,0.02,0.31+newShift-0.002,0.11)
        line0.Draw()
        labelTxt.DrawLatex(0.33+shift+0.005+newShift,yvallab,nameMap['Wenu'])
        line2=ROOT.TLine(0.458+newShift-0.002,0.02,0.458+newShift-0.002,0.11)
        line2.Draw()
        labelTxt.DrawLatex(0.48+shift+0.005+newShift,yvallab,nameMap['Wmunu'])
        line3=ROOT.TLine(0.605+newShift-0.001,0.02,0.605+newShift-0.001,0.11)
        line3.Draw()
        labelTxt.DrawLatex(0.645+shift+newShift,yvallab,nameMap['Zll'])
        line4=ROOT.TLine(0.752+newShift,0.02,0.752+newShift,0.11)
        line4.Draw()        
        labelTxt.DrawLatex(0.81+newShift,yvallab,"SR")
        line5=ROOT.TLine(0.9+newShift,0.02,0.9+newShift,0.11)
        line5.Draw()
        hline=ROOT.TLine(0.16+newShift,0.08,0.9+newShift,0.08)
        hline.Draw()
        hline0=ROOT.TLine(0.16+newShift,0.02,0.9+newShift,0.02)
        hline0.Draw()
    else:
        if options.combinePlusMinus:
            labelTxt.SetTextSize(0.045)
        line00=ROOT.TLine(0.16,0.02,0.16,0.11)
        line00.Draw()
        labelTxt.DrawLatex(0.21+shift,yvallab,nameMap['FakeE'])
        line0=ROOT.TLine(0.345,0.02,0.345,0.11)
        line0.Draw()
        labelTxt.DrawLatex(0.395+shift,yvallab,nameMap['Wenu'])
        line2=ROOT.TLine(0.53,0.02,0.53,0.11)
        line2.Draw()
        labelTxt.DrawLatex(0.58+shift,yvallab,nameMap['Wmunu'])
        line3=ROOT.TLine(0.715,0.02,0.715,0.11)
        line3.Draw()
        labelTxt.DrawLatex(0.765+shift,yvallab,nameMap['Zll'])
        line5=ROOT.TLine(0.9,0.02,0.9,0.11)
        line5.Draw()
        hline=ROOT.TLine(0.16,0.08,0.9,0.08)
        hline.Draw()
        hline0=ROOT.TLine(0.16,0.02,0.9,0.02)
        hline0.Draw()        

    if not options.quite:
        raw_input("Press Enter to continue")

    extraName=''
    if options.cronly:
        extraName='_cronly'
    if not options.unBlindSR:
        extraName+='_blind'
    if options.preliminary:
        extraName+='_prelim'
    if options.saveAs and options.postFitPickleDir!=None:
        can.SaveAs("postFit"+extraName+"."+options.saveAs)
        can.SaveAs("postFit"+extraName+".root")
    elif options.saveAs:
        can.SaveAs("preFit"+extraName+"."+options.saveAs)
        can.SaveAs("preFit"+extraName+".root")        

    rfile.Close()


def compareMain(options):
    if options.quite:
        ROOT.gROOT.SetBatch(True)
    openRfiles={}
    for i,rfile in enumerate(options.compare.split(",")):
        openRfiles[i]=ROOT.TFile(rfile)

    ATLAS.Style()
    byNum=9
    if options.combinePlusMinus:
        byNum=5
    mjjBins=None
    # loop over all hists in input file and add their content to the right hist
    histDict={}
    for i in openRfiles:
        print "loading",openRfiles[i].GetName()
        histDict[i]={"bkg":None}
        if options.data:
            histDict[i]["data"]=None
            histDict[i]["Data/Bkg"]=None
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
                    histDict[i]["bkg"]=ROOT.TH1F("bkg{}".format(i),"",byNum*mjjBins,0,byNum*mjjBins)
                    addContent(histDict[i]["bkg"], histObj.nbin, histObj.hist.GetBinContent(options.nBin), histObj.hist.GetBinError(options.nBin))
            elif histObj.isData() and options.data:
                try:
                    addContent(histDict[i]["data"], histObj.nbin, histObj.hist.GetBinContent(options.nBin), histObj.hist.GetBinError(options.nBin))
                except:
                    histDict[i]["data"]=ROOT.TH1F("data{}".format(i),"",byNum*mjjBins,0,byNum*mjjBins)
                    addContent(histDict[i]["data"], histObj.nbin, histObj.hist.GetBinContent(options.nBin), histObj.hist.GetBinError(options.nBin))

        if options.data:
            histDict[i]["Data/Bkg"]=histDict[i]["data"].Clone("Data/Bkg{}".format(i))
            histDict[i]["Data/Bkg"].Divide(histDict[i]["bkg"])

        for k in histDict:
            for r in histDict[k]:
                try:
                    histDict[k][r].SetLineColor(k+1)
                    histDict[k][r].SetLineWidth(3)
                except:
                    print r,"not found",openRfiles[k].GetName()

    c1=ROOT.TCanvas("c1","c2",1600,1200)

    dummyHist=ROOT.TH1F("dummy","",byNum*mjjBins,0,byNum*mjjBins)
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
                    if p=="Data/Bkg":
                        var=var/len(HistClass.regionBins[n])
                        varE=varE/len(HistClass.regionBins[n])
                    tmpForRatioVals.append(var)
                    colmVals.append(str(round(var,2))+" $\\pm$ "+str(round(varE,2)))
                tmpForRatio.append(tmpForRatioVals)
                rowVals.append(colmVals)
            if options.ratio and not(p=="Data/Bkg"): #TODO add this also for Data/Bkg summary table
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
        if p=="Data/Bkg":
            c1.SetLogy(0)
            dummyHist.SetMaximum(3)
            dummyHist.SetMinimum(0)
            dummyHist.GetYaxis().SetTitle("Data / Bkg")
            line1=dummyHist.Clone("line1")
            for i in range(1,line1.GetNbinsX()+1):
                line1.SetBinContent(i,1)
            Style.setLineAttr(line1,2,2,3)
            dummyHist.Draw()
            line1.Draw("histsame")
        else:
            c1.SetLogy()
            dummyHist.SetMaximum(9000)
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
            if entry_name=='bkgs':
                entry_name='Uncertainty'
            if entry_name=='bkgs' and options.postFitPickleDir!=None:
                entry_name='Fit Uncertainty'
            leg.AddEntry(histDict[k][p],entry_name,"l")
            histDict[k][p].Draw("Ehistsame")
        texts = ATLAS.getATLASLabels(c1, 0.54, 0.78, options.lumi, selkey="",preliminary=options.preliminary)
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


def setBinWidth(var, histList):
    #return
    for h in histList: 
        if var=="jj_mass":
            for ib in range(2,h.GetNbinsX()+1):
                wid=h.GetXaxis().GetBinWidth(ib)
                #print 'wid',wid
                if wid<500.0 and wid>100.0:
                    expV=h.GetBinContent(ib)
                    expE=h.GetBinError(ib)
                    h.SetBinContent(ib,expV*500.0/wid)
                    h.SetBinError(ib,expE*500.0/wid)

def plotVar(options):
    if options.quite:
        ROOT.gROOT.SetBatch(True)
    ATLAS.Style()
    opt=options.plot.split(",")
    var=opt[0]
    reg=opt[1]
    mjjBins=opt[2].split("_")
    plotIndex=0
    if reg=='twoEleCR':
        plotIndex=7
    if reg=='twoMuCR':
        plotIndex=8
    if reg=='oneMuPosCR':
        plotIndex=5
    if reg=='oneMuNegCR':
        plotIndex=6
    if options.ph_ana:
        if reg=='twoLepCR':
            plotIndex=3
        if reg=='oneMuCR':
            plotIndex=2
        if reg=='oneEleCR':
            plotIndex=1
    if options.combinePlusMinus:
        if reg=='twoLepCR':
            plotIndex=4
        if reg=='oneMuCR':
            plotIndex=3
        if reg=='oneEleCR':
            plotIndex=1
        if reg=='oneEleLowSigCR':
            plotIndex=2
        if options.fakeMu:
            if reg=='twoLepCR':
                plotIndex=5
            if reg=='oneMuCR':
                plotIndex=3
            if reg=='oneMuMTCR':
                plotIndex=1
            if reg=='oneEleCR':
                plotIndex=2
            if reg=='oneEleLowSigCR':
                plotIndex=3
    rfile=ROOT.TFile(options.input)
    AltDphi=True
    postFitPickles=None
    fittedSRVals={}
    fittedSRErrs={}
    fittedSRTotErrs={}
    fittedMCVals={}
    fittedMCErrs={}
    if options.postFitPickleDir!=None:
        postFitPickles = LoadPickleFiles(options.postFitPickleDir)
        for fpickle in postFitPickles: # example Fitted_events_VH125_VBFjetSel_2
            #['SR7', 'oneElePosCR7', 'oneEleNegCR7', 'oneElePosLowSigCR7', 'oneEleNegLowSigCR7', 'oneMuPosCR7', 'oneMuNegCR7', 'twoEleCR7', 'twoMuCR7']
            pickle_region_names = fpickle['names'] # these are the CR and SR names as entered. just a description of the entries
            #print pickle_region_names #['SR8', 'oneEleCR8', 'oneEleLowSigCR8', 'oneMuCR8', 'twoLepCR8']
            if 'TOTAL_FITTED_bkg_events_err' in fpickle:
                fittedSRTotErrs[pickle_region_names[0][2:]]=fpickle['TOTAL_FITTED_bkg_events_err'][plotIndex]
            for pickle_key in fpickle.keys():
                print pickle_key
                if not options.scaleSig:
                    if 'VH125' in pickle_key:
                        continue
                    if 'VBFH125' in pickle_key:
                        continue
                    if 'VBFHgam125' in pickle_key:
                        continue                    
                    if 'ggFH125' in pickle_key:
                        continue
                if  ('Fitted_events_' in pickle_key): # only process the fitted events here
                    pickle_key_remFit = pickle_key[len('Fitted_events_'):]
                    #print 'pickle_key_remFit:',pickle_key_remFit
                    #print fpickle[pickle_key][0],pickle_region_names[0],pickle_region_names
                    fittedSRVals[pickle_key_remFit]=fpickle[pickle_key][plotIndex] # 0 is the SR
                    #print 'Fitted_events_',pickle_key_remFit,fpickle[pickle_key][plotIndex]
                elif ('Fitted_err_' in pickle_key):
                    pickle_key_remFit = pickle_key[len('Fitted_err_'):]
                    fittedSRErrs[pickle_key_remFit]=fpickle[pickle_key][plotIndex] # 0 is the SR
                    #print 'Fitted_err_',pickle_key_remFit,fpickle[pickle_key][plotIndex]
                elif ('MC_exp_events_' in pickle_key):
                    pickle_key_remFit = pickle_key[len('MC_exp_events_'):]
                    fittedMCVals[pickle_key_remFit]=fpickle[pickle_key][plotIndex] # 0 is the SR
                elif ('MC_exp_err_' in pickle_key):
                    pickle_key_remFit = pickle_key[len('MC_exp_err_'):]
                    fittedMCErrs[pickle_key_remFit]=fpickle[pickle_key][plotIndex] # 0 is the SR                    
                else:
                    continue

    print 'multijet_VBFjetSel_X'
    for ib in range(1,3):
        areaName='multijet_VBFjetSel_X'.replace('X','%s' %ib)
        print areaName,fittedMCVals[areaName],fittedMCErrs[areaName],fittedSRVals[areaName],fittedSRErrs[areaName]
    
    bkgDict={}
    bkgPreFitDict={}
    bkgPreFit=None
    sigDict={}
    systHistAsymTot = None #ROOT.TGraphAsymmErrors(systHist)
    systHistAsym = None #ROOT.TGraphAsymmErrors(systHist)
    #for i in range(0,systHist.GetNbinsX()):
    #    systHistAsym.SetPointEXhigh(i-1,systHist.GetXaxis().GetBinWidth(i)/2.0)
    #    systHistAsym.SetPointEXlow(i-1,systHist.GetXaxis().GetBinWidth(i)/2.0)
    #systHistAsym.SetPointEYlow(regDict[iname.rstrip('_cuts')]-1,e_new)
    #systHistAsym.SetPointEYhigh(regDict[iname.rstrip('_cuts')]-1,e_new)
    HistClass.Irfile=rfile
    bkg=None
    signal=None
    multijet=None
    hnames=[j.GetName() for j in rfile.GetListOfKeys() if (("Nom" in j.GetName() or "NONE" in j.GetName()) and var in j.GetName() and reg in j.GetName()) ]

    for h in hnames:
        if h.count('Z_strongPTVExt'):
            continue
        hObj=HistClass(h, var)
        # check the bin width
        if not postFitPickles:
            setBinWidth(var,[hObj.hist])
        
        systHistAsym=hObj.hist.Clone()
        setBinWidth(var,[systHistAsym])
        if hObj.isBkg() and (hObj.mr in mjjBins):
            bkgPreFitDict[hObj.proc]=hObj.hist.Clone()
            setBinWidth(var,[bkgPreFitDict[hObj.proc]])
            if bkgPreFit==None:
                #print 'prefit: ',h
                bkgPreFit=hObj.hist.Clone()
                setBinWidth(var,[bkgPreFit])
            else:
                #print 'prefit: ',h
                #setBinWidth(var,[bkgPreFitDict[hObj.proc]])
                bkgPreFit.Add(bkgPreFitDict[hObj.proc])
        #print h
        #if systHistAsym==None:
            #systHistAsym=ROOT.TGraphAsymmErrors(hObj.hist.Clone())
            
            #for i in range(0,hObj.hist.GetNbinsX()):
                #systHistAsym.SetPointEXhigh(i-1,hObj.hist.GetXaxis().GetBinWidth(i)/2.0)
                #systHistAsym.SetPointEXlow(i-1,hObj.hist.GetXaxis().GetBinWidth(i)/2.0)
        if postFitPickles:
            #print h[1:h.find('Nom')] #hZ_EWK_VBFjetSel_1Nom_SR1_obs_jj_mass need to map to VBFH125_VBFjetSel_8
            key_name=h[1:h.find('Nom')]
            print 'key_name:',key_name,hObj.hist.Integral()
            if key_name in fittedSRVals:
                #hObj.hist.SetBinContent(int(hObj.mr)+1,float(fittedSRVals[key_name]))
                total_err = ROOT.double(0.0)
                totalInt=hObj.hist.IntegralAndError(0,1001,total_err)
                if totalInt>0.0:
                    hObj.hist.Scale(float(fittedSRVals[key_name])/totalInt)
                else:
                    hObj.hist.Scale(0.0)
                setBinWidth(var,[hObj.hist])
                if totalInt>0.0:
                    error_fraction = fittedSRErrs[key_name]/totalInt
                    for ib in range(1,hObj.hist.GetNbinsX()+1):
                        mc_stat_err=0.0
                        if options.show_mc_stat_err:
                            mc_stat_err = hObj.hist.GetBinError(ib)
                        hObj.hist.SetBinError(ib,math.sqrt(mc_stat_err**2+(error_fraction*hObj.hist.GetBinContent(ib))**2))
                        # need to spread these out bin by bin
                        systHistAsym.SetBinContent(ib,hObj.hist.GetBinContent(ib))
                        systHistAsym.SetBinError(ib,math.sqrt(mc_stat_err**2+(error_fraction*hObj.hist.GetBinContent(ib))**2))
            else:
                setBinWidth(var,[hObj.hist])
            if not (hObj.mr in mjjBins):
                print 'skipping: ',hObj.mr,h
                continue
            
            if hObj.isBkg():
                if not systHistAsymTot:
                    systHistAsymTot=systHistAsym.Clone()
                    systHistAsymTot.Sumw2(True)
                else:
                    systHistAsymTot.Add(systHistAsym)

        if not (hObj.mr in mjjBins):
            continue
                    
        if hObj.isSignal():
            key=hObj.proc
            signal_scale=1.0
            if not options.scaleSig:
                signal_scale=options.hscale
            try:
                sigDict[key].Add(hObj.hist,signal_scale)
            except:
                sigDict[key]=hObj.hist.Clone(key)
                sigDict[key].Scale(signal_scale)
                sigDict[key].SetTitle(key)
                Style.setStyles(sigDict[key], Style.styleDict[key])
        signalS=ROOT.THStack()
        #setBinWidth(var,sigDict.values())
        for h in sorted(sigDict.values()): #TODO this sorting does not work. implement lambda
            signalS.Add(h)

        if hObj.isBkg():
            key=hObj.proc
            if not ("W" in key or "Z" in key):
                if 'multijet' in key:
                    key='multijet'
                elif 'eleFakes' in key:
                    key='eleFakes'
                elif 'muoFakes' in key:
                    key='muoFakes'
                else:
                    key="ttbar"
            try:
                bkgDict[key].Add(hObj.hist)
            except:
                bkgDict[key]=hObj.hist.Clone(key)
                bkgDict[key].SetTitle(key)
                Style.setStyles(bkgDict[key], Style.styleDict[key])
                
        bkg=ROOT.THStack()
        #setBinWidth(var,bkgDict.values())
        if 'multijet' in bkgDict:
            bkg.Add(bkgDict['multijet'])
        if 'eleFakes' in bkgDict:
            bkg.Add(bkgDict['eleFakes'])
        if 'muoFakes' in bkgDict:
            bkg.Add(bkgDict['muoFakes'])            
        if 'ttbar' in bkgDict:
            bkg.Add(bkgDict['ttbar'])
        for h in sorted(bkgDict.values()): #TODO this sorting does not work. implement lambda
            if 'multijet' in bkgDict:
                if h==bkgDict['multijet']:
                    continue
            if 'ttbar' in bkgDict:
                if h==bkgDict['ttbar']:
                    continue
            if 'eleFakes' in bkgDict:
                if h==bkgDict['eleFakes']:
                    continue
            if 'muoFakes' in bkgDict:
                if h==bkgDict['muoFakes']:
                    continue
            if 'W_EWK' in bkgDict:
                if h==bkgDict['W_EWK']:
                    continue
            if 'W_strong' in bkgDict:
                if h==bkgDict['W_strong']:
                    continue                                
            bkg.Add(h)
        if 'W_EWK' in bkgDict:
            bkg.Add(bkgDict['W_EWK'])
        if 'W_strong' in bkgDict:
            bkg.Add(bkgDict['W_strong'])
        if hObj.isData():
            key=hObj.proc
            #setBinWidth(var,[hObj.hist])
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

    for h in sorted(sigDict.values()): #TODO this sorting does not work. implement lambda
        if signal==None:
            signal=h.Clone()
            signal.SetName('signal')
            signal.SetTitle('signal')
        else:
            signal.Add(h)
    if var=='jj_mass':
        signal.SetBinContent(2,signal.GetBinContent(3))
    can=ROOT.TCanvas("c1","c1",1600,1000)
    if options.ratio:
        can.Divide(1,2)
        can.cd(1)
        ROOT.gPad.SetBottomMargin(0)
        ROOT.gPad.SetRightMargin(0.1)
        ROOT.gPad.SetPad(0,0.4,1,1)
        can.cd(2)
        ROOT.gPad.SetTopMargin(0)
        ROOT.gPad.SetBottomMargin(0.35)
        ROOT.gPad.SetRightMargin(0.1)
        ROOT.gPad.SetPad(0,0,1,0.4)
        can.cd(1)

    bkgH=get_THStack_sum(bkg)
    bkgH.GetXaxis().SetTitle(var)
    bkgH.GetYaxis().SetTitle("Entries")
    bkgH.GetYaxis().SetTitleOffset(0.55)
    
    bkgH.GetYaxis().SetTitleSize(1.8*bkgH.GetYaxis().GetTitleSize())
    bkgH.GetYaxis().SetLabelSize(1.5*bkgH.GetYaxis().GetLabelSize())
    bkgH.GetYaxis().SetTickLength(0.0135)
    bkgH.GetXaxis().SetTickLength(0.03)
    dataH.GetYaxis().SetTickLength(0.02)
    dataH.GetXaxis().SetTickLength(0.05)    
    if var=='jj_mass':
        ROOT.gPad.SetLogy(1)
        bkgH.GetXaxis().SetRangeUser(800,5000.0)
        bkgH.GetYaxis().SetRangeUser(10,40000.0)
        bkgH.GetYaxis().SetTitle("Events / 500 GeV")
    if var=='jj_dphi':
        bkgH.GetYaxis().SetTitle("Events / 0.5 rad")
    if var=='met_tst_et':
        bkgH.GetYaxis().SetTitle("Events / 50 GeV")
    if var=='jj_deta':
        bkgH.GetYaxis().SetTitle("Events / 0.5")
    bkg.Draw("hist ")
    if var!='jj_mass':
        upperV=bkg.GetHistogram().GetMaximum()
        bkgH.GetYaxis().SetRangeUser(0.1, 1.25*upperV)
        if AltDphi and var=='jj_dphi':
            bkgH.GetXaxis().SetRangeUser(0,2.0)
            bkgH.GetYaxis().SetRangeUser(0.1, 1.45*upperV)            
    bkgH.Draw('AXIS')
    bkg.Draw("HIST same")
    signal.Draw("HIST same")
    if options.data:
        dataH.Draw("PEsame")

    #fillStyle = 3004
    fillStyle = 3345
    Style.setStyles(systHistAsymTot,[0,0,0,1,fillStyle,0,0,0])
    systHistAsymTot.SetFillColor(1)
    systHistAsymTot.SetLineWidth(2)
    systHistAsymTot.SetFillStyle(fillStyle)
    systHistAsymTotA=ROOT.TGraphAsymmErrors(systHistAsymTot)
    for i in range(0,systHistAsymTot.GetNbinsX()+3):
        systHistAsymTotA.SetPointEXhigh(i-1,systHistAsymTot.GetXaxis().GetBinWidth(i)/2.0)
        systHistAsymTotA.SetPointEXlow(i-1,systHistAsymTot.GetXaxis().GetBinWidth(i)/2.0)
    Style.setStyles(systHistAsymTotA,[0,0,0,1,fillStyle,0,0,0])
    systHistAsymTotA.SetMarkerSize(0)
    systHistAsymTotA.Draw("SAME E2")
    systHistAsymTotA.SetName('Uncertainty')
    systHistAsymTotA.SetTitle('Uncertainty')

    bkg.SetTitle(reg+" "+",".join(mjjBins))

    #leg=ROOT.gPad.BuildLegend(0.65,0.6,0.85,0.9)
    #leg.SetFillColor(0)
    #leg.SetBorderSize(0)
    #leg.SetNColumns  (2)

    #alllabels=[]
    #legA=leg.Clone()
    #prims=legA.GetListOfPrimitives()
    #leg.Clear()
    #for ik in prims:
    #    if ik.GetLabel() not in alllabels:
    #        alllabels+=[ik.GetLabel()]
    #        leg.AddEntry(ik.GetObject(),ik.GetLabel())
    #    else:
    #        ik.Delete()
    poskeys=[0.6,0.5,0.87,0.93]
    ncolumns=2
    if var=='jj_dphi':
        poskeys=[0.7,0.35,0.9,0.93]
        ncolumns=1
        if AltDphi:
            poskeys=[0.6,0.65,0.9,0.91]
            ncolumns=2
    legP=make_legend(ROOT.gPad,poskeys,ncolumns=ncolumns)
    legP.Draw()
    texts = ATLAS.getATLASLabels(can, 0.2, 0.85, options.lumi, selkey="",preliminary=options.preliminary,scaling=1.1)
    for text in texts:
        text.Draw()

    blindStr=""
    if not options.unBlindSR and reg=="SR":
        blindStr=", SR blinded"
    preFitLabel=ROOT.TLatex(.45,.88,"Pre-fit"+blindStr)
    if options.postFitPickleDir!=None:
        preFitLabel=ROOT.TLatex(.45,.85,"Post-fit"+blindStr)        
    preFitLabel.SetNDC()
    preFitLabel.SetTextFont(72)
    preFitLabel.SetTextSize(0.075)
    preFitLabel.SetTextAlign(11)    
    preFitLabel.SetTextColor(ROOT.kBlack)
    preFitLabel.Draw()

    if options.ratio:
        can.cd(2)
        rHist=dataH.Clone("ratioHist")
        #sum_bkg=get_THStack_sum(bkg)
        rHist.GetYaxis().SetRangeUser(0.601,1.399)
        rHist.GetYaxis().SetRangeUser(0.7501,1.2499)
        rHist.GetYaxis().SetNdivisions(505)
        rHist.Divide(get_THStack_sum(bkg))
        #rHist.GetYaxis().SetTitle("Data / Bkg")
        rHist.GetYaxis().SetTitle("Ratio")
        rHist.GetXaxis().SetTitle(var)
        #rHist.GetYaxis().SetTitleOffset(.338)
        rHist.GetYaxis().SetTitleOffset(.338)
        rHist.GetYaxis().SetTitleSize(0.14)
        rHist.GetXaxis().SetTitleOffset(1.0)
        rHist.GetXaxis().SetTitleSize(0.15)
        rHist.GetYaxis().CenterTitle()
        rHist.GetXaxis().SetLabelSize(0.12)
        rHist.GetYaxis().SetLabelSize(0.1)
        #rHist.GetXaxis().SetTitle('Dijet Invariant Mass m_{jj} [GeV]')
        rHist.GetXaxis().SetTitle('#it{m}_{jj} [GeV]')
        if var=='jj_mass':
            rHist.GetXaxis().SetRangeUser(800,5000.0)
        if var=='jj_dphi':
            rHist.GetXaxis().SetTitle("#Delta#it{#phi}_{jj}")
            if AltDphi:
                rHist.GetXaxis().SetRangeUser(0,2.0)
        if var=='met_tst_et':
            rHist.GetXaxis().SetTitle("Missing Transverse Momentum #it{E}_{T}^{miss} [GeV]")
        if var=='jj_deta':
            rHist.GetXaxis().SetTitle("#Delta#eta_{jj}")        
        systHistAsymTotRatio=systHistAsymTot.Clone()
        sum_bkg=systHistAsymTot.Clone()

        rsignal=signal.Clone()
        rbkgPreFit=bkgPreFit.Clone()
        rmultijet=bkgPreFit.Clone()
        if 'multijet' in  bkgDict:
            rmultijet = bkgDict['multijet'].Clone()
        bkgR=get_THStack_sum(bkg).Clone()
        for ib in range(0,bkgR.GetNbinsX()+1):
            bkgR.SetBinError(ib,0.0)
            rbkgPreFit.SetBinError(ib,0.0)
            if bkgR.GetBinContent(ib)==0:
                bkgR.SetBinContent(ib,0.000001)
                rbkgPreFit.SetBinContent(ib,0.000001)
        rsignal.Add(bkgR)
        rsignal.Divide(bkgR)
        #bkgR.Add(multijet,-1.0)
        rmultijet.Add(bkgR)
        rmultijet.Divide(bkgR)
        rmultijet.SetLineWidth(1)
        #rmultijet.SetLineColor(Style.styleDict["multijet"][3])
        rmultijet.SetLineColor(Style.styleDict["eleFakes"][3])
        rmultijet.SetLineStyle(7)
        rmultijet.SetFillColor(0)
        rmultijet.SetFillStyle(0)
        rsignal.SetLineStyle(1)
        rsignal.SetLineWidth(1)
        if var=='jj_mass':
            rsignal.SetBinContent(2,rsignal.GetBinContent(3))
            rbkgPreFit.SetBinContent(2,rbkgPreFit.GetBinContent(3))
            bkgR.SetBinContent(2,bkgR.GetBinContent(3))
        
        rbkgPreFit.SetLineColor(ROOT.kBlue)
        rbkgPreFit.SetLineStyle(9)
        rbkgPreFit.SetMarkerSize(0)
        rbkgPreFit.SetMarkerColor(ROOT.kBlue)
        rbkgPreFit.SetLineWidth(1)
        rbkgPreFit.SetFillColor(0)
        rbkgPreFit.SetFillStyle(0)
        rbkgPreFit.Divide(bkgR)
        for i in range(0,sum_bkg.GetNbinsX()+1):
            sum_bkg.SetBinError(i,0.0)
            #print i,systHistAsymTotRatio.GetBinError(i)
        systHistAsymTotRatio.Divide(sum_bkg)
        systHistAsymTotRatioA=ROOT.TGraphAsymmErrors(systHistAsymTotRatio)
        for i in range(0,systHistAsymTot.GetNbinsX()+3):
            systHistAsymTotRatioA.SetPointEXhigh(i-1,systHistAsymTot.GetXaxis().GetBinWidth(i)/2.0)
            systHistAsymTotRatioA.SetPointEXlow(i-1,systHistAsymTot.GetXaxis().GetBinWidth(i)/2.0)
            #print i,systHistAsymTotRatio.GetBinContent(i)
        Style.setStyles(systHistAsymTotRatioA,[0,0,0,ROOT.kGray+3,fillStyle,0,0,0])
        #print ROOT.gStyle.GetHatchesLineWidth()
        
        ROOT.gStyle.SetHatchesLineWidth(1)
        line1=dataH.Clone("line1")
        for i in range(1,line1.GetNbinsX()+1):
            line1.SetBinContent(i,1)
        Style.setLineAttr(line1,1,2,3)
        rHist.SetTitle("")
        rHist.SetStats(0)
        rHist.Draw()
        line1.Draw("histsame")
        systHistAsymTotRatioA.Draw("SAME E2")
        if reg=='SR':
            rsignal.Draw('same HIST')
            rmultijet.Draw('same HIST')
        rbkgPreFit.Draw('same HIST')
        rHist.Draw('same')

        # legend
        #legR=ROOT.TLegend(0.1747,0.79,0.4554,1.0)
        #legR=ROOT.TLegend(0.18,0.805,0.545,0.99)
        legR=ROOT.TLegend(0.18,0.78,0.545,0.99)
        if var=="jj_dphi":
            if AltDphi:
                #legR=ROOT.TLegend(0.60,0.745,0.87,1.0)
                legR=ROOT.TLegend(0.50,0.735,0.87,1.0)
            else:
                #legR=ROOT.TLegend(0.6565,0.69,0.87,1.0)
                legR=ROOT.TLegend(0.6565,0.69,0.87,1.0)
        legR.SetTextFont(42)
        #legR.SetNColumns(ncolumns)
        legR.SetTextSize(0.07)
        legR.SetFillColor(0)
        legR.SetBorderSize(0)
        legR.AddEntry(rHist,'Data/Bkg')
        systHistAsymTotRatioA.SetMarkerColor(0)
        systHistAsymTotRatioA.SetLineWidth(0)
        systHistAsymTotRatioA.SetMarkerSize(0)
        systHistAsymTotRatioAR=systHistAsymTotRatioA.Clone()
        systHistAsymTotRatioAR.SetMarkerSize(0)
        legR.AddEntry(systHistAsymTotRatioA,'Uncertainty',"f")
        legR.AddEntry(rbkgPreFit,'Pre-/Post-fit')
        if reg=='SR':
            legR.AddEntry(rsignal,'1+Signal/Bkg')
            legR.AddEntry(rmultijet,'1+Multijet/Bkg')
        
        legR.SetNColumns(3)
        #if reg=='SR':
        for ik in legR.GetListOfPrimitives():
            if ik.GetLabel() =='Uncertainty':
                #ik.GetObject().SetMarkerSize(0.1)
                ik.GetObject().SetMarkerColor(0)
                ik.GetObject().SetLineWidth(0)
                ik.GetObject().SetLineColor(0)
                #ik.GetObject().SetMarkerStyle(1)                
                #ik.GetObject().SetMarkerSize(0.1)

        legR.Draw()
        systHistAsymTotRatioA.Draw("SAME E2")
        if reg=='SR':
            rsignal.Draw('same HIST')
            rmultijet.Draw('same HIST')
        rbkgPreFit.Draw('same HIST')
        rHist.Draw('same')
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
    extraName=''
    if options.preliminary:
        extraName+='_prelim'
    if options.saveAs:
        can.SaveAs(options.plot.replace(",","_")+extraName+"."+options.saveAs)
    del can

if __name__=='__main__':
    p = OptionParser()

    p.add_option('-i', '--input', type='string', help='input file. Created from plotEvent.py')
    p.add_option('-c', '--compare', type='string', help='Compare any number of input files. Does not support --syst atm. example: --compare rfile1.root,rfile2.root')

    p.add_option('--lumi', type='float', default=139, help='Defines the integrated luminosity shown in the label')
    p.add_option('--hscale', type='float', default=0.13, help='normalization for the signal')
    p.add_option('--nBin', type='int', default=1, help='Defines which bin is plotted')
    p.add_option('-s', '--syst', type='string', default="", help='NEEDS FIXING. defines the systematics that are plotted. -s all <- will plot all available systematics. Otherwise give a key to the dict in systematics.py')# FIXME
    p.add_option('-d', '--data', action='store_true', help='Draw data')
    p.add_option('--unBlindSR', action='store_true', help='Unblinds the SR bins')
    p.add_option('--preliminary', action='store_true', help='Labels with preliminary')
    p.add_option('--scaleSig', action='store_true', help='scale the signal to the post fit values')
    p.add_option('--fakeMu', action='store_true', help='Add Fake muon CR')        
    p.add_option('--stack-signal', action='store_true', help='Stack the signal')
    p.add_option('--cronly', action='store_true', help='Shows the CR only')    
    p.add_option('--ph-ana', action='store_true', help='Photon analysis')    
    p.add_option('--debug', action='store_true', help='Print in debug mode')
    p.add_option('--combinePlusMinus', action='store_true', help='Combine the plus and minus')
    p.add_option('-r', '--ratio', action='store_true', help='Draw Data/Bkg ratio in case of -i and adds ratios to tables for both -i and -c')
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
