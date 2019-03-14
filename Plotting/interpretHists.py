import sys
import ROOT
from ROOT import *
import interpretInput

inputFile=sys.argv[1]

inFile=ROOT.TFile(inputFile,"READ")
stack=inFile.Get("stack")

list0=stack.GetPad(0).GetListOfPrimitives()

saveInput = raw_input("Save plots? (T/F) ")
save = interpretInput.BooleanInput(saveInput)

mjjIn = raw_input("Which Mjj bin? ")

hist=[0]*10
count=-1


for pad in list0:
    #print pad
    lst=pad.GetListOfPrimitives()
    for entry in lst:
        #print entry
        if entry.InheritsFrom('THStack'):
	    inStack=entry
	elif entry.InheritsFrom('TH1') and entry.GetEntries>0:
	    count+=1
	    hist[count]=entry
	
	

higgsHist=hist[0]
bkgdHist=hist[1]

bins=hist[2].GetSize()-2
sbHist=TH1D("hist","hist",bins,0.,float(bins))
srootbHist=TH1D("hist1","hist1",bins,0.,float(bins))
srootbZNormHist=TH1D("hist2","QG Tagging Regions - "+mjjIn,bins,0.,float(bins))
for i in range(bins):
	sb=float("{0:.3f}".format(hist[2].GetBinContent(i+1)))
	srb=float("{0:.3f}".format(hist[4].GetBinContent(i+1)))
	srbz=float("{0:.3f}".format(hist[5].GetBinContent(i+1)))
	sbHist.Fill(i,sb)
	srootbHist.Fill(i,srb)
	srootbZNormHist.Fill(i,srbz)
	srootbZNormHist.GetXaxis().SetBinLabel(i+1,hist[2].GetXaxis().GetBinLabel(i+1))
	print str(i)+" & "+str(sb)+" & "+str(srb)+" & "+str(srbz)+" \\\ \hline"


for i in range(bins):
            print str(i)+" & "+"{0:.3f}".format(higgsHist.GetBinContent(i+1))+" & "+"{0:.3f}".format(bkgdHist.GetBinContent(i+1))+" \\\ \hline"

legend=TLegend(0.5,0.7,0.7,0.9)
ratioCan=TCanvas("ratioCan","ratioCan",1200,600)
srootbZNormHist.Draw("hist text15 same")
sbHist.Draw("same hist text15")
sbHist.SetLineColor(kBlack)
sbHist.SetLineWidth(2)
sbHist.SetStats(0)
legend.AddEntry(sbHist,"S/B","l")
srootbHist.Draw("hist text15 same")
srootbHist.SetLineColor(kRed)
srootbHist.SetLineWidth(2)
srootbHist.SetStats(0)
legend.AddEntry(srootbHist,"S/sqrt(B)","l")
srootbZNormHist.SetLineColor(kGreen)
srootbZNormHist.SetLineWidth(2)
srootbZNormHist.SetStats(0)
legend.AddEntry(srootbZNormHist,"S/sqrt(B) Z Norm","l")
srootbZNormHist.GetYaxis().SetRangeUser(0.,1.4)
legend.Draw()


if save:
	ratioCan.SaveAs("SBs_"+mjjIn+".png")


