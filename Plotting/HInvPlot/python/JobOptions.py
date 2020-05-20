import math

#-----------------------------------------
def BinomialErr(n2, n1, err1=0.0):
    err=0.0
    if n1==0:
        return err
    total_num=n1
    if err1>0.0:
        total_num = (n1/err1)**2


    eff = n2/n1
    if total_num<0.0:
        return 1;
    if total_num<1.3 and total_num>0.0 and eff==1.0:
        return 0.2/math.sqrt(total_num);
    elif total_num<1500.3 and total_num>0.0 and eff==1.0:
        return 0.01/math.sqrt(total_num);

    if eff>1.0:
        print 'eff too high',eff
        #print total_num
        if total_num>0.0:
            return 0.5/math.sqrt(total_num);
        else:
            return 1.0
    if eff<0.0:
        print 'eff too low',eff
        return 0
    err = math.sqrt(eff*(1.0-eff)/total_num)
    return err

#-----------------------------------------
def DivideBin(n1,d1):

    m = n1.Clone()
    for i in range(0,n1.GetNbinsX()+1):

        r=0.0
        if n1.GetBinContent(i)>0.0:
            r = d1.GetBinContent(i)/n1.GetBinContent(i)
        err = BinomialErr(d1.GetBinContent(i), n1.GetBinContent(i), n1.GetBinError(i))
        #print err
        m.SetBinContent(i,r)
        m.SetBinError(i,err)
    return m
#-----------------------------------------
def ComputeEff(nums, dens, w=1.0):

    if len(nums)!=1:
        print 'ERROR doing it wrong'

    num = nums[0]
    den = dens[0]

    ratio = num.Clone()
    ratio.Divide(den)
    ratios=[]

    # Set the binomial errors
    for i in range(0,num.GetNbinsX()+1):
        ratio.SetBinError(i, BinomialErr(num.GetBinContent(i), den.GetBinContent(i), den.GetBinError(i)))

    ratios+=[ratio]

    #ratio1 = num.Clone()
    #ratio1.Divide(den1)
    ## Set the binomial errors
    #for i in range(0,num.GetNbinsX()+1):
    #    ratio1.SetBinError(i, BinomialErr(num.GetBinContent(i), den.GetBinContent(i), den.GetBinError(i)))
    #ratios+=[ratio1]
    return ratios

#---------------------------------------------------------------------
# Make logger object
#
def getLog(name, level = 'INFO', debug=False):

    import logging
    import sys

    f = logging.Formatter("Py:%(name)s: %(levelname)s - %(message)s")
    h = logging.StreamHandler(sys.stdout)
    h.setFormatter(f)

    log = logging.getLogger(name)
    log.addHandler(h)

    if debug:
        log.setLevel(logging.DEBUG)
    else:
        if level == 'DEBUG':   log.setLevel(logging.DEBUG)
        if level == 'INFO':    log.setLevel(logging.INFO)
        if level == 'WARNING': log.setLevel(logging.WARNING)
        if level == 'ERROR':   log.setLevel(logging.ERROR)

    return log

