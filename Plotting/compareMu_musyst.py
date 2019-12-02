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

def quad(x0,x1):
	return math.sqrt(x0**2 + x1**2)
#############################################

SetAtlasStyle()

print "To draw PRW systematics as a band (rather than cross error bars), call program with argument \"bands\" "

inDir=sys.argv[1]
if inDir[-1]!='/':
        inDir+='/'

print len(sys.argv)
bands=False
if len(sys.argv)==3:
	if sys.argv[2]=="bands":
		bands=True

inFiles=os.listdir(inDir)
inFiles.sort(key=str.lower)#alphebetize
fileSets=len(inFiles)/3.
print "Found "+str(len(inFiles))+" file(s)"
print str(fileSets)+" sets of 3 files"

dataHists=[[] for _ in xrange(int(fileSets))]
bkgdHists=[[] for _ in xrange(int(fileSets))]
names=[]

count=-1
mcStats=[]
hists=[]
for infile in inFiles:
	nom=False
	if infile.find("up")<=0 and infile.find("down")<=0:
		names.append(infile)
		count+=1	
		nom=True

	in_tmp=ROOT.TFile(inDir+infile,"READ")
	#print in_tmp
	data=in_tmp.Get("data_averageIntPerXing")
	data.SetDirectory(0)
	dataHists[count].append(data)
	bkgd=in_tmp.Get("totbkg_averageIntPerXing")
	bkgd.SetDirectory(0)
	bkgdHists[count].append(bkgd)
	if nom:
		stack=in_tmp.Get("stack")
		list0=stack.GetListOfPrimitives()
		for entry in list0:
			if entry.InheritsFrom('TGraph'):
				mcStats.append(entry)
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
		upMC=mcStats[i].GetErrorYhigh(j)
		downMC=mcStats[i].GetErrorYlow(j) 
		#print upMC, downMC
		#print "Bin "+str(j+1)
		#print "BKGD: "+str(nomVal)+"(up "+str(upVar)+", down "+str(downVar)+")"
		bkgdArray[i].append(nomVal)
		dataArray[i].append(dataHists[i][0].GetBinContent(j+1))
		if downVar>0 and upVar>0:	
			#bkgdArrayUp[i].append(upVar)
			#bkgdArrayDown[i].append(downVar)
			bkgdArrayUp[i].append(quad(upVar,upMC))
			bkgdArrayDown[i].append(quad(downVar,downMC))
		elif downVar<0 and upVar<0:
			#bkgdArrayUp[i].append(abs(downVar))
			#bkgdArrayDown[i].append(abs(upVar))
			bkgdArrayUp[i].append(quad(downVar,upMC))
			bkgdArrayDown[i].append(quad(upVar,downMC))
		else:
			if downVar<0:
				#bkgdArrayUp[i].append(math.sqrt(upVar**2+abs(downVar)**2))
				#bkgdArrayDown[i].append(0.0)
				bkgdArrayUp[i].append(quad(quad(upVar,downVar),upMC))
				bkgdArrayDown[i].append(downMC)
			else:
				#bkgdArrayUp[i].append(0.0)
				#bkgdArrayDown[i].append(math.sqrt(downVar**2+abs(upVar)**2))
				bkgdArrayUp[i].append(upMC)
				bkgdArrayDown[i].append(quad(quad(upVar,downVar),downMC))
	bkgdGraph.append(TGraphAsymmErrors(xbins,xbinArray,bkgdArray[i],halfXbin,halfXbin,bkgdArrayDown[i],bkgdArrayUp[i]))
	dataGraphNom.append(TGraph(xbins,xbinArray,dataArray[i]))
	bkgdGraphNom.append(TGraph(xbins,xbinArray,bkgdArray[i]))


