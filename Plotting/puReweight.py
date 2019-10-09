import sys
import ROOT
from ROOT import *
import math
from array import array
import interpretInput



def functionalWeights(bkgd2Hist, bkgd34Hist, data2Hist, data34Hist):
	#data/bkg
	ratio2=data2Hist.Clone()
	ratio2.Divide(bkgd2Hist)
	ratio34=data34Hist.Clone()
	ratio34.Divide(bkgd34Hist)

	ratio2_zoom = TH2D("ratio2_zoom","ratio2_zoom",13,39.5,52.5,22,-4.5,4.5)
	ratio34_zoom = TH2D("ratio34_zoom","ratio34_zoom",13,39.5,52.5,22,-4.5,4.5)


	binsy=ratio2.GetNbinsY()
	x_zoom=-1
	for x in range(ratio2.GetNbinsX()):
		center=ratio2.GetXaxis().GetBinCenter(ratio2.GetXaxis().FindBin(x+1))
		for y in range(binsy):
			oldbin=ratio2.GetBinContent(x+1,y+1)
			oldbin34=ratio34.GetBinContent(x+1,y+1)
			if oldbin>50:#fill zoomed plot with bins without outlier high weights
				ratio2.SetBinContent(x+1,y+1,0)
			if oldbin34>50:#fill zoomed plot with bins without outlier high weights
				ratio34.SetBinContent(x+1,y+1,0)
		if 39<center<54:
			x_zoom+=1
			for y in range(binsy):
				oldbin=ratio2.GetBinContent(x+1,y+1)
				oldbin34=ratio34.GetBinContent(x+1,y+1)
				if oldbin<50:#fill zoomed plot with bins without outlier high weights
					ratio2_zoom.SetBinContent(x_zoom,y+1,oldbin)
				if oldbin34<50:#fill zoomed plot with bins without outlier high weights
					ratio34_zoom.SetBinContent(x_zoom,y+1,oldbin34)

	bins = ratio2_zoom.GetNbinsY()#eta bins
	binsx = ratio2_zoom.GetNbinsX()#mu bins
	xArray = array('d')
	aveArray2 =array('d')
	aveArray34 =array('d')

	for x in range(bins):
		xArray.append(ratio2_zoom.GetYaxis().GetBinCenter(x+1))#indexing to account for global bin numbering scheme
		binVals2 = 0.0
		binVals34 = 0.0
		for mu in range(binsx):
			binVals2+=ratio2_zoom.GetBinContent(mu+1,x+1)#bin counting begins at 1, not 0
			binVals34+=ratio34_zoom.GetBinContent(mu+1,x+1)
		aveArray2.append(binVals2/float(bins))
		aveArray34.append(binVals34/float(bins))


	graph2 = TGraph(bins,xArray,aveArray2)
	graph34 = TGraph(bins,xArray,aveArray34)
	fit2=TF1("fit2","[1]*x+[0]",-4.5,4.5)
	fit2_zoom=TF1("fit2_zoom","[1]*x+[0]",-3,3)
	graph2.Fit("fit2","R")
	graph2.Fit("fit2_zoom","R")
	fit34=TF1("fit34","[2]*x*x+[1]*x+[0]")
	graph34.Fit("fit34")


	saveInput = raw_input("Save plots? (T/F) ")
	save = interpretInput.BooleanInput(saveInput)
	if save:
		can2 = TCanvas("can2","can2",600,600)
		ratio2_zoom.SetStats(0)
		ratio2_zoom.SetTitle("WCR, M_{jj}<0.8 TeV, Njet==2;#mu; #eta(j_{2})")
		#ratio2_zoom.SetMinimum(0)
		#can2.SetLogz()
		ratio2_zoom.Draw("COLZ")

		can34 = TCanvas("can34","can34",600,600)
		ratio34_zoom.SetStats(0)
		ratio34_zoom.SetTitle("WCR, M_{jj}<0.8 TeV, Njet==3,4;#mu; #eta(j_{3})")
		#ratio34_zoom.SetMinimum(0)
		#can34.SetLogz()
		ratio34_zoom.Draw("COLZ")

		can2.SaveAs("muVsJ3eta_njet2_"+ana+"_lin.png")
		can34.SaveAs("muVsJ3eta_njet34_"+ana+"_lin.png")
		
		can2a = TCanvas("can2a","can2a",600,600)
		ratio2.SetStats(0)
		ratio2.SetTitle("WCR, M_{jj}<0.8 TeV, Njet==2;#mu; #eta(j_{2})")
		#ratio2.SetMinimum(0)
		can2a.SetLogz()
		ratio2.Draw("COLZ")

		can2a.SaveAs("muVsJ3eta_njet2_"+ana+"_full.png")
		can34a.SaveAs("muVsJ3eta_njet34_"+ana+"_full.png")

		can34a = TCanvas("can34a","can34a",600,600)
		ratio34.SetStats(0)
		ratio34.SetTitle("WCR, M_{jj}<0.8 TeV, Njet==3,4;#mu; #eta(j_{3})")
		#ratio34.SetMinimum(0)
		ratio34.Draw("COLZ")

		can2a.SaveAs("muVsJ3eta_njet2_"+ana+"_full.png")
		can34a.SaveAs("muVsJ3eta_njet34_"+ana+"_full.png")
		can2g = TCanvas("can2g","can2g",600,600)
		#graph2.SetTitle(";jet2Eta;average data/MC over 40<#mu<52")
		graph2.SetTitle(";jet2Eta;average MC/data over 40<#mu<52")
		graph2.Draw("AC*")
		fit2_zoom.SetLineColor(kBlue)
		fit2_zoom.Draw("same")
		fit2.Draw("same")

		can34g = TCanvas("can34g","can34g",600,600)
		#graph34.SetTitle(";jet3Eta;average data/MC over 40<#mu<52")
		graph34.SetTitle(";jet3Eta;average MC/data over 40<#mu<52")
		graph34.Draw("AC*")

		can2g.SaveAs("etaFnFit_njet2.png")
		can34g.SaveAs("etaFnFit_njet34.png")