#-------------------------------------------------------------------------
# Common command line option parser
#
def getParser():

    from optparse import OptionParser

    p = OptionParser(usage='usage: <path:ROOT file directory>', version='0.1')

    #
    # Options for plotEvent.py
    #
    p.add_option('-n','--nevent',  type='int',    dest='nevent',         default=0,         help='number of events')
    p.add_option('--year',         type='int',    dest='year',           default=2016,      help='analysis year')
    p.add_option('--TheorySystWeight',         type='int',    dest='TheorySystWeight',           default=0,      help='theory syst weight: 0 none, 10 both up, 4 both down, 8,6,5,9 other options')

    p.add_option('--int-lumi',     type='float',  default=36207.66,       dest='int_lumi',    help='int luminosity 2017: 44307.4, 2018: 58450.1')
    p.add_option('-r','--rfile',   type='string', default='out.root',    dest='rfile',      help='output ROOT file')
    p.add_option('-c','--cfile',   type='string', default=None,          dest='cfile',      help='cutflow tables')
    p.add_option('-t','--tfile',   type='string', default=None,          dest='tfile',      help='tree files')
    p.add_option('-l','--lfile',   type='string', default=None,          dest='lfile',      help='limit root file')
    p.add_option('-i', '--input',  type='string', default=None,          dest='input',      help='Input text file with root files')
    p.add_option('-f', '--files',  type='string', default=None,          dest='files',      help='Input files (comma separated)')

    p.add_option('--debug-alg',    type='string', default='no',          dest='debug_alg',  help='')
    p.add_option('--print-alg',    type='string', default='no',          dest='print_alg',  help='')

    p.add_option('--region',       type='string', default='sr,gamsr,zcr,wcr,gamzcr,gamwcr,metsf',          dest='region',     help='')
    p.add_option('--chan',         type='string', default=None,          dest='chan',       help='')
    p.add_option('--njet',         type='string', default=None,          dest='njet',       help='')
    p.add_option('--syst',         type='string', default='Nominal',     dest='syst',       help='')
    p.add_option('--sample',       type='string', default='all',         dest='sample',        help='')
    p.add_option('-a','--analysis',     type='string', default='allmjj',      dest='analysis',        help='')
    p.add_option('--cut',          type='string', default='BeforeMT',    dest='cut',        help='')
    p.add_option('--var',          type='string', default='Mll',         dest='var',        help='MT variable used for limits')
    p.add_option('--lep-sign',     type='string', default='0',           dest='lep_sign',   help='Lepton Sign...0 is opposite sign, 1 is SS')
    p.add_option('--trees',        type='string', default='',      dest='trees',      help='Tree name: QCDunwNominal,VBFH125Nominal,VH125Nominal,VVVNominal,W_strongNominal,Z_strongNominal,Z_strongPTVExtNominal,Z_strong_VBFFiltNominal,ggFH125Nominal,QCDwNominal,VBFHOtherNominal,VVNominal,W_EWKNominal,Z_EWKNominal,Z_strongExtNominal,Z_strong_LowMassNominal,dataNominal,ttbarNominal')
    p.add_option('--trig-name',    type='string', default='',            dest='trig_name',  help='Trigger name if wanted. TRIG_xe80_tclcw, TRIG_lep, TRIG_2mu8_EFxe40_tclcw')
    p.add_option('--mj-trig-name', type='choice', default='TriggerEffWeightBDT', dest='mj_trigger_name', choices=['TriggerEffWeightBDT', 'TriggerEffWeight'], help='Trigger for multijet.')
    p.add_option('--mj-norm', type='choice', default="sr", dest="mj_norm", choices=['off', 'dphijj3', 'sr'], help="Normalization for QCD background.")
    p.add_option('--mva-weights-path',    type='string', default='',            dest='mva_weights_path',  help='full path to weights files for tmva')
    p.add_option('--met-choice',         type='string', default='met_tst_et',     dest='met_choice',       help='')
    p.add_option('--mergePTV',  action='store_true', default=False,   dest='mergePTV',          help='Merge the pTV slices')
    p.add_option('--mergeKTPTV',  action='store_true', default=False,   dest='mergeKTPTV',          help='Merge the KT pTV slices')    
    p.add_option('--mergeMGExt',  action='store_true', default=False,   dest='mergeMGExt',          help='Merge the MG extensions')
    p.add_option('--mergeExt',  action='store_true', default=False,   dest='mergeExt',          help='Merge the Sherpa extension slices')
    p.add_option('--r207Ana',  action='store_true', default=False,   dest='r207Ana',          help='Run the release 20.7 analysis')
    p.add_option('--noVjWeight',  action='store_true', default=False,   dest='noVjWeight',          help='Disable V+jets reweighing')
    # Should try to reduce these number of options
    p.add_option('--skim',         action='store_true', default=False,   dest='skim',           help='Skim ntuples to met trigger or 3L')
    p.add_option('--jet-veto-pt',  type='float'       , default=-10,     dest='jet_veto_pt',    help='pT for jet veto')
    p.add_option('--BTagCut',  type='float'       , default=-10,     dest='BTagCut',    help='BTagCut for tagging: 0.94, 0.83, 0.64, 0.11 for the 60, 70, 77, and 85 OP')
    p.add_option('--DetailLvl',    type='int'       ,   default=0,       dest='DetailLvl',      help='Integer for detail level of plotting. =1 plots jet variables only, 10 removes a lot of plots')
    p.add_option('--metsf-cuts',   type='int',   default=0,  dest='metsf_cuts',          help='METSF cuts: 0 Nominal, 1 nj3, 2 no centrality')

    p.add_option('--vv-vr',    action='store_true', default=False,   dest='vv_vr',            help='Run the VV VR')
    p.add_option('--pu-weight-one',    action='store_true', default=False,   dest='pu_weight_one',            help='Pileup Weight One')

    p.add_option('--no-plot',  action='store_true', default=False,   dest='no_plot',          help='Do not plot')
    p.add_option('--ignore-njet',  action='store_true', default=False,   dest='ignore_njet',        help='Ignore Njet')
    p.add_option('--ignore-met',   action='store_true', default=False,   dest='ignore_met',         help='Ignore MET')
    p.add_option('--LoadBaseLep',  action='store_true', default=False,   dest='LoadBaseLep',        help='Use looser leptons')
    p.add_option('--OverlapPh',    action='store_true', default=False,   dest='OverlapPh',          help='Overlap remove photons')
    p.add_option('--ReverseFJVT',  action='store_true', default=False,   dest='ReverseFJVT',        help='Reverse the FJVT cuts')
    p.add_option('--ReverseLeadFJVT',  action='store_true', default=False,   dest='ReverseLeadFJVT',        help='Reverse lead jet FJVT cuts')
    p.add_option('--CutFJVTVal',  type='float'       , default=0.2,   dest='CutFJVTVal',        help='Change cut on jet FJVT cuts at low met')            
    p.add_option('--debug',        action='store_true', default=False,   dest='debug',      help='')
    p.add_option('--print',        action='store_true', default=False,   dest='print',      help='')
    p.add_option('--print-run',    action='store_true', default=False,   dest='print_run',  help='')
    p.add_option('--print-xsec',   action='store_true', default=False,   dest='print_xsec', help='')
    p.add_option('--print-raw',    action='store_true', default=False,   dest='print_raw',  help='')
    p.add_option('--print-evt',    action='store_true', default=False,   dest='print_evt',  help='')
    p.add_option('--mc-evt-count', action='store_true', default=False,   dest='mc_evt_count', help='Do not apply mc event weight. Shows raw mc counts')
    p.add_option('--unblind',      action='store_true', default=False,   dest='unblind',    help='')
    p.add_option('--prec',         action='store_true', default=False,   dest='prec',       help='Increase the cutflow precision')

    p.add_option('--sumw',         type='float'       , default=0,       dest='sumw',       help='Sumw of total dataset')
    p.add_option('--nraw',         type='float'       , default=0,       dest='nraw',       help='Raw number of events of the subset that one is running over')

    #
    # Options for batchPenn.py
    #
    p.add_option('--njob',        type='int',          default=0,         dest='njob')
    p.add_option('--job-key',     type='string',       default='job',     dest='job_key')

    p.add_option('--submit',      action='store_true', default=False,     dest='submit_penn', help='submit jobs')
    p.add_option('--overwrite',   action='store_true', default=False,     dest='overwrite',   help='overwrite files')
    p.add_option('--save-tree',   action='store_true', default=False,     dest='save_tree',   help='save trees')

    return p

