#!/usr/bin/env python
import os
import sys
import subprocess
import argparse
import ROOT
import math
import numpy as np

parser = argparse.ArgumentParser( description = "Changing to MG relative uncertainties", add_help=True , fromfile_prefix_chars='@')
parser.add_argument("--lumi", dest='lumi', default=139, help="Lumi")
parser.add_argument("--year", dest='year', default='2019', help="Year")
parser.add_argument("--input", dest='input', default='v37ALL_fjvt05.root', help="input file name")
parser.add_argument("--inputfail", dest='inputfail', default='v37ALL_fjvt05rev.root', help="input file name")
parser.add_argument("--mvar", dest='mvar', default='jj_mass_variableBin', help="MET variable: met_cst_jet, met_tst_et, met_tenacious_tst_et")
parser.add_argument("--outdir", dest='outdir', default='/tmp/plotTrig', help="Output Directory")
parser.add_argument("--wait", action='store_true', dest='wait', default=False, help="wait")
parser.add_argument("--mg", action='store_true', dest='mg', default=False, help="measure mg")
parser.add_argument("--style", dest='style', default='/Users/schae/testarea/SUSY/JetUncertainties/testingMacros/atlasstyle/' , help="ATLAS style path")
parser.add_argument("--lowFJVT", action='store_true', dest='lowfjvt', default=False, help="Inputs consider low-MET region with low fJVT requirement (0.2)")
parser.add_argument("--save", action='store_true', dest='save', default=False, help="Save plots as pdf")
args, unknown = parser.parse_known_args()

import HInvPlot.JobOptions as config
import HInvPlot.CutsDef    as hstudy

#-----------------------------------------
def Style(atlas_style_path):
    if not os.path.exists(atlas_style_path):
        print("Error: could not find ATLAS style macros at: " + atlas_style_path)
        sys.exit(1)
    ROOT.gROOT.LoadMacro(os.path.join(atlas_style_path, 'AtlasStyle.C'))
    ROOT.SetAtlasStyle()

def SetOverflow(h):

    under = h.GetBinContent(0)
    undere = h.GetBinError(0)
    under1 = h.GetBinContent(1)
    undere1 = h.GetBinError(1)
    h.SetBinContent(0,0.0)
    h.SetBinError(0,0.0)
    h.SetBinContent(1,under+under1)
    h.SetBinError(1,math.sqrt(undere**2+undere1**2))

    maxB=h.GetNbinsX()
    under = h.GetBinContent(maxB)
    undere = h.GetBinError(maxB)
    under1 = h.GetBinContent(maxB+1)
    undere1 = h.GetBinError(maxB+1)
    h.SetBinContent(maxB+1,0.0)
    h.SetBinError(maxB+1,0.0)
    h.SetBinContent(maxB,under+under1)
    h.SetBinError(maxB,math.sqrt(undere**2+undere1**2))

def GetZNFHists(f,cut_pathtmp, mvar, year, met=150.0):
    cut_path = cut_pathtmp.replace('_sr_','_zcr_')
    cut_path = cut_path.replace('_nn_','_ll_')
    dpath    = cut_path+'/plotEvent_data/'+mvar
    bkgpaths=[cut_path+'/plotEvent_wqcd/'+mvar,
                  cut_path+'/plotEvent_wewk/'+mvar,
                  cut_path+'/plotEvent_tall/'+mvar,]
    sigpaths = [cut_path+'/plotEvent_zqcd/'+mvar,
                    cut_path+'/plotEvent_zewk/'+mvar,]
    dplot    = f.Get(dpath)
    if not dplot:
        print "Could not find "+str(dpath)+" in "+str(f)+" - GetZNFHists"
        sys.exit(0)
    dplot    = f.Get(dpath).Clone()
    bkgTot=None
    sigTot=None
    for b in bkgpaths:
        a=f.Get(b).Clone()
        if bkgTot==None:
            bkgTot=a.Clone()
        else:
            bkgTot.Add(a)
    for b in sigpaths:
        a=f.Get(b).Clone()
        if sigTot==None:
            sigTot=a.Clone()
        else:
            sigTot.Add(a)
                        
    dplot.Add(bkgTot,-1.0)
    errordata = ROOT.Double(0.0)
    errormc = ROOT.Double(0.0)  
    data_minus_bkg = dplot.IntegralAndError(0,10001,errordata)
    signEvt = sigTot.IntegralAndError(0,10001,errormc)
    # correct for the differences in Znn simulation in 2018 and combined
    xtra=1.0
    if year==2018:
        xtra= 1.2
    if year==2019:
        xtra= 1.03 # correcting inclusively
    
    if signEvt>0.0:
        NFerr = math.sqrt(errordata**2+errormc**2)/signEvt
        return xtra*data_minus_bkg/signEvt,NFerr
    return xtra

