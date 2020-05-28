import ROOT
import math
import os
from optparse import OptionParser
from helper import HistEntry


p = OptionParser(usage="python ratioHists.py -p <path> -v <variables, comma seperated> -f <files>--wait -n <suffix>", version="0.1")
p.add_option('--file','-f',           type='string', default='hists_extract_Zee_QCD,hists_extract_Zmm_QCD', dest='file')
p.add_option('--var','-v',           type='string', default='', dest='var') #all/Incl/boson_pt,all/Incl/boson_pt
p.add_option('--path','-p', type='string', default='./processed', dest='path')
p.add_option('--wait',          action='store_true', default=False,   dest='wait')
p.add_option('--doFit',          action='store_true', default=False,   dest='doFit')
p.add_option('--name','-n', type='string', default='test', dest='name')
p.add_option('--logscale', '-l',         action='store_true', default=False,   dest='logscale')
p.add_option('--atlasrootstyle','-s', type='string', default='/afs/desy.de/user/o/othrif/atlasrootstyle', dest='atlasrootstyle')
(options, args) = p.parse_args()

#-----------------------------------------
def getall(d, basepath="/"):
    "Walk the directory structure and content in and below a directory. Return (path, obj) pairs"
    for key in d.GetListOfKeys():
        kname = key.GetName()
        if key.IsFolder():
            for i in getall(d.Get(kname), basepath+kname+"/"):
                yield i
        else:
            yield basepath+kname, d.Get(kname)
#-----------------------------------------
def Style():
    ROOT.gROOT.LoadMacro(options.atlasrootstyle+'/AtlasStyle.C')
    ROOT.gROOT.LoadMacro(options.atlasrootstyle+'/AtlasUtils.C')
    ROOT.SetAtlasStyle()
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

def printHist(h,name):
    print(name+':')
    for i in range(1,h.GetNbinsX()+1):
        valb = h.GetBinContent(i)
        errb = h.GetBinError(i)
        print '{0:.4} +- {1:.4}'.format(h.GetBinContent(i), h.GetBinError(i))

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