#-----------------------------------------------------------------------------
# Load necessary shared libraries
#
def loadLibs(root, options = None):
    #
    # Load libraries
    #
    root.gErrorIgnoreLevel = root.kError
    root.gSystem.Load('libCore')
    root.gSystem.Load('libTree')
    root.gSystem.Load('libPhysics')
    root.gROOT.ProcessLine (".x $ROOTCOREDIR/scripts/load_packages.C");

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
    root.gStyle.SetLabelFont(font,'xyz')
    root.gStyle.SetStatFont(font)
    root.gStyle.SetTitleFont(font)
    root.gStyle.SetTitleFont(font,'xyz')
    root.gStyle.SetTextFont(font)
    root.gStyle.SetTitleX(0.3)
    root.gStyle.SetTitleW(0.4)

   # Set Line Widths
   #gStyle->SetFrameLineWidth(0)
    root.gStyle.SetFuncWidth(2)
    root.gStyle.SetHistLineWidth(2)
    root.gStyle.SetFuncColor(2)

   # Set tick marks and turn off grids
    root.gStyle.SetNdivisions(505,'xyz')

   # Set Data/Stat/... and other options
    root.gStyle.SetOptDate(0)
    root.gStyle.SetDateX(0.1)
    root.gStyle.SetDateY(0.1)
   #gStyle->SetOptFile(0)
    #root.gStyle.SetOptStat(1110)
    root.gStyle.SetOptStat('reimo')
    root.gStyle.SetOptFit(111)
    root.gStyle.SetStatFormat('6.3f')
    root.gStyle.SetFitFormat('6.3f')
   #gStyle->SetStatTextColor(1)
   #gStyle->SetStatColor(1)
   #gStyle->SetOptFit(1)
   #gStyle->SetStatH(0.20)
   #gStyle->SetStatStyle(0)
   #gStyle->SetStatW(0.30)
   #gStyle -SetStatLineColor(0)
    root.gStyle.SetStatX(0.919)
    root.gStyle.SetStatY(0.919)
    root.gStyle.SetOptTitle(0)
   #gStyle->SetStatStyle(0000)    # transparent mode of Stats PaveLabel
    root.gStyle.SetStatBorderSize(0)

    root.gStyle.SetLabelSize(0.065,'xyz')
    #gStyle -> SetLabelOffset(0.005,'xyz')
    #root.gStyle.SetTitleY(.5)
    root.gStyle.SetTitleOffset(1.05,'xz')
    root.gStyle.SetTitleOffset(1.25,'y')
    root.gStyle.SetTitleSize(0.065, 'xyz')
    root.gStyle.SetLabelSize(0.065, 'xyz')
    root.gStyle.SetTextAlign(22)
    root.gStyle.SetTextSize(0.12)

    #root.gStyle.SetPaperSize(root.TStyle.kA4)
    root.gStyle.SetPalette(1)

    #root.gStyle.SetHistMinimumZero(True)

    root.gROOT.ForceStyle()

