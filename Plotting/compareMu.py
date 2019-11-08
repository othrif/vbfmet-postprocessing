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

outName=sys.argv[2]

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


dataCanvas=TCanvas("dataCanvas","dataCanvas",600,600)
legend=TLegend(0.7,0.7,0.9,0.9)
if "SR-MJ" in labels:
	sr=labels.index("SR-MJ")
else:
	sr=len(dataHists)+1#is never reached
if "SR" in labels:
	sr2=labels.index("SR")
else:
	sr2=len(dataHists)+1#is never reached

for i in range(len(dataHists)):
	if i!=sr and i!=sr2:# and names[i].find("nomj")<=0:
		dataHists[i].Draw("SAME HIST E1")
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
dataCanvas.SaveAs("compareMu_data_"+outName+".png")

legend2=TLegend(0.7,0.7,0.9,0.9)
bkgdCanvas=TCanvas("bkgdCanvas","bkgdCanvas",600,600)
for i in range(len(dataHists)):
	bkgdHists[i].Draw("SAME HIST E1")
	bkgdHists[i].SetStats(0)
	bkgdHists[i].SetLineColor(i+1)
	bkgdHists[i].SetMarkerSize(0.5)
	bkgdHists[i].SetMarkerColor(i+1)
	legend2.AddEntry(bkgdHists[i],labels[i],'l')
myText(0.65, 0.6, 1, "#sqrt{s}= 13 TeV")
myText(0.65, 0.55, 1, "59.9/fb")
myText(0.65, 0.5, 1, "VBF Hinv")
ATLASLabel(0.65, 0.65, "Internal")
bkgdHists[0].SetMaximum(ymax(bkgdHists))
bkgdHists[0].SetTitle("Sum of Backgrounds (+QCD);averageIntPerXing;Entries")
legend2.Draw()
bkgdCanvas.SaveAs("compareMu_bkgd_"+outName+".png")




print "Computing ratios with respect to 0LVR-MJ"
#area normalize ratio wrt 0lvr
nolep=labels.index("0LVR-MJ")
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
	if i!=sr and i!=sr2:# and names[i].find("nomj")<=0:
		dataHistsNorm[i].Draw("SAME HIST E1")
		dataHistsNorm[i].SetStats(0)
		dataHistsNorm[i].SetLineColor(i+1)
		dataHistsNorm[i].SetMarkerSize(0)
myText(0.65, 0.6, 1, "#sqrt{s}= 13 TeV")
myText(0.65, 0.55, 1, "59.9/fb")
myText(0.65, 0.5, 1, "VBF Hinv")
ATLASLabel(0.65, 0.65, "Internal")
dataHistsNorm[0].SetMaximum(ymax(dataHistsNorm))
dataHistsNorm[0].SetTitle("Area Normalized Data; ; Normalized Entries")
legend.Draw()
dataCanvasNorm.cd(2)
for j in range(len(dataHistsRatio)):
	if j!=sr and j!=sr2:# and names[j].find("nomj")<=0:
		dataHistsRatio[j].Draw("SAME HIST")
		dataHistsRatio[j].SetStats(0)
		dataHistsRatio[j].SetLineColor(j+1)
		dataHistsRatio[j].SetMarkerSize(0)
dataHistsRatio[0].SetTitle(" ; averageIntPerXing (#mu); Ratio (region / 0LVR)")
dataHistsRatio[0].GetYaxis().SetRangeUser(0,2)
dataCanvasNorm.SaveAs("compareMu_dataNorm_"+outName+".png")


bkgdCanvasNorm=TCanvas("bkgdCanvasNorm","bkgdCanvasNorm",600,800)
bkgdCanvasNorm.Divide(1,2,0,0)
bkgdCanvasNorm.cd(1)
for i in range(len(bkgdHistsNorm)):
	bkgdHistsNorm[i].Draw("SAME HIST E1")
	bkgdHistsNorm[i].SetStats(0)
	bkgdHistsNorm[i].SetLineColor(i+1)
	bkgdHistsNorm[i].SetMarkerSize(0)
myText(0.65, 0.6, 1, "#sqrt{s}= 13 TeV")
myText(0.65, 0.55, 1, "59.9/fb")
myText(0.65, 0.5, 1, "VBF Hinv")
ATLASLabel(0.65, 0.65, "Internal")
bkgdHistsNorm[0].SetMaximum(ymax(bkgdHistsNorm))
bkgdHistsNorm[0].SetTitle("Area Normalized Bkgd; ; Normalized Entries")
legend2.Draw()
bkgdCanvasNorm.cd(2)
for j in range(len(bkgdHistsRatio)):
	bkgdHistsRatio[j].Draw("SAME HIST")
	bkgdHistsRatio[j].SetStats(0)
	bkgdHistsRatio[j].SetLineColor(j+1)
	bkgdHistsRatio[j].SetMarkerSize(0)
bkgdHistsRatio[0].SetTitle(" ; averageIntPerXing (#mu); Ratio (region / 0LVR)")
bkgdHistsRatio[0].GetYaxis().SetRangeUser(0,2)
bkgdCanvasNorm.SaveAs("compareMu_bkgdNorm_"+outName+".png")