def scalarWeights(b2muHist, b34muHist, d2muHist, d34muHist):

	#data/bkg
	ratio2=d2muHist.Clone()
	ratio2.Divide(b2muHist)
	ratio34=d34muHist.Clone()
	ratio34.Divide(b34muHist)

	ratio2_zoom = TH1D("ratio2_zoom","ratio2_zoom",13,39.5,52.5)
	ratio34_zoom = TH1D("ratio34_zoom","ratio34_zoom",13,39.5,52.5)

	ave2=0.0
	tot2=0.
	ave34=0.0
	tot34=0.
	x_zoom=-1
	for x in range(ratio2.GetNbinsX()):
		center=ratio2.GetXaxis().GetBinCenter(ratio2.GetXaxis().FindBin(x+1))
		oldbin=ratio2.GetBinContent(x+1)
		oldbin34=ratio34.GetBinContent(x+1)
		if oldbin>50:#fill zoomed plot with bins without outlier high weights
			ratio2.SetBinContent(x+1,0)
		if oldbin34>50:#fill zoomed plot with bins without outlier high weights
			ratio34.SetBinContent(x+1,0)
		if 39<center<54:
			x_zoom+=1
			oldbin=ratio2.GetBinContent(x+1)
			oldbin34=ratio34.GetBinContent(x+1)
			if oldbin<50:#fill zoomed plot with bins without outlier high weights
				ratio2_zoom.SetBinContent(x_zoom,oldbin)
				ave2+=oldbin
				tot2+=1.
			if oldbin34<50:#fill zoomed plot with bins without outlier high weights
				ratio34_zoom.SetBinContent(x_zoom,oldbin34)
				ave34+=oldbin34
				tot34+=1.

	ave2/=tot2
	ave34/=tot34

	print ave2
	print ave34

	saveInput = raw_input("Save plots? (T/F) ")
	save = interpretInput.BooleanInput(saveInput)
	if save:
		can2 = TCanvas("can2","can2",600,600)
		ratio2_zoom.SetStats(0)
		ratio2_zoom.SetTitle("WCR, M_{jj}<0.8 TeV, Njet==2;#mu; #eta(j_{2})")
		#ratio2_zoom.SetMinimum(0)
		#can2.SetLogz()
		ratio2_zoom.Draw("COLZ")

		can34 = TCanvas("can34","can34",600,600)
		ratio34_zoom.SetStats(0)
		ratio34_zoom.SetTitle("WCR, M_{jj}<0.8 TeV, Njet==3,4;#mu; #eta(j_{3})")
		#ratio34_zoom.SetMinimum(0)
		#can34.SetLogz()
		ratio34_zoom.Draw("COLZ")

		can2a = TCanvas("can2a","can2a",600,600)
		ratio2.SetStats(0)
		ratio2.SetTitle("WCR, M_{jj}<0.8 TeV, Njet==2;#mu; #eta(j_{2})")
		#ratio2.SetMinimum(0)
		can2a.SetLogz()
		ratio2.Draw("COLZ")

		can34a = TCanvas("can34a","can34a",600,600)
		ratio34.SetStats(0)
		ratio34.SetTitle("WCR, M_{jj}<0.8 TeV, Njet==3,4;#mu; #eta(j_{3})")
		#ratio34.SetMinimum(0)
		ratio34.Draw("COLZ")

		can2.SaveAs("mu_njet2_"+ana+".png")
		can34.SaveAs("mu_njet34_"+ana+".png")
		can2a.SaveAs("mu_njet2_"+ana+"_full.png")
		can34a.SaveAs("mu_njet34_"+ana+"_full.png")
		
		


######################################################################################
######################################################################################
######################################################################################
######################################################################################
######################################################################################
inputFile=sys.argv[1]

inFile=ROOT.TFile(inputFile,"READ")
inFile.AddDirectory(kFALSE)

ana=sys.argv[2]


methodInput = raw_input("Scalar weight? (T; F for functional weight) ")
method = interpretInput.BooleanInput(methodInput)



if method:
	inFile.cd("pass_wcr_"+ana+"_l_Nominal")
	gDirectory.cd("plotEvent_bkgs")
	b2muHist=gDirectory.Get("mu_njet2")
	b34muHist=gDirectory.Get("mu_njet34")
	inFile.cd()
	inFile.cd("pass_wcr_"+ana+"_l_Nominal")
	gDirectory.cd("plotEvent_data")
	d2muHist=gDirectory.Get("mu_njet2")
	d34muHist=gDirectory.Get("mu_njet34")
	scalarWeights(b2muHist,b34muHist,d2muHist,d34muHist)
else:
	inFile.cd("pass_wcr_"+ana+"_l_Nominal")
	gDirectory.cd("plotEvent_bkgs")
	bkgd2Hist=gDirectory.Get("j3EtaMuNjet2")
	bkgd34Hist=gDirectory.Get("j3EtaMuNjet34")
	inFile.cd()
	inFile.cd("pass_wcr_"+ana+"_l_Nominal")
	gDirectory.cd("plotEvent_data")
	data2Hist=gDirectory.Get("j3EtaMuNjet2")
	data34Hist=gDirectory.Get("j3EtaMuNjet34")
	functionalWeights(bkgd2Hist,bkgd34Hist,data2Hist,data34Hist)

