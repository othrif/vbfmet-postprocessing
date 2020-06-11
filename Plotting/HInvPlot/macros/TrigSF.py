#!/usr/bin/env python
import os
import sys
import subprocess
import argparse
import ROOT
import math

parser = argparse.ArgumentParser( description = "Changing to MG relative uncertainties", add_help=True , fromfile_prefix_chars='@')
parser.add_argument("--lumi", dest='lumi', default=36, help="Lumi")
parser.add_argument("--year", dest='year', default='2016', help="Year")
parser.add_argument("--input", dest='input', default='v34ALooseMETPassThru_ktmerge.root', help="input file name")
parser.add_argument("--mvar", dest='mvar', default='met_tst_et', help="MET variable: met_cst_jet, met_tst_et, met_tenacious_tst_et")
parser.add_argument("--outdir", dest='outdir', default='/tmp/plotTrig', help="Output Directory")
parser.add_argument("--wait", action='store_true', dest='wait', default=False, help="wait")
parser.add_argument("--mg", action='store_true', dest='mg', default=False, help="measure mg")
args, unknown = parser.parse_known_args()

import HInvPlot.JobOptions as config
import HInvPlot.CutsDef    as hstudy

#-----------------------------------------
def Style():
    atlas_style_path='/Users/schae/testarea/SUSY/JetUncertainties/testingMacros/atlasstyle/'
    if not os.path.exists(atlas_style_path):
        print("Error: could not find ATLAS style macros at: " + atlas_style_path)
        sys.exit(1)
    ROOT.gROOT.LoadMacro(os.path.join(atlas_style_path, 'AtlasStyle.C'))
    #ROOT.gROOT.LoadMacro(os.path.join(atlas_style_path, 'AtlasUtils.C'))
    ROOT.SetAtlasStyle()
    
class function_turnon:
    def __call__(self, x, parameters):
        #0.5*(1+TMath::Erf((150-p0)/(TMath::Sqrt(2)*p1)))
        p0 = parameters[0] # shape
        p1 = parameters[1] # location of minimum
        x = x[0]
        y = 0.5*(1+ROOT.TMath.Erf((150-p0)/(ROOT.TMath.Sqrt(2)*p1)))
        return y
    
def myfunc(x, p):
    #return p[0]*np.exp(-(x/p[1])**2) + p[1]*np.exp(-(x/p[2])**2)
    return 0.5*(1+ROOT.TMath.Erf((x-p[0])/(ROOT.TMath.Sqrt(2)*p[1])))

def GetHists(f,cut_path, zcut_path, mvar):
    dpath    = cut_path+'/plotEvent_data/'+mvar
    wQCDpath = cut_path+'/plotEvent_wqcd/'+mvar
    wEWKpath = cut_path+'/plotEvent_wewk/'+mvar
    zQCDpath = zcut_path+'/plotEvent_zqcd/'+mvar
    zEWKpath = zcut_path+'/plotEvent_zewk/'+mvar
    zgQCDpath = zcut_path+'/plotEvent_zgam/'+mvar    
    if args.mg:
        zQCDpath = zcut_path+'/plotEvent_zqcdMad/'+mvar
        wQCDpath = zcut_path+'/plotEvent_wqcdMad/'+mvar
    #zEWKpath = zcut_path+'/plotEvent_zewk/'+mvar

    zBkgEWKpath = cut_path+'/plotEvent_zewk/'+mvar
    zBkgQCDpath = cut_path+'/plotEvent_zqcd/'+mvar
    topBkgpath = cut_path+'/plotEvent_tall/'+mvar
    if args.mg:
        zBkgQCDpath = cut_path+'/plotEvent_zqcdMad/'+mvar
    dplot    = f.Get(dpath)
    if not dplot:
        print dpath
        sys.exit(0)
    dplot    = f.Get(dpath).Clone()
    wQCDplot = f.Get(wQCDpath).Clone()
    wEWKplot = f.Get(wEWKpath).Clone()
    zBkgEWKplot = f.Get(zBkgEWKpath).Clone()
    zBkgQCDplot = f.Get(zBkgQCDpath).Clone()
    topBkgplot = f.Get(topBkgpath).Clone()

    bkgTot = wQCDplot.Clone()
    bkgTot.Add(wEWKplot)
    bkgTot.Add(zBkgEWKplot)
    bkgTot.Add(zBkgQCDplot)
    bkgTot.Add(topBkgplot)
    
    zQCDplot = f.Get(zQCDpath).Clone()
    zgQCDplot = f.Get(zgQCDpath).Clone()    
    zEWKplot = f.Get(zEWKpath).Clone()

    rebin=2
    plts = [dplot,wQCDplot,wEWKplot,zQCDplot,zgQCDplot,zEWKplot,bkgTot]
    if not mvar.count('nolep') or True:
        for p in plts:
            p.Rebin(rebin)
    
    return dplot,wQCDplot,wEWKplot,zQCDplot,zgQCDplot,zEWKplot,bkgTot