def GetWNFHists(f,cut_pathtmp, mvar, year, met=150.0):
    cut_path = cut_pathtmp.replace('_sr_','_wcr_')
    cut_path = cut_path.replace('_nn_','_l_')
    mvarA='mt'
    dpath    = cut_path+'/plotEvent_data/'+mvarA
    bkgpaths=[cut_path+'/plotEvent_zqcd/'+mvarA,
                  cut_path+'/plotEvent_zewk/'+mvarA,
                  cut_path+'/plotEvent_tall/'+mvarA,]
    sigpaths = [cut_path+'/plotEvent_wqcd/'+mvarA,
                    cut_path+'/plotEvent_wewk/'+mvarA,]
    dplot = f.Get(dpath)
    if not dplot:
        print "Could not find "+str(dpath)+" in "+str(f)+" - GetWNFHists"
        sys.exit(0)
    dplot = f.Get(dpath).Clone()
    bkgTot=None
    sigTot=None
    for b in bkgpaths:
        a=f.Get(b).Clone()
        if bkgTot==None:
            bkgTot=a.Clone()
        else:
            bkgTot.Add(a)
    for b in sigpaths:
        a=f.Get(b).Clone()
        if sigTot==None:
            sigTot=a.Clone()
        else:
            sigTot.Add(a)

    errordata = ROOT.Double(0.0)
    errormc = ROOT.Double(0.0)    
    dplot.Add(bkgTot,-1.0)
    data_minus_bkg = dplot.IntegralAndError(25,10001,errordata)
    signEvt = sigTot.IntegralAndError(25,10001,errormc)
    if signEvt>0.0:
        NFerr = math.sqrt(errordata**2+errormc**2)/signEvt
        return data_minus_bkg/signEvt,NFerr
    return 1.0
    
def GetHists(f,cut_path, mvar, year, met=150.0, computeNF=False):
    dpath    = cut_path+'/plotEvent_data/'+mvar
    bkgpaths=[cut_path+'/plotEvent_wqcd/'+mvar,
                  cut_path+'/plotEvent_zqcd/'+mvar,
                  cut_path+'/plotEvent_wewk/'+mvar,
                  cut_path+'/plotEvent_zewk/'+mvar,
                  cut_path+'/plotEvent_tall/'+mvar,
                  ]
    dplot    = f.Get(dpath)
    if not dplot:        
        print "Could not find "+str(dpath)+" in "+str(f)+" - GetHists"
        sys.exit(0)
    dplot    = f.Get(dpath).Clone()
    SetOverflow(dplot)
    bkgTot=None
    for b in bkgpaths:
        #print b
        a=f.Get(b).Clone()
        if b.count('zqcd') or b.count('zewk'):
            znf=1.0
            znferr=0.0
            if computeNF:
                znf,znferr=GetZNFHists(f,cut_path, mvar,year)
                print 'zNF: ',znf,znferr
            else:
                znf=GetZNF(f,cut_path, mvar,year)
            a.Scale(znf) # correcting that Znn sample in 2018
            for ibin in range(0,a.GetNbinsX()+2):
                binerr = a.GetBinError(ibin)
                bincont = a.GetBinContent(ibin)
                a.SetBinError(ibin,math.sqrt(binerr**2+(bincont*znferr)**2))
        if b.count('wqcd') or b.count('wewk'):
            wnf=1.0
            wnferr=0.0
            if computeNF:
                wnf,wnferr=GetWNFHists(f,cut_path, mvar,year)
                if wnferr<0.02:
                    wnferr=0.02
                print 'wNF: ',wnf,wnferr
            else:
                wnf=GetWNF(f,cut_path, mvar,year,met=met)
            a.Scale(wnf) # correcting that Wlnu to the control regions
            for ibin in range(0,a.GetNbinsX()+2):
                binerr = a.GetBinError(ibin)
                bincont = a.GetBinContent(ibin)
                a.SetBinError(ibin,math.sqrt(binerr**2+(bincont*wnferr)**2))
        if bkgTot==None:
            bkgTot=a.Clone()
        else:
            bkgTot.Add(a)
            
    SetOverflow(bkgTot)
    dplot.Add(bkgTot,-1.0)
    return dplot #,bkgTot

def GetWNF(f, num_path, mvar, year=2016, met=150.0):
    if met>140:
        return 1.01
    return 1.06

def GetZNF(f, num_path, mvar, year=2016):
    
    #hdataMinBkg_passFJVT = GetHists(f, num_path, mvar)
    if year==2018:
        return 1.2

    if year==2019:
        return 1.03 # correcting inclusively
    return 1.04
    
