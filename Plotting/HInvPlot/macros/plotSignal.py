import ROOT
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
        a = ROOT.TLatex(x, y-0.04, '#sqrt{s}=13 TeV, %.1f fb^{-1}' %(59000/1.0e3))
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

def Draw(hname1,f1,f2,can,h1_norm,h2_norm,GetError=True, hpath=''):
    can.Clear()
   
    hname=hpath+hname1
    hnamev2=hname
    hnamev3=hname
    hnamev4=hname
    if True:
        hnamev2=hpath.replace('_hvbf','_hvbf500')+hname1
        hnamev3=hpath.replace('_hvbf','_hvbf1k')+hname1
        hnamev4=hpath.replace('_hvbf','_hvbf3k')+hname1
    print hname
    print hnamev2
    h1 = f1.Get(hname)
    h2 = f2.Get(hnamev2)
    h3 = f2.Get(hnamev3)
    h4 = f2.Get(hnamev4)
    h1.Scale(h1_norm)
    h2.Scale(h2_norm)
    h1.SetStats(0)
    h2.SetStats(0)
    h3.SetStats(0)
    h4.SetStats(0)
    h1.SetLineColor(1)
    h1.SetMarkerColor(1)
    h2.SetLineColor(2)
    h2.SetMarkerColor(2)
    h1.SetMarkerSize(0.5)
    h2.SetMarkerSize(0.5)
    h3.SetLineColor(3)
    h3.SetMarkerColor(3)
    h4.SetLineColor(4)
    h4.SetMarkerColor(4)    
    h3.SetMarkerSize(0.5)
    h4.SetMarkerSize(0.5)    

    # pads
    pad1 = ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0);
    pad1.SetBottomMargin(0); # Upper and lower plot are joined
    #pad1.SetGridx();         # Vertical grid
    pad1.Draw();             # Draw the upper pad: pad1
    pad1.cd();               # pad1 becomes the current pad
    extra_text_save='_vbfHighMass'
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
    if hname=='ph_pt_lead':
        h1.Rebin(5)
        h2.Rebin(5)
        h1.GetXaxis().SetRangeUser(5.0,1000.0)
        h2.GetXaxis().SetRangeUser(5.0,1000.0)
    if hname1=='jj_mass':
        h1.Rebin(rebin)
        h2.Rebin(rebin)
        h4.Rebin(rebin)
        h3.Rebin(rebin)
    if hname1=='jj_deta':
        h1.Rebin(rebin)
        h2.Rebin(rebin)
        h3.Rebin(rebin)
        h4.Rebin(rebin)
    if hname1=='met_tst_et':
        h1.Rebin(rebin)
        h2.Rebin(rebin) 
        h3.Rebin(rebin) 
        h4.Rebin(rebin) 
    if hname1=='jj_dphi':
        h1.Rebin(rebin)
        h2.Rebin(rebin) 
        h3.Rebin(rebin) 
        h4.Rebin(rebin) 
    if GetError:
        h1.GetYaxis().SetTitle('Relative Error')        
    else:
        h1.GetYaxis().SetTitle('Events')


    if GetError:
        h1 = PlotError(h1)
        h2 = PlotError(h2)
    h1.Draw()
    h2.Draw('same')
    h3.Draw('same')
    h4.Draw('same')

    e=ROOT.Double(0.0)
    print 'Integral old: ',h1.IntegralAndError(0,1001,e),'+/-',e
    print 'Integral new: ',h2.IntegralAndError(0,1001,e),'+/-',e
    
    leg = ROOT.TLegend(0.4,0.5,0.8,0.8)
    leg.SetBorderSize(0)
    leg.SetFillColor(0)
    leg.AddEntry(h1,'H125 Signal')
    leg.AddEntry(h2,'H500 Signal')
    leg.AddEntry(h3,'H1000 Signal')    
    leg.AddEntry(h4,'H3000 Signal')    

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
    hratio.Divide(h1)
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
    elif  hname.count('jj_mass'):
        hratio.GetXaxis().SetTitle('m_{jj} [GeV]')
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
    hratio.GetYaxis().SetTitle('Signal / H125')
    hratio.GetYaxis().SetRangeUser(0.0,0.5)       
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
    hratio3 = h3.Clone()
    hratio4 = h4.Clone()
    hratio3.Divide(h1)
    hratio4.Divide(h1)
    hratio3.Draw('same')
    hratio4.Draw('same')
    can.Update()
    can.WaitPrimitive()
    #raw_input()
    if GetError:
        can.SaveAs(hname1+extra_text_save+'_err.pdf')
    else:
        can.SaveAs(hname1+extra_text_save+'.pdf')
    
def Fit(_suffix=''):

    can=ROOT.TCanvas('can',"can",600,600)
    Style();
    #f1 = ROOT.TFile.Open('365500_VBFTruth_out.root')
    #f2 = ROOT.TFile.Open('365510b_VBFTruth_out.root')
    #f1 = ROOT.TFile.Open('/tmp/v26Loose_BTAGW_sig.root')
    #f2 = ROOT.TFile.Open('../v26LooseNewSig.root')        
    #f1 = ROOT.TFile.Open('/tmp/v26Loose_BTAGW_sig_nj25.root')
    #f2 = ROOT.TFile.Open('/tmp/v26LooseNewSigLoosenNjet.root')

    f2 = ROOT.TFile.Open('/tmp/v34PFTSother.root')
    f1 = ROOT.TFile.Open('/tmp/v34PFTSother.root')

    h1_norm=1.0 #36.100
    h2_norm=1.0 #36.100 #hggf, hvh, hvbf
    hnames=['met_tst_et','jj_mass','jj_deta','jj_dphi','n_jet','j3Pt','met_truth_et','jj_mass','jj_deta','met_tst_et','jj_dphi']#'elneg_pt','elpos_pt','ph_pt_lead','ph_eta_lead','ph_pt','ph_eta','boson_pt','boson_eta','njet','dr_ph_el','dr_ph_j','dr_ph_boson']
    for hname in hnames:
        Draw(hname,f1,f2,can,h1_norm,h2_norm,GetError=False, hpath='pass_sr_allmjj_nn_Nominal/plotEvent_hvbf/')
        #Draw(hname,f1,f2,can,h1_norm,h2_norm,GetError=False, hpath='pass_sr_njgt2lt5_nn_Nominal/plotEvent_hvbf/')        
    #raw_input('a')

setPlotDefaults(ROOT)
Fit('90V')