#-------------------------------------------------------------------------
def getATLASLabels(ROOT,pad, x, y, text=None, lumi=4.71, year='2011',trigger=None, split=0.07):

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
        p = ROOT.TLatex(x+0.15, y, 'Internal')
        p.SetNDC()
        p.SetTextFont(42)
        p.SetTextSize(0.055)
        p.SetTextAlign(11)
        p.SetTextColor(ROOT.kBlack)
        p.Draw()
        labs += [p]
        if year=='2012':
            if lumi!=None:
                a = ROOT.TLatex(x, y-split, '#sqrt{s}=8 TeV, #int L dt = %.1f fb^{-1}' %(lumi))
            else:
                a = ROOT.TLatex(x, y-split, '#sqrt{s}=8 TeV')
        else:
            if lumi!=None:
                a = ROOT.TLatex(x, y-split, '#sqrt{s}=7 TeV, #int L dt = %.1f fb^{-1}' %(lumi))
            else:
                a = ROOT.TLatex(x, y-split, '#sqrt{s}=7 TeV')
        a.SetNDC()
        a.SetTextFont(42)
        a.SetTextSize(0.04)
        a.SetTextAlign(12)
        a.SetTextColor(ROOT.kBlack)
        a.Draw()
        labs += [a]

        if trigger:
            b = ROOT.TLatex(x, y-split*2.0+0.01, '%s' %(trigger))

            b.SetNDC()
            b.SetTextFont(42)
            b.SetTextSize(0.04)
            b.SetTextAlign(12)
            b.SetTextColor(ROOT.kBlack)
            b.Draw()
            labs += [b]


    if text != None:

        c = ROOT.TLatex(x, y-split*2.0+0.01, text)
        c.SetNDC()
        c.SetTextFont(42)
        c.SetTextSize(0.04)
        c.SetTextAlign(12)
        c.SetTextColor(ROOT.kBlack)
        c.Draw()
        labs += [c]

    return labs

#------------------------------
# List of systematics to run
#
def SystematicsNames():
    systs=['nom',
        ]
    return systs
