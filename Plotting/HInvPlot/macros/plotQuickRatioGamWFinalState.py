import ROOT
import math
from optparse import OptionParser

p = OptionParser(usage="usage: <path:ROOT file directory>", version="0.1")
p.add_option('--var',           type='string', default='jj_mass_variableBin,truth_jj_mass_variableBin,truth_jj_mass,truth_jj_deta,truth_jj_dphi,truth_j1_pt,truth_j2_pt,jj_deta,jj_dphi,met_tst_nolep_et', dest='var') #SherpaVTruthPt
p.add_option('--filename','-f', type='string', default='/tmp/v34ATest_v18.root', dest='filename')
p.add_option('--year',         type='int',    default=2019,          dest='year') #: 2016, 2017, 2018, 2019=all years
p.add_option('--wait',          action='store_true', default=False,   dest='wait')
#p.add_option('--filename','-f', type='string', default='pass_sr_hipt_1j_eu', dest='filename')
(options, args) = p.parse_args()
#-------------------------------------------------------------------------
def getATLASLabels(pad, x, y, text=None, selkey=None):

    l = ROOT.TLatex(x, y, 'ATLAS')
    l.SetNDC()
    l.SetTextFont(72)
    l.SetTextSize(0.055)
    l.SetTextAlign(11)
    l.SetTextColor(ROOT.kBlack)
    l.Draw()

    delx = 0.05*pad.GetWh()/(pad.GetWw())
    labs = [l]

    if True:
        p = ROOT.TLatex(x+0.12, y, ' Internal') #
        p.SetNDC()
        p.SetTextFont(42)
        p.SetTextSize(0.055)
        p.SetTextAlign(11)
        p.SetTextColor(ROOT.kBlack)
        p.Draw()
        labs += [p]
    if True:
        a = ROOT.TLatex(x, y-0.04, '#sqrt{s}=13 TeV, %.0f fb^{-1}' %(59000/1.0e3))
        if options.year==2016:
            a = ROOT.TLatex(x, y-0.04, '#sqrt{s}=13 TeV, %.0f fb^{-1}' %(36000/1.0e3))
        if options.year==2017:
            a = ROOT.TLatex(x, y-0.04, '#sqrt{s}=13 TeV, %.0f fb^{-1}' %(44000/1.0e3))
        if options.year==2019:
            a = ROOT.TLatex(x, y-0.04, '#sqrt{s}=13 TeV, %.0f fb^{-1}' %(139000/1.0e3))
        a.SetNDC()
        a.SetTextFont(42)
        a.SetTextSize(0.04)
        a.SetTextAlign(12)
        a.SetTextColor(ROOT.kBlack)
        a.Draw()
        labs += [a]
    if text!='':
        b = ROOT.TLatex(x, y-0.08, text)
        b.SetNDC()
        b.SetTextFont(42)
        b.SetTextSize(0.04)
        b.SetTextAlign(12)
        b.SetTextColor(ROOT.kBlack)
        b.Draw()
        labs += [b]

    return labs
