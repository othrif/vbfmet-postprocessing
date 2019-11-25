import sys
import os
import ROOT
from ROOT import *
from array import array
import math
ROOT.gROOT.LoadMacro("/export/home/asteinhe/atlasstyle/AtlasStyle.C")
ROOT.gROOT.LoadMacro("/export/home/asteinhe/atlasstyle/AtlasUtils.C") 
ROOT.gROOT.LoadMacro("/export/home/asteinhe/atlasstyle/AtlasLabels.C")
import interpretInput

#############################################
def ymax(array):
	ymax=0.0
	for i in range(len(array)):
		if array[i].GetMaximum()>ymax:
			ymax=array[i].GetMaximum()
	return ymax+ymax*0.2

def ymaxArray(array):
	ymax=0.0
	for i in range(len(array)):
		for j in range(len(array[i])):
			if array[i][j].GetMaximum()>ymax:
				ymax=array[i][j].GetMaximum()
	return ymax+ymax*0.2
#############################################

SetAtlasStyle()

inDir=sys.argv[1]
if inDir[-1]!='/':
        inDir+='/'

inFiles=os.listdir(inDir)
inFiles.sort(key=str.lower)#alphebetize
fileSets=len(inFiles)/3.
print "Found "+str(len(inFiles))+" file(s)"
print str(fileSets)+" sets of 3 files"

dataHists=[[] for _ in xrange(int(fileSets))]
bkgdHists=[[] for _ in xrange(int(fileSets))]
names=[]

print inFiles

count=0
#get plots - hardcoded like a coward
in_tmp=ROOT.TFile(inDir+inFiles[0],"READ")
in_tmp.cd("pass_wcr_mjjLow200_u_Nominal")
gDirectory.cd("plotEvent_data")
data=gDirectory.Get("averageIntPerXing")
data.Rebin(4)
data.SetDirectory(0)
dataHists[count].append(data)
gFile.cd()
in_tmp.cd("pass_wcr_mjjLow200_u_Nominal")
gDirectory.cd("plotEvent_bkgs")
bkgd=gDirectory.Get("averageIntPerXing")
bkgd.Rebin(4)
bkgd.SetDirectory(0)
bkgdHists[count].append(bkgd)
in_tmp.Close()
in_tmp=ROOT.TFile(inDir+inFiles[1],"READ")
in_tmp.cd("pass_wcr_mjjLow200_u_PRW_DATASF__1down")
gDirectory.cd("plotEvent_data")
data=gDirectory.Get("averageIntPerXing")
data.Rebin(4)
data.SetDirectory(0)
dataHists[count].append(data)
gFile.cd()
in_tmp.cd("pass_wcr_mjjLow200_u_PRW_DATASF__1down")
gDirectory.cd("plotEvent_bkgs")
bkgd=gDirectory.Get("averageIntPerXing")
bkgd.Rebin(4)
bkgd.SetDirectory(0)
bkgdHists[count].append(bkgd)
in_tmp.Close()
in_tmp=ROOT.TFile(inDir+inFiles[2],"READ")
in_tmp.cd("pass_wcr_mjjLow200_u_PRW_DATASF__1up")
gDirectory.cd("plotEvent_data")
data=gDirectory.Get("averageIntPerXing")
data.Rebin(4)
data.SetDirectory(0)
dataHists[count].append(data)
gFile.cd()
in_tmp.cd("pass_wcr_mjjLow200_u_PRW_DATASF__1up")
gDirectory.cd("plotEvent_bkgs")
bkgd=gDirectory.Get("averageIntPerXing")
bkgd.Rebin(4)
bkgd.SetDirectory(0)
bkgdHists[count].append(bkgd)
in_tmp.Close()




dataArray=[array('d') for _ in xrange(int(fileSets))]
bkgdArray=[array('d') for _ in xrange(int(fileSets))]
bkgdArrayUp=[array('d') for _ in xrange(int(fileSets))]
bkgdArrayDown=[array('d') for _ in xrange(int(fileSets))]

dataGraphNom=[]
bkgdGraphNom=[]
bkgdGraph=[]

xbins=dataHists[0][0].GetNbinsX()
xbinWidth=dataHists[0][0].GetBinWidth(1)
xbinArray,halfXbin=array('d'),array('d')
for xbin in range(xbins):
	xbinArray.append(dataHists[0][0].GetBinCenter(xbin+1))
	halfXbin.append(xbinWidth/2.0)

#use syst to set errors
for i in range(len(bkgdHists)):
	for j in range(xbins):
		nomVal=bkgdHists[i][0].GetBinContent(j+1)
		upVal=bkgdHists[i][1].GetBinContent(j+1)
		downVal=bkgdHists[i][2].GetBinContent(j+1)
		upVar=upVal-nomVal
		downVar=nomVal-downVal
		#print "Bin "+str(j+1)
		#print "BKGD: "+str(nomVal)+"(up "+str(upVar)+", down "+str(downVar)+")"
		bkgdArray[i].append(nomVal)
		dataArray[i].append(dataHists[i][0].GetBinContent(j+1))
		if downVar>0 and upVar>0:	
			bkgdArrayUp[i].append(upVar)
			bkgdArrayDown[i].append(downVar)
		elif downVar<0 and upVar<0:
			bkgdArrayUp[i].append(abs(downVar))
			bkgdArrayDown[i].append(abs(upVar))
		else:
			if downVar<0:
				bkgdArrayUp[i].append(math.sqrt(upVar**2+abs(downVar)**2))
				bkgdArrayDown[i].append(0.0)
			else:
				bkgdArrayUp[i].append(0.0)
				bkgdArrayDown[i].append(math.sqrt(downVar**2+abs(upVar)**2))
	bkgdGraph.append(TGraphAsymmErrors(xbins,xbinArray,bkgdArray[i],halfXbin,halfXbin,bkgdArrayDown[i],bkgdArrayUp[i]))
	dataGraphNom.append(TGraph(xbins,xbinArray,dataArray[i]))
	bkgdGraphNom.append(TGraph(xbins,xbinArray,bkgdArray[i]))


labels=[]
if "SR-MJ" in labels:
	sr=labels.index("SR-MJ")
else:
	sr=len(names)+1#is never reached
if "SR" in labels:
	sr2=labels.index("SR")
else:
	sr2=len(names)+1#is never reached


print labels
labels.append("1LVR_u")

stackGraph=[]
canvas=[]
legend=TLegend(0.65,0.55,0.9,0.65)
legend.AddEntry(bkgdGraph[0],"All backgrounds-MJ",'l')
legend.AddEntry(dataGraphNom[0],"Data",'p')
for i in range(len(bkgdGraph)):
	stackGraph.append(TMultiGraph())
	bkgdGraph[i].SetMarkerSize(0)
	stackGraph[i].Add(bkgdGraph[i],"ap")
	if i!=sr and i!=sr2:
		stackGraph[i].Add(dataGraphNom[i],"P")

	canvas.append(TCanvas("canvas"+str(i),"canvas"+str(i),600,600))
	bkgdGraph[i].SetTitle("2018 Data;averageIntPerXing (PRW syst);Entries")
	stackGraph[i].Draw()
	ATLASLabel(0.6, 0.9, "Internal")
	myText(0.65, 0.85, 1, "#sqrt{s}= 13 TeV")
	myText(0.65, 0.8, 1, "59.9/fb")
	myText(0.65, 0.75, 1, "VBF Hinv")
	myText(0.65, 0.7, 1, labels[i])
	legend.SetBorderSize(0)
	legend.Draw()
	canvas[i].SaveAs("musyst_"+labels[i]+".png")
