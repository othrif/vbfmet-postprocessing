#!/usr/bin/env python

import os,sys
import re
import sys
import math
import copy
import ROOT
import numpy as np
import os, errno
import array

from optparse import OptionParser

p = OptionParser(usage="usage: <path:ROOT file directory>", version="0.1")

p.add_option('--vars',         type='string', default="jj_mass",          dest='vars')
p.add_option('--wait',          action='store_true', default=False,   dest='wait')
p.add_option('--save',          action='store_true', default=False,   dest='save')
p.add_option('--int-lumi',     type='float',  default=36207.66,       dest='int_lumi') # 2017: 44307.4, 2018: 58.45
p.add_option('--year',         type='int',    default=2016,          dest='year')
p.add_option('--draw-syst',       action='store_true', default=False,   dest='draw_syst')
p.add_option('--atlas-style', dest='atlas_style_path', default="/Applications/root_v6.10.08/RootUtils/")
p.add_option('-o','--output',   type='string', default='outdir/',    dest='outdir',      help='output directory')
p.add_option('--do-pdf',          action='store_true', default=False,   dest='do_pdf')

(options, args) = p.parse_args()

if not options.wait:
    ROOT.gROOT.SetBatch(True)

atlas_style_path = options.atlas_style_path

#-------------------------------------------------------------------------
def chmkDir( path ):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
#-------------------------------------------------------------------------
def Style():
    if not os.path.exists(atlas_style_path):
        print("Error: could not find ATLAS style macros at: " + atlas_style_path)
        sys.exit(1)
    ROOT.gROOT.LoadMacro(os.path.join(atlas_style_path, 'AtlasStyle.C'))
    ROOT.gROOT.LoadMacro(os.path.join(atlas_style_path, 'AtlasUtils.C'))
    ROOT.SetAtlasStyle()

#-------------------------------------------------------------------------
def shifthists(hist, col):
    hi = hist.Clone()
    hi.SetDirectory(0)
    lo = hist.Clone()
    lo.SetDirectory(0)
    for b in range(0, hist.GetNbinsX()+1):
        #print b, hist.GetBinContent(b), hist.GetBinErrorLow(b), hist.GetBinErrorUp(b)
        hi.SetBinContent(b, hist.GetBinContent(b)+hist.GetBinErrorUp(b))
        lo.SetBinContent(b, hist.GetBinContent(b)-hist.GetBinErrorLow(b))
    hi.SetFillColor(col)
    hi.SetLineColor(col)
    hi.SetLineWidth(0)
    lo.SetFillColor(10)
    lo.SetLineColor(0)
    lo.SetLineWidth(0)
    return hi, lo

#-------------------------------------------------------------------------
def shifthistsRatio(hist, col):
    hi = hist.Clone()
    hi.SetDirectory(0)
    lo = hist.Clone()
    lo.SetDirectory(0)
    for b in range(0, hist.GetNbinsX()+1):
        #print b, hist.GetBinContent(b), hist.GetBinErrorLow(b), hist.GetBinErrorUp(b)
        if hist.GetBinContent(b) == 0:
            hi.SetBinContent(b, hist.GetBinContent(b)+hist.GetBinErrorUp(b))
            lo.SetBinContent(b, hist.GetBinContent(b)-hist.GetBinErrorLow(b))
        else:
            hi.SetBinContent(b, (hist.GetBinContent(b)+hist.GetBinErrorUp(b))/hist.GetBinContent(b))
            lo.SetBinContent(b, (hist.GetBinContent(b)-hist.GetBinErrorLow(b))/hist.GetBinContent(b))
    hi.SetFillColor(col)
    hi.SetLineColor(col)
    hi.SetLineWidth(0)
    lo.SetFillColor(10)
    lo.SetLineColor(0)
    lo.SetLineWidth(0)
    return hi, lo
#-------------------------------------------------------------------------
def dataMinMC(hisMC, hisData):
    hisNew = hisData.Clone()
    hisNew.SetName( hisData.GetName() +"_MINUS_("+ hisMC.GetName() +")" )
    hisNew.SetDirectory(0)
    hisNew.Add(hisMC, -1)
    return hisNew