#-----------------------------------------------------------------------------
# Load necessary shared libraries
#
def setPlotDefaults(root, options = None):

    #root.gROOT.SetStyle('Plain')

    root.gStyle.SetFillColor(10)
    root.gStyle.SetFrameFillColor(10)
    root.gStyle.SetCanvasColor(10)
    root.gStyle.SetPadColor(10)
    root.gStyle.SetTitleFillColor(0)
    root.gStyle.SetStatColor(10)

    root.gStyle.SetCanvasBorderMode(0)
    root.gStyle.SetFrameBorderMode(0)
    root.gStyle.SetPadBorderMode(0)
    root.gStyle.SetDrawBorder(0)
    root.gStyle.SetTitleBorderSize(0)

    root.gStyle.SetFuncWidth(2)
    root.gStyle.SetHistLineWidth(2)
    root.gStyle.SetFuncColor(2)

    root.gStyle.SetPadTopMargin(0.08)
    root.gStyle.SetPadBottomMargin(0.16)
    root.gStyle.SetPadLeftMargin(0.16)
    root.gStyle.SetPadRightMargin(0.12)

    # set axis ticks on top and right
    root.gStyle.SetPadTickX(1)
    root.gStyle.SetPadTickY(1)

    # Set the background color to white
    root.gStyle.SetFillColor(10)
    root.gStyle.SetFrameFillColor(10)
    root.gStyle.SetCanvasColor(10)
    root.gStyle.SetPadColor(10)
    root.gStyle.SetTitleFillColor(0)
    root.gStyle.SetStatColor(10)


    # Turn off all borders
    root.gStyle.SetCanvasBorderMode(0)
    root.gStyle.SetFrameBorderMode(0)
    root.gStyle.SetPadBorderMode(0)
    root.gStyle.SetDrawBorder(0)
    root.gStyle.SetTitleBorderSize(0)

    # Set the size of the default canvas
    root.gStyle.SetCanvasDefH(400)
    root.gStyle.SetCanvasDefW(650)
    #gStyle->SetCanvasDefX(10)
    #gStyle->SetCanvasDefY(10)

    # Set fonts
    font = 42
    #root.gStyle.SetLabelFont(font,'xyz')
    #root.gStyle.SetStatFont(font)
    #root.gStyle.SetTitleFont(font)
    #root.gStyle.SetTitleFont(font,'xyz')
    #root.gStyle.SetTextFont(font)
    #root.gStyle.SetTitleX(0.3)
    #root.gStyle.SetTitleW(0.4)

   # Set Line Widths
   #gStyle->SetFrameLineWidth(0)
   #root.gStyle.SetFuncWidth(2)
   #root.gStyle.SetHistLineWidth(2)
   #root.gStyle.SetFuncColor(2)
   #
   # Set tick marks and turn off grids
    root.gStyle.SetNdivisions(505,'xyz')
   #
   # Set Data/Stat/... and other options
   #root.gStyle.SetOptDate(0)
   #root.gStyle.SetDateX(0.1)
   #root.gStyle.SetDateY(0.1)
   #gStyle->SetOptFile(0)
   ##root.gStyle.SetOptStat(1110)
    root.gStyle.SetOptStat(1111)
    #root.gStyle.SetOptFit(111)
    root.gStyle.SetStatFormat('4.3f')
    root.gStyle.SetFitFormat('4.3f')
   #gStyle->SetStatTextColor(1)
   #gStyle->SetStatColor(1)
   #gStyle->SetOptFit(1)
   #gStyle->SetStatH(0.20)
   #gStyle->SetStatStyle(0)
   #gStyle->SetStatW(0.30)
   #gStyle -SetStatLineColor(0)
   #root.gStyle.SetStatX(0.919)
   #root.gStyle.SetStatY(0.919)
   #root.gStyle.SetOptTitle(0)
   #gStyle->SetStatStyle(0000)    # transparent mode of Stats PaveLabel
   #root.gStyle.SetStatBorderSize(0)
   #
    #root.gStyle.SetLabelSize(0.065,'xyz')
    #gStyle -> SetLabelOffset(0.005,'xyz')
    #root.gStyle.SetTitleY(.5)
    root.gStyle.SetTitleOffset(1.0,'xz')
    root.gStyle.SetTitleOffset(1.1,'y')
    root.gStyle.SetTitleSize(0.065, 'xyz')
    root.gStyle.SetLabelSize(0.065, 'xyz')
    #root.gStyle.SetTextAlign(22)
    root.gStyle.SetTextSize(0.1)
   #
   ##root.gStyle.SetPaperSize(root.TStyle.kA4)
    root.gStyle.SetPalette(1)
   #
   ##root.gStyle.SetHistMinimumZero(True)

    root.gROOT.ForceStyle()
#-----------------------------------------
def Format(h):

    h.SetLineColor(1)
    h.SetMarkerColor(1)
    h.SetTitle('Projection of 2D Efficiency')

#-----------------------------------------
def PlotError(h):

    hnew = h.Clone()
    for i in range(0,h.GetNbinsX()+1):
        valb = h.GetBinContent(i)
        errb = h.GetBinError(i)

        newval=0.0
        if valb!=0.0:
            newval = errb/abs(valb)

        hnew.SetBinContent(i,newval)
        hnew.SetBinError(i,0.0)
    return hnew
