import ROOT
import math
import json
from optparse import OptionParser
from helper import HistEntry
from array import array

p = OptionParser(usage="python plotTree.py -p <path>--wait -n <suffix>", version="0.1")
p.add_option('--file','-f',           type='string', default='Z_strong,Z_strong_ckkw15', dest='file')
p.add_option('--path','-p', type='string', default='.', dest='path')
p.add_option('--wait',          action='store_true', default=False,   dest='wait')
p.add_option('--name','-n', type='string', default='', dest='name')
p.add_option('--logscale', '-l',         action='store_true', default=False,   dest='logscale')
p.add_option('--atlasrootstyle','-s', type='string', default='/afs/desy.de/user/o/othrif/atlasrootstyle', dest='atlasrootstyle')
p.add_option('--config', type=str, default='/nfs/dust/atlas/user/othrif/vbf/myPP/source/TheoryUnc/TJV_study/pyAnalysis/hists_config_tree.json', dest='config', help='json file containing configurations for making histograms')
p.add_option('--ratioMin', '-m', type='float', default='0.5', dest='ratioMin')
p.add_option('--ratioMax', '-M', type='float', default='1.5', dest='ratioMax')

(options, args) = p.parse_args()
config = json.load(file(options.config))

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

def Draw(h1, h2,f1, f2,can,GetError=True):
    can.Clear()

    #h1 = f1.Get(hname1)
    #h2 = f2.Get(hname2)
    #h1.Scale(h1_norm)
    #h2.Scale(h2_norm)
    hname1=h1.GetName()
    hname2=h2.GetName()

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
   #h1.GetYaxis().SetRangeUser(0.001, max_bin*1.2)
    #if options.logscale:
    #    h1.GetYaxis().SetRangeUser(0.001, max_bin*2.5)

    h1.Draw('hist')
    h2.Draw('hist same')

    leg = ROOT.TLegend(0.6,0.7,0.8,0.8)
    leg.SetBorderSize(0)
    leg.SetFillColor(0)
    leg.AddEntry(h1,'21.2.10')#hname1)
    leg.AddEntry(h2,'21.2.87')#hname2)

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
    pad1.SetLogy(0)
    if options.logscale:
        pad1.SetLogy(1)
    pad2.SetLogy(0)
    pad1.SetLogx(0)
    pad2.SetLogx(0)

    if  hname1.count('jj_mass'):
        hratio.GetXaxis().SetTitle('m_{jj} [GeV]')
    if  hname1.count('V_dressed_pt'):
        hratio.GetXaxis().SetTitle('Dressed Boson p_{T} [GeV]')
    if  hname1.count('jet1_pt'):
        hratio.GetXaxis().SetTitle('Lead Jet p_{T} [GeV]')
    if  hname1.count('jet2_pt'):
        hratio.GetXaxis().SetTitle('Sub-Lead Jet p_{T} [GeV]')

    #hratio.GetYaxis().SetTitle(hname1.split("/")[-1]+' / '+hname2.split("/")[-1])
    hratio.GetYaxis().SetTitle('21.2.10/21.2.87')
    hratio.GetYaxis().SetRangeUser(options.ratioMin,options.ratioMax)
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

    if options.wait:
        can.WaitPrimitive()
    log_label=''
    if options.logscale:
        log_label='_log'

    if GetError:
        can.SaveAs(options.path+'/'+hname1.split("/")[-1]+'_'+hname1.split("/")[-1]+'_'+options.name+log_label+'_err.pdf')
    else:
        can.SaveAs(options.path+'/'+hname2.split("/")[-1]+'_'+hname2.split("/")[-1]+'_'+options.name+log_label+'.pdf')

def Fit(_suffix=''):

    can=ROOT.TCanvas('can',"can",600,600)
    Style();
    path=options.path

    files=options.file.split(',')

    if len(files) != 2:
        print("WARNING: number of files is not 2!")
        return


    files = [ROOT.TFile.Open(path+'/'+files[0]+'.root'), ROOT.TFile.Open(path+'/'+files[1]+'.root')]
    hists = []
    for f in files:
        keyList = f.GetListOfKeys()
        for keyName in keyList:
            inputTreeName=keyName.GetName()
        tree = f.Get(inputTreeName)
        for cut in config['cuts']:
            for toDraw in config['draw']:
                histName = toDraw['name']+inputTreeName
                histDimension = len(toDraw['draw'].split(':'))
                if "nbins" in toDraw:
                  print "\tTree "+inputTreeName+": making {4}D histogram with {1} bins from {2} to {3}".format(toDraw['name'], toDraw['nbins'], toDraw['min'], toDraw['max'], histDimension)
                  if histDimension == 1:
                    h = ROOT.TH1F(histName,histName,toDraw['nbins'], toDraw['min'], toDraw['max'])
                  else:
                    raise ValueError('Not handling higher dim for now {0}'.format(toDraw))
                elif "edges" in toDraw:
                  print "\tTree "+inputTreeName+": making {1}D histogram with bin edges: {0}".format(toDraw['edges'], histDimension)
                  if histDimension == 1:
                    h = ROOT.TH1F(histName,histName,len(toDraw['edges'])-1,array('d',toDraw['edges']))
                  else:
                    raise ValueError('Not handling higher dim for now {0}'.format(toDraw))
                else:
                  print "ERROR: problem configuring the binning of the histograms..."
                  exit()
                # things look ok, so we draw to the histogram
                print "\t\tdrawing {0}\n\t\twith cut ({1})".format(toDraw['draw'], cut['name'])
                tree.Draw(toDraw['draw'] + ' >> ' + histName, '({0:s})'.format( cut['cut']) )
                print "\t\t Integral = {0:.4f}".format(h.Integral())
                samename=h.GetName()
                hnew = HistEntry(h, histName)
                hnew=hnew.merge_bins() # merge upper overflow bin
                hnew.SetName(samename)
                hists.append(hnew)

    for i in range(len(config['draw'])):
        Draw(hists[i],hists[i+len(config['draw'])],files[0],files[1],can,GetError=False)



setPlotDefaults(ROOT)
Fit('test')