def Draw(hname1, hname2,f1, f2,can,GetError=True):
    can.Clear()

    hname = hname1
    h1 = f1.Get(hname1)
    h2 = f2.Get(hname2)
    #h1.Scale(h1_norm)
    #h2.Scale(h2_norm)
    print('\n'+f1.GetName()+' '+f2.GetName())

    # Fix labels

    type_sample='QCD '
    type_sample_out='qcd'
    if f1.GetName().count('EWK') or f2.GetName().count('EWK'):
        type_sample='EWK '
        type_sample_out='ewk'
    num_name = 'Z#rightarrow#nu#nu'
    den_name = 'Z#rightarrow#nu#nu'
    comp1='znn'
    comp2='znn'
    if f1.GetName().count('_Zll'):
        num_name = 'Z#rightarrow ll'
        comp1='zll'
    if f1.GetName().count('_Zmm'):
        num_name = 'Z#rightarrow #mu#mu'
        comp1='zmm'
    if f1.GetName().count('_Zee'):
        num_name = 'Z#rightarrow ee'
        comp1='zee'
    if f1.GetName().count('_Zvv'):
        num_name = 'Z#rightarrow#nu#nu'
    if f1.GetName().count('_Wlv'):
        num_name = 'W#rightarrowl#nu'
        comp1='wln'
    if f1.GetName().count('_Wev'):
        num_name = 'W#rightarrowe#nu'
        comp1='wen'
    if f1.GetName().count('_Wmv'):
        num_name = 'W#rightarrow#mu#nu'
        comp1='wmn'
    if f2.GetName().count('_Zll'):
        den_name = 'Z#rightarrow ll'
        comp2='zll'
    if f2.GetName().count('_Zmm'):
        den_name = 'Z#rightarrow #mu#mu'
        comp2='zmm'
    if f2.GetName().count('_Zee'):
        den_name = 'Z#rightarrow ee'
        comp2='zee'
    if f2.GetName().count('_Zvv'):
        den_name = 'Z#rightarrow#nu#nu'
    if f2.GetName().count('_Wlv'):
        den_name = 'W#rightarrowl#nu'
        comp2='wln'
    if f2.GetName().count('_Wev'):
        den_name = 'W#rightarrowe#nu'
        comp2='wen'
    if f2.GetName().count('_Wmv'):
        den_name = 'W#rightarrow#mu#nu'
        comp2='wmn'

    var_num_name = 'N_{jet}^{25} = 2'
    var_den_name = 'N_{jet}^{25} #geq 2'
    num_name = num_name + ' ' + var_num_name
    den_name = den_name + ' ' + var_den_name

    h1.SetStats(0)
    h2.SetStats(0)
    h1.SetLineColor(1)
    h1.SetMarkerColor(1)
    h2.SetLineColor(2)
    h2.SetMarkerColor(2)
    h1.SetMarkerSize(1)
    h2.SetMarkerSize(1)


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

    max_bin = max(h1.GetMaximum(),h2.GetMaximum())
    h1.GetYaxis().SetRangeUser(0,max_bin*1.2)
    if options.logscale:
        h1.GetYaxis().SetRangeUser(1e-8, max_bin*1.5)

    h1.Draw('hist')
    h2.Draw('same hist')

    chi2 = 1.#h1.Chi2Test      (h2, 'UW CHI2')
    kval = 1.#h1.KolmogorovTest(h2, '')
    #print 'chi2: ',chi2,' ks: ',kval
    ks_text2 = ROOT.TLatex(0.3, 0.95, 'KS: %.2f' %kval)
    ks_text2.SetNDC()
    ks_text2.SetTextSize(0.055)
    ks_text2.SetTextAlign(11)
    ks_text2.SetTextColor(ROOT.kBlack)
    #ks_text2.Draw()

    e=ROOT.Double(0.0)
    #print 'Integral '+num_name+': ',h1.IntegralAndError(0,1001,e),'+/-',e
    #print 'Integral '+den_name+': ',h2.IntegralAndError(0,1001,e),'+/-',e

    leg = ROOT.TLegend(0.6,0.7,0.8,0.8)
    leg.SetBorderSize(0)
    leg.SetFillColor(0)
    leg.AddEntry(h1,num_name)
    leg.AddEntry(h2,den_name)

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
    #intden = h1.Integral()
    #if intden>0.0:
    #    hratio.Scale(h2.Integral()/intden)
    #hratio.Divide(h2)

    printHist(h1,num_name)
    printHist(h2,den_name)
    hratio.Divide(h1,h2,1.0,1.0,"B");
    printHist(hratio,num_name+'/'+den_name)

    pad1.SetLogy(0)
    if options.logscale:
        pad1.SetLogy(1)
    pad2.SetLogy(0)
    pad1.SetLogx(0)
    pad2.SetLogx(0)

    print "drawing ", hname, "..."
    if  hname.count('boson_pt'):
        hratio.GetXaxis().SetTitle('Boson p_{T} [GeV]')
    elif  hname.count('boson_m'):
        hratio.GetXaxis().SetTitle('Boson Mass [GeV]')
    elif  hname.count('jj_mass'):
        hratio.GetXaxis().SetTitle('m_{jj} [GeV]')
    elif  hname.count('jj_deta'):
        hratio.GetXaxis().SetTitle('#Delta#eta_{jj}')
    elif  hname.count('jj_dphi'):
        hratio.GetXaxis().SetTitle('#Delta#phi_{jj}')
    elif  hname.count('jet1_pt'):
        hratio.GetXaxis().SetTitle('Lead Jet p_{T} [GeV]')
    elif  hname.count('jet2_pt'):
        hratio.GetXaxis().SetTitle('Sub-Lead Jet p_{T} [GeV]')
    elif  hname.count('jet3_pt'):
        hratio.GetXaxis().SetTitle('3rd jet p_{T} [GeV]')
    elif hname.count('met_et'):
        hratio.GetXaxis().SetTitle('MET [GeV]')
    elif  hname.count('met_nolep_et'):
        hratio.GetXaxis().SetTitle('MET (no leptons) [GeV]')
    elif hname.count('el1_pt'):
        hratio.GetXaxis().SetTitle('Lead Electron p_{T} [GeV]')
    elif hname.count('el2_pt'):
        hratio.GetXaxis().SetTitle('Sub-Lead Electron p_{T} [GeV]')
    elif hname.count('el1_eta'):
        hratio.GetXaxis().SetTitle('Lead Electron  #eta [GeV]')
    elif hname.count('el2_eta'):
        hratio.GetXaxis().SetTitle('Sub-Lead Electron #eta [GeV]')
    elif hname.count('mu1_pt'):
        hratio.GetXaxis().SetTitle('Lead Muon p_{T} [GeV]')
    elif hname.count('mu2_pt'):
        hratio.GetXaxis().SetTitle('Sub-Lead Muon p_{T} [GeV]')
    elif hname.count('mu1_eta'):
        hratio.GetXaxis().SetTitle('Lead Electron  #eta [GeV]')
    elif hname.count('mu2_eta'):
        hratio.GetXaxis().SetTitle('Sub-Lead Electron #eta [GeV]')
    elif hname.count('nu1_pt'):
        hratio.GetXaxis().SetTitle('Lead Neutrino p_{T} [GeV]')
    elif hname.count('nu2_pt'):
        hratio.GetXaxis().SetTitle('Sub-Lead Neutrino p_{T} [GeV]')
    elif hname.count('nu1_eta'):
        hratio.GetXaxis().SetTitle('Lead Neutrino  #eta [GeV]')
    elif hname.count('nu2_eta'):
        hratio.GetXaxis().SetTitle('Sub-Lead Neutrino #eta [GeV]')
    elif hname.count('lep_jet_dR'):
        hratio.GetXaxis().SetTitle('#DeltaR(#ell,jet)')
    elif  hname.count('n_jet25'):
        hratio.GetXaxis().SetTitle('N_{jet}^{25}')
    elif  hname.count('n_jet50'):
        hratio.GetXaxis().SetTitle('N_{jet}^{50}')
    elif  hname.count('n_jet'):
        hratio.GetXaxis().SetTitle('N_{jet}')
    elif  hname.count('n_el'):
        hratio.GetXaxis().SetTitle('N_{e}')
    elif  hname.count('n_mu'):
        hratio.GetXaxis().SetTitle('N_{#mu}')
    elif  hname.count('n_nu'):
        hratio.GetXaxis().SetTitle('N_{#nu}')

    #hratio.GetYaxis().SetTitle(num_name+' / '+den_name)
    hratio.GetYaxis().SetTitle(var_num_name+' / '+var_den_name)
    hratio.GetYaxis().SetRangeUser(0.,.5)
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
    hratio.Draw('EL')
    can.Update()

    if options.wait and False:
        can.WaitPrimitive()
    log_label=''
    if options.logscale:
        log_label='_log'


    mypath=options.path+'/plots/'
    if not os.path.exists(mypath):
        os.makedirs(mypath)
    mypath=mypath+hname[1:].replace("/", "_")
    if GetError:
        can.SaveAs(mypath+'_'+comp1+'_'+comp2+'_'+options.name+log_label+'_err.pdf')
    else:
        can.SaveAs(mypath+'_'+comp1+'_'+comp2+'_'+options.name+log_label+'.pdf')

    return hratio