def GetFJVT(can, num_path, mvar, fnameA, fnameFailfjvt, year=2019):    
    
    f = ROOT.TFile.Open(fnameA)
    ffail = ROOT.TFile.Open(fnameFailfjvt)
    if not f or not ffail:
        print 'file: ',fnameA,fnameFailfjvt
        sys.exit(0)
    fname=fnameA.rstrip('.root')
    print 'GetFJVT: num_path = ',num_path
    hdataMinBkg_passFJVT = GetHists(f,     num_path, mvar, year, computeNF=True)

    if num_path.count('nj2dphijj'):
        den_path=num_path.replace('nj2dphijj','dphijj')
    else:
        den_path=num_path.replace('nj2','allmjj')
    print 'den_path:',den_path
    hdataMinBkg_failFJVT = GetHists(ffail, den_path, mvar, year)

    hdataMinBkg_passFJVT.GetXaxis().SetTitle('m_{jj} [GeV]')
    hdataMinBkg_failFJVT.GetXaxis().SetTitle('m_{jj} [GeV]')
    rebin=-1
    if mvar.count('met'):
        hdataMinBkg_passFJVT.GetXaxis().SetTitle('E_{T}^{miss} [GeV]')
        hdataMinBkg_failFJVT.GetXaxis().SetTitle('E_{T}^{miss} [GeV]')        
    elif mvar.count('jj_dphi'):
        hdataMinBkg_passFJVT.GetXaxis().SetTitle('#Delta#phi_{jj}')
        hdataMinBkg_failFJVT.GetXaxis().SetTitle('#Delta#phi_{jj}')
        rebin=10        
    elif mvar.count('jetPt0'):
        hdataMinBkg_passFJVT.GetXaxis().SetTitle('Jet p_{T} [GeV]')
        hdataMinBkg_failFJVT.GetXaxis().SetTitle('Jet p_{T} [GeV]')

    if rebin>1:
        hdataMinBkg_failFJVT.Rebin(rebin)
        hdataMinBkg_passFJVT.Rebin(rebin)

    # do the division
    hdataMinBkg_passFJVT.Divide(hdataMinBkg_failFJVT)        
    hdataMinBkg_passFJVT.GetYaxis().SetTitle('Pass Lead FJVT / Fail')
    can.Clear()
    can.Draw()
    can.cd()
    hdataMinBkg_passFJVT.Draw()
    can.Update()
    #can.WaitPrimitive()

    rv = hdataMinBkg_passFJVT.Clone()
    rv.SetDirectory(0)
    hdataMinBkg_failFJVT.SetDirectory(0)
    return rv,hdataMinBkg_failFJVT

def getATLASLabels(pad, x, y, text=None, selkey=None, text2=None):
    l = ROOT.TLatex(x, y, 'ATLAS')
    l.SetNDC()
    l.SetTextFont(62)
    l.SetTextSize(0.07)
    l.SetTextAlign(11)
    l.SetTextColor(ROOT.kBlack)
    l.Draw()

    delx = 0.05*pad.GetWh()/(pad.GetWw())
    labs = [l]

    if True:
        p = ROOT.TLatex(x+0.22, y, ' Internal') #
        p.SetNDC()
        p.SetTextFont(42)
        p.SetTextSize(0.065)
        p.SetTextAlign(11)
        p.SetTextColor(ROOT.kBlack)
        p.Draw()
        labs += [p]

        a = ROOT.TLatex(x, y-0.04, '#sqrt{s}=13 TeV, %s fb^{-1}' %(args.lumi))        
        a.SetNDC()
        a.SetTextFont(42)
        a.SetTextSize(0.05)
        a.SetTextAlign(12)
        a.SetTextColor(ROOT.kBlack)
        a.Draw()
        labs += [a]
        
    if text != None:

        c = ROOT.TLatex(x, y-0.1, text)
        c.SetNDC()
        c.SetTextFont(42)
        c.SetTextSize(0.05)
        c.SetTextAlign(12)
        c.SetTextColor(ROOT.kBlack)
        labs += [c]
    if text2 != None:
        d = ROOT.TLatex(x, y-0.16, text2)
        d.SetNDC()
        d.SetTextFont(42)
        d.SetTextSize(0.05)
        d.SetTextAlign(12)
        d.SetTextColor(ROOT.kBlack)
        labs += [d]
    return labs
        
