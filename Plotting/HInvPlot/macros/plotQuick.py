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
    if False:
        a = ROOT.TLatex(x, y-0.04, '#sqrt{s}=13 TeV, %.1f fb^{-1}' %(36000/1.0e3))
        a.SetNDC()
        a.SetTextFont(42)
        a.SetTextSize(0.04)
        a.SetTextAlign(12)
        a.SetTextColor(ROOT.kBlack)
        a.Draw()
        labs += [a]

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
    ROOT.gROOT.LoadMacro('/afs/cern.ch/work/s/ssevova/public/dark-photon-atlas/atlasstyle/AtlasStyle.C')                   
    ROOT.gROOT.LoadMacro('/afs/cern.ch/work/s/ssevova/public/dark-photon-atlas/atlasstyle/AtlasUtils.C')
    ROOT.SetAtlasStyle()

def Draw(hname,f1,p1,p2,can,GetError=True):
 
    can.Clear()

    hname1 = p1+"/"+hname
    hname2 = p2+"/"+hname
    
    h1 = f1.Get(hname1)
    h2 = f1.Get(hname2)

    if hname == 'ptllg':
        h1.Rebin(2)
        h2.Rebin(2)
    elif hname == 'ptll' or hname == 'mt_mety': 
        h1.Rebin(5)
        h2.Rebin(5)

    #h1.Scale(1./h1.Integral())
    #h2.Scale(1./h2.Integral())

    h1.SetStats(0)
    h2.SetStats(0)
    h1.SetLineColor(1)
    h1.SetMarkerColor(1)
    h2.SetLineColor(2)
    h2.SetMarkerColor(2)
    h1.SetMarkerSize(0.5)
    h2.SetMarkerSize(0.5)


    # pads
    pad1 = ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0);
    pad1.SetBottomMargin(0); # Upper and lower plot are joined
    #pad1.SetGridx();         # Vertical grid
    pad1.Draw();             # Draw the upper pad: pad1
    pad1.cd();               # pad1 becomes the current pad


    if GetError:
        h1.GetYaxis().SetTitle('Relative Error')        
    else:
        h1.GetYaxis().SetTitle('Events')

    if GetError:
        h1 = PlotError(h1)
        h2 = PlotError(h2)
    h1.Draw()
    h2.Draw('same')

    leg = ROOT.TLegend(0.69,0.65,0.9,0.8)
    leg.SetBorderSize(0)
    leg.SetFillColor(0)
    leg.AddEntry(h1,'ZH(#gamma+Gr) 600059')
    leg.AddEntry(h2,'ZH(#gamma+invis) 345319')
    leg.Draw()

    texts = getATLASLabels(can, 0.6, 0.85, "")
    for text in texts:
        text.Draw()

    can.cd();          # Go back to the main canvas before defining pad2
    pad2 = ROOT.TPad("pad2", "pad2", 0, 0.03, 1, 0.3);
    pad2.SetTopMargin(0);
    pad2.SetBottomMargin(0.3);
    pad2.SetGridy(); # vertical grid
    pad2.Draw();
    pad2.cd();       # pad2 becomes the current pad

    hratio = h1.Clone()
    hratio.Divide(h2)
    #pad1.SetLogy(0)
    #pad2.SetLogy(0)
    #pad1.SetLogx(0)
    #pad2.SetLogx(0)


    if  hname=='n_jet':
        hratio.GetXaxis().SetTitle('N(R=0.4 jets)')
    elif  hname=='n_ph':
        hratio.GetXaxis().SetTitle('N(photons)')
    elif  hname=='n_mu':
        hratio.GetXaxis().SetTitle('N(muons)')        
    elif  hname=='met_tight_tst_et':
        hratio.GetXaxis().SetTitle('tight E_{T}^{miss} [GeV]')        
    elif  hname=='lepPt0':
        hratio.GetXaxis().SetTitle('leading lepton p_{T} [GeV]')        
    elif  hname=='lepPt1':
        hratio.GetXaxis().SetTitle('trailing lepton p_{T} [GeV]')        
    elif  hname=='phPt':
        hratio.GetXaxis().SetTitle('photon p_{T} [GeV]')
    elif  hname=='ptll':
        hratio.GetXaxis().SetTitle('p_{T}^{ll} [GeV]')        
    elif  hname=='ptllg':
        hratio.GetXaxis().SetTitle('p_{T}^{ll#gamma} [GeV]')
    elif  hname=='mt_mety':
        hratio.GetXaxis().SetTitle('m_{T}(E_{T}^{miss},p_{T}^{#gamma}) [GeV]')
    hratio.GetYaxis().SetTitle('Gr / invis')
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
    can.Update()
#    can.WaitPrimitive()
    if GetError:
        can.SaveAs(hname+'_err.pdf')
    else:
        can.SaveAs(hname+".pdf")

    del pad1
    del pad2
    del h1
    del h2
    del hratio

def Plot():

    can=ROOT.TCanvas('can',"can",600,600)
    Style();
    f1 = ROOT.TFile.Open('outtree_v04_nodata.root')
    p1 = "pass_sr_all_uu_Nominal/plotEvent_hyGr"
    p2 = "pass_sr_all_uu_Nominal/plotEvent_hvh"

    hnames=['n_ph','n_mu','n_jet','met_tight_tst_et', 'lepPt0', 'lepPt1', 'phPt', 'ptll', 'ptllg', 'mt_mety']
    for hname in hnames:
        Draw(hname,f1,p1,p2,can,GetError=False)

setPlotDefaults(ROOT)
Plot()