def Ratio(h1, h2,f1name,f2name,can,GetError=True):
    can.Clear()

    hname = h1.GetName()
    #h1.Scale(h1_norm)
    #h2.Scale(h2_norm)
   # print f1name,f2name

    # Fix labels

    type_sample='QCD '
    type_sample_out='qcd'
    if f1name.count('EWK') or f2name.count('EWK'):
        type_sample='EWK '
        type_sample_out='ewk'
    num_name = 'Z#rightarrow#nu#nu'
    den_name = 'Z#rightarrow#nu#nu'
    comp1='znn'
    comp2='znn'
    if f1name.count('_Zll'):
        num_name = 'Z#rightarrow ll'
        comp1='zll'
    if f1name.count('_Zmm'):
        num_name = 'Z#rightarrow #mu#mu'
        comp1='zmm'
    if f1name.count('_Zee'):
        num_name = 'Z#rightarrow ee'
        comp1='zee'
    if f1name.count('_Zvv'):
        num_name = 'Z#rightarrow#nu#nu'
    if f1name.count('_Wlv'):
        num_name = 'W#rightarrowl#nu'
        comp1='wln'
    if f1name.count('_Wev'):
        num_name = 'W#rightarrowe#nu'
        comp1='wen'
    if f1name.count('_Wmv'):
        num_name = 'W#rightarrow#mu#nu'
        comp1='wmn'
    if f2name.count('_Zll'):
        den_name = 'Z#rightarrow ll'
        comp2='zll'
    if f2name.count('_Zmm'):
        den_name = 'Z#rightarrow #mu#mu'
        comp2='zmm'
    if f2name.count('_Zee'):
        den_name = 'Z#rightarrow ee'
        comp2='zee'
    if f2name.count('_Zvv'):
        den_name = 'Z#rightarrow#nu#nu'
    if f2name.count('_Wlv'):
        den_name = 'W#rightarrowl#nu'
        comp2='wln'
    if f2name.count('_Wev'):
        den_name = 'W#rightarrowe#nu'
        comp2='wen'
    if f2name.count('_Wmv'):
        den_name = 'W#rightarrow#mu#nu'
        comp2='wmn'

    var_num_name = 'N_{jet}^{25} = 2'
    var_den_name = 'N_{jet}^{25} #geq 2'
    num_name_l = num_name + ' ' + var_num_name + '/' + var_den_name
    den_name_l = den_name + ' ' + var_num_name + '/' + var_den_name

    h1.SetStats(0)
    h2.SetStats(0)
    h1.SetLineColor(1)
    h1.SetMarkerColor(1)
    h2.SetLineColor(2)
    h2.SetMarkerColor(2)
    h1.SetMarkerSize(1)
    h2.SetMarkerSize(1)


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

    max_bin = max(h1.GetMaximum(),h2.GetMaximum())
    #print h1.GetMaximum(),h2.GetMaximum()
    #h1.GetYaxis().SetRangeUser(0,0.75)
    h1.GetYaxis().SetRangeUser(0.,0.3)
    if options.logscale:
        h1.GetYaxis().SetRangeUser(1e-8, max_bin*1.5)

    h1.Draw('hist')
    h2.Draw('same hist')

    chi2 = 1.#h1.Chi2Test      (h2, 'UW CHI2')
    kval = 1.#h1.KolmogorovTest(h2, '')
    #print 'chi2: ',chi2,' ks: ',kval
    ks_text2 = ROOT.TLatex(0.3, 0.95, 'KS: %.2f' %kval)
    ks_text2.SetNDC()
    ks_text2.SetTextSize(0.055)
    ks_text2.SetTextAlign(11)
    ks_text2.SetTextColor(ROOT.kBlack)
    #ks_text2.Draw()

    e=ROOT.Double(0.0)
    #print 'Integral '+comp1+': ',h1.IntegralAndError(0,1001,e),'+/-',e
    #print 'Integral '+comp2+': ',h2.IntegralAndError(0,1001,e),'+/-',e

    leg = ROOT.TLegend(0.5,0.6,0.8,0.8)
    leg.SetBorderSize(0)
    leg.SetFillColor(0)
    leg.AddEntry(h1,num_name_l)
    leg.AddEntry(h2,den_name_l)

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
    intden = h1.Integral()
    #if intden>0.0:
    #    hratio.Scale(h2.Integral()/intden)
    hratio.Divide(h2)
    #hratio.Divide(h1,h2,1.0,1.0,"B");
    pad1.SetLogy(0)
    if options.logscale:
        pad1.SetLogy(1)
    pad2.SetLogy(0)
    pad1.SetLogx(0)
    pad2.SetLogx(0)

    print "drawing ", hname, "..."
    hratio.GetXaxis().SetTitle('m_{jj} [GeV]')

    if  hname.count('boson_pt'):
        hratio.GetXaxis().SetTitle('Boson p_{T} [GeV]')
    elif  hname.count('jj_mass'):
        hratio.GetXaxis().SetTitle('m_{jj} [GeV]')
    elif hname.count('met_et'):
        hratio.GetXaxis().SetTitle('MET [GeV]')
    elif  hname.count('met_nolep_et'):
        hratio.GetXaxis().SetTitle('MET (no leptons) [GeV]')


    #hratio.GetYaxis().SetTitle(num_name+' / '+den_name)
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
    hratio.Draw('EL')
    par0=0
    par1=0
    if options.doFit:
        hratio.Fit('pol1',"R","",800.0,5000.0)
        myfunc = hratio.GetFunction('pol1')
        par0 = myfunc.GetParameter(0)
        err0 = myfunc.GetParError(0)
        par1 = myfunc.GetParameter(1)
    printHist(hratio,num_name+' / '+den_name)
    can.Update()

    if options.wait:
        can.WaitPrimitive()
    log_label=''
    if options.logscale:
        log_label='_log'


    mypath=options.path+'/plots/'
    if not os.path.exists(mypath):
        os.makedirs(mypath)
    mypath=mypath+hname[1:].replace("/", "_")
    if GetError:
        can.SaveAs(mypath+'_'+comp1+'_'+comp2+'_'+options.name+log_label+'_err.pdf')
    else:
        can.SaveAs(mypath+'_'+comp1+'_'+comp2+'_'+options.name+log_label+'.pdf')

def Fit(_suffix=''):

    can=ROOT.TCanvas('can',"can",600,600)
    Style();
    path=options.path

    files=options.file.split(',')
    f=[]
    for fname in files:
        f.append(ROOT.TFile.Open(path+'/'+fname+'.root'))

    if options.var:
        hnames=options.var.split(',')
        if len(files) != 2 or len(hnames) != 2:
            print("WARNING: number of files or number of histogram names is not equal to 2, insure this is satisfied!")
            return
        hratio1 = Draw(hnames[0],hnames[1],f[0],f[0],can,GetError=False)
        hratio2 = Draw(hnames[0],hnames[1],f[1],f[1],can,GetError=False)
        Ratio(hratio1,hratio2,files[0],files[1],can,GetError=False)
    else:
        print "Provide ..."
        return





setPlotDefaults(ROOT)
Fit('test')

