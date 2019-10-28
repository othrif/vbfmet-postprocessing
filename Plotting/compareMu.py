import sys
import os
import ROOT
from ROOT import *
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
#############################################

SetAtlasStyle()

inDir=sys.argv[1]
if inDir[-1]!='/':
        inDir+='/'

dataHistsRatio=[]
bkgdHistsRatio=[]
names=[]

inFiles=os.listdir(inDir)
print "Found "+str(len(inFiles))+" file(s)"
for infile in inFiles:
	names.append(infile)
	in_tmp=ROOT.TFile(inDir+infile,"READ")
	data=in_tmp.Get("data_averageIntPerXing")
	data.SetDirectory(0)
	dataHistsRatio.append(data)
	bkgd=in_tmp.Get("totbkg_averageIntPerXing")
	bkgd.SetDirectory(0)
	bkgdHistsRatio.append(bkgd)
	in_tmp.Close()

dataHists=[]
bkgdHists=[]
dataHistsNorm=[]
bkgdHistsNorm=[]
for i in range(len(dataHistsRatio)):
	dataHists.append(dataHistsRatio[i].Clone())
	bkgdHists.append(bkgdHistsRatio[i].Clone())
	dataHistsNorm.append(dataHistsRatio[i].Clone())
	bkgdHistsNorm.append(bkgdHistsRatio[i].Clone())


labels=[]
for infile in names:
	if infile.find("allmjj")>0:
		labels.append("WCR_"+infile[infile.find("allmjj")+7])
	elif infile.find("mjjLow200")>0 and infile[infile.find("mjjLow200")+10]!="n":#1lvr
		labels.append("1LVR_"+infile[infile.find("mjjLow200")+10])
	elif infile.find("mjjLow200")>0 and infile[infile.find("mjjLow200")+10]=="n":#0lvr
		labels.append("0LVR")


dataCanvas=TCanvas("dataCanvas","dataCanvas",600,600)
legend=TLegend(0.7,0.7,0.9,0.9)
for i in range(len(dataHists)):
	dataHists[i].Draw("same HIST")
	dataHists[i].SetStats(0)
	dataHists[i].SetLineColor(i+1)
	dataHists[i].SetMarkerSize(0.5)
	dataHists[i].SetMarkerColor(i+1)
	legend.AddEntry(dataHists[i],labels[i],'l')
myText(0.65, 0.6, 1, "#sqrt{s}= 13 TeV")
myText(0.65, 0.55, 1, "59.9/fb")
myText(0.65, 0.5, 1, "VBF Hinv")
ATLASLabel(0.65, 0.65, "Internal")
dataHists[0].SetMaximum(ymax(dataHists))
dataHists[0].SetTitle("2018 Data;averageIntPerXing;Entries")
legend.Draw()
dataCanvas.SaveAs("compareMu_data.png")

bkgdCanvas=TCanvas("bkgdCanvas","bkgdCanvas",600,600)
for i in range(len(dataHists)):
	bkgdHists[i].Draw("same HIST")
	bkgdHists[i].SetStats(0)
	bkgdHists[i].SetLineColor(i+1)
	bkgdHists[i].SetMarkerSize(0.5)
	bkgdHists[i].SetMarkerColor(i+1)
myText(0.65, 0.6, 1, "#sqrt{s}= 13 TeV")
myText(0.65, 0.55, 1, "59.9/fb")
myText(0.65, 0.5, 1, "VBF Hinv")
ATLASLabel(0.65, 0.65, "Internal")
bkgdHists[0].SetMaximum(ymax(bkgdHists))
bkgdHists[0].SetTitle("Sum of Backgrounds (+QCD);averageIntPerXing;Entries")
legend.Draw()
bkgdCanvas.SaveAs("compareMu_bkgd.png")





#area normalize ratio wrt 0lvr
nolep=labels.index("0LVR")
dataHistsRatio[nolep].Scale(1/dataHistsRatio[nolep].Integral())
bkgdHistsRatio[nolep].Scale(1/bkgdHistsRatio[nolep].Integral())
for i in range(len(dataHistsNorm)):
	dataHistsNorm[i].Scale(1/dataHistsNorm[i].Integral())
	bkgdHistsNorm[i].Scale(1/bkgdHistsNorm[i].Integral())
	if i!=nolep:
		dataHistsRatio[i].Scale(1/dataHistsRatio[i].Integral())
		bkgdHistsRatio[i].Scale(1/bkgdHistsRatio[i].Integral())
		dataHistsRatio[i].Divide(dataHistsRatio[nolep])
		bkgdHistsRatio[i].Divide(bkgdHistsRatio[nolep])
#so that the normalizing hist doesn't get ammended before it's finished normalizing all the others
dataHistsRatio[nolep].Divide(dataHistsRatio[nolep])
bkgdHistsRatio[nolep].Divide(bkgdHistsRatio[nolep])

dataCanvasNorm=TCanvas("dataCanvasNorm","dataCanvasNorm",600,800)
dataCanvasNorm.Divide(1,2,0,0)
dataCanvasNorm.cd(1)
for i in range(len(dataHistsNorm)):
	dataHistsNorm[i].Draw("same HIST")
	dataHistsNorm[i].SetStats(0)
	dataHistsNorm[i].SetLineColor(i+1)
myText(0.65, 0.6, 1, "#sqrt{s}= 13 TeV")
myText(0.65, 0.55, 1, "59.9/fb")
myText(0.65, 0.5, 1, "VBF Hinv")
ATLASLabel(0.65, 0.65, "Internal")
dataHistsNorm[0].SetMaximum(ymax(dataHistsNorm))
dataHistsNorm[0].SetTitle("Area Normalized Data; ; Normalized Entries")
legend.Draw()
dataCanvasNorm.cd(2)
for j in range(len(dataHistsRatio)):
	dataHistsRatio[j].Draw("same HIST C")
	dataHistsRatio[j].SetStats(0)
	dataHistsRatio[j].SetLineColor(j+1)
dataHistsRatio[0].SetTitle(" ; averageIntPerXing (#mu); Ratio (region / 0LVR)")
dataCanvasNorm.SaveAs("compareMu_dataNorm.png")


bkgdCanvasNorm=TCanvas("bkgdCanvasNorm","bkgdCanvasNorm",600,800)
bkgdCanvasNorm.Divide(1,2,0,0)
bkgdCanvasNorm.cd(1)
for i in range(len(bkgdHistsNorm)):
	bkgdHistsNorm[i].Draw("same HIST")
	bkgdHistsNorm[i].SetStats(0)
	bkgdHistsNorm[i].SetLineColor(i+1)
myText(0.65, 0.6, 1, "#sqrt{s}= 13 TeV")
myText(0.65, 0.55, 1, "59.9/fb")
myText(0.65, 0.5, 1, "VBF Hinv")
ATLASLabel(0.65, 0.65, "Internal")
bkgdHistsNorm[0].SetMaximum(ymax(bkgdHistsNorm))
bkgdHistsNorm[0].SetTitle("Area Normalized Bkgd; ; Normalized Entries")
legend.Draw()
bkgdCanvasNorm.cd(2)
for j in range(len(bkgdHistsRatio)):
	bkgdHistsRatio[j].Draw("same HIST C")
	bkgdHistsRatio[j].SetStats(0)
	bkgdHistsRatio[j].SetLineColor(j+1)
bkgdHistsRatio[0].SetTitle(" ; averageIntPerXing (#mu); Ratio (region / 0LVR)")
bkgdCanvasNorm.SaveAs("compareMu_bkgdNorm.png")