#-----------------------------------------
def Style():
    ROOT.gROOT.LoadMacro('/Users/schae/testarea/SUSY/JetUncertainties/testingMacros/atlasstyle/AtlasStyle.C')
    ROOT.gROOT.LoadMacro('/Users/schae/testarea/SUSY/JetUncertainties/testingMacros/atlasstyle/AtlasUtils.C')
    ROOT.SetAtlasStyle()

#-----------------------------------------
def GetHistsRatio(hname1,f1,hpath1all=[''],hpath2all=['']):

    h1=None
    hname=''
    for hpath1 in hpath1all:
        hname=hpath1+hname1
        print hname
        h1b = f1.Get(hname)
        if h1:
            h1.Add(h1b)
        else:
            h1 = h1b.Clone()
    h2=None
    hnamev2=''
    for hpath2 in hpath2all:
        hnamev2=hpath2+hname1
        print hnamev2
        h2b = f1.Get(hnamev2)
        if h2:
            h2.Add(h2b)
        else:
            h2 = h2b.Clone()
    rebin=2
    if hname=='ph_pt_lead' or hname1=="phPt":
        h1.Rebin(5)
        h2.Rebin(5)
        h1.GetXaxis().SetRangeUser(5.0,1000.0)
        h2.GetXaxis().SetRangeUser(5.0,1000.0)
    if hname1=='jj_mass':
        h1.Rebin(rebin)
        h2.Rebin(rebin)
    if  hname=='truth_jj_mass':
        h1.Rebin(10)
        h2.Rebin(10)
    if hname1=='jj_deta':
        h1.Rebin(rebin)
        h2.Rebin(rebin)
    if hname1=='met_tst_et':
        h1.Rebin(rebin)
        h2.Rebin(rebin)
    if hname1=='jj_dphi':
        h1.Rebin(rebin)
        h2.Rebin(rebin)
    if hname1=='met_tst_nolep_et':
        h1.Rebin(5)
        h2.Rebin(5)
    hratio = h2.Clone()
    intden = h2.Integral()
    if intden>0.0:
        hratio.Scale(h1.Integral()/intden)
    hratio.Divide(h1)
    return hratio

def GetName(hpath1):

    num_name = '#gamma+Z#rightarrow#nu#nu'
    comp1='znn'
    if hpath1.count('zcr') or hpath1.count('zgamcr'):
        num_name = '#gamma+Z#rightarrow ll'
        comp1='zll'
        if hpath1.count('_uu_'):
            num_name = '#gammaZ#rightarrow #mu#mu'
            comp1='zmm'
        if hpath1.count('_ee_'):
            num_name = '#gamma+Z#rightarrow ee'
            comp1='zee'
    if hpath1.count('_sr_') or hpath1.count('_gamsr_'):
        num_name = '#gamma+Z#rightarrow#nu#nu'
        if hpath1.count('_wewk') or hpath1.count('_wqcd') or hpath1.count('_wgam'):
            num_name = '#gamma+W#rightarrowe_{lost}#nu'
    if hpath1.count('_wcr_') or hpath1.count('_gamwcr_'):
        num_name = '#gamma+W#rightarrow e#nu'
        comp1='wle'
        if hpath1.count('_u_'):
            num_name = '#gamma+W#rightarrow #mu#nu'
            comp1='wmn'
        if hpath1.count('_e_'):
            num_name = '#gamma+W#rightarrow e#nu'
            comp1='wen'
    if hpath1.count('higgs'):
        num_name = 'Signal VBF+MET+#gamma'
    return num_name,comp1