def DoFit(name, hist, color=1):
    ROOT.gROOT.LoadMacro("fit.C");
    func=ROOT.TF1("func", ROOT.fitf, 120.0,300.0, 2)
    func.SetParameters(110.0,30.0)
    func.SetParNames("p0", "p1")
    func.SetParLimits(0,   10.0,   200.0)
    func.SetParLimits(1, 0.0,  100.0)
    myfit = hist.Fit(func)
    func.SetLineColor(2)
    #myfit.SetLineColor(2)
    print name,func.GetParameter(0),func.GetParameter(1)
    hist.GetFunction("func").SetLineColor(color);
    print 'Par error: ', hist.GetFunction("func").GetParError(0)
    print 'Par error: ', hist.GetFunction("func").GetParError(1)    
    func.SetName(name)
    return func

def DrawError(trig, input_hist):
    input_err = input_hist.Clone()
    input_err.SetDirectory(0)
    
    p0 = 68.8679; p1 = 54.0594; e0=0.000784094; e1 = 0.06;
    if trig.count('xe70'):
        p0 = 110.396; p1 = 19.4147; e1 = 0.06;
    elif trig.count('xe90'):
        p0 = 111.684; p1 = 19.147;  e1 = 0.08;
    for i in range(0,input_err.GetNbinsX()+1):
        x=input_err.GetXaxis().GetBinCenter(i)
        val = 0.5*(1+ROOT.TMath.Erf((x-p0)/(ROOT.TMath.Sqrt(2)*p1)))
        err = ((e0)*(150-x)+e1)*0.6
        if x>210:
            err=0.01
        input_err.SetBinContent(i,val)
        input_err.SetBinError(i,err)
    return input_err
    
