#############################################################
#
#  interpretHists.py
#  A. Steinhebel, Mar. 2019
#
#  Input(s): .root file resulting from the running of drawStack.py with the option --do-root AND --do-ratio
#  Output(s): Canvas reprinting do-ratio output plots including bin values (with option of saving as .png);
#             Terminal printout of Latex-formatted tables of (S/B, sigma_mu, Z-norm sigma_mu) and yields of (Higgs, background)
#
#  Run:
#  python -i interpretHists.py <input.root>
#
#  Note:
#  Will ONLY run if --do-ratio option used - otherwise structure of Primitives is different
#
#############################################################

import sys
import ROOT
from ROOT import *


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def BooleanInput(inStr):
    if inStr in ['T','t','True','true','TRUE','yes','Yes','YES','y','Y']:
        save=True
    elif inStr in ['F','f','False','false','FALSE','n','N','no','No','NO']:
        save=False
    else:
        print "Improper input"

    return save
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main body
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Set initial variables
inputFile=sys.argv[1]

inFile=ROOT.TFile(inputFile,"READ")
stack=inFile.Get("stack")

saveInput = raw_input("Save plots? (T/F) ")
save = BooleanInput(saveInput)

mjjIn = raw_input("Which Mjj bin? (For plot labeling) ")

#Create empty place-holders for the contents of stack
hist=[0]*10
count=-1

#Pull out all histograms
#ONLY works with structure created with --do-ratio option
list0=stack.GetPad(0).GetListOfPrimitives()
for pad in list0:
    lst=pad.GetListOfPrimitives()
    for entry in lst:
	if entry.InheritsFrom('THStack'):
	    inStack=entry
	elif entry.InheritsFrom('TH1') and entry.GetEntries>0:
	    count+=1
	    hist[count]=entry
	

#Assign readable titles to important histograms - may need to be updated depending on running (sb, etc also hardcoded)
higgsHist=hist[0]
bkgdHist=hist[1]

bins=hist[2].GetSize()-2
sbHist=TH1D("hist","hist",bins,0.,float(bins))
sigMuHist=TH1D("hist1","hist1",bins,0.,float(bins))
sigMuZNormHist=TH1D("hist2","QG Tagging Regions - "+mjjIn,bins,0.,float(bins))

#Refill new histograms with rounded ratio values, and print values to terminal
print "Function values: Bin, S/B, sigma_mu, sigma_mu Norm"
for i in range(bins):
	sb=float("{0:.3f}".format(hist[2].GetBinContent(i+1)))
	srb=float("{0:.3f}".format(hist[4].GetBinContent(i+1)))
	srbz=float("{0:.3f}".format(hist[5].GetBinContent(i+1)))
	sbHist.Fill(i,sb)
	sigMuHist.Fill(i,srb)
	sigMuZNormHist.Fill(i,srbz)
	sigMuZNormHist.GetXaxis().SetBinLabel(i+1,hist[2].GetXaxis().GetBinLabel(i+1))
	print str(i)+" & "+str(sb)+" & "+str(srb)+" & "+str(srbz)+" \\\ \hline"

#Print yields to terminal
print "Yields: Bin, Higgs, Background"
for i in range(bins):
	    print str(i)+" & "+"{0:.3f}".format(higgsHist.GetBinContent(i+1))+" & "+"{0:.3f}".format(bkgdHist.GetBinContent(i+1))+" \\\ \hline"

#Format output plot
legend=TLegend(0.5,0.7,0.7,0.9)
ratioCan=TCanvas("ratioCan","ratioCan",1200,600)
sigMuZNormHist.Draw("hist text15 same")
sbHist.Draw("same hist text15")
sbHist.SetLineColor(kBlack)
sbHist.SetLineWidth(2)
sbHist.SetStats(0)
legend.AddEntry(sbHist,"S/B","l")
sigMuHist.Draw("hist text15 same")
sigMuHist.SetLineColor(kRed)
sigMuHist.SetLineWidth(2)
sigMuHist.SetStats(0)
legend.AddEntry(sigMuHist,"#sigma_{#mu}","l")
sigMuZNormHist.SetLineColor(kGreen)
sigMuZNormHist.SetLineWidth(2)
sigMuZNormHist.SetStats(0)
legend.AddEntry(sigMuZNormHist,"#sigma_{#mu} Z Norm","l")
sigMuZNormHist.GetYaxis().SetRangeUser(0.,1.4)
legend.Draw()


if save:
	ratioCan.SaveAs("SBs_"+mjjIn+".png")