def Draw(hname1,f1les=[],can=None,GetError=True, hpath1all=[''],hpath2all=[''],hpath3all=[],extra=''):
    can.Clear()

    f1=f1les[0]
    f1up=None
    f1dw=None
    if len(f1les)>1:
        f1up=f1les[1]
        f1dw=f1les[2]
    h1=None
    hname=''
    for hpath1 in hpath1all:
        hname=hpath1+hname1
        print hname
        h1b = f1.Get(hname)
        if not h1b:
            print 'histogram above does not exist'
        #print hname,h1b.Integral()
        if h1:
            h1.Add(h1b)
        else:
            h1 = h1b.Clone()
    #print 'Total: ',hname,h1.Integral()
    h2=None
    hnamev2=''
    for hpath2 in hpath2all:
        hnamev2=hpath2+hname1
        print hnamev2
        h2b = f1up.Get(hnamev2)
        #print hnamev2,h2b.Integral()
        if h2:
            h2.Add(h2b)
        else:
            h2 = h2b.Clone()
    #print 'Total: ',hnamev2,h2.Integral()
    h3=None
    hnamev3=''
    for hpath3 in hpath3all:
        hnamev3=hpath3+hname1
        print hnamev3
        h3b = f1dw.Get(hnamev3)
        #print hnamev3,h3b.Integral()
        if h3:
            h3.Add(h3b)
        else:
            h3 = h3b.Clone()
    #print 'Total: ',hnamev3,h3.Integral()
    
    h1.SetStats(0)
    h2.SetStats(0)
    h1.SetLineColor(1)
    h1.SetMarkerColor(1)
    h2.SetLineColor(2)
    h2.SetMarkerColor(2)
    h1.SetMarkerSize(0.5)
    h2.SetMarkerSize(0.5)
    hpath3=''
    if h3:
        h3.SetLineColor(3)
        h3.SetMarkerColor(3)
        h3.SetStats(0)
        h3.SetMarkerSize(0.5)
        hpath3=hpath3all[0]
        
    hpath1=hpath1all[0]
    hpath2=hpath2all[0]

    type_sample='QCD '
    type_sample_out='qcd'
    if hpath1.count('_zgam') or hpath1.count('_wgam'):
        type_sample='QCD '
    if hpath1.count('_zgamewk') or hpath1.count('_wgamewk'):
        type_sample='EWK '
        type_sample_out='ewk'
    if len(hpath1all)>1:
        type_sample='QCD+EWK '
        type_sample_out='qcdewk'
    num_name = 'Z#rightarrow#nu#nu'
    den_name = 'Z#rightarrow ll'
    comp1='znn'
    comp2='znn'

    den_name,comp2=GetName(hpath2)
    den2_name,comp3=GetName(hpath3)
    num_name,comp1=GetName(hpath1)
    
    # pads
    pad1 = ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0);
    pad1.SetBottomMargin(0); # Upper and lower plot are joined
    #pad1.SetGridx();         # Vertical grid
    pad1.Draw();             # Draw the upper pad: pad1
    pad1.cd();               # pad1 becomes the current pad
    extra_text_save='_varComp'
    extra_text='VBF H125+#gamma'
    rebin=2
    if hname.count('_hggf'):
        extra_text='ggF H125'
        extra_text_save='_ggf'
        rebin=5
    elif hname.count('_hvh'):
        extra_text='VH H125'
        extra_text_save='_hvh'
        rebin=5

    if hname.count('ph_pt'):
        h1.GetXaxis().SetTitle('Photon p_{T} [GeV]')
    if hname=='ph_pt_lead' or hname1=="phPt":
        h1.Rebin(2)
        h2.Rebin(2)
        if h3: h3.Rebin(2)
        h1.GetXaxis().SetRangeUser(5.0,1000.0)
        h2.GetXaxis().SetRangeUser(5.0,1000.0)
    if hname1=='jj_mass':
        h1.Rebin(rebin)
        h2.Rebin(rebin)
        if h3: h3.Rebin(rebin)        
    if  hname=='truth_jj_mass':
        h1.Rebin(10)
        h2.Rebin(10)
        if h3: h3.Rebin(10)        
    if hname1=='jj_deta':
        h1.Rebin(rebin)
        h2.Rebin(rebin)
        if h3: h3.Rebin(rebin)        
    if hname1=='met_tst_et':
        h1.Rebin(rebin)
        h2.Rebin(rebin)
        if h3: h3.Rebin(rebin)        
    if hname1=='jj_dphi':
        h1.Rebin(rebin)
        h2.Rebin(rebin)
        if h3: h3.Rebin(rebin)        
    if hname1=='met_tst_nolep_et':
        h1.Rebin(5)
        h2.Rebin(5)
        if h3: h3.Rebin(5)
    if GetError:
        h1.GetYaxis().SetTitle('Relative Error')
    else:
        h1.GetYaxis().SetTitle('Events')

    if GetError:
        h1 = PlotError(h1)
        h2 = PlotError(h2)
        if h3: h3 = PlotError(h3)
            
    h1.GetYaxis().SetRangeUser(0.01,h1.GetMaximum()*1.5)
    h1.Draw()
    h1.GetYaxis().SetRangeUser(0.001,h1.GetMaximum()*1.5)    
    h2.Draw('same')
    if h3:
        h3.Draw('same')
        kval = h1.KolmogorovTest(h3, '')
        print ' ks: ',kval
        ks_text3 = ROOT.TLatex(0.3, 0.88, 'KS: %.2f' %kval)
        ks_text3.SetNDC()
        ks_text3.SetTextSize(0.055)
        ks_text3.SetTextAlign(11)
        ks_text3.SetTextColor(3)
        ks_text3.Draw()
    chi2 = h1.Chi2Test      (h2, 'UW CHI2')
    kval = h1.KolmogorovTest(h2, '')
    print 'chi2: ',chi2,' ks: ',kval
    ks_text2 = ROOT.TLatex(0.3, 0.95, 'KS: %.2f' %kval)
    ks_text2.SetNDC()
    ks_text2.SetTextSize(0.055)
    ks_text2.SetTextAlign(11)
    ks_text2.SetTextColor(ROOT.kRed)
    ks_text2.Draw()

    e=ROOT.Double(0.0)
    print 'Integral old: ',h1.IntegralAndError(0,1001,e),'+/-',e
    print 'Integral new: ',h2.IntegralAndError(0,1001,e),'+/-',e
    if h3:
        print 'Integral new: ',h3.IntegralAndError(0,1001,e),'+/-',e
        
    leg = ROOT.TLegend(0.6,0.5,0.92,0.76)
    leg.SetBorderSize(0)
    leg.SetFillColor(0)
    leg.AddEntry(h1,'#gamma+W#rightarrowe#nu')
    leg.AddEntry(h2,'#gamma+W#rightarrow#mu#nu')
    if h3:
        leg.AddEntry(h3,'#gamma+W#rightarrow#tau#nu')        #type_sample+
    leg.Draw()

    texts = getATLASLabels(can, 0.6, 0.85, extra_text)
    for text in texts:
        text.Draw()

    can.cd();          # Go back to the main canvas before defining pad2
    pad2 = ROOT.TPad("pad2", "pad2", 0, 0.03, 1, 0.3);
    pad2.SetTopMargin(0);
    pad2.SetBottomMargin(0.3);
    pad2.SetGridy(); # vertical grid
    pad2.Draw();
    pad2.cd();       # pad2 becomes the current pad

    hratio = h2.Clone()
    intden = h2.Integral()
    if intden>0.0:
        hratio.Scale(h1.Integral()/intden)
    hratio.Divide(h1)
    hratio.GetYaxis().SetRangeUser(0,2.0)
    pad1.SetLogy(0)
    pad2.SetLogy(0)
    pad1.SetLogx(0)
    pad2.SetLogx(0)
    hratio2 = None
    if h3:
        hratio2 = h3.Clone()
        intden2 = h3.Integral()
        if intden2>0.0:
            hratio2.Scale(h1.Integral()/intden2)
        hratio2.Divide(h1)
    hratioUp=None
    hratioDw=None
    hsysr = hratio.Clone()
    hsys=ROOT.TGraphAsymmErrors(hsysr)
    for i in range(0,hsysr.GetNbinsX()+1):
        hsys.SetPointEXhigh(i-1,hsysr.GetXaxis().GetBinWidth(i)/2.0)
        hsys.SetPointEXlow(i-1,hsysr.GetXaxis().GetBinWidth(i)/2.0)
        hsys.SetFillColor(1)
        hsys.SetLineColor(1)
        hsys.SetFillStyle(3018)
        hsys.SetLineWidth(0)
        hsys.SetMarkerSize(0)
        hsys.SetMarkerColor(1)
    if hname=='ph_pt_lead' or hname1=="phPt":
        hratio.GetXaxis().SetTitle('Lead Photon p_{T} [GeV]')
        h1.GetXaxis().SetRangeUser(11.0,1000.0)
        h2.GetXaxis().SetRangeUser(11.0,1000.0)
        hratio.GetXaxis().SetRangeUser(11.0,1000.0)
        #if not GetError:
        #    pad1.SetLogy(1)
            #pad2.SetLogy(1)
            #pad1.SetLogx(1)
            #pad2.SetLogx(1)
    elif hname=='elneg_pt':
        hratio.GetXaxis().SetTitle('Electron p_{T} [GeV]')
        if not GetError:
            pad1.SetLogy(1)
            #pad2.SetLogy(1)
            pad1.SetLogx(1)
            pad2.SetLogx(1)
    elif hname=='elpos_pt':
        hratio.GetXaxis().SetTitle('Electron p_{T} [GeV]')
        if not GetError:
            pad1.SetLogy(1)
            #pad2.SetLogy(1)
            pad1.SetLogx(1)
            pad2.SetLogx(1)

    elif  hname=='ph_pt':
        hratio.GetXaxis().SetTitle('Photon p_{T} [GeV]')
    elif  hname=='ph_eta':
        hratio.GetXaxis().SetTitle('Photon #eta')
    elif  hname=='ph_eta_lead':
        hratio.GetXaxis().SetTitle('Lead Photon #eta')
    elif  hname=='boson_eta':
        hratio.GetXaxis().SetTitle('Boson #eta')
    elif  hname=='boson_pt':
        hratio.GetXaxis().SetTitle('Boson p_{T} [GeV]')
    elif  hname=='njet' or hname.count('n_jet'):
        hratio.GetXaxis().SetTitle('N_{jet}')
    elif  hname=='dr_ph_el':
        hratio.GetXaxis().SetTitle('#DeltaR(#gamma,e)')
    elif  hname=='dr_ph_j':
        hratio.GetXaxis().SetTitle('#DeltaR(#gamma,jet)')
    elif  hname=='dr_ph_boson':
        hratio.GetXaxis().SetTitle('#DeltaR(#gamma,boson)')
    elif  hname.count('truth_jj_mass'):
        hratio.GetXaxis().SetTitle('Truth m_{jj} [GeV]')
    elif  hname.count('jj_mass'):
        hratio.GetXaxis().SetTitle('m_{jj} [GeV]')
    elif  hname.count('truth_jj_deta'):
        hratio.GetXaxis().SetTitle('Truth #Delta#eta_{jj}')
    elif  hname.count('truth_jj_dphi'):
        hratio.GetXaxis().SetTitle('Truth #Delta#phi_{jj}')
    elif  hname.count('truth_j1_pt'):
        hratio.GetXaxis().SetTitle('Truth Lead Jet p_{T} [GeV]')
    elif  hname.count('truth_j2_pt'):
        hratio.GetXaxis().SetTitle('Truth Sub-Lead Jet p_{T} [GeV]')
    elif  hname.count('SherpaVTruthPt'):
        hratio.GetXaxis().SetTitle('Truth p_{T}^{V} [GeV]')
    elif  hname.count('jj_deta'):
        hratio.GetXaxis().SetTitle('#Delta#eta_{jj}')
    elif  hname.count('jj_dphi'):
        hratio.GetXaxis().SetTitle('#Delta#phi_{jj}')
    elif  hname.count('met_tst_et'):
        hratio.GetXaxis().SetTitle('MET [GeV]')
    elif  hname.count('met_truth_et'):
        hratio.GetXaxis().SetTitle('Truth MET [GeV]')
    elif  hname.count('j3Pt'):
        hratio.GetXaxis().SetTitle('3rd jet p_{T} [GeV]')
    elif  hname.count('met_tst_nolep_et'):
        hratio.GetXaxis().SetTitle('MET (no leptons) [GeV]')

    hratio.GetYaxis().SetTitle(den_name +' / '+ num_name)
    if hratio2:
        hratio.GetYaxis().SetTitle('sample / '+ num_name)        
    hratio.GetYaxis().SetRangeUser(0.0,2.4999)
    hratio.GetYaxis().SetNdivisions(505);
    hratio.GetYaxis().SetTitleSize(15);
    hratio.GetYaxis().SetTitleFont(43);
    hratio.GetYaxis().SetTitleOffset(1.55);
    hratio.GetYaxis().SetLabelFont(43);
    hratio.GetYaxis().SetLabelSize(15);
    hratio.GetXaxis().SetTitleSize(20);
    hratio.GetXaxis().SetTitleFont(43);
    hratio.GetXaxis().SetTitleOffset(4.);
    hratio.GetXaxis().SetLabelFont(43); # Absolute font size in pixel (precision 3)
    hratio.GetXaxis().SetLabelSize(15);
    hratio.Draw()
    if hratio2:
        hratio2.Draw('same')
        
    can.Update()
    if options.wait:
        can.WaitPrimitive()
    extra_text_save+=extra
    if GetError:
        can.SaveAs(hname1+'_'+comp1+'_'+comp2+'_'+type_sample_out+extra_text_save+'_err.pdf')
    else:
        can.SaveAs(hname1+'_'+comp1+'_'+comp2+'_'+type_sample_out+extra_text_save+'.pdf')