#-------------------------------------------------------------------------
def chmkDir( path ):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

#-------------------------------------------------------------------------
def main():

    if len(args) != 1:
        print('Need exactly one input argument: %s' %str(args))
        sys.exit(1)

    rpath = args[0]

    if not os.path.isfile(rpath):
        print('Input argument is not a valid file: %s' %rpath)
        sys.exit(1)

    Style()

    if options.year==2018 and options.int_lumi==36207.66:
        options.int_lumi=58450.1
    if options.year==2017 and options.int_lumi==36207.66:
        options.int_lumi=44307.4
    if options.year==9999 and options.int_lumi==36207.66:
        options.int_lumi=44307.4+58450.1+36207.66

    rfile  = ROOT.TFile(rpath, 'READ')

    # sr > data, z, w
    # zcr > data, z
    # wcr > data, w

    regions          = ["zcr_allmjj_ll","wcr_allmjj_l","zcr_allmjj_uu","wcr_allmjj_u","zcr_allmjj_ee","wcr_allmjj_e"] # zcr, wcr
    processes        = ["data","zqcd","zewk","wqcd","wewk","tall"] # zqcd+zewk , wqcd+wewk
    processes_type   = [ "z", "w"]
    variables        = ["jj_mass"]#, "met_tst_et"]
    ratioregions     = ["wcr_allmjj_eOVERzcr_allmjj_ee","wcr_allmjj_uOVERzcr_allmjj_uu","wcr_allmjj_lOVERzcr_allmjj_ll"]
    ratioregionsTeX  = ["#frac{W(e#nu)+jets}{Z(ee)+jets}","#frac{W(#mu#nu)+jets}{Z(#mu#mu)+jets}","#frac{W(l#nu)+jets}{Z(ll)+jets}"]

    # region, process, variable
    tmphists        = np.zeros( (len(regions), len(processes), len(variables)), dtype=ROOT.TH1F )
    # region, variable
    # processes: w,z
    MChists         = np.zeros( (len(regions), len(processes_type), len(variables)),  dtype=ROOT.TH1F )
    Datahists       = np.zeros( (len(regions), len(processes_type), len(variables)),  dtype=ROOT.TH1F )
    Rhists          = np.zeros( (2, len(ratioregions), len(variables)),  dtype=ROOT.TH1F )
    Ratios          = np.zeros( (len(ratioregions), len(variables)),  dtype=ROOT.TH1F )
    can             = np.zeros( (len(ratioregions), len(variables)),  dtype=ROOT.TCanvas )



    for r in regions:
        for p in processes:
            for v in variables:
                hname = "pass_"+r+"_Nominal/plotEvent_"+p+"/"+v
                tmphists[regions.index(r)][processes.index(p)][variables.index(v)] = rfile.Get(hname).Clone()
                tmphists[regions.index(r)][processes.index(p)][variables.index(v)].SetDirectory(0)
                #tmphists[regions.index(r)][processes.index(p)][variables.index(v)].Sumw2()

    for r in regions:
        #print "\n ********* ", r, " ********* "
        for v in variables:
            found={"z":0,"w":0}
            for p in processes:
                for t in found:
                    if (re.search("^"+t+".*",p)):
                        if found[t] == 0:
                            MChists[regions.index(r)][processes_type.index(t)][variables.index(v)] = tmphists[regions.index(r)][processes.index(p)][variables.index(v)].Clone()
                        else:
                            MChists[regions.index(r)][processes_type.index(t)][variables.index(v)].Add(tmphists[regions.index(r)][processes.index(p)][variables.index(v)].Clone())
                        found[t] = found[t]+1
            #print "\nMC Single Z:", MChists[regions.index(r)][processes_type.index("z")][variables.index(v)].Integral()
            #print "MC Single W:", MChists[regions.index(r)][processes_type.index("w")][variables.index(v)].Integral()

            for t in processes_type:
                tmp = tmphists[regions.index(r)][processes.index("tall")][variables.index(v)].Clone()
                tmp.Add(tmphists[regions.index(r)][processes.index(processes_type[abs(processes_type.index(t)-1)]+"qcd")][variables.index(v)])
                tmp.Add(tmphists[regions.index(r)][processes.index(processes_type[abs(processes_type.index(t)-1)]+"ewk")][variables.index(v)])
                Datahists[regions.index(r)][processes_type.index(t)][variables.index(v)] = dataMinMC(tmp, tmphists[regions.index(r)][processes.index("data")][variables.index(v)])
                #print "Data", t, tmphists[regions.index(r)][processes.index("data")][variables.index(v)].Integral()
                #print "Data-other", t, Datahists[regions.index(r)][processes_type.index(t)][variables.index(v)].Integral()



    # rebin
    newBinning = array.array('d',[800,1200,1500,2000,2500,3500,5000])
    for r in regions:
        for v in variables:
            if "jj_mass" in v:
                for t in processes_type:
                    Datahists[regions.index(r)][processes_type.index(t)][variables.index(v)] = Datahists[regions.index(r)][processes_type.index(t)][variables.index(v)].Rebin(len(newBinning)-1,Datahists[regions.index(r)][processes_type.index(t)][variables.index(v)].GetName()+"_rebinned", array.array('d',[800,1200,1500,2000,2500,3500,5000]))
                    MChists[regions.index(r)][processes_type.index(t)][variables.index(v)] = MChists[regions.index(r)][processes_type.index(t)][variables.index(v)].Rebin(len(newBinning)-1,MChists[regions.index(r)][processes_type.index(t)][variables.index(v)].GetName()+"_rebinned", newBinning)



    for rt in ratioregions:
        for v in variables:
            reg1=rt.split("OVER")[0]
            reg2=rt.split("OVER")[1]
            proc_type1="z"
            proc_type2="z"
            if "w" in reg1: proc_type1="w"
            if "w" in reg2: proc_type2="w"

            Rhists[0][ratioregions.index(rt)][variables.index(v)] = MChists[regions.index(reg1)][processes_type.index(proc_type1)][variables.index(v)].Clone()
            Rhists[0][ratioregions.index(rt)][variables.index(v)].Divide(MChists[regions.index(reg2)][processes_type.index(proc_type2)][variables.index(v)])

            Rhists[1][ratioregions.index(rt)][variables.index(v)] = Datahists[regions.index(reg1)][processes_type.index(proc_type1)][variables.index(v)].Clone()
            Rhists[1][ratioregions.index(rt)][variables.index(v)].Divide(Datahists[regions.index(reg2)][processes_type.index(proc_type2)][variables.index(v)])

            ratiorangeY = 3 * Datahists[regions.index(reg1)][processes_type.index(proc_type1)][variables.index(v)].Integral()/Datahists[regions.index(reg2)][processes_type.index(proc_type2)][variables.index(v)].Integral()
            Rhists[1][ratioregions.index(rt)][variables.index(v)].SetMinimum(0.0)
            Rhists[1][ratioregions.index(rt)][variables.index(v)].SetMaximum(ratiorangeY)
            Rhists[1][ratioregions.index(rt)][variables.index(v)].GetXaxis().SetRangeUser(800,5000)

            Rhists[1][ratioregions.index(rt)][variables.index(v)].SetLineColor(ROOT.kBlack)
            Rhists[1][ratioregions.index(rt)][variables.index(v)].SetMarkerSize(1.2)
            Rhists[1][ratioregions.index(rt)][variables.index(v)].SetLineWidth(2)
            Rhists[1][ratioregions.index(rt)][variables.index(v)].SetMarkerStyle(20)
            Rhists[1][ratioregions.index(rt)][variables.index(v)].SetBarWidth(0.4);

            Rhists[0][ratioregions.index(rt)][variables.index(v)].SetLineColor(ROOT.kRed)
            Rhists[0][ratioregions.index(rt)][variables.index(v)].SetMarkerSize(0)
            Rhists[0][ratioregions.index(rt)][variables.index(v)].SetLineWidth(4)
            Rhists[0][ratioregions.index(rt)][variables.index(v)].SetFillColor(ROOT.kWhite)
            #
            Ratios[0][variables.index(v)] = Rhists[1][ratioregions.index(rt)][variables.index(v)].Clone()
            Ratios[0][variables.index(v)].Divide(Rhists[0][ratioregions.index(rt)][variables.index(v)])

            Rhists[1][ratioregions.index(rt)][variables.index(v)].GetXaxis().SetTitleSize(0)
            Rhists[1][ratioregions.index(rt)][variables.index(v)].GetXaxis().SetLabelSize(0)
            Rhists[1][ratioregions.index(rt)][variables.index(v)].GetYaxis().SetNdivisions(505)
            Rhists[1][ratioregions.index(rt)][variables.index(v)].GetYaxis().SetTitleSize(27)
            Rhists[1][ratioregions.index(rt)][variables.index(v)].GetYaxis().SetTitleFont(43)
            Rhists[1][ratioregions.index(rt)][variables.index(v)].GetYaxis().SetTitleOffset(1.55)
            Rhists[1][ratioregions.index(rt)][variables.index(v)].GetYaxis().SetLabelFont(43)
            Rhists[1][ratioregions.index(rt)][variables.index(v)].GetYaxis().SetLabelSize(24)
            Rhists[1][ratioregions.index(rt)][variables.index(v)].GetYaxis().SetTitle(ratioregionsTeX[ratioregions.index(rt)])
            Rhists[1][ratioregions.index(rt)][variables.index(v)].SetTitle("")
            Ratios[0][variables.index(v)].SetMinimum(0.4)#(0.9)#(0.5)
            Ratios[0][variables.index(v)].SetMaximum(1.6)#(1.1)#(1.5)
            Ratios[0][variables.index(v)].GetXaxis().SetRangeUser(800,5000)
            Ratios[0][variables.index(v)].GetXaxis().SetTitle("m_{jj} [GeV]")
            Ratios[0][variables.index(v)].GetYaxis().SetTitle("#frac{Data}{Pred.}")
            Ratios[0][variables.index(v)].GetYaxis().SetNdivisions(5)
            Ratios[0][variables.index(v)].SetTitle("")
            Ratios[0][variables.index(v)].GetYaxis().SetTitleSize(27)
            Ratios[0][variables.index(v)].GetYaxis().SetTitleFont(43)
            Ratios[0][variables.index(v)].GetXaxis().SetTitleSize(27)
            Ratios[0][variables.index(v)].GetXaxis().SetTitleFont(43)
            Ratios[0][variables.index(v)].GetYaxis().SetLabelSize(24)
            Ratios[0][variables.index(v)].GetYaxis().SetLabelFont(43)
            Ratios[0][variables.index(v)].GetYaxis().SetTitleOffset(1.55)
            Ratios[0][variables.index(v)].GetXaxis().SetLabelSize(24)
            Ratios[0][variables.index(v)].GetXaxis().SetLabelFont(43)
            Ratios[0][variables.index(v)].GetXaxis().SetTitleOffset(5)
            Ratios[0][variables.index(v)].SetStats(0)

            # MC uncertainty hists
            uppUnc, lowUnc = shifthists(Rhists[0][ratioregions.index(rt)][variables.index(v)], ROOT.kGray)
            uppUncRatio, lowUncRatio = shifthistsRatio(Rhists[0][ratioregions.index(rt)][variables.index(v)], ROOT.kGray)

            can[ratioregions.index(rt)][variables.index(v)]=ROOT.TCanvas("c_" + rt + "_" + v, "c_" + rt + "_" + v, 0, 0, 1000, 800)
            ROOT.gStyle.SetOptStat(0)
            #ROOT.gStyle.SetErrorX(1)

            # Pad 1
            pad1 = ROOT.TPad("pad1_" + rt, "pad1_" + rt,
                          0, 0.25, 1, 1)
            ROOT.SetOwnership(pad1, False)
            pad1.SetFillColor(0)
            pad1.SetBorderMode(0)
            pad1.SetBorderSize(2)
            pad1.SetTickx(1)
            pad1.SetTicky(1)
            pad1.SetLeftMargin(0.12)
            pad1.SetRightMargin(0.05)
            pad1.SetTopMargin(0.05)
            pad1.SetBottomMargin(0.02)
            pad1.SetFrameBorderMode(0)
            pad1.SetFillColor(0)
            pad1.SetBorderMode(0)
            pad1.SetBorderSize(2)
            pad1.Draw()
            pad1.cd()
            Rhists[1][ratioregions.index(rt)][variables.index(v)].Draw("ep")
            uppUnc.Draw("histsame")
            lowUnc.Draw("histsame")
            Rhists[0][ratioregions.index(rt)][variables.index(v)].Draw("hist,same")
            Rhists[1][ratioregions.index(rt)][variables.index(v)].Draw("ep,same")

            legend = ROOT.TLegend(0.65,0.65,0.88,0.9)
            legend.SetFillColor(ROOT.kWhite)
            legend.SetTextColor(ROOT.kBlack)
            legend.SetTextSize(0.04)
            legend.SetBorderSize(0)
            legend.AddEntry(Rhists[1][ratioregions.index(rt)][variables.index(v)], ratioregionsTeX[ratioregions.index(rt)] + " Data", "lp")
            legend.AddEntry(Rhists[0][ratioregions.index(rt)][variables.index(v)], ratioregionsTeX[ratioregions.index(rt)] + " MC", "l")

            legend.Draw("same")
            ROOT.gPad.RedrawAxis()
            l = ROOT.TLatex()
            l.SetNDC()
            l.SetTextFont(72)
            l.SetTextColor(ROOT.kBlack)
            l.SetTextSize(0.05)
            l.DrawLatex(0.2, 0.87, "ATLAS")
            l.SetTextFont(42)
            l.DrawLatex(0.3, 0.87, "Work in progress")
            l.DrawLatex(0.17, 0.80, "#int Ldt = #scale[0.9]{"+str(round(float(options.int_lumi)/1000.,1)) +" fb^{-1}, #sqrt{s} = 13 TeV}")
            can[ratioregions.index(rt)][variables.index(v)].cd()

            # Pad 2
            pad2 = ROOT.TPad("pad2_"+ rt, "pad2_" + rt,
                          0, 0, 1, 0.25)
            ROOT.SetOwnership(pad2, False)
            pad2.Range(0, 0, 1, 1)
            pad2.SetFillColor(0)
            pad2.SetBorderMode(0)
            pad2.SetBorderSize(2)
            pad2.SetGridy()
            pad2.SetTickx(1)
            pad2.SetTicky(1)
            pad2.SetLeftMargin(0.12)
            pad2.SetRightMargin(0.05)
            pad2.SetTopMargin(0)
            pad2.SetBottomMargin(0.35)
            pad2.SetFrameBorderMode(0)
            pad2.Draw()
            pad2.cd()
            Ratios[0][variables.index(v)].Draw("ep")
            uppUncRatio.Draw("histsame")
            lowUncRatio.Draw("histsame")
            Ratios[0][variables.index(v)].Draw("ep,same")

            if options.wait:
                can[ratioregions.index(rt)][variables.index(v)].WaitPrimitive()

            #can[ratioregions.index(rt)][variables.index(v)].SaveAs("test.pdf")
#            if options.save:
#                print "Saving to", options.outdir
#                chmkDir(options.outdir)
#                can[ratioregions.index(rt)][variables.index(v)].Print(options.outdir+rt+".eps")
#                if options.do_pdf:
#                    can[ratioregions.index(rt)][variables.index(v)].Print(options.outdir+rt+".pdf")


#-------------------------------------------------------------------------
if __name__ == "__main__":
    ROOT.gErrorIgnoreLevel = ROOT.kWarning
    #ROOT.gROOT.SetBatch(True)
    main()

