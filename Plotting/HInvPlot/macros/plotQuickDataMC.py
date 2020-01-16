import ROOT
import sys
from optparse import OptionParser

p = OptionParser(usage="usage: <path:ROOT file directory>", version="0.1")
p.add_option('--var',           type='string', default='n_jet,met_cst_jet,jj_mass_variableBin,jj_deta,jj_dphi,met_tst_nolep_et,mll', dest='var') #SherpaVTruthPt
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

def GetHist(hname1, hpath, f1,  can, sigsamples, doData=False):
    h1=None
    for hsamp in sigsamples:
        hname=hpath+hsamp+'/'+hname1
        print hname
        h1b = f1.Get(hname)
        #print hsamp,' ',h1b.Integral()
        if h1:
            if doData:
                h1.Add(h1b,-1.0)
            else:
                h1.Add(h1b)
        else:
            h1 = h1b.Clone()

    #print 'Total: ',h1.Integral()
    return h1.Clone()
    
def Draw(can, hname, bkgsub1hist, bkgsub2hist,  sig1hist, sig2hist, hpath1, hpath2, dataMinBkg=True):
    
    can.Clear()
    hname1=hname
    h1 = bkgsub1hist
    h2 = bkgsub2hist
    h1.SetStats(0)
    h2.SetStats(0)
    h1.SetLineColor(1)
    h1.SetMarkerColor(1)
    h2.SetLineColor(2)
    h2.SetMarkerColor(2)
    h1.SetMarkerSize(0.5)
    h2.SetMarkerSize(0.5)
    h3 = sig1hist.Clone()
    h4 = sig2hist.Clone()
    histos = [h1,h2,h3,h4]
    ncolor=1
    for h in histos:
        h.SetMarkerSize(0.5)
        h.SetStats(0)
        h.SetLineColor(ncolor)
        h.SetMarkerColor(ncolor)
        ncolor+=1
    type_sample=''
    type_sample_out='dataMinusBkg'
    #if hpath1.count('_zqcd') or hpath1.count('_wqcd'):
    #    type_sample='QCD '
    #if hpath1.count('_zewk') or hpath1.count('_wewk'):
    #    type_sample='EWK '
    #    type_sample_out='ewk'
    #if len(hpath1all)>1:
    #    type_sample='QCD+EWK '
    #    type_sample_out='qcdewk'
    num_name = 'Z#rightarrow#nu#nu'
    den_name = 'Z#rightarrow ll'
    comp1='znn'
    comp2='znn'
    if hpath1.count('zcr'):
        num_name = 'Z#rightarrow ll'
        comp1='zll'
        if hpath1.count('_uu_'):
            num_name = 'Z#rightarrow #mu#mu'
            comp1='zmm'
        if hpath1.count('_ee_'):
            num_name = 'Z#rightarrow ee'
            comp1='zee'
    if hpath1.count('_sr_'):
        num_name = 'Z#rightarrow#nu#nu'
    if hpath1.count('_wcr_'):
        num_name = 'W#rightarrow l#nu'
        comp1='wle'        
        if hpath1.count('_u_'):
            num_name = 'W#rightarrow #mu#nu'
            comp1='wmn'
        if hpath1.count('_e_'):
            num_name = 'W#rightarrow e#nu'
            comp1='wen'            
    if hpath2.count('zcr'):
        den_name = 'Z#rightarrow ll'
        comp2='zll'
        if hpath2.count('_uu_'):
            den_name = 'Z#rightarrow #mu#mu'
            comp2='zmm'
        if hpath2.count('_ee_'):
            den_name = 'Z#rightarrow ee'
            comp2='zee'
    if hpath2.count('_sr_'):
        den_name = 'Z#rightarrow#nu#nu'
    if hpath2.count('_wcr_'):
        den_name = 'W#rightarrow l#nu'
        comp2='wln'
        if hpath2.count('_u_'):
            den_name = 'W#rightarrow #mu#nu'
            comp2='wmn'
        if hpath2.count('_e_'):
            den_name = 'W#rightarrow e#nu'
            comp2='wen'
    # pads
    pad1 = ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0);
    pad1.SetBottomMargin(0); # Upper and lower plot are joined
    #pad1.SetGridx();         # Vertical grid
    pad1.Draw();             # Draw the upper pad: pad1
    pad1.cd();               # pad1 becomes the current pad
    extra_text_save='_regComp'
    extra_text='VBF H125'
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
    if hname=='mll':
        for h in histos:
            h.Rebin(5)
    if hname1=='jj_mass' or hname1=='jj_deta':
        for h in histos:
            h.Rebin(rebin)
    if  hname.count('truth_jj_mass'):
        for h in histos:
            h.Rebin(10)
    if hname1=='met_cst_jet':
        for h in histos:
            h.Rebin(5)
    if hname1=='met_tst_et':
        for h in histos:
            h.Rebin(rebin) 
    if hname1=='jj_dphi':
        for h in histos:
            h.Rebin(rebin)
    if hname1=='met_tst_nolep_et':
        for h in histos:
            h.Rebin(5)
    if dataMinBkg:
        h1.GetYaxis().SetTitle('Normalized (Data - Bkg)')
    else:
        h1.GetYaxis().SetTitle('Normalized Events')

    #h1.Draw()
    #h2.Draw('same')
    h1.GetYaxis().SetRangeUser(0.001,h1.GetMaximum()*1.7)
    h1.DrawNormalized()
    h2.DrawNormalized('same')
    

    e=ROOT.Double(0.0)
    print 'Integral old: ',h1.IntegralAndError(0,1001,e),'+/-',e
    print 'Integral new: ',h2.IntegralAndError(0,1001,e),'+/-',e
    
    leg = ROOT.TLegend(0.6,0.5,0.92,0.75)
    leg.SetBorderSize(0)
    leg.SetFillColor(0)
    leg.AddEntry(h1,type_sample+num_name)
    leg.AddEntry(h2,type_sample+den_name)

    leg.Draw()
        
    texts = getATLASLabels(can, 0.6, 0.85, extra_text)
    for text in texts:
        text.Draw()

    chi2 = h1.Chi2Test      (h2, 'UW CHI2')
    kval = h1.KolmogorovTest(h2, '')
    ks_text = ROOT.TLatex(0.3, 0.95, 'KS: %.2f' %kval)
    ks_text.SetNDC()
    ks_text.SetTextSize(0.055)
    ks_text.SetTextAlign(11)
    ks_text.SetTextColor(ROOT.kBlack)
    ks_text.Draw()

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

    hratioMC = h4.Clone()
    intden = h4.Integral()
    if intden>0.0:
        hratioMC.Scale(h3.Integral()/intden)    
    hratioMC.Divide(h3)
    
    hratio.GetYaxis().SetRangeUser(0,2.0)
    hratioMC.GetYaxis().SetRangeUser(0,2.0)
    pad1.SetLogy(0)
    pad2.SetLogy(0)
    pad1.SetLogx(0)
    pad2.SetLogx(0)
    if hname=='ph_pt_lead':
        hratio.GetXaxis().SetTitle('Lead Photon p_{T} [GeV]')
        h1.GetXaxis().SetRangeUser(11.0,1000.0)
        h2.GetXaxis().SetRangeUser(11.0,1000.0)
        hratio.GetXaxis().SetRangeUser(11.0,1000.0) 
        if not GetError:
            pad1.SetLogy(1)
            #pad2.SetLogy(1)
            pad1.SetLogx(1)
            pad2.SetLogx(1)
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
        hratio.GetXaxis().SetTitle('#Delta#eta_{jj}')
    elif  hname.count('truth_jj_dphi'):
        hratio.GetXaxis().SetTitle('#Delta#phi_{jj}')
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
    elif  hname.count('mll'):
        hratio.GetXaxis().SetTitle('m_{ll} [GeV]')
    elif  hname.count('n_jet'):
        hratio.GetXaxis().SetTitle('N_{jet}')
    elif  hname.count('met_cst_jet'):
        hratio.GetXaxis().SetTitle('E_{T,miss}^{jet,no-jvt} [GeV]')
       
    hratio.GetYaxis().SetTitle(num_name+' / '+den_name)
    hratio.GetYaxis().SetRangeUser(0.5,1.5)       
    hratio.GetYaxis().SetNdivisions(505);
    hratio.GetYaxis().SetTitleSize(20);
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
    hratioMC.Draw('same')
    leg1 = ROOT.TLegend(0.7,0.8,0.92,0.99)
    leg1.SetBorderSize(0)
    leg1.SetFillColor(0)
    leg1.AddEntry(hratio,'Data - bkg')
    leg1.AddEntry(hratioMC,'MC ratio')
    leg1.Draw()

    chi2 = hratio.Chi2Test      (hratioMC, 'UW CHI2')
    kval = hratio.KolmogorovTest(hratioMC, '')
    print 'chi2: ',chi2,' KS: ',kval    
    ks_text2 = ROOT.TLatex(0.3, 0.92, 'KS MC and data-bkg: %.2f' %kval)
    ks_text2.SetNDC()
    ks_text2.SetTextSize(0.095)
    ks_text2.SetTextAlign(11)
    ks_text2.SetTextColor(ROOT.kBlack)
    ks_text2.Draw()
    
    can.Update()
    if options.wait:
        can.WaitPrimitive()
    #if GetError:
    #    can.SaveAs(hname1+'_'+comp1+'_'+comp2+'_'+type_sample_out+extra_text_save+'_err.pdf')
    #else:
    can.SaveAs(hname1+'_'+comp1+'_'+comp2+'_'+type_sample_out+extra_text_save+'.pdf')
    