def Fit(_suffix=''):

    can=ROOT.TCanvas('can',"can",600,600)
    Style();
    f1 = ROOT.TFile.Open('/tmp/v41Amergept15bWenu.root')
    f1up = ROOT.TFile.Open('/tmp/v41Amergept15bWmnu.root')
    f1dw = ROOT.TFile.Open('/tmp/v41Amergept15bWtnu.root')


    h1_norm=1.0 #36.100
    h2_norm=1.0 #36.100 #hggf, hvh, hvbf
    hnames=['met_tst_et','jj_mass','jj_deta','jj_dphi','n_jet','j3Pt','met_truth_et','jj_mass','jj_deta','met_tst_et','jj_dphi']
    hnames = options.var.split(',')

    #path1=['pass_zcr_allmjj_ee_Nominal/plotEvent_zqcd/']
    #path2=['pass_zcr_allmjj_uu_Nominal/plotEvent_zqcd/']
    #for hname in hnames:
    #    Draw(hname,[f1,f1up,f1dw],can,GetError=False, hpath1all=path1,hpath2all=path2)
    #sys.exit(0)
    path1=['pass_gamwcr_allmjj_l_Nominal/plotEvent_wgam/','pass_gamwcr_allmjj_l_Nominal/plotEvent_wgamewk/']
    path2=['pass_gamwcr_allmjj_l_Nominal/plotEvent_wgam/','pass_gamwcr_allmjj_l_Nominal/plotEvent_wgamewk/']
    path3 = ['pass_gamwcr_allmjj_l_Nominal/plotEvent_wgam/','pass_gamwcr_allmjj_l_Nominal/plotEvent_wgamewk/']
    for hname in hnames:
        Draw(hname,[f1,f1up,f1dw],can,GetError=False, hpath1all=path1,hpath2all=path2,hpath3all=path3,extra='_WFinalState')

    # SR
    path1=['pass_gamsr_allmjj_nn_Nominal/plotEvent_wgam/','pass_gamsr_allmjj_nn_Nominal/plotEvent_wgamewk/']
    path2=['pass_gamsr_allmjj_nn_Nominal/plotEvent_wgam/','pass_gamsr_allmjj_nn_Nominal/plotEvent_wgamewk/']
    path3 = ['pass_gamsr_allmjj_nn_Nominal/plotEvent_wgam/','pass_gamsr_allmjj_nn_Nominal/plotEvent_wgamewk/']
    for hname in hnames:
        Draw(hname,[f1,f1up,f1dw],can,GetError=False, hpath1all=path1,hpath2all=path2,hpath3all=path3,extra='_WFinalState')
setPlotDefaults(ROOT)
Fit('90V')
