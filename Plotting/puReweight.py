import sys
import ROOT
from ROOT import *
import math

inputFile=sys.argv[1]

inFile=ROOT.TFile(inputFile,"READ")
#inFile.SetDirectory(0)
inFile.AddDirectory(kFALSE)

ana=sys.argv[2]

inFile.cd("pass_wcr_"+ana+"_l_Nominal")
gDirectory.cd("plotEvent_bkgs")
bkgd2Hist=gDirectory.Get("j3EtaMuNjet2")
bkgd34Hist=gDirectory.Get("j3EtaMuNjet34")
inFile.cd()
inFile.cd("pass_wcr_"+ana+"_l_Nominal")
gDirectory.cd("plotEvent_data")
data2Hist=gDirectory.Get("j3EtaMuNjet2")
data34Hist=gDirectory.Get("j3EtaMuNjet34")


ratio2=data2Hist.Clone()
ratio2.Divide(bkgd2Hist)
ratio2.Rebin2D()#default merges 2X and 2Y bins into one new xy bin
ratio34=data34Hist.Clone()
ratio34.Divide(bkgd34Hist)
ratio34.Rebin2D()
for i in range(ratio2.GetNbinsX()):
	for j in range(ratio2.GetNbinsY()):
		if ratio2.GetBinContent(i,j)<0:
			ratio2.SetBinContent(i,j,abs(ratio2.GetBinContent(i,j)))
		if ratio34.GetBinContent(i,j)<0:
			ratio34.SetBinContent(i,j,abs(ratio34.GetBinContent(i,j)))
		if ratio2.GetBinContent(i,j)>50:
			ratio2.SetBinContent(i,j,0.0)
		if ratio34.GetBinContent(i,j)>50:
			ratio34.SetBinContent(i,j,0.0)


ratio2_zoom=ratio2.Clone()
ratio2_zoom.GetXaxis().SetRangeUser(40,52)
ratio34_zoom=ratio34.Clone()
ratio34_zoom.GetXaxis().SetRangeUser(40,52)

can2 = TCanvas("can2","can2",600,600)
ratio2_zoom.SetStats(0)
ratio2_zoom.SetTitle("WCR, M_{jj}<0.8 TeV, Njet==2;#mu; #eta(j_{3})")
can2.SetLogz()
ratio2_zoom.Draw("COLZ")
can34 = TCanvas("can34","can34",600,600)
ratio34_zoom.SetStats(0)
ratio34_zoom.SetTitle("WCR, M_{jj}<0.8 TeV, Njet==3,4;#mu; #eta(j_{3})")
can34.SetLogz()
ratio34_zoom.Draw("COLZ")


ratio2.SaveAs("muVsJ3eta_njet2_"+ana+".png")
ratio34.SaveAs("muVsJ3eta_njet34_"+ana+".png")