def DrawList(can,plts,names,plt_name,ytitle='Trigger Eff.',trig='xe110',input_err=None):
    print plts
    can.Clear();
    color=1
    leg = ROOT.TLegend(0.65, 0.2, 0.98, 0.5)
    leg.SetBorderSize(0)
    leg.SetFillStyle (0)
    leg.SetTextFont(42);
    leg.SetTextSize(0.04);    
    
    plts[0].GetXaxis().SetTitle('Loose MET [GeV]')
    #if mvar.count('tenacious'):
    #plts[0].GetXaxis().SetTitle('Tenacious MET [GeV]')
    #plts[0].GetXaxis().SetRangeUser(0.6,1.2)
    plts[0].GetYaxis().SetTitle(ytitle)
    for p in plts:
        p.SetLineColor(color)
        p.SetMarkerColor(color)
        if color==1:
            p.Draw()
            if input_err:
                input_err.SetLineColor(ROOT.kMagenta)
                input_err.SetMarkerColor(ROOT.kMagenta)
                input_err.SetFillColor(ROOT.kMagenta)
                input_err.SetFillStyle(3003)
                input_err.Draw('same e5')
                p.Draw('same')                
        else:
            p.Draw('same')
        leg.AddEntry(p,names[color-1])
        color+=1
        p.GetYaxis().SetRangeUser(0.6,1.2)
    if input_err:
        leg.AddEntry(input_err,'Fit+Err')
    leg.Draw()
    if args.lowfjvt:
      texts = getATLASLabels(can, 0.2, 0.88,trig,'low fJVT')
    else:
      texts = getATLASLabels(can, 0.2, 0.88,trig)   
    for t in texts:
        t.Draw()
    can.Update()
    if args.wait:
        can.WaitPrimitive()
    can.SaveAs(args.outdir+'/'+plt_name+'.pdf')