def Fit(_suffix=''):

    can=ROOT.TCanvas('can',"can",600,600)
    Style();
    f1 = ROOT.TFile.Open(options.filename)

    h1_norm=1.0 #36.100
    h2_norm=1.0 #36.100 #hggf, hvh, hvbf
    hnames=['met_tst_et','jj_mass','jj_deta','jj_dphi','n_jet','j3Pt','met_truth_et','jj_mass','jj_deta','met_tst_et','jj_dphi']
    hnames = options.var.split(',')

    sigsamples1 = ['zqcd','zewk']
    bkgsamples1 = ['data','wewk','wqcd','tall']#,'dqcd']
    path1='pass_zcr_allmjj_ee_Nominal/plotEvent_'
    path2='pass_zcr_allmjj_uu_Nominal/plotEvent_'
    for hname in hnames:
        sig1hist = GetHist(hname, path1, f1, can, sigsamples1, doData=False)
        bkgsub1hist = GetHist(hname, path1, f1, can, bkgsamples1, doData=True)
        sig2hist = GetHist(hname, path2, f1, can, sigsamples1, doData=False)
        bkgsub2hist = GetHist(hname, path2, f1, can, bkgsamples1, doData=True)

        Draw(can, hname, bkgsub1hist,bkgsub2hist, sig1hist, sig2hist, path1, path2, dataMinBkg=True)
        #Draw(can, hname,sig1hist,sig2hist, path1,path2)        

    sigsamples1 = ['wqcd','wewk']
    bkgsamples1 = ['data','zewk','zqcd','tall']#,'dqcd']
    path1='pass_wcr_allmjj_e_Nominal/plotEvent_'
    path2='pass_wcr_allmjj_u_Nominal/plotEvent_'
    for hname in hnames:
        sig1hist = GetHist(hname, path1, f1, can, sigsamples1, doData=False)
        bkgsub1hist = GetHist(hname, path1, f1, can, bkgsamples1, doData=True)
        sig2hist = GetHist(hname, path2, f1, can, sigsamples1, doData=False)
        bkgsub2hist = GetHist(hname, path2, f1, can, bkgsamples1, doData=True)
        
        Draw(can, hname,bkgsub1hist,bkgsub2hist, sig1hist, sig2hist, path1, path2, dataMinBkg=True)
        #Draw(can, hname,sig1hist,sig2hist, path1,path2)    
    sys.exit(0)

    

setPlotDefaults(ROOT)
Fit('90V')