labels=[]
analysis=[]
for infile in names:
	if infile.find("allmjj")>0:
		analysis.append("allmjj")
		if infile[infile.find("allmjj")+7]!="n":
			labels.append("WCR_"+infile[infile.find("allmjj")+7])
		elif infile[infile.find("allmjj")+7]=="n":
			labels.append("SR")
	elif infile.find("mjjLow200")>0:
		analysis.append("mjjLow200")
		if infile[infile.find("mjjLow200")+10]!="n":#1lvr
			labels.append("1LVR_"+infile[infile.find("mjjLow200")+10])
		elif infile[infile.find("mjjLow200")+10]=="n":#0lvr
			labels.append("0LVR")
	elif infile.find("njgt4")>0:
		analysis.append("njgt4")
		if infile[infile.find("njgt4")+6]!="n":
			labels.append("WCR_"+infile[infile.find("njgt4")+6])
		elif infile[infile.find("njgt4")+6]=="n":
			labels.append("SR")
	elif infile.find("mjjLowNjetFJVT")>0:
		analysis.append("mjjLowNjetFJVT")
		if infile[infile.find("mjjLowNjetFJVT")+15]!="n":#1lvr
			labels.append("1LVR_"+infile[infile.find("mjjLowNjetFJVT")+15])
		elif infile[infile.find("mjjLowNjetFJVT")+15]=="n":#0lvr
			labels.append("0LVR")
	elif infile.find("njgt")>0:
		analysis.append("njgt")
		if infile[infile.find("njgt")+5]!="n":
			labels.append("WCR_"+infile[infile.find("njgt")+5])
		elif infile[infile.find("njgt")+5]=="n":
			labels.append("SR")
	elif infile.find("mjjLowNjet")>0:
		analysis.append("mjjLowNjet")
		if infile[infile.find("mjjLowNjet")+11]!="n":#1lvr
			labels.append("1LVR_"+infile[infile.find("mjjLowNjet")+11])
		elif infile[infile.find("mjjLowNjet")+11]=="n":#0lvr
			labels.append("0LVR")
	elif infile.find("fjvtVR")>0:
		analysis.append("fjvtVR")
		if infile[infile.find("fjvtVR")+7]!="n":#1lvr
			labels.append("1LfjvtVR_"+infile[infile.find("fjvtVR")+7])
		elif infile[infile.find("fjvtVR")+7]=="n":#0lvr
			labels.append("0LfjvtVR")

sr=[]
if "SR" in labels:
	sr.append(labels.index("SR"))

#print sr, len(sr)

stackGraph=[]
canvas=[]
legend=TLegend(0.65,0.5,0.9,0.6)
legend.AddEntry(bkgdGraph[0],"All backgrounds-MJ",'l')
legend.AddEntry(dataGraphNom[0],"Data",'p')
for i in range(len(bkgdGraph)):
	stackGraph.append(TMultiGraph())
	if bands:
		bkgdGraph[i].SetFillColor(kBlack)
		bkgdGraph[i].SetFillStyle(3003)
		stackGraph[i].Add(bkgdGraph[i],"a3")
		stackGraph[i].Add(bkgdGraphNom[i],"C")
		bkgdGraph[i].SetMarkerSize(0)
	else:
		bkgdGraph[i].SetMarkerSize(0)
		stackGraph[i].Add(bkgdGraph[i],"ap")
	if (len(sr)>0 and i not in sr) or len(sr)==0:
		stackGraph[i].Add(dataGraphNom[i],"P")

	canvas.append(TCanvas("canvas"+str(i),"canvas"+str(i),600,600))
	bkgdGraph[i].SetTitle("2018 Data;averageIntPerXing (PRW syst);Entries")
	stackGraph[i].Draw()
	ATLASLabel(0.6, 0.9, "Internal")
	myText(0.65, 0.85, 1, "#sqrt{s}= 13 TeV")
	myText(0.65, 0.8, 1, "59.9/fb")
	myText(0.65, 0.75, 1, "VBF Hinv")
	myText(0.65, 0.7, 1, labels[i])
	myText(0.65, 0.65, 1, MC stat+PRW error bars")
	legend.SetBorderSize(0)
	legend.Draw()
	if bands:
		canvas[i].SaveAs("musyst_"+analysis[i]+"_"+labels[i]+"_bands.png")
	else:
		canvas[i].SaveAs("musyst_"+analysis[i]+"_"+labels[i]+".png")

if not os.path.exists("compareMuOutput_musyst"):
	os.system("mkdir compareMuOutput_musyst")
os.system("mv *.png compareMuOutput_musyst")