def DrawSF(can,trig, lep, mvar, fnameA,year=2018):    
    
    if lep=='u':
        #met_tenacious_tst_et
        mvar = mvar.replace('_tst_et','_tst_nolep_et')
    
    f = ROOT.TFile.Open(fnameA)
    if not f:
        print 'file: ',fnameA
        sys.exit(0)
    fname=fnameA.rstrip('.root')
    den_path = 'pass_metsf_metsf'+trig+'_'+lep+'_Nominal'
    num_path = 'pass_metsf_metsftrig'+trig+'J400_'+lep+'_Nominal'    
    zden_path = 'pass_metsf_metsf'+trig+'_nn_Nominal'
    znum_path = 'pass_metsf_metsftrig'+trig+'J400_nn_Nominal'
    if year==2018:
        mytrig='trig'
        if trig=="VBFTopo":
            mytrig='trigOR'
        den_path = 'pass_metsf_metsf'+trig+'_'+lep+'_Nominal'
        num_path = 'pass_metsf_metsf'+trig+mytrig+'_'+lep+'_Nominal'    
        zden_path = 'pass_metsf_metsf'+trig+'_nn_Nominal'
        znum_path = 'pass_metsf_metsf'+trig+mytrig+'_nn_Nominal'
        
    dnum,wQCDnum,wEWKnum,zQCDnum,zgQCDnum,zEWKnum,bkgNum = GetHists(f,num_path, znum_path, mvar)
    dden,wQCDden,wEWKden,zQCDden,zgQCDden,zEWKden,bkgDen = GetHists(f,den_path, zden_path, mvar)

    deff = config.ComputeEff([dnum],[dden])
    wQCDeff = config.ComputeEff([wQCDnum],[wQCDden])
    wEWKeff = config.ComputeEff([wEWKnum],[wEWKden])
    #zQCDeff = config.ComputeEff([zQCDnum],[zQCDden])
    #zEWKeff = config.ComputeEff([zEWKnum],[zEWKden])
    bkgeff = config.ComputeEff([bkgNum],[bkgDen])

    wnum = wQCDnum.Clone(); wnum.Add(wEWKnum)
    wden = wQCDden.Clone(); wden.Add(wEWKden)

    zgnum = zgQCDnum.Clone(); zgden = zgQCDden.Clone();
    znum = zQCDnum.Clone(); znum.Add(zEWKnum)
    zden = zQCDden.Clone(); zden.Add(zEWKden)
    print 'Integral: ',zden_path,znum.Integral(0,1001),zden.Integral(0,1001)
    weff = config.ComputeEff([wnum],[wden])
    zeff = config.ComputeEff([znum],[zden])
    zgeff = config.ComputeEff([zgnum],[zgden])    
    
    deff[0].SetLineColor(1)
    deff[0].SetMarkerColor(1)
    zeff[0].SetLineColor(3)
    zeff[0].SetMarkerColor(3)
    zgeff[0].SetLineColor(ROOT.kOrange)
    zgeff[0].SetMarkerColor(ROOT.kOrange)
    weff[0].SetLineColor(2)
    weff[0].SetMarkerColor(2)
    bkgeff[0].SetLineColor(4)
    bkgeff[0].SetMarkerColor(4)

    trig_err = DrawError(trig, bkgeff[0]);
    
    can.Clear()
    can.Draw()
    can.cd()
    deff[0].GetXaxis().SetRangeUser(100.0,300.0)
    deff[0].GetYaxis().SetRangeUser(0.7,1.15)
    deff[0].GetXaxis().SetTitle('Loose MET [GeV]')
    if mvar.count('tenacious'):
        deff[0].GetXaxis().SetTitle('Tenacious MET [GeV]')
        
    deff[0].GetYaxis().SetTitle('Trigger Eff.')    
    deff[0].Draw()
    weff[0].Draw('same')
    zeff[0].Draw('same')
    zgeff[0].Draw('same')
    bkgeff[0].Draw('same')
    deff[0].SetDirectory(0)
    weff[0].SetDirectory(0)
    zeff[0].SetDirectory(0)
    zgeff[0].SetDirectory(0)
    bkgeff[0].SetDirectory(0)
    
    leg = ROOT.TLegend(0.65, 0.2, 0.98, 0.5)
    leg.SetBorderSize(0)
    leg.SetFillStyle (0)
    leg.SetTextFont(42);
    leg.SetTextSize(0.04);    
    leg.AddEntry(deff[0],'Data')
    leg.AddEntry(zeff[0],'Z')
    leg.AddEntry(zgeff[0],'Z#gamma')
    leg.AddEntry(weff[0],'W')
    leg.AddEntry(bkgeff[0],'W+bkg')
    
    leg.Draw()
    can.Update()
    if args.wait:
        can.WaitPrimitive()
    #raw_input('waiting...')
    can.SaveAs(args.outdir+'/'+den_path+'.pdf')

    SFW = deff[0].Clone()
    SFZ = deff[0].Clone()
    SFBkg = deff[0].Clone()
    SFZg = deff[0].Clone()
    SFW.SetDirectory(0)
    SFZ.SetDirectory(0)
    SFZg.SetDirectory(0)
    SFBkg.SetDirectory(0)
    
    SFW.Divide(weff[0])
    SFZ.Divide(zeff[0])
    SFBkg.Divide(bkgeff[0])
    SFZg.Divide(zgeff[0])    
    SFW.GetXaxis().SetRangeUser(100.0,300.0)
    SFW.GetYaxis().SetRangeUser(0.7,1.15)    
    SFW.GetXaxis().SetTitle('Loose MET [GeV]')
    if mvar.count('tenacious'):
        SFW.GetXaxis().SetTitle('Tenacious MET [GeV]')    
    SFW.GetYaxis().SetTitle('Trigger SF')
    SFW.SetLineColor(1)
    SFW.SetMarkerColor(1)
    SFZ.SetLineColor(2)
    SFZ.SetMarkerColor(2)    
    SFBkg.SetLineColor(3)
    SFBkg.SetMarkerColor(3)
    SFZg.SetLineColor(4)
    SFZg.SetMarkerColor(4)
    SFW.Draw()
    SFZ.Draw('same')
    SFZg.Draw('same')
    SFBkg.Draw('same')
    leg.Clear()
    leg.AddEntry(SFZ,'Z#rightarrow#nu#nu')
    leg.AddEntry(SFW,'W#rightarrow l#nu')
    leg.AddEntry(SFBkg,'W+bkg')
    leg.AddEntry(SFZg,'Z(#rightarrow#nu#nu)+#gamma')
    leg.Draw()
    can.Update()
    if args.wait:
        can.WaitPrimitive()
    #raw_input('waiting...')
    can.SaveAs(args.outdir+'/'+fname+'_'+den_path+'_SF.pdf')
    print 'Wfunc'
    Wfunc=DoFit('WSFFit'+fname+'_'+den_path,SFW, SFW.GetLineColor())
    print 'Zfunc'
    Zfunc=DoFit('ZSFFit'+fname+'_'+den_path,SFZ, SFZ.GetLineColor())
    Zfunc.SetLineColor(2)
    print 'bkgfunc'
    bkgfunc=DoFit('bkgSFFit'+fname+'_'+den_path,SFBkg, SFBkg.GetLineColor())
    bkgfunc.SetLineColor(3)
    #SFBkg.GetFunction("func").SetFillColor(SFBkg.GetLineColor())
    #SFBkg.GetFunction("func").SetFillStyle(3001)
    #SFBkg.GetFunction("func").Draw('E3 same')
    WfuncSyst = SFBkg.Clone()
    # Count bins
    nbinsX =0
    for x in range(1,WfuncSyst.GetNbinsX()+1):
        if 100<=WfuncSyst.GetXaxis().GetBinLowEdge(x):
            nbinsX+=1
        if 300<WfuncSyst.GetXaxis().GetBinLowEdge(x):
            break
    chi2 = SFBkg.GetFunction("func").GetChisquare()
    chi2_ndof = (chi2)/(nbinsX-2)
    print 'chi2: ',chi2_ndof
    
    for x in range(1,WfuncSyst.GetNbinsX()+1):
        binx = WfuncSyst.GetXaxis().GetBinCenter(x)
        yval = SFBkg.GetFunction("func").Eval(binx)
        WfuncSyst.SetBinContent(x, yval)
        sferr=0.003
        e0=0.000784094;
        e1=0.04
        if args.year=='2016':
            e1=0.045
        if binx<210.0:
            sferr=((e0)*(150-binx)+e1)*0.6
        WfuncSyst.SetBinError(x,sferr )
    WfuncSyst.SetMarkerSize(0)
    WfuncSyst.SetLineStyle(4)
    WfuncSyst.SetFillColor(SFBkg.GetLineColor())
    WfuncSyst.SetFillStyle(3001)
    WfuncSyst.Draw("same E3")
    leg.AddEntry(WfuncSyst,'SF Unc')
    texts = getATLASLabels(can, 0.2, 0.88, trig, text2='#chi^{2}/N_{dof}=%0.3f' %chi2_ndof)
    for t in texts:
        t.Draw()
    can.Update()
    if args.wait:
        can.WaitPrimitive()
    can.SaveAs(args.outdir+'/'+fname+'_'+den_path+'_SFfit.pdf')
    f.Close()
    return [SFZ,SFW,SFBkg,deff[0],weff[0],zeff[0],bkgeff[0],Wfunc,Zfunc,bkgfunc,trig_err]

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
    
    Style()
    can = ROOT.TCanvas('stack', 'stack', 500, 500)
    mvar = 'met_tst_et'
    #mvar = 'met_tenacious_tst_et'
    #mvar = 'met_cst_jet'
    trig='xe90'
    lep='u'
    fname=args.input
    mvar = args.mvar
    print 'Year: ',args.year
    if args.year=='2016':
        xe90_u_detajj25 = DrawSF(can,trig,lep, mvar, fname,year=2016)
        trig='xe70'
        xe70_u_detajj25 = DrawSF(can,trig,lep, mvar, fname,year=2016)
        trig='xe110'
        xe110_u_detajj25 = DrawSF(can,trig,lep, mvar, fname,year=2016)
        lep='e'
        xe90_e_detajj25 = DrawSF(can,trig,lep, mvar, fname,year=2016)
        trig='xe70'
        xe70_e_detajj25 = DrawSF(can,trig,lep, mvar, fname,year=2016)
        trig='xe110'
        xe110_e_detajj25 = DrawSF(can,trig,lep, mvar, fname,year=2016)    

        DrawList(can,[xe70_u_detajj25[2],xe90_u_detajj25[2],xe110_u_detajj25[2]],['xe70J400','xe90J400','xe110J400'],'METSF20156',ytitle='Trigger SF',trig=trig)
        DrawList(can,[xe110_e_detajj25[2],xe110_u_detajj25[2]],['W#rightarrow e#nu','W#rightarrow#mu#nu'],'METSFxe110_e_vs_mu',ytitle='Trigger SF',trig=trig)
        DrawList(can,[xe110_e_detajj25[6],xe110_u_detajj25[6],xe110_u_detajj25[5]],['W#rightarrow e#nu','W#rightarrow#mu#nu','Z#rightarrow#nu#nu'],'METEffxe110_e_vs_mu',ytitle='Trigger Eff',trig=trig)

    elif args.year=='2017':
        args.lumi='44'
        trig='xe110L155'
        xe110_2017_u_detajj25 = DrawSF(can,trig,lep, mvar, fname,year=2018)
        lep='e'
        xe110_2017_e_detajj25 = DrawSF(can,trig,lep, mvar, fname,year=2018)
        DrawList(can,[xe110_2017_e_detajj25[2],xe110_2017_u_detajj25[2]],['W#rightarrow e#nu','W#rightarrow#mu#nu'],'METSFxe110_2017_e_vs_mu',ytitle='Trigger SF',trig=trig)
        DrawList(can,[xe110_2017_e_detajj25[6],xe110_2017_u_detajj25[6],xe110_2017_u_detajj25[5]],['W#rightarrow e#nu','W#rightarrow#mu#nu','Z#rightarrow#nu#nu'],'METEffxe110_2017_e_vs_mu',ytitle='Trigger Eff',trig=trig)        
    elif args.year=='2018':
        args.lumi='59'
        trig='xe110XE70'
        xe110_2018_u_detajj25 = DrawSF(can,trig,lep, mvar, fname,year=2018)
        lep='e'
        xe110_2018_e_detajj25 = DrawSF(can,trig,lep, mvar, fname,year=2018)
        DrawList(can,[xe110_2018_e_detajj25[2],xe110_2018_u_detajj25[2]],['W#rightarrow e#nu','W#rightarrow#mu#nu'],'METSFxe110_2018_e_vs_mu',ytitle='Trigger SF',trig=trig)
        DrawList(can,[xe110_2018_e_detajj25[6],xe110_2018_u_detajj25[6],xe110_2018_u_detajj25[5]],['W#rightarrow e#nu','W#rightarrow#mu#nu','Z#rightarrow#nu#nu'],'METEffxe110_2018_e_vs_mu',ytitle='Trigger Eff',trig=trig)
    else:
        print 'Trigger is not defined. Try 2016, 2017, or 2018'
    ####
    ####
    ####trig='xe70'
    ####mvar = 'met_tst_et'
    #####fname='v26metsf_v8_tenac_detjj25_CST120'
    ####fname='v26metsf_v8_tenac_detjj25_loose'
    ####xe110_u_detajj25_metLoose = DrawSF(can,trig,lep, mvar, fname)
    ####fname='v26metsf_v8_tenac_detjj25_CST120'
    ####xe110_u_cst120_metLoose = DrawSF(can,trig,lep, mvar, fname)
    ####
    #####[SFZ,SFW,SFBkg,deff[0],weff[0],zeff[0],bkgeff[0],Wfunc,Zfunc,bkgfunc]
    ####lep='e' 
    ####mvar = 'met_tenacious_tst_et'   
    ####xe110_e_nj3 = DrawSF(can,trig,lep, mvar, fname)
    ####lep='u'
    ####xe110_u_nj3 = DrawSF(can,trig,lep, mvar, fname)
    ####lep='e'
    ####fname='v26metsf_v4_tenac'
    ####xe110_e_tenac = DrawSF(can,trig,lep, mvar, fname)
    ####lep='u'
    ####xe110_u_tenac = DrawSF(can,trig,lep, mvar, fname)
    ####fname='v26metsf_v8_tenac_detjj25'
    ####xe110_u_tenac_eta25 = DrawSF(can,trig,lep, mvar, fname)    
    ####fname='v26metsf_nobias_2TeV'
    ####fname='v26metsf_nobias_2TeV_loose'    
    ####xe110_u_2TeV = DrawSF(can,trig,lep, mvar, fname)
    ####fname='v26metsf_nobias_15TeV'    
    ####xe110_u_15TeV = DrawSF(can,trig,lep, mvar, fname)
    ####fname='v26metsf_nobias_1TeV'
    ####xe110_u_1TeV = DrawSF(can,trig,lep, mvar, fname)
    ####fname='v26metsf_nobias_bothforward'
    ####xe110_u_bothfwd = DrawSF(can,trig,lep, mvar, fname)
    ####fname='v26metsf_nobias_eta25'
    ####xe110_u_eta25_nobias = DrawSF(can,trig,lep, mvar, fname)
    ####fname='v26metsf_nobias'
    ####xe110_u_nobias = DrawSF(can,trig,lep, mvar, fname)
    ####
    ####fname='v26metsf_bias_1TeV'
    ####xe110_u_bias_1TeV = DrawSF(can,trig,lep, mvar, fname)
    ####fname='v26metsf_bias_15TeV'
    ####xe110_u_bias_15TeV = DrawSF(can,trig,lep, mvar, fname)
    ####fname='v26metsf_bias_2TeV'
    ####xe110_u_bias_2TeV = DrawSF(can,trig,lep, mvar, fname)
    ####fname='v26metsf_bias_bothfwd'
    ####xe110_u_bias_bothfwd = DrawSF(can,trig,lep, mvar, fname)
    ####
    #####fname='v26metsf_v6_tenac_detajj25'
    ####fname='v26metsf_v8_tenac_detjj25'
    ####lep='e'    
    ####xe110_e_detajj25 = DrawSF(can,trig,lep, mvar, fname)
    ####lep='u'
    #####fname='v26metsf_v8_tenac_detjj25_CST120'
    #####fname='v26metsf_nobias'
    ####print 'xe110_u_detajj25'
    ####xe110_u_detajj25 = DrawSF(can,trig,lep, mvar, fname)
    ####fname='v26metsf_nobias'
    ####print 'xe110_u_detajj25'
    ####xe110_nn_detajj25 = DrawSF(can,trig,lep, mvar, fname)
    ####
    ####fname='v26metsf_v7_tenac_fjvt'
    ####xe110_u_fjvt = DrawSF(can,trig,lep, mvar, fname)
    #####fname='v26metsf_v7_tenac_fjvtCST120'
    ####fname='v26metsf_v8_tenac_detjj25_CST120'
    ####print fname
    ####xe110_u_fjvtCST120 = DrawSF(can,trig,lep, mvar, fname)
    #####fname='v26metsf_v7_tenac_fjvtCST120'
    ####fname='v26metsf_v8_tenac_detjj25_CST120'
    ####lep='e'
    ####xe110_e_fjvtCST120 = DrawSF(can,trig,lep, mvar, fname)
    #####fname='v26metsf_v7_tenac_fjvt'
    ####fname='v26metsf_v7_tenac_fjvt'
    ####xe110_e_fjvt = DrawSF(can,trig,lep, mvar, fname)   
    #####print xe110_e_nj3
    ####DrawList(can,[xe110_e_nj3[0],xe110_e_nj3[2]],['Z','W+bkg'],trig+'test',trig=trig)
    ####DrawList(can,[xe110_e_tenac[2],xe110_e_detajj25[2]],['e','e LooserCuts'],trig+'e_default_vs_detajj25',trig=trig)
    ####DrawList(can,[xe110_u_tenac[2],xe110_u_detajj25[2]],['#mu','#mu LooserCuts'],trig+'u_default_vs_detajj25',trig=trig)
    ####
    ####DrawList(can,[xe110_u_nj3[2],xe110_e_tenac[2],xe110_u_tenac[2]],['#mu+3j','e+2j','#mu+2j'],trig+'njet_mu3j_vs_e2j_SF',ytitle='Trigger SF',trig=trig)
    ####DrawList(can,[xe110_u_nj3[6],xe110_e_tenac[6],xe110_u_tenac[6]],['#mu+3j','e+2j','#mu+2j'],trig+'njet_mu3j_vs_e2j_eff',trig=trig)        
    ####
    ####DrawList(can,[xe110_u_tenac[2],xe110_u_detajj25[2],xe110_u_fjvt[2],xe110_u_fjvtCST120[2],xe110_u_fjvtCST120[0],xe110_e_fjvtCST120[0]],['#mu','#mu LooserCuts','fjvt','fjvt+cst120','Z in SR','Z SR lep'],trig+'u_default_vs_detajj25_vs_fjvt_cst120',trig=trig)
    ####DrawList(can,[xe110_e_tenac[2],xe110_e_detajj25[2],xe110_e_fjvt[2],xe110_e_fjvtCST120[2],xe110_e_fjvtCST120[0]],['e','e LooserCuts','fjvt','fjvt+cst120','Z in SR'],trig+'e_default_vs_detajj25_vs_fjvt_cst120',trig=trig)   
    ####DrawList(can,[xe110_u_tenac[4],xe110_u_detajj25[4],xe110_u_fjvt[4],xe110_u_fjvtCST120[4],xe110_u_fjvtCST120[4],xe110_e_fjvtCST120[5]],['#mu','#mu LooserCuts','fjvt','fjvt+cst120','Z in SR','Z SR lep'],trig+'u_eff_default_vs_detajj25_vs_fjvt_cst120',trig=trig)
    ####DrawList(can,[xe110_nn_detajj25[5],xe110_e_detajj25[5],xe110_e_fjvt[5],xe110_e_fjvtCST120[5],xe110_u_2TeV[5]],['#nu#nu','#nu#nu |#Delta#eta_{jj}|>2.5','fjvt','fjvt+cst120','Z in SR','M_{jj}>2TeV'],trig+'nn_Zeff_default_vs_detajj25_vs_fjvt_cst120',trig=trig)
    ####DrawList(can,[xe110_u_nobias[5],xe110_u_eta25_nobias[5],xe110_u_1TeV[5],xe110_u_15TeV[5],xe110_u_2TeV[5]],['#nu#nu','#nu#nu |#Delta#eta_{jj}|>2.5','M_{jj}>1TeV','M_{jj}>1.5TeV','M_{jj}>2TeV'],trig+'nn_Zeff_default_vs_detajj25_vs_mjj',trig=trig)      
    ####DrawList(can,[xe110_e_tenac[4],xe110_e_detajj25[4],xe110_e_fjvt[4],xe110_e_fjvtCST120[4]],['e','e |#Delta#eta_{jj}|>2.5','fjvt','fjvt+cst120','Z in SR'],trig+'e_Zeff_default_vs_detajj25_vs_fjvt_cst120',trig=trig)
    ####
    ##### Wbkg Eff
    ####DrawList(can,[xe110_e_tenac[6],xe110_e_detajj25[6],xe110_e_fjvt[6],xe110_e_fjvtCST120[6]],['e','e |#Delta#eta_{jj}|>2.5','fjvt cuts','fjvt cuts+cst120','Z in SR'],trig+'eBkg_Weff_default_vs_detajj25_vs_fjvt_cst120',trig=trig)
    ####DrawList(can,[xe110_u_tenac[6],xe110_u_detajj25[6],xe110_u_fjvt[6],xe110_u_fjvtCST120[6]],['#mu','#mu |#Delta#eta_{jj}|>2.5','fjvt cuts','fjvt cuts+cst120','Z in SR'],trig+'uBkg_Weff_default_vs_detajj25_vs_fjvt_cst120',trig=trig)
    ##### trigger SF
    ####DrawList(can,[xe110_e_tenac[1],xe110_e_detajj25[1],xe110_e_fjvt[1],xe110_e_fjvtCST120[1]],['e','e |#Delta#eta_{jj}|>2.5','fjvt cuts','fjvt cuts+cst120','Z in SR'],trig+'eBkg_WSF_default_vs_detajj25_vs_fjvt_cst120',ytitle='Trigger SF',trig=trig,input_err=xe110_u_detajj25_metLoose[10])
    ####DrawList(can,[xe110_u_tenac[1],xe110_u_detajj25[1],xe110_u_fjvt[1],xe110_u_fjvtCST120[1]],['#mu','#mu |#Delta#eta_{jj}|>2.5','fjvt cuts','fjvt cuts+cst120','Z in SR'],trig+'uBkg_WSF_default_vs_detajj25_vs_fjvt_cst120',ytitle='Trigger SF',trig=trig,input_err=xe110_u_detajj25_metLoose[10])
    ##### lepton comparison
    #####DrawList(can,[xe110_e_detajj25[6],xe110_u_detajj25[6],xe110_e_detajj25[5]],['e','#mu','#nu#nu',],'e_default_vs_detajj25_vs_fjvt_cst120')
    ####DrawList(can,[xe110_e_detajj25[6],xe110_u_detajj25[6],xe110_nn_detajj25[5]],['e','#mu','#nu#nu'],trig+'e_vs_mu_vs_nn_eff',trig=trig)
    ####DrawList(can,[xe110_e_detajj25[2],xe110_nn_detajj25[2]],['e','#mu','#nu#nu'],trig+'e_vs_mu_SF',ytitle='Trigger SF',trig=trig)
    ####
    ####
    ####DrawList(can,[xe110_u_detajj25[2],xe110_u_detajj25_metLoose[2]],['#mu Loose','#mu Tenacious'],trig+'Tenacious_vs_Loose_SF',ytitle='Trigger SF',trig=trig)
    ####DrawList(can,[xe110_u_detajj25[6],xe110_u_detajj25_metLoose[6]],['#mu Loose','#mu Tenacious'],trig+'Tenacious_vs_Loose_Eff',ytitle='Trigger Eff',trig=trig)        
    ####
    ####DrawList(can,[xe110_u_fjvtCST120[2],xe110_u_cst120_metLoose[2]],['#mu Loose','#mu Tenacious'],'Tenacious_vs_Loose_CST_SF',ytitle='Trigger SF',trig=trig)
    ####DrawList(can,[xe110_u_fjvtCST120[6],xe110_u_cst120_metLoose[6]],['#mu Loose','#mu Tenacious'],'Tenacious_vs_Loose_CST_Eff',ytitle='Trigger Eff',trig=trig) 
    ####
    ##### Compare triggers
    ####DrawList(can,[xe70_u_detajj25[2],xe90_u_detajj25[2],xe110_u_detajj25[2]],['#mu xe70','#mu xe90','#mu xe110'],'xeComparison_SF', ytitle='Trigger SF',trig='xe70,90,110',input_err=xe110_u_detajj25_metLoose[10])
    ####DrawList(can,[xe70_u_detajj25[6],xe90_u_detajj25[6],xe110_u_detajj25[6]],['#mu xe70','#mu xe90','#mu xe110'],'xeComparison_Eff',ytitle='Trigger Eff',trig='xe70,90,110')        
    ####
    ####
    ####DrawList(can,[xe110_u_tenac_eta25[6],xe110_u_bias_1TeV[6],xe110_u_bias_15TeV[6],xe110_u_bias_2TeV[6],xe110_u_bias_bothfwd[6]],['#mu |#Delta#eta_{jj}|>2.5','#mu m_{jj}>1 TeV','m_{jj}>1.5TeV','m_{jj}>2 TeV','both fwd'],trig+'mu_biasmjj_Eff',ytitle='Trigger Eff',trig=trig)
    ####DrawList(can,[xe110_u_bias_15TeV[2],xe110_u_bias_2TeV[2],xe110_u_bias_bothfwd[2],xe110_u_tenac_eta25[2],xe110_u_bias_1TeV[2]],['m_{jj}>1.5TeV','m_{jj}>2 TeV','both fwd','#mu |#Delta#eta_{jj}|>2.5','#mu m_{jj}>1 TeV'],trig+'mu_biasmjj_SF',ytitle='Trigger SF',trig=trig,input_err=xe110_u_detajj25_metLoose[10])            
    
    # Check
    lep='u'
    #trig='VBFTopo'
    trig='xe110XE70'
    #trig='xe110XE65'
    #fname='/tmp/v28Loose_metsf_VBFTopo'
    #fname='/tmp/v28Loose_metsf'
    #xe1108_u_tenac = DrawSF(can, trig, lep, mvar, fname)
    #
    #fname='/tmp/v27Loose_metsf'
    #trig='metsfxe100L150'
    #xe1107_u_tenac = DrawSF(can, trig, lep, mvar, fname, year=2017)
    #
    #fname='/tmp/v26Loose_metsf'
    #trig='xe110'
    #xe1106_u_tenac = DrawSF(can, trig, lep, mvar, fname, year=2016)

    #trig='xe110'
    #trig='xe110L155'
    #trig='VBFTopo'
    ##trig='VBFTopo'
    #fname ='v28Loose_metsf_reg' #v28Loose_metsf_VBFTopo.root
    ##Generic_u_tenac = DrawSF(can, trig, lep, mvar, fname)
    ##v28Loose_metsf_VBFMETUniq.root
    ##v28Loose_metsf_VBFTopo.root
    #trig='VBFTopo'
    ##trig='VBFTopo'
    #fname ='/tmp/v28Loose_metsf_METOnly_9070' #v28Loose_metsf_VBFTopo.root
    #XEOnly_u_tenac = DrawSF(can, trig, lep, mvar, fname)
    #fname ='/tmp/v28Loose_metsf_withORVBFTopo_9070' #v28Loose_metsf_VBFTopo.root    
    #fname ='v28Loose_metsf_withORVBFTopo_9070_tenac_xe90VBFVersion' #v28Loose_metsf_VBFTopo.root    
    #VBFTopo_u_tenac = DrawSF(can, trig, lep, mvar, fname)
    ##fname ='/tmp/v28Loose_metsf_METOnly_9070' #v28Loose_metsf_VBFTopo.root
    ##VBFTopoUniq_u_tenac = DrawSF(can, trig, lep, mvar, fname)        
    #
    #DrawList(can,[XEOnly_u_tenac[3],VBFTopo_u_tenac[3]],['#mu XE','#mu XEORVBFxe90'],'xeComparison_mu_SF_xe90', ytitle='Trigger Eff.',trig='xe,VBFOR')
    #
    #lep='e'
    #fname ='/tmp/v28Loose_metsf_METOnly_9070' #v28Loose_metsf_VBFTopo.root
    #XEOnly_u_tenac = DrawSF(can, trig, lep, mvar, fname)
    #fname ='/tmp/v28Loose_metsf_withORVBFTopo_9070' #v28Loose_metsf_VBFTopo.root    
    #VBFTopo_u_tenac = DrawSF(can, trig, lep, mvar, fname)
    #DrawList(can,[XEOnly_u_tenac[3],VBFTopo_u_tenac[3]],['e XE','e XEORVBFxe90'],'xeComparison_e_SF_xe90', ytitle='Trigger Eff.',trig='xe,VBFOR')    
