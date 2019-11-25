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

outName=sys.argv[2]

inFiles=os.listdir(inDir)
inFiles.sort(key=str.lower)#alphebetize
fileSets=len(inFiles)/3.
print "Found "+str(len(inFiles))+" file(s)"
print str(fileSets)+" sets of 3 files"

dataHists=[[] for _ in xrange(int(fileSets))]
bkgdHists=[[] for _ in xrange(int(fileSets))]
names=[]

count=-1
for infile in inFiles:
	if infile.find("up")<=0 and infile.find("down")<=0:
		names.append(infile)
		count+=1	

	in_tmp=ROOT.TFile(inDir+infile,"READ")
	print in_tmp
	data=in_tmp.Get("data_averageIntPerXing")
	data.SetDirectory(0)
	dataHists[count].append(data)
	bkgd=in_tmp.Get("totbkg_averageIntPerXing")
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
for infile in names:
	if infile.find("nomj")>0:
		if infile.find("allmjj")>0 and infile[infile.find("allmjj")+7]=="n":
			labels.append("SR-MJ")
		elif infile.find("mjjLow200")>0 and infile[infile.find("mjjLow200")+10]=="n":#0lvr
			labels.append("0LVR-MJ")
		elif infile.find("njgt")>0 and infile[infile.find("njgt")+5]=="n":
			labels.append("SR-MJ")
		elif infile.find("mjjLowNjetFJVT")>0 and infile[infile.find("mjjLowNjetFJVT")+15]=="n":#0lvr
			labels.append("0LVR-MJ")
		
	else:
		if infile.find("allmjj")>0 and infile[infile.find("allmjj")+7]!="n":
			labels.append("WCR_"+infile[infile.find("allmjj")+7])
		elif infile.find("allmjj")>0 and infile[infile.find("allmjj")+7]=="n":
			labels.append("SR")
		elif infile.find("mjjLow200")>0 and infile[infile.find("mjjLow200")+10]!="n":#1lvr
			labels.append("1LVR_"+infile[infile.find("mjjLow200")+10])
		elif infile.find("mjjLow200")>0 and infile[infile.find("mjjLow200")+10]=="n":#0lvr
			labels.append("0LVR")
		elif infile.find("njgt")>0 and infile[infile.find("njgt")+5]!="n":
			labels.append("WCR_"+infile[infile.find("njgt")+5])
		elif infile.find("njgt")>0 and infile[infile.find("njgt")+5]=="n":
			labels.append("SR")
		elif infile.find("mjjLowNjetFJVT")>0 and infile[infile.find("mjjLowNjetFJVT")+15]!="n":#1lvr
			labels.append("1LVR_"+infile[infile.find("mjjLowNjetFJVT")+15])
		elif infile.find("mjjLowNjetFJVT")>0 and infile[infile.find("mjjLowNjetFJVT")+15]=="n":#0lvr
			labels.append("0LVR")


if "SR-MJ" in labels:
	sr=labels.index("SR-MJ")
else:
	sr=len(names)+1#is never reached
if "SR" in labels:
	sr2=labels.index("SR")
else:
	sr2=len(names)+1#is never reached

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
	canvas[i].SaveAs("musyst_"+labels[i]+str(i)+".png")

os.system("mkdir compareMuOutput_musyst_"+outName)
os.system("mv *.png compareMuOutput_musyst_"+outName)