###########################################################################
# Main function for command line execuation
#
if __name__ == "__main__":

    if args.outdir:
        if not os.path.exists(args.outdir):
            os.mkdir(args.outdir)
    
    Style(args.style)
    if args.lowfjvt:
      can = ROOT.TCanvas('stack', 'stack', 900,500)
    else:
      can = ROOT.TCanvas('stack', 'stack', 500, 500)
    fname=args.input
    fnameFailfjvt = args.inputfail
    mvar = args.mvar

    if args.lowfjvt:
      num_path='pass_sr_nj2_nn_Nominal'
      h1,cr1=GetFJVT(can, num_path, mvar, '../160met200/v37MJSyst.root','../160met200/v37MJSyst_rev.root')#for high met comparison region
      h2,cr2=GetFJVT(can, num_path, mvar, '/eos/atlas/atlascerngroupdisk/penn-ww/schae/June7_FJVTCR/v37ALL_SR_fjvt02_met100.root','/eos/atlas/atlascerngroupdisk/penn-ww/schae/June7_FJVTCR/v37ALL_SR_fjvt02rev_met100.root')
      h3,cr3=GetFJVT(can, num_path, mvar, '/eos/atlas/atlascerngroupdisk/penn-ww/schae/June7_FJVTCR/v37ALL_SR_fjvt02_met130.root','/eos/atlas/atlascerngroupdisk/penn-ww/schae/June7_FJVTCR/v37ALL_SR_fjvt02rev_met130.root')
      h4,cr4=GetFJVT(can, num_path, mvar, '/eos/atlas/atlascerngroupdisk/penn-ww/schae/June7_FJVTCR/v37ALL_SR_fjvt02_met140.root','/eos/atlas/atlascerngroupdisk/penn-ww/schae/June7_FJVTCR/v37ALL_SR_fjvt02rev_met140.root')
      h5,cr5=GetFJVT(can, num_path, mvar, '/eos/atlas/atlascerngroupdisk/penn-ww/schae/June7_FJVTCR/v37ALL_SR_fjvt02_met150.root','/eos/atlas/atlascerngroupdisk/penn-ww/schae/June7_FJVTCR/v37ALL_SR_fjvt02rev_met150.root')
      #individual elements of h1 (160-200 slice)
      hA,crA=GetFJVT(can, num_path, mvar, '../160met200/out_v37AMJSyst_dougHighMET.root','../160met200/out_v37AMJSyst_rev_dougHighMET.root',year=2016)
      hD,crD=GetFJVT(can, num_path, mvar, '../160met200/out_v37DMJSyst_dougHighMET.root','../160met200/out_v37DMJSyst_rev_dougHighMET.root',year=2017)
      hE,crE=GetFJVT(can, num_path, mvar, '../160met200/out_v37EMJSyst_dougHighMET.root','../160met200/out_v37EMJSyst_rev_dougHighMET.root',year=2018)
      h9=None
      can.Clear()
      #h2.GetYaxis().SetRangeUser(0,5.0)
      h2.GetYaxis().SetRangeUser(0,3.0)
      if args.mvar.count('jetPt'):
          h2.GetXaxis().SetRangeUser(50.0,150.0)
      elif mvar.count('met'):
          h2.GetYaxis().SetRangeUser(0,1)
      h2.Draw()
      h3.SetLineColor(2)
      h3.SetMarkerColor(2)
      h4.SetLineColor(4)
      h4.SetMarkerColor(4)
      h5.SetLineColor(5)
      h5.SetMarkerColor(5)
      h3.Draw('same')
      h4.Draw('same')
      h5.Draw('same')

    else:
      #h1=DrawFJVT(can,trig,lep, mvar, fname,fnameFailfjvt)
      #num_path='pass_sr_LowMETQCDSRFJVT_nn_Nominal'
      num_path='pass_sr_nj2_nn_Nominal'
      #num_path='pass_sr_nj2dphijj2_nn_Nominal'
      ntuplev='v37ALL'
      fjvt='fjvt02'
      #ntuplev='v37D'
      #h1,cr1=GetFJVT(can, num_path, mvar, fname, fnameFailfjvt)
      h1=None
      cr1=None
      cr3=None
      h3=None
      if fjvt=='fjvt05':
          h1,cr1=GetFJVT(can, num_path, mvar, ntuplev+'Loose_SR_'+fjvt+'_met100.root', ntuplev+'Loose_SR_'+fjvt+'rev_met100.root')
          #num_path='pass_sr_nj2dphijj1_nn_Nominal'
          h3,cr3=GetFJVT(can, 'pass_sr_allmjj_nn_Nominal', mvar, ntuplev+'_'+fjvt+'.root', ntuplev+'_SR_'+fjvt+'rev.root')        
      else:
          h1,cr1=GetFJVT(can, num_path, mvar, ntuplev+'_SR_'+fjvt+'_met100.root', ntuplev+'_SR_'+fjvt+'rev_met100.root')    
      #num_path='pass_sr_allmjj_nn_Nominal'
      num_path='pass_sr_nj2_nn_Nominal'
      h2,cr2=GetFJVT(can, num_path, mvar, ntuplev+'_SR_'+fjvt+'_met150.root', ntuplev+'_SR_'+fjvt+'rev_met150.root')
      h30,cr30=GetFJVT(can, num_path, mvar, ntuplev+'_SR_'+fjvt+'_met130.root', ntuplev+'_SR_'+fjvt+'rev_met130.root')    
      num_path='pass_sr_allmjj_nn_Nominal'
     
      num_path='pass_sr_nj2_nn_Nominal'
      h4=None
      h5=None
      if fjvt=='fjvt05':
          h4,cr4=GetFJVT(can, num_path, mvar, ntuplev+'_SR_'+fjvt+'_met170.root', ntuplev+'_SR_'+fjvt+'rev_met170.root')
          h5,cr5=GetFJVT(can, num_path, mvar, ntuplev+'_SR_'+fjvt+'_met180.root', ntuplev+'_SR_'+fjvt+'rev_met180.root')
      print '140'
      h6,cr6=GetFJVT(can, num_path, mvar, ntuplev+'_SR_'+fjvt+'_met140.root', ntuplev+'_SR_'+fjvt+'rev_met140.root')
      #h6,cr6=GetFJVT(can, num_path, mvar, ntuplev+'_SR_'+fjvt+'_met140.root', ntuplev+'_SR_'+fjvt+'rev_met140_nomjj.root')
      h7=None
      h8=None
      cr7=None
      cr8=None
      if fjvt=='fjvt05':
          h7,cr7=GetFJVT(can, num_path, mvar, ntuplev+'_SR_'+fjvt+'_met190.root', ntuplev+'_SR_'+fjvt+'rev_met190.root')
          h8,cr8=GetFJVT(can, num_path, mvar, ntuplev+'_SR_'+fjvt+'_met200.root', ntuplev+'_SR_'+fjvt+'rev_met200.root')    
      num_path='pass_sr_nj2_nn_Nominal'    
      #h9,cr9=GetFJVT(can, num_path, mvar, ntuplev+'_SR_fjvt02_met140.root', ntuplev+'_SR_fjvt02rev_met140.root')
      h9,cr9=GetFJVT(can, num_path, mvar, ntuplev+'_SR_fjvt02_met140.root', ntuplev+'_SR_fjvt02rev_met140_nomjj.root')
      #h9,cr9=GetFJVT(can, num_path, mvar, ntuplev+'_SR_fjvt02_met150.root', ntuplev+'_SR_fjvt02rev_met150.root')
      #h9,cr9=GetFJVT(can, num_path, mvar, ntuplev+'_SR_fjvt02_met120.root', ntuplev+'_SR_fjvt02rev_met120.root')        
     
      num_path='pass_sr_allmjj_nn_Nominal'
      fjvt='fjvt05'
      hA,crA=GetFJVT(can, num_path, mvar, 'v37A_'+fjvt+'.root', 'v37A_SR_'+fjvt+'rev.root')
      hD,crD=GetFJVT(can, num_path, mvar, 'v37D_'+fjvt+'.root', 'v37D_SR_'+fjvt+'rev.root')
      hE,crE=GetFJVT(can, num_path, mvar, 'v37E_'+fjvt+'.root', 'v37E_SR_'+fjvt+'rev.root')
      #if args.mvar=='met_tst_et':
      #    h1.SetBinContent(11,1.5)
      #    if h5:
      #        h5.SetBinContent(18,1.55)
      #    if h4:
      #        h4.SetBinContent(17,1.44)
      can.Clear()
      h1.GetYaxis().SetRangeUser(0,5.0)
      if args.mvar.count('jetPt0'):
          h1.GetXaxis().SetRangeUser(50.0,150.0)
      h1.Draw()
      h2.SetLineColor(2)
      h2.SetMarkerColor(2)
      if h3:
          h3.SetLineColor(3)
          h3.SetMarkerColor(3)
      if h4:
          h4.SetLineColor(4)
          h4.SetMarkerColor(4)
      if h5:
          h5.SetLineColor(5)
          h5.SetMarkerColor(5)
      h6.SetLineColor(ROOT.kMagenta)
      h6.SetMarkerColor(ROOT.kMagenta)
      if h7:
          h7.SetLineColor(ROOT.kOrange+5)
          h7.SetMarkerColor(ROOT.kOrange+5)
      if h8:
          h8.SetLineColor(ROOT.kOrange)
          h8.SetMarkerColor(ROOT.kOrange)
      h9.SetLineColor(ROOT.kPink)
      h9.SetMarkerColor(ROOT.kPink)
      h30.SetLineColor(ROOT.kPink)
      h30.SetMarkerColor(ROOT.kPink)    
      h2.Draw('same')
      #h3.Draw('same')
      if h4:
          h4.Draw('same')
      if h5:
          h5.Draw('same')
      h6.Draw('same')
      if h7:
          h7.Draw('same')
      if h8:
          h8.Draw('same')
      h30.Draw('same')    
      #h9.Draw('same')

    #### --- setup systematics
    # setup systematics
    if args.lowfjvt:
      WfuncSyst = h2.Clone()
    else:
      WfuncSyst = h1.Clone()
    WfuncSyst.SetMarkerSize(0)
    WfuncSyst.SetLineStyle(4)
    WfuncSyst.SetFillColor(ROOT.kGreen)
    WfuncSyst.SetFillStyle(3001)

    # generate xyz - for 140 slice
    if h9:
      for i in range(1,h9.GetNbinsX()+2):
        print 'Bin %0.1f Val: %0.3f ' %(h9.GetXaxis().GetBinLowEdge(i),h9.GetBinContent(i))
    # getting the weighted average
    if args.lowfjvt:
      listofh = [h2,h3,h4,h5]
    else:
      listofh = [h1,h30,h6,h2,h4,h5,h7,h8]
      if not h7:
        listofh = [h1,h30,h6,h2]

    allvs=[]
    alles=[]
    for i in range(1,h1.GetNbinsX()+2):
        vals=[]
        errs=[]
        for hi in listofh:
            if hi.GetBinContent(i)>0 and hi.GetBinError(i)>0.0:
                vals+=[hi.GetBinContent(i)]
                allvs+=[hi.GetBinContent(i)]
            else:
                vals+=[0]
            if hi.GetBinContent(i)>0.0 and hi.GetBinError(i)>0.0:
                errs+=[(hi.GetBinContent(i)/hi.GetBinError(i))**2]
                alles+=[(hi.GetBinContent(i)/hi.GetBinError(i))**2]
                #errs+=[(1.0/hi.GetBinError(i))**2]
            else:
                errs+=[0.0]
        if sum(vals)>0.0:
            print vals
            # get average:
            npvals=np.array(vals)
            nperrs=np.array(errs)
            weightedAvg = np.average(npvals,weights = nperrs, returned = False)
            avgerr = np.std(npvals)
            variance = np.average((npvals-weightedAvg)**2, weights=nperrs)
            
            #(average, math.sqrt(variance))
            print 'Bin %0.1f Average: %0.3f +/- %0.3f (std dev.) +/- %0.3f (weighted err) relative Error: %0.2f (rel. error on weighted avg)' %(h1.GetXaxis().GetBinLowEdge(i),weightedAvg,avgerr, math.sqrt(variance), (math.sqrt(variance)/weightedAvg))
            WfuncSyst.SetBinContent(i,weightedAvg)
            WfuncSyst.SetBinError(i,math.sqrt(variance))
        else:
            WfuncSyst.SetBinContent(i,0)
            WfuncSyst.SetBinError(i,0)
    WfuncSystline = WfuncSyst.Clone()
    if args.mvar=='met_tst_et':
        npvals=np.array(allvs)
        nperrs=np.array(alles)
        weightedAvg = np.average(npvals, weights = nperrs, returned = False)
        avgerr = np.std(npvals)
        variance = np.average((npvals-weightedAvg)**2, weights=nperrs)
        relavgError = (math.sqrt(variance)/weightedAvg)
        if relavgError<0.2:
            relavgError=0.2
        for u in range(1,WfuncSyst.GetNbinsX()+1):
            WfuncSyst.SetBinContent(u,weightedAvg)
            WfuncSystline.SetBinContent(u,weightedAvg)
            WfuncSystline.SetBinError(u,0.0)
            WfuncSyst.SetBinError(u,relavgError*weightedAvg)
    WfuncSyst.SetLineWidth(1)
    WfuncSyst.SetLineColor(1)
    WfuncSyst.SetLineStyle(3)    
    WfuncSyst.Draw('same E3')
    WfuncSystline.SetFillColor(0)
    WfuncSystline.SetLineStyle(3)
    WfuncSystline.Draw('same ')

    #### --- end systematics
    
    leg = ROOT.TLegend(0.65, 0.2, 0.98, 0.5)
    leg.SetBorderSize(0)
    leg.SetFillStyle (0)
    leg.SetTextFont(42);
    leg.SetTextSize(0.04);
    if args.lowfjvt:
      texts = getATLASLabels(can, 0.2, 0.88,'low fJVT')
      leg = ROOT.TLegend(0.7, 0.4, 0.98, 0.7)
      leg.AddEntry(h2,'100<MET<130')
      leg.AddEntry(h3,'130<MET<140')
      leg.AddEntry(h4,'140<MET<150')
      leg.AddEntry(h5,'150<MET<160')
    else:
      texts = getATLASLabels(can, 0.2, 0.88,'')
      leg.AddEntry(h1,'100< MET<130')
      leg.AddEntry(h30,'130< MET<140')
      leg.AddEntry(h6,' 140<MET<150')
      leg.AddEntry(h2,' 150<MET<160')
      if h4:
          leg.AddEntry(h4,' 160<MET<170')
      if h5:
          leg.AddEntry(h5,' 170<MET<180')
      if h7:
          leg.AddEntry(h7,' 180<MET<190')
      if h8:
          leg.AddEntry(h8,' 190<MET<200')
      #leg.AddEntry(h9,' met140 FJVT>0.2')
    for t in texts:
        t.Draw()
    leg.AddEntry(WfuncSyst,' Syst Band')
    #leg.AddEntry(h3,'MET>200')
    leg.Draw()
    can.Update()
    if args.save:
      canSave = can.Clone()
      canSave.SaveAs(mvar+'.pdf')
    if args.wait:
      can.WaitPrimitive()
      raw_input('')

    can.Clear()
    if args.lowfjvt:
      fulldist=cr1
    elif cr3:
      fulldist=cr3
    else:
      fulldist=None

    if fulldist:
        fulldist.GetYaxis().SetTitle('MJ CR Yields')
        fulldist.Draw()
        can.Update()
        if args.wait:
            can.WaitPrimitive()
        for i in range(1,h1.GetNbinsX()+1):
            ibin=fulldist.GetBinContent(i)
            ibine=fulldist.GetBinError(i)
            isf=WfuncSyst.GetBinContent(i)
            fulldist.SetBinContent(i,ibin*isf)
            fulldist.SetBinError(i,ibine*isf)
            for hCR in [crA,crD,crE]:
                hCR.SetBinContent(i,hCR.GetBinContent(i)*isf)
                hCR.SetBinError(i,hCR.GetBinError(i)*isf)

        can.Clear()
        fulldist.GetYaxis().SetTitle('MJ Prediction')
        fulldist.Draw()
        if args.wait:
          can.WaitPrimitive()
        can.Update()
        mjerr=ROOT.Double()
        print 'MJ yields: %0.2f +/- %0.2f' %(fulldist.IntegralAndError(0,10001,mjerr,''),mjerr)
    err = ROOT.Double(0.0)
    totalBkg = crA.IntegralAndError(0,1001,err)
    print 'MJ A yields: %0.2f +/- %0.2f' %(totalBkg,err)
    totalBkg = crD.IntegralAndError(0,1001,err)
    print 'MJ D yields: %0.2f +/- %0.2f' %(totalBkg,err)
    totalBkg = crE.IntegralAndError(0,1001,err)
    print 'MJ E yields: %0.2f +/- %0.2f' %(totalBkg,err)
    if fulldist:
        for i in range(1,h1.GetNbinsX()+1):
            print 'Bin %0.1f Yield: %0.1f' %(h1.GetXaxis().GetBinLowEdge(i), fulldist.GetBinContent(i))


    if args.lowfjvt:
      #hardcoded for 140<MET<150 for direct comparison
      hA,crA=GetFJVT(can, num_path, mvar, '/eos/atlas/atlascerngroupdisk/penn-ww/schae/June7_FJVTCR/v37A_SR_fjvt02_met140.root','/eos/atlas/atlascerngroupdisk/penn-ww/schae/June7_FJVTCR/v37A_SR_fjvt02rev_met140.root',year=2016)
      hD,crD=GetFJVT(can, num_path, mvar, '/eos/atlas/atlascerngroupdisk/penn-ww/schae/June7_FJVTCR/v37D_SR_fjvt02_met140.root','/eos/atlas/atlascerngroupdisk/penn-ww/schae/June7_FJVTCR/v37D_SR_fjvt02rev_met140.root',year=2016)
      hE,crE=GetFJVT(can, num_path, mvar, '/eos/atlas/atlascerngroupdisk/penn-ww/schae/June7_FJVTCR/v37E_SR_fjvt02_met140.root','/eos/atlas/atlascerngroupdisk/penn-ww/schae/June7_FJVTCR/v37E_SR_fjvt02rev_met140.root',year=2016)
      can.Clear()
      #hA.GetYaxis().SetRangeUser(0,5.0)
      hA.GetYaxis().SetRangeUser(0,3.0)
      if mvar.count('jetPt'):
          hA.GetXaxis().SetRangeUser(70,150)
      elif mvar.count('met'):
          hA.GetYaxis().SetRangeUser(0,1)
      hA.Draw()
      hD.SetLineColor(2)
      hD.SetMarkerColor(2)
      hE.SetLineColor(3)
      hE.SetMarkerColor(3)
      hD.Draw('same')
      hE.Draw('same')
      WfuncSyst.Draw('same E3')
      texts=[]
      texts = getATLASLabels(can, 0.2, 0.88,'140<MET<150')
      for t in texts:
          t.Draw()
      leg.Clear()
      leg.AddEntry(hA,'2015/6')
      leg.AddEntry(hD,'2017')
      leg.AddEntry(hE,'2018')
      leg.AddEntry(WfuncSyst,'SystBand')
      leg.Draw()
      can.Update()
      if args.wait:
        can.WaitPrimitive()
      if args.save:
        canSave = can.Clone()
        canSave.SaveAs(mvar+'_years.pdf')
    else:
      for j in ['140','160']:
          num_path='pass_sr_allmjj_nn_Nominal'
          ntuplev='v37A'
          hA,crA=GetFJVT(can, num_path, mvar, ntuplev+'_SR_'+fjvt+'_met%s.root' %(j), ntuplev+'_SR_'+fjvt+'rev_met%s.root' %(j),year=2016)
          ntuplev='v37D'
          hD,crD=GetFJVT(can, num_path, mvar, ntuplev+'_SR_'+fjvt+'_met%s.root' %(j), ntuplev+'_SR_'+fjvt+'rev_met%s.root' %(j),year=2017)
          ntuplev='v37E'
          hE,crE=GetFJVT(can, num_path, mvar, ntuplev+'_SR_'+fjvt+'_met%s.root' %(j), ntuplev+'_SR_'+fjvt+'rev_met%s.root' %(j),year=2018)
          can.Clear()
          hA.GetYaxis().SetRangeUser(0,5.0)
          hA.Draw()
          hD.SetLineColor(2)
          hD.SetMarkerColor(2)
          hE.SetLineColor(3)
          hE.SetMarkerColor(3)
          hD.Draw('same')
          hE.Draw('same')
          WfuncSyst.Draw('same E3')
          texts=[]
          if j=='140':
              texts = getATLASLabels(can, 0.2, 0.88,'%s<MET<150' %(j))
          if j=='160':
              texts = getATLASLabels(can, 0.2, 0.88,'150<MET<160')
          for t in texts:
              t.Draw()
          leg.Clear()
          leg.AddEntry(hA,'2015/6')
          leg.AddEntry(hD,'2017')
          leg.AddEntry(hE,'2018')    
          leg.AddEntry(WfuncSyst,'SystBand')    
          leg.Draw()
          can.Update()
          can.WaitPrimitive()

      # compare the different years in the low MET region
      num_path='pass_sr_LowMETQCDSRFJVT_nn_Nominal'
      ntuplev='v37A'
      hA,crA=GetFJVT(can, num_path, mvar, ntuplev+'_'+fjvt+'.root', ntuplev+'_'+fjvt+'rev.root',year=2016)
      ntuplev='v37D'
      hD,crD=GetFJVT(can, num_path, mvar, ntuplev+'_'+fjvt+'.root', ntuplev+'_'+fjvt+'rev.root',year=2017)
      ntuplev='v37E'
      hE,crE=GetFJVT(can, num_path, mvar, ntuplev+'_'+fjvt+'.root', ntuplev+'_'+fjvt+'rev.root',year=2018)    
      can.Clear()
      hA.GetYaxis().SetRangeUser(0,5.0)
      hA.Draw()
      hD.SetLineColor(2)
      hD.SetMarkerColor(2)
      hE.SetLineColor(3)
      hE.SetMarkerColor(3)
      hD.Draw('same')
      hE.Draw('same')
      WfuncSyst.Draw('same E3')
      texts = getATLASLabels(can, 0.2, 0.88,'Low MET')
      for t in texts:
          t.Draw()
      leg.Clear()
      leg.AddEntry(hA,'2015/6')
      leg.AddEntry(hD,'2017')
      leg.AddEntry(hE,'2018')
      leg.AddEntry(WfuncSyst,'SystBand')
      leg.Draw()
      can.Update()
      can.WaitPrimitive()
