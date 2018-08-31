#!/usr/bin/env python

import os,sys
import re
import sys
import math

from optparse import OptionParser

p = OptionParser(usage="usage: <path:ROOT file directory>", version="0.1")

p.add_option('-n',             type='int',    default=0,             dest='nevent')
p.add_option('--hscale',       type='int',    default=None,          dest='hscale')
p.add_option('--hmass',        type='string', default='125',         dest='hmass')

p.add_option('--selkey',       type='string', default='pass_sr_hipt_1j_eu', dest='selkey')
p.add_option('--algkey',       type='string', default='plotEvent',   dest='algkey')
p.add_option('--vars',         type='string', default=None,          dest='vars')
p.add_option('--outdir',       type='string', default=None,          dest='outdir')

p.add_option('--pref',         type='string', default=None,          dest='pref')
p.add_option('--syst',         type='string', default='Nominal',     dest='syst')
p.add_option('--syst-sel',     type='string', default='Nominal',     dest='syst_sel')
p.add_option('--syst-see',     type='string', default='Nominal',     dest='syst_see')
p.add_option('--sf-file',      type='string', default=None,          dest='sf_file')
p.add_option('--do-nf',        type='string', default=None,          dest='do_nf')
p.add_option('--extract-sig',  type='string', default=None,          dest='extract_sig')
p.add_option('--syst-table',   type='string', default=None,          dest='syst_table')

p.add_option('--int-lumi',     type='float',  default=36100.0,       dest='int_lumi')
p.add_option('--ymin',         type='float',  default=None,          dest='ymin')
p.add_option('--ymax',         type='float',  default=None,          dest='ymax')
p.add_option('--xmax',         type='float',  default=None,          dest='xmax')
p.add_option('--xmin',         type='float',  default=None,          dest='xmin')

p.add_option('--blind',         action='store_true', default=False,   dest='blind')
p.add_option('--do-eps',        action='store_true', default=False,   dest='do_eps')
p.add_option('--do-pdf',        action='store_true', default=False,   dest='do_pdf')
p.add_option('--do-logy',       action='store_true', default=False,   dest='do_logy')
p.add_option('--no-logy',       action='store_true', default=False,   dest='no_logy')
p.add_option('--draw-norm',     action='store_true', default=False,   dest='draw_norm')
p.add_option('--do-ratio',      action='store_true', default=False,   dest='do_ratio')
p.add_option('--force-ratio',   action='store_true', default=False,   dest='force_ratio')
p.add_option('--stack-signal',  action='store_true',default=False,   dest='stack_signal')

p.add_option('--debug',         action='store_true', default=False,   dest='debug')
p.add_option('--wait',          action='store_true', default=False,   dest='wait')
p.add_option('--save',          action='store_true', default=False,   dest='save')
p.add_option('--save-algkey',   action='store_true', default=False,   dest='save_algkey')
p.add_option('--syst-fakes',    type='int',          default=0,       dest='syst_fakes')
p.add_option('--syst-trkmet',   type='int',          default=0,       dest='syst_trkmet')
p.add_option('--no-underflow',  action='store_true', default=False,   dest='no_underflow')

p.add_option('--draw-syst',       action='store_true', default=False,   dest='draw_syst')
p.add_option('--make-syst-table', action='store_true', default=False,   dest='make_syst_table')

(options, args) = p.parse_args()  

import ROOT
import HInvPlot.JobOptions as config
import HInvPlot.CutsDef    as hstudy

#config.setPlotDefaults(ROOT)

if not options.wait:
    ROOT.gROOT.SetBatch(True)

log = config.getLog('drawStack.py', debug=options.debug)

# List of plots to symmeterize
symm_list = {'ResoSoftTrackMetScaleDown_ptHard': 'ResoSoftTrackMetScaleUp_ptHard',
             'ResoSoftTrackMetDownPerp_ptHard' : 'ResoSoftTrackMetUpPerp_ptHard',
             'ResoSoftTrackMetScaleDown_uncorr': 'ResoSoftTrackMetScaleUp_uncorr',
             'ResoSoftTrackMetDownPerp_uncorr' : 'ResoSoftTrackMetUpPerp_uncorr',

            'SoftTrackResoParaDown' : 'SoftTrackResoPara',
            'SoftTrackResoPerpDown' : 'SoftTrackResoPerp',                           
             }
#-----------------------------------------
def Style():
    ROOT.gROOT.LoadMacro('/Users/schae/testarea/SUSY/JetUncertainties/testingMacros/atlasstyle/AtlasStyle.C')                   
    ROOT.gROOT.LoadMacro('/Users/schae/testarea/SUSY/JetUncertainties/testingMacros/atlasstyle/AtlasUtils.C')
    ROOT.SetAtlasStyle()

#-------------------------------------------------------------------------
def getSelKeyPath():
    
    if options.save_algkey:
        return '%s_%s' %(options.selkey, options.algkey)
    return options.selkey

#-------------------------------------------------------------------------
def getSelKeyLabel(selkey):

    proc = None
    decay = 'Invis'
    if selkey != None: # and selkey.count('hww') or selkey.count('lowmet'):
        if True:
            if selkey.count('_nn'): proc = 'VBF H#rightarrow%s' %decay
            elif selkey.count('_ll'): proc = 'Z#rightarrow ll'
            elif selkey.count('_ee'): proc = 'Z#rightarrow ee'
            elif selkey.count('_eu'): proc = 'e#mu'
            elif selkey.count('_em'): proc = 'W#rightarrow e^{-}#nu'
            elif selkey.count('_uu'): proc = 'Z#rightarrow#mu#mu'
            elif selkey.count('_l'): proc = 'W#rightarrow l#nu'
            elif selkey.count('_e'): proc = 'W#rightarrow e#nu'
            elif selkey.count('_u'): proc = 'W#rightarrow#mu#nu'
                           
        if selkey.count('sr_'):  proc += ', SR'
        if selkey.count('wcr'): proc += ', WCR'
        if selkey.count('zcr'): proc += ', ZCR'


    return proc
    
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
        p = ROOT.TLatex(x+0.15, y, ' Internal') #
        p.SetNDC()
        p.SetTextFont(42)
        p.SetTextSize(0.055)
        p.SetTextAlign(11)
        p.SetTextColor(ROOT.kBlack)        
        p.Draw()
        labs += [p]

        a = ROOT.TLatex(x, y-0.04, '#sqrt{s}=13 TeV, %.1f fb^{-1}' %(options.int_lumi/1.0e3))
        a.SetNDC()
        a.SetTextFont(42)
        a.SetTextSize(0.04)
        a.SetTextAlign(12)
        a.SetTextColor(ROOT.kBlack)
        a.Draw()
        labs += [a]

    proc = getSelKeyLabel(selkey)
    if proc != None:
        
        c = ROOT.TLatex(x, y-0.08, proc)
        c.SetNDC()
        c.SetTextFont(42)
        c.SetTextSize(0.04)
        c.SetTextAlign(12)
        c.SetTextColor(ROOT.kBlack)
        labs += [c]
       
    return labs

#-------------------------------------------------------------------------
def getHistPars(hist):
    
    labels = {
        #
        # Kinematics histograms
        #
        'jet0Eta': {'xtitle':'Leading jet #eta'  ,           'ytitle':'Events', 'rebin':2},
        'jet0Phi': {'xtitle':'Leading jet #phi'  ,           'ytitle':'Events', 'rebin':2},
        'jetPt0' : {'xtitle':'p_{T}^{jet 1} [GeV]',          'ytitle':'Events / (10 GeV)', 'rebin':10},
        'jet1Eta': {'xtitle':'Sub-Leading jet #eta'  ,       'ytitle':'Events', 'rebin':2},
        'jet1Phi': {'xtitle':'Sub-Leading jet #phi'  ,       'ytitle':'Events', 'rebin':2},
        'jetPt1' : {'xtitle':'p_{T}^{jet 2} [GeV]',          'ytitle':'Events / (10 GeV)', 'rebin':10},
        'n_jet'   : {'xtitle':'Number of Jets',               'ytitle':'Events', 'rebin':0},
        'n_bjet'  : {'xtitle':'Number of B Jets',             'ytitle':'Events', 'rebin':0},

        'lepPt0'   : {'xtitle':'Anti-Id Electron p_{T} [GeV]', 'ytitle':'Events', 'rebin':0},
        'elec_num_pt'   : {'xtitle':'Id Electron p_{T} [GeV]', 'ytitle':'Events', 'rebin':5},
        'muon_den_pt'   : {'xtitle':'Anti-Id Muon p_{T} [GeV]', 'ytitle':'Events', 'rebin':0},
        'lepEta' : {'xtitle':'Lepton #eta [GeV]',              'ytitle':'Events', 'rebin':0,    'ymin':0.0},
        'lepPhi' : {'xtitle':'Lepton #phi [GeV]',              'ytitle':'Events', 'rebin':0,    'ymin':0.0},
        'dphill' : {'xtitle':'#Delta #phi_{ll}',                 'ytitle':'Events', 'rebin':5,  'ymin':0.01},
        'jj_dphi' : {'xtitle':'#Delta #phi_{jj}',                 'ytitle':'Events', 'rebin':2,  'ymin':0.01},
        'met_tst_et'    : {'xtitle':'E_{T}^{miss} [GeV]',                 'ytitle':'Events / (25 GeV)', 'rebin':5,  'ymin':0.01, 'logy':False},
        'met_tst_phi'    : {'xtitle':'E_{T}^{miss} #phi',                 'ytitle':'Events', 'rebin':4,  'ymin':0.01, 'logy':False},        
        'met_tst_nolep_et'    : {'xtitle':'E_{T,miss} (remove leptons) [GeV]',                 'ytitle':'Events / (25 GeV)', 'rebin':5,  'ymin':0.01, 'logy':False},
        'met_tst_nolep_et'    : {'xtitle':'E_{T,miss} (remove leptons) #phi',                 'ytitle':'Events', 'rebin':4,  'ymin':0.01, 'logy':False},        
        'mll'    : {'xtitle':'m_{ll} [GeV]'  ,                    'ytitle':'Events / (5 GeV)', 'rebin':4,  'ymin':0.001, 'xmax':150.0},
        'jj_mass'    : {'xtitle':'m_{jj} [GeV]'  ,                   'ytitle':'Events / (500 GeV)', 'rebin':5,  'ymin':0.01,'logy':False},        
        'jj_deta' : {'xtitle':'#Delta #eta_{jj}'  ,               'ytitle':'Events', 'rebin':2,  'ymin':0.001},        
        'ptll'   : {'xtitle':'P_{T,ll} [GeV]',                   'ytitle':'Events / (25 GeV)', 'rebin':5,  'ymin':0.0},
        'mt'     : {'xtitle':'M_{T} [GeV]'   ,         'ytitle':'Events / (10 GeV)', 'rebin':10,  'ymin':0.01,'logy':False},
        'met_significance'     : {'xtitle':'MET Significance [GeV^{1/2}]'   ,         'ytitle':'Events', 'rebin':10,  'ymin':0.01,'logy':False},
        }

    try:
        return labels[hist]
    except KeyError:
        log.warning('getHistPars - unknown histogram: %s' %hist)
        return labels
    
#-------------------------------------------------------------------------
def getLabelSortKey(sample):
    
    if   sample == 'top2': return 1
    elif sample == 'data': return 0    # 11     
    elif sample == 'wzzz': return 2
    elif sample == 'wz': return 2
    elif sample == 'zz': return 4               
    elif sample == 'smww': return 1 # was 3
    elif sample == 'top1': return 4
    elif sample == 'tall': return 5
    elif sample == 'zjet': return 18
    elif sample == 'qflip': return 3       
    elif sample == 'zjhf': return 18
    elif sample == 'zvbf': return 18
    elif sample == 'zall': return 18
    elif sample == 'zjll': return 18
    elif sample == 'zjtt': return 7
    elif sample == 'wjet': return 6
    elif sample == 'wjdt': return 1
    elif sample == 'dqcd': return 18
    elif sample == 'wjdte': return 16
    elif sample == 'wjdtm': return 17
    elif sample == 'zqcd': return 8
    elif sample == 'hggf': return 9
    elif sample == 'hvbf': return 10
    #elif sample == 'data': return 11
    elif sample == 'bkgs': return 12
    elif sample == 'zewk': return 13
    elif sample == 'wqcd': return 14
    elif sample == 'wewk': return 15
    elif sample == 'wdpi': return 16
    elif sample == 'wgas': return 17
    elif sample == 'vvv': return 6
    elif sample == 'ttv': return 7
    elif sample == 'higgs': return 20
    elif sample == 'jpsi': return 21
    elif sample == 'upsl': return 22
    
    log.warning('getSampleSortKey - unknown key: %s' %sample)
    return 100

#-------------------------------------------------------------------------
def getSampleSortKey(sample):
    
    if   sample == 'smww': return 1
    elif sample == 'zqcd': return 3
    elif sample == 'zewk': return 1
    elif sample == 'wqcd': return -2    
    elif sample == 'wewk': return -1
    elif sample == 'top2': return 4
    elif sample == 'top1': return 5
    elif sample == 'tall': return 5
    elif sample == 'higgs': return 8
    elif sample == 'hggf': return 8
    elif sample == 'hvbf': return 9
    elif sample == 'data': return -10
    elif sample == 'bkgs': return 11

    log.warning('getLabelSortKey - unknown key: %s' %sample)
    return 100

#-------------------------------------------------------------------------
def getSampleLabel(sample):
    
    if options.hscale != None:
        hlabel = '%s #times %d' %(options.hmass, options.hscale)
    else:
        hlabel = options.hmass
    
    labels = {
        'smww': 'WW/W#gamma',
        'zjet': 'Z+jets',
        #'zjet': 'Charge Flip',
        'qflip': 'Charge Flip',        
        'zqcd': 'Z+jets QCD',
        'zewk': 'Z+jets EWK',
        'wqcd': 'W+jets QCD',
        'wewk': 'W+jets EWK',        
        'top1': 'Single Top',
        'top2': 't#bar{t}',
        'tall': 'Top',        
        'wzzz': 'ZV',#'WZ/ZZ',
        'wz': 'WZ',
        'zz': 'ZZ',        
        #'wzzz': 'WZ/ZZ/W#gamma',
        'wgam': 'W#gamma',
        'wgas': 'W#gamma*',
        'zgas': 'Z#gamma*',
        'htau':  '%s H#rightarrow#tau#tau'%options.hmass,        
        'hggf':  'ggF Higgs',
        'higgs':  'Higgs',        
        'hvbf':  'Higgs',
        'ttv' : 't#bar{t}V+tV',        
        'data': 'Data',
        'bkgs': 'Total SM',
        }

    try:
        return labels[sample]
    except KeyError:
        log.error('getSampleLabel - unknown sample: %s' %sample)
        sys.exit(1)

#-------------------------------------------------------------------------
def getColor(color_index):

    color_vec=[2, 3, 4, 5, 6,
               ROOT.kBlue   -9,
               ROOT.kGreen  -3,
               ROOT.kCyan   -9,
               ROOT.kYellow +2,
               ROOT.kYellow +1,
               ROOT.kMagenta-3,
               ROOT.kOrange,
               ROOT.kOrange-3,
               ]
    
    if len(color_vec)>color_index:
        return color_vec[color_index]
    return color_index

#-------------------------------------------------------------------------
def getStyle(sample):
    #
    # Read mini dilep ntuple
    #
    color_zewk = ROOT.kBlue   -9
    color_zqcd = ROOT.kGreen  -3
    color_wqcd = ROOT.kGreen  -7
    color_wewk = ROOT.kCyan   -9
    color_top1 = ROOT.kYellow +2
    color_top2 = ROOT.kYellow +1
    color_tall = ROOT.kYellow +1 #ROOT.kRed+1    
    color_wzzz = ROOT.kMagenta-3
    color_wz = ROOT.kTeal-8 #ROOT.kMagenta-3
    color_zz = ROOT.kAzure-4 #ROOT.kMagenta-3        
    color_wgam = ROOT.kOrange
    color_zgam = ROOT.kOrange-3
    color_wdpi = ROOT.kOrange-5
    color_wgas = ROOT.kOrange-7
    color_zgas = ROOT.kOrange-7            
    color_higgs = ROOT.kViolet-9 #ROOT.kRed    +0
    color_higgsall = ROOT.kRed+1 #ROOT.kRed    +0
    color_bkgs = ROOT.kBlue   +1
    color_data = ROOT.kBlack

    styles = {
        'zewk':{'color':color_zewk, 'fill_style':1001, 'marker_style': 0, 'line_width':0, 'leg_opt':'f'},        
        'zqcd':{'color':color_zqcd, 'fill_style':1001, 'marker_style': 0, 'line_width':0, 'leg_opt':'f'},
        'wqcd':{'color':color_wqcd, 'fill_style':1001, 'marker_style': 0, 'line_width':0, 'leg_opt':'f'},
        'wewk':{'color':color_wewk, 'fill_style':1001, 'marker_style': 0, 'line_width':0, 'leg_opt':'f'},
        'top1':{'color':color_top1, 'fill_style':1001, 'marker_style': 0, 'line_width':0, 'leg_opt':'f'},
        'top2':{'color':color_top2, 'fill_style':1001, 'marker_style': 0, 'line_width':0, 'leg_opt':'f'},
        'tall':{'color':color_tall, 'fill_style':1001, 'marker_style': 0, 'line_width':0, 'leg_opt':'f'},        
        'higgs':{'color':color_higgsall, 'fill_style':0, 'marker_style': 0, 'line_width':5,'line_style':2, 'leg_opt':'f'},
        #'hggf':{'color':color_hggf, 'fill_style':1001, 'marker_style': 0, 'line_width':0, 'leg_opt':'f'},
        #'hvbf':{'color':color_hvbf, 'fill_style':0,    'marker_style': 0, 'line_width':0, 'leg_opt':'f'},
        'data':{'color':color_data, 'fill_style':0,    'marker_style':20, 'line_width':0, 'leg_opt':'ple'},
        'bkgs':{'color':color_bkgs, 'fill_style':1001, 'marker_style': 0, 'line_width':0, 'leg_opt':'f'},
        }

    if options.stack_signal:
        styles['higgs']={'color':color_higgs, 'fill_style':3144,    'marker_style': 0, 'line_width':0, 'leg_opt':'f'}

    try:
        return styles[sample]
    except KeyError:
        log.error('getLabel - unknown sample: %s' %sample)
        sys.exit(1)
    
#-------------------------------------------------------------------------
def updateCanvas(can, name=None, leg=None, option = ''):
    
    if not can:
        sys.exit(0)

    can.Modified()        
    can.Update()

    plist = can.GetPad(0).GetListOfPrimitives()

    hists = []
    
    stath = 0.25
    staty = 1.0
    statw = 0.20
    statx = 0.80
    
    for p in plist:
        try:
            if not p.InheritsFrom('TH1'):
                continue
            p.GetYaxis().SetTitleSize(0.055)
            #p.GetYaxis().SetTitleOffset(0.1)            
            hists.append(p)
            stats = p.FindObject('stats')
            
            if stats:
                stats.SetTextColor(p.GetLineColor())
                stats.SetY1NDC(staty-stath)
                stats.SetY2NDC(staty)
                stats.SetX2NDC(statx+statw)
                stats.SetX1NDC(statx)            
                staty = staty - stath
        except:
            print 'Failed'

    can.Modified()
    can.Update()

    if options.wait:
        can.WaitPrimitive()

    if not can:
        sys.exit(0)

    if options.save and name != None:
        if options.do_logy:
            name+='_logy'
        if options.pref != None:
            name = '%s_%s' %(options.pref, name)

        if options.outdir != None:
            if not os.path.exists(options.outdir): os.system('mkdir %s' %(options.outdir))
            name = '%s/%s' %(options.outdir.rstrip(), name)
        
        can.Print('%s.png' %name, 'png')

        if options.do_eps:
            can.Print('%s.eps' %name, 'eps')

        if options.do_pdf:
            #can.SaveAs('%s.pdf' %name)
            can.Print('%s.pdf' %name, 'pdf')   
    
#-------------------------------------------------------------------------
def rescaleFirstBin(hist, scale):

    if not hist or not (scale > 0.0) or hist.GetNbinsX() < 2:
        return

    val = hist.GetBinContent(1)
    err = hist.GetBinError  (1)

    hist.SetBinContent(1, val*scale)
    hist.SetBinError  (1, err*scale)

    xl = hist.GetXaxis().GetBinCenter (1)- 0.3*hist.GetXaxis().GetBinWidth(1)
    yl = hist.GetBinContent(1)+ 5.0*hist.GetBinError(1)
    
    #c = ROOT.TLatex(0.15, 0.1, '#times %.1f' %scale)
    c = ROOT.TLatex(xl, yl, '#times %.1f' %scale)
    c.SetNDC(False)
    c.SetTextFont(42)
    c.SetTextSize(0.035)
    c.SetTextAlign(12)
    c.SetTextColor(ROOT.kBlack)

    return c

#-------------------------------------------------------------------------
class HistEntry:
    """HistEntry - one histogram in a stacked plot"""
        
    def __init__(self, hist, sample, hname, nf_map):
        
        self.sample   = sample
        self.hname    = hname
        self.hist     = hist.Clone()
        self.leg_opt  = 'l'
        self.leg_text = getSampleLabel(sample)
        self.text1st  = None
        self.nf_map   = nf_map
        
        self.hist.SetStats    (False)
        self.hist.SetDirectory(0)

        #
        # Add overflow
        #
        if not options.no_underflow:
            self.hist.SetBinContent(1,self.hist.GetBinContent(0)+self.hist.GetBinContent(1))
            self.hist.SetBinError(1,math.sqrt(self.hist.GetBinError(0)**2+self.hist.GetBinError(1)**2))
            self.hist.SetBinContent(0,0)
            self.hist.SetBinError(0,0)            
            last_bin=self.hist.GetNbinsX()
            # find last bin if option is set
            if 'xmax' in getHistPars(self.hname):
                for mbin in range(0,self.hist.GetNbinsX()+1):
                    if self.hist.GetXaxis().GetBinUpEdge(mbin)>=getHistPars(self.hname)['xmax']:
                        last_bin=mbin
                        break
            #print 'last_bin: ',last_bin,' ',self.hist.GetNbinsX()
            my_err = ROOT.Double(0)
            my_last_bin_val = self.hist.IntegralAndError(last_bin,self.hist.GetNbinsX()+5, my_err)
            self.hist.SetBinContent(last_bin,my_last_bin_val)
            self.hist.SetBinError(last_bin,my_err)
            for mbin in range(last_bin+1,self.hist.GetNbinsX()+2):
                self.hist.SetBinContent(mbin,0.0)
                self.hist.SetBinError(mbin,0.0)                

        if self.sample in self.nf_map:
            self.hist.Scale(self.nf_map[self.sample])
            log.info('Scaling Sample %s by %s ' %(self.sample,self.nf_map[self.sample]))
        self.UpdateStyle(sample)

    def UpdateStyle(self, sample):

        self.sample   = sample
        self.leg_text = getSampleLabel(sample)

        style = getStyle   (sample)
        hpars = getHistPars(self.hname)
        
        self.logy = 'logy' in hpars and hpars['logy']
        if options.do_logy:
            self.logy = options.do_logy
        if 'xtitle' in hpars:
            self.hist.GetXaxis().SetTitle(hpars['xtitle'])
        if 'ytitle' in hpars:
            self.hist.GetYaxis().SetTitle(hpars['ytitle'])            
        if 'color' in style:
            self.hist.SetLineColor(style['color'])
            self.leg_opt = 'f'            

            if 'fill_style' in style and style['fill_style'] > 0:
                self.hist.SetLineColor(ROOT.kBlack)
                self.hist.SetLineWidth(1)
                self.hist.SetFillColor(style['color'])
                self.hist.SetLineColor(style['color'])                
                self.hist.SetFillStyle(style['fill_style'])
                self.leg_opt = 'f'

            elif 'marker_style' in style and style['marker_style'] > 0:
                self.hist.SetMarkerColor(style['color'])
                self.hist.SetMarkerStyle(style['marker_style'])
                self.leg_opt = 'p'

        if 'line_width' in style and style['line_width'] > 0:
            self.hist.SetLineWidth(style['line_width'])
        if 'line_style' in style and style['line_style'] > 0:
            self.hist.SetLineStyle(style['line_style'])

        if 'leg_opt' in style:
            self.leg_opt = style['leg_opt']

        if 'rebin' in hpars and hpars['rebin'] > 1:
            self.hist.Rebin(hpars['rebin'])        
        if 'scale1st' in hpars:
            self.text1st = rescaleFirstBin(self.hist, hpars['scale1st'])
        
    def DrawHist(self, opt=None, leg=None, my_signal=False):
        if self.hist == None:
            return

        if type(opt) == type(''):  
            if options.draw_norm: self.hist.DrawNormalized(opt)
            else:                 self.hist.Draw(opt) 
        if leg != None:
            if my_signal:
                leg.AddEntry(self.hist, self.leg_text,"l")
            else:
                leg.AddEntry(self.hist, self.leg_text, self.leg_opt)

#-------------------------------------------------------------------------
class SystHists:
    """ Collection of systematics histograms for all bakgrounds"""

    def __init__(self):
        pass
    
#-------------------------------------------------------------------------
def getSystSumSortKey(value):    
    return math.fabs(value[1]-value[2])

#-------------------------------------------------------------------------
class DrawStack:
    """DrawStack - a set of histograms for one stacked plot"""
        
    def __init__(self, name, file, sign, data, bkgs, nf_map, extract_sig):

        self.name   = name
        self.selkey = options.selkey
        self.algkey = options.algkey
        self.nf_map = nf_map
        self.file_pointer = file

        self.sign = self.ReadSample(file, sign)
        if options.hscale!=None:
            self.sign.hist.Scale(float(options.hscale))
        self.data = self.ReadSample(file, data)
        self.abkg = None
        self.bkgs = {}
        self.extract_sig = {}        
        self.pads = []
        self.pad  = None

        self.sys_hist = []
        self.sys_bkgs = {}
        self.sys_sigs = {}
        self.error_map= {}
        
        self.bkg_table = None
        self.sig_table = None        
        
        self.stack    = None
        self.stackeg  = None
        self.leg      = None
        self.texts    = None
        self.ratio    = None
        self.err_bands= []    
        sum = 0.0

        self.sign.hist.SetLineWidth(2)
        log.info('DrawStack  - integral=%5.2f sample=%s' %(self.data.hist.Integral(), 'data'))        
        log.info('DrawStack  - integral=%5.2f sample=%s' %(self.sign.hist.Integral(), 'signal'))
        for bkg in bkgs:
            self.bkgs[bkg] = self.ReadSample(file, bkg)

        for extract_s in extract_sig:
            self.extract_sig[extract_s] = self.ReadSample(file, extract_s)
        sum_err_total = 0.0
        e_double=ROOT.Double(0.0)
        for bkg in bkgs:
            log.info('DrawStack  - integral=%5.2f error=%5.2f mean=%5.2f rms=%5.2f sample=%s' %(self.bkgs[bkg].hist.IntegralAndError(0,10000,e_double), e_double,
                                                                                               self.bkgs[bkg].hist.GetMean(), self.bkgs[bkg].hist.GetRMS(), bkg))
            errdouble = ROOT.Double(0.0)
            sum += self.bkgs[bkg].hist.IntegralAndError(0,10001,errdouble)
            sum_err_total+=errdouble*errdouble
        sum_err_total=math.sqrt(sum_err_total)
        log.info('DrawStack  - integral=%5.2f +/- %5.2f sample=total bkg' %(sum,sum_err_total))
            
    def GetHistPath(self, sample, syst=None):

        if self.name.count('lim') and options.syst_sel != None:
            histname = '%s_%s_%s' %(sample, self.selkey, options.syst_sel)
        else:
            histname = '/%s/%s_%s/%s' %(self.selkey, self.algkey, sample, self.name)

        if syst != None and options.syst_sel != None:
            histname = histname.replace(options.syst_sel, syst)

        return histname

    def ReadSample(self, file, sample, syst=None, DO_SYMM=False):

        path = self.GetHistPath(sample, syst)
        hist = file.Get(path)

        if not hist:
            file.ls()
            raise KeyError('DrawStack - missing histogram: file=%s hist=%s' %(file.GetPath(), path))

        log.debug('ReadSample - integral=%5.1f sample=%s, syst=%s' %(hist.Integral(), sample, syst))

        if DO_SYMM:
            print 'COMPUTING systematic'
            hist_central_value = self.file_pointer.Get(path)
            self.Symmeterize(hist_central_value, hist)
            
        return HistEntry(hist, sample, self.name, self.nf_map)

    #------------------------
    def Symmeterize(self, hnom, hvar):
        #
        # Symmeterize(nominal_histogram, variation_histogram)
        #    This function symmeterizes the systematics for the track met
        #       using the lognormal variation: Nominal/Up_variation 
        #    The variations for var/nom<0.5 are treated special so that very 
        #       large variations do not occur because of low MC stats.
        for i in range(0,hnom.GetNbinsX()+1):
            diff_up = 1.0
            if hnom.GetBinContent(i)>0.0 and hvar.GetBinContent(i)>0.0:
                diff_up = hvar.GetBinContent(i)/hnom.GetBinContent(i)
                if diff_up<0.5:
                    diff_up=0.5
            hvar.SetBinContent(i, (1.0/diff_up)*hnom.GetBinContent(i)) # this is:  nominal * (nominal / up_variation)

    #-------------------------
    def ReadSystFiles(self, sfiles):
        
        for syst, sfile in sfiles.iteritems():

            # check if we need to symmeterize
            DO_SYMM=False
            if syst in symm_list:
                DO_SYMM=True
            
            bkg_ent = None
            
            for bkg in self.bkgs:
                bhist = self.ReadSample(sfile, bkg, syst, DO_SYMM=DO_SYMM)

                if bkg_ent == None:
                    bkg_ent = bhist
                else:
                    bkg_ent.hist.Add(bhist.hist)
            if bkg_ent == None:
                log.warning('ReadSysts - missing background syst histograms: %s' %syst)
                sys.exit(1)

            bkg_ent.sample = 'bkgs'
            self.sys_bkgs[syst] = bkg_ent
            self.sys_sigs[syst] = self.ReadSample(sfile, self.sign.sample, syst, DO_SYMM=DO_SYMM)

    #-------------------------
    def GetTotalBkgHist(self):

        bhist = None
        
        for bkg, ent in self.bkgs.iteritems():
            if bhist == None:
                bhist = ent.hist.Clone()
                bhist.SetDirectory(0)
            else:
                bhist.Add(ent.hist)
                
        return bhist

    #--------------------------
    def PrintBkgSystYields(self):

        sum_nom = 0.0
        sum_sys = []
        
        for bkg, ent in self.bkgs.iteritems():
            sum_nom += ent.hist.Integral()

        for sys, ent in self.sys_bkgs.iteritems():
            sum_sys += [(sys, ent.hist.Integral(), sum_nom)]

        log.info('PrintBkgSystYields - sum_nom=%3.1f' %(sum_nom))

        for value in sorted(sum_sys, key=getSystSumSortKey):
            log.info('                     sum_sys=%3.1f %s' %(value[1], value[0]))

        h = ROOT.TH1D('bkg_syst', 'bkg_syst', len(sum_sys), 0.0, len(sum_sys))
        h.SetDirectory(0)
        
        if sum_nom > 0.0:
            sum_sys = sorted(sum_sys, key = lambda val: val[0])
            
            for i in range(0, len(sum_sys)):
                sum = sum_sys[i]
                h.SetBinContent(i+1, sum[1]/sum_nom)
                h.GetXaxis().SetBinLabel(i+1, sum[0])

        return h

    #----------------------
    def PrintSigSystYields(self):

        sum_nom = self.sign.hist.Integral()
        sum_sys = []
        
        for sys, ent in self.sys_sigs.iteritems():
            sum_sys += [(sys, ent.hist.Integral(), sum_nom)]

        log.info('PrintSigSystYields - sum_nom=%3.1f' %(sum_nom))

        for value in sorted(sum_sys, key=getSystSumSortKey):
            log.info('                     sum_sys=%3.1f %s' %(value[1], value[0]))

        h = ROOT.TH1D('sig_syst', 'sig_syst', len(sum_sys), 0.0, len(sum_sys))
        h.SetDirectory(0)

        if sum_nom > 0.0:
            sum_sys = sorted(sum_sys, key = lambda val: val[0])
            
            for i in range(0, len(sum_sys)):
                sum = sum_sys[i]
                h.SetBinContent(i+1, sum[1]/sum_nom)
                syst_name_map=syst_names()
                my_name=sum[0]
                if sum[0] in syst_name_map:
                    my_name=syst_name_map[sum[0]]
                h.GetXaxis().SetBinLabel(i+1, my_name)

        return h
    
    #------------------------
    def GetBkgSystBinError(self, ibin):

        cbin = 0.0
        cval = 0.0
        cerr = 0.0
        
        for bkg, ent in self.bkgs.iteritems():
            if ibin >= 0 and ibin <= ent.hist.GetNbinsX()+1:
                cval += ent.hist.GetBinContent(ibin)
                cbin  = ent.hist.GetBinCenter (ibin)
                
        for sys, ent in self.sys_bkgs.iteritems():
            if ibin >= 0 and ibin <= ent.hist.GetNbinsX()+1:                
                sval = ent.hist.GetBinContent(ibin)
                cerr += (cval-sval)*(cval-sval)

                ratio = 0.0
                if cval > 0.0:
                    ratio = sval/cval
                
                log.debug('GetBkgSystBinError - bin=%3d center=%6.1f val=%3.2f: sval=%3.2f ratio=%1.2f syst=%s' %(ibin, cbin, cval, sval, ratio, sys))
        
        return (cval, math.sqrt(cerr))

    #------------------------
    def PlotSystSig(self, syst, can):
        if syst not in self.sys_sigs:
            return None

        log.info('PlotSystSig - %s: %s' %(self.name, syst))

        sys = self.sys_sigs[syst].hist.Clone()
        sig = self.sign.hist.Clone()

        sig.SetLineWidth(2)
        sys.SetLineWidth(2) 

        sig.SetLineColor(1)
        sys.SetLineColor(2)

        hpars = getHistPars(self.name)
        sys.GetXaxis().SetTitle(hpars['xtitle'])        
        sys.GetXaxis().CenterTitle()

        sig_sum = sig.Integral()
        sys_sum = sys.Integral()        

        log.info('   draw ratio')
        sys.Divide(sig)

        if math.fabs(sys.GetMinimum()-1.0) < 0.15 and math.fabs(sys.GetMaximum()-1.0) < 0.15:
            sys.GetYaxis().SetRangeUser(0.80, 1.20)
        elif math.fabs(sys.GetMinimum()-1.0) < 0.7 and math.fabs(sys.GetMaximum()-1.0) < 0.7:
            sys.GetYaxis().SetRangeUser(0.20, 1.80)
        else:
            sys.GetYaxis().SetRangeUser(0.0, 3.0)
        sys.GetYaxis().SetRangeUser(0.7, 1.3)

        sys.GetYaxis().SetTitle('Nominal/%s' %syst)
        sys.GetYaxis().CenterTitle()        
        if options.draw_norm: sys.DrawNormalized('HIST')
        else: sys.Draw('HIST')

        t = '#splitline{Nominal: %.3f}{%s: %.3f}' %(sig_sum, syst, sys_sum)        
        l = ROOT.TLatex(0.5, 0.85, t)
        l.SetNDC()
        l.SetTextFont(42)
        l.SetTextSize(0.04)
        l.SetTextAlign(11)
        l.SetTextColor(ROOT.kBlack)
        l.Draw()

        p = getSelKeyLabel(options.selkey) + ' (signal)'
        if p != None:            
            c = ROOT.TLatex(0.2, 0.96, p)
            c.SetNDC()
            c.SetTextFont(42)
            c.SetTextSize(0.04)
            c.SetTextAlign(12)
            c.SetTextColor(ROOT.kBlack)
        
        updateCanvas(can, name='%s_%s_%s_sig' %(getSelKeyPath(), self.name, syst))

    #----------------------
    def PlotSystBkg(self, syst, can):
        if syst not in self.sys_bkgs:
            return None

        log.info('PlotSystBkg - %s: %s' %(self.name, syst))

        sys = self.sys_bkgs[syst].hist.Clone()
        bkg = self.GetTotalBkgHist()

        bkg.SetLineWidth(2)
        sys.SetLineWidth(2)        

        bkg.SetLineColor(1)
        sys.SetLineColor(4)

        bkg.SetFillColor(0)
        bkg.SetFillStyle(0)        

        sys.SetFillColor(0)
        sys.SetFillStyle(0)  

        hpars = getHistPars(self.name)
        sys.GetXaxis().SetTitle(hpars['xtitle'])        
        sys.GetXaxis().CenterTitle()

        bkg_sum = bkg.Integral()
        sys_sum = sys.Integral()        

        sys.Divide(bkg)
        log.info('   draw bkg ratio: min/max = %.2f/%.2f' %(sys.GetMinimum(), sys.GetMaximum()))

        if math.fabs(sys.GetMinimum()-1.0) < 0.15 and math.fabs(sys.GetMaximum()-1.0) < 0.15:
            sys.GetYaxis().SetRangeUser(0.80, 1.20)
        elif math.fabs(sys.GetMinimum()-1.0) < 0.7 and math.fabs(sys.GetMaximum()-1.0) < 0.7:
            sys.GetYaxis().SetRangeUser(0.0, 1.80)            
        else:
            sys.GetYaxis().SetRangeUser(0.0, 3.0)
        sys.GetYaxis().SetRangeUser(0.7, 1.3)            
            
        sys.GetYaxis().SetTitle('%s/Nominal' %syst)
        sys.GetYaxis().CenterTitle()        
        
        if options.draw_norm: sys.DrawNormalized('HIST')
        else:  sys.Draw('HIST')

        t = '#splitline{Nominal: %.2f}{%s: %.2f}' %(bkg_sum, syst, sys_sum)        
        l = ROOT.TLatex(0.5, 0.85, t)
        l.SetNDC()
        l.SetTextFont(42)
        l.SetTextSize(0.04)
        l.SetTextAlign(11)    
        l.SetTextColor(ROOT.kBlack)
        l.Draw()

        p = getSelKeyLabel(options.selkey) + ' (sum of backgrounds)'
        if p != None:            
            c = ROOT.TLatex(0.2, 0.96, p)
            c.SetNDC()
            c.SetTextFont(42)
            c.SetTextSize(0.04)
            c.SetTextAlign(12)
            c.SetTextColor(ROOT.kBlack)
        
        updateCanvas(can, name='%s_%s_%s_bkg' %(getSelKeyPath(), self.name, syst))

    #-------------------
    def PlotManySyst(self, systs, can, isSignal=False, fillData=False):
        #if syst not in self.sys_bkgs:
        #    return None
        if len(self.pads)>1:
            self.pads[0].Clear()
            self.pads[1].Clear()
            self.pads[0].cd()            
            self.pads[0].SetBottomMargin(0.15);
        sys=[]
        ratio_sys = []
        for s in systs:
            if isSignal:
                sys       += [self.sys_sigs[s].hist.Clone()]
                ratio_sys += [self.sys_sigs[s].hist.Clone()]                
            else:                   
                sys       += [self.sys_bkgs[s].hist.Clone()]
                ratio_sys += [self.sys_bkgs[s].hist.Clone()]

        #fillData=True
        #self.pads[0].SetLogy(1)
        mydata=None
        if fillData:
            mydata = self.data.hist.Clone()
            mydata.SetLineWidth(2)
            mydata.SetLineColor(1)
            mydata.SetFillColor(0)
            mydata.SetFillStyle(0)        
        
        bkg = self.GetTotalBkgHist()
        if isSignal:
            bkg = self.sign.hist.Clone()            
        bkg.SetLineWidth(2)
        bkg.SetLineColor(2)
        bkg.SetFillColor(0)
        bkg.SetFillStyle(0)        
        
        hpars = getHistPars(self.name)

        bkg.GetXaxis().SetTitle(hpars['xtitle'])        
        bkg.GetYaxis().SetTitle(hpars['ytitle'])        
        max_bin = bkg.GetMaximum()
        # Set the systematics plots
        tmp_color=3
        i=0
        for s in sys:

            log.info('PlotManySyst - %s: %s Mean: %0.2f RMS: %0.2f' %(self.name, systs[i], s.GetMean(), s.GetRMS()))
            s.SetLineColor(getColor(tmp_color))
            s.SetMarkerColor(getColor(tmp_color))
            s.SetLineWidth(2)        
            s.SetFillColor(0)
            s.SetFillStyle(0)
            tmp_color+=1
            i+=1
            if max_bin<s.GetMaximum():
                max_bin = s.GetMaximum()
        
        bkg.GetYaxis().SetRangeUser(0.0, 1.2*max_bin)
        self.UpdateHist(bkg)
        bkg.Draw('HIST E0')
        if fillData:
            mydata.Draw('SAME')        
        for s in sys:
            s.Draw('HIST SAME')

        p = getSelKeyLabel(options.selkey) + ' (sum of backgrounds)'
        if isSignal:
            p = getSelKeyLabel(options.selkey) + ' (sum of signal)'            
        if p != None:            
            c = ROOT.TLatex(0.2, 0.96, p)
            c.SetNDC()
            c.SetTextFont(42)
            c.SetTextSize(0.04)
            c.SetTextAlign(12)
            c.SetTextColor(ROOT.kBlack)
            c.Draw()
        self.texts = getATLASLabels(can, 0.2, 0.88, selkey=self.selkey)
        for text in self.texts:
            text.Draw()

        self.leg = ROOT.TLegend(0.51, 0.62, 0.93, 0.89)
        self.leg.SetBorderSize(0)
        self.leg.SetFillStyle (0)
        #self.leg.SetNColumns  (2)
        self.leg.SetTextFont(42);    
        self.leg.SetTextSize(0.04);         
        if fillData:
            self.leg.AddEntry(mydata, 'Data')                
        self.leg.AddEntry(bkg,    'Nominal')
        i=0        
        while i<len(systs):
            self.leg.AddEntry(sys[i],systs[i])
            i+=1
        self.leg.Draw()

        # Draw the ratios
        if len(self.pads)>1:
            self.pads[1].cd()
            
            # Set the ratio histograms
            tmp_color=3
            bkg_ratio=bkg.Clone()
            if fillData:
                bkg_ratio.Divide(mydata)
            for s in ratio_sys:
                
                # Divide
                if fillData:
                    s.Divide(mydata)
                else:
                    s.Divide(bkg)

                # SetRange
                if math.fabs(s.GetMinimum()-1.0) < 0.15 and math.fabs(s.GetMaximum()-1.0) < 0.15:
                    s.GetYaxis().SetRangeUser(0.80, 1.20)
                elif math.fabs(s.GetMinimum()-1.0) < 0.5 and math.fabs(s.GetMaximum()-1.0) < 0.5:
                    s.GetYaxis().SetRangeUser(0.50, 1.50)
                elif math.fabs(s.GetMinimum()-1.0) < 1.0 and math.fabs(s.GetMaximum()-1.0) < 1.0:
                    s.GetYaxis().SetRangeUser(0.0, 2.00)
                else:
                    s.GetYaxis().SetRangeUser(0.0, 3.0)

                # Style
                s.SetLineColor(getColor(tmp_color))
                s.SetMarkerColor(getColor(tmp_color))                
                s.SetLineWidth(2)
                s.SetFillColor(0)
                s.SetFillStyle(0)
                if fillData:
                    s.GetYaxis().SetTitle('%s / Data' %'Syst')
                    if tmp_color==3:
                        self.UpdateHist(bkg_ratio)
                        bkg_ratio.GetYaxis().SetTitle('%s / Data' %'Syst')
                        bkg_ratio.GetYaxis().SetRangeUser(0.80, 1.20)                        
                        bkg_ratio.Draw('HIST')
                else:
                    s.GetYaxis().SetTitle('%s / Nominal' %'Syst')                    
                s.GetYaxis().CenterTitle()        
                tmp_color+=1
                
                if tmp_color==4 and not fillData:
                    self.UpdateHist(s)
                    s.GetYaxis().SetRangeUser(0.80, 1.20)                                            
                    s.Draw('HIST')
                else:
                    s.Draw('HIST SAME')                    

        if isSignal:
            updateCanvas(can, name='%s_%s_%s_sig' %(getSelKeyPath(), self.name, 'systall'))
        else:
            updateCanvas(can, name='%s_%s_%s_bkg' %(getSelKeyPath(), self.name, 'systall'))              

    #------------------------------
    def PlotSystTables(self, can):

        self.bkg_table = self.PrintBkgSystYields()
        self.sig_table = self.PrintSigSystYields()
        
        if self.bkg_table == None or self.sig_table == None:
            return

        #
        # Draw background
        #
        self.bkg_table.SetFillStyle(2001)
        self.bkg_table.SetFillColor(4)
        
        self.bkg_table.SetStats(False)
        self.bkg_table.GetYaxis().SetRangeUser(0.82, 1.18)

        self.bkg_table.GetYaxis().SetTitle('Systematics/Nominal')
        self.bkg_table.GetYaxis().CenterTitle()
        self.bkg_table.GetYaxis().SetTitleOffset(1.0)         
        self.bkg_table.GetYaxis().SetTitleSize(0.05)
        self.bkg_table.GetYaxis().SetLabelSize(0.05)        
        self.bkg_table.GetXaxis().SetLabelSize(0.05)
                
        if options.draw_norm: self.bkg_table.DrawNormalized('HBAR')
        else: self.bkg_table.Draw('HBAR')

        p = getSelKeyLabel(options.selkey)
        if p != None:
            p +=  ' (backgrounds)'
            c = ROOT.TLatex(0.30, 0.95, p)
            c.SetNDC()
            c.SetTextFont(42)
            c.SetTextSize(0.04)
            c.SetTextAlign(12)
            c.SetTextColor(ROOT.kBlack)
        
        updateCanvas(can, name='%s_%s_bkg_table' %(getSelKeyPath(), self.name))

        #
        # Draw signal
        #
        self.sig_table.SetFillStyle(2001)
        self.sig_table.SetFillColor(2)
        
        self.sig_table.SetStats(False)
        #self.sig_table.GetYaxis().SetRangeUser(0.82, 1.18)
        self.sig_table.GetYaxis().SetRangeUser(0.82, 1.18)        

        self.sig_table.GetYaxis().SetTitle('Systematics/Nominal')
        self.sig_table.GetYaxis().CenterTitle()
        self.sig_table.GetYaxis().SetTitleOffset(1.0)         
        self.sig_table.GetYaxis().SetTitleSize(0.05)
        self.sig_table.GetYaxis().SetLabelSize(0.05)        
        self.sig_table.GetXaxis().SetLabelSize(0.05)

        my_line = ROOT.TLine(1.0,0,1.0,len(self.sys_sigs))
        my_line.SetLineColor(1)
        my_line.SetLineWidth(3)
        my_line.SetLineStyle(2)
        my_line.Draw('same')
        p = getSelKeyLabel(options.selkey)
        if p != None:
            p += ' (signal)'
            c = ROOT.TLatex(0.30, 0.95, p)
            c.SetNDC()
            c.SetTextFont(42)
            c.SetTextSize(0.04)
            c.SetTextAlign(12)
            c.SetTextColor(ROOT.kBlack)
        
        updateCanvas(can, name='%s_%s_sig_table' %(getSelKeyPath(), self.name))
    #-------------------------------------
    def IsLogy(self):
        if options.do_logy: return True
        if options.no_logy: return False
        
        if self.sign != None and self.sign.logy:
            return True
        if self.data != None and self.data.logy:
            return True

        return False
    
    #-------------------------------------
    def GetErrorHists(self):
        bkg_herr = self.stack.GetHistogram().Clone()
        norm_hists_bkg=[]
        for hk,hg in self.bkgs.iteritems():
            norm_hists_bkg+=[hg.hist.Clone()]
            bkg_herr.Add(hg.hist)
        return norm_hists_bkg,bkg_herr
    
    #-------------------------------------
    def Draw(self, can):
        log.info('DrawStack - draw: %s' %self.name)
        
        #self.leg = ROOT.TLegend(0.58, 0.72, 0.85, 0.89)
        self.leg = ROOT.TLegend(0.51, 0.67, 0.93, 0.89)        
        self.leg.SetBorderSize(0)
        self.leg.SetFillStyle (0)
        self.leg.SetTextFont(42);    
        self.leg.SetTextSize(0.04);
        self.leg1= ROOT.TLegend(0.51, 0.52, 0.83, 0.67)
        self.leg1.SetBorderSize(0)
        self.leg1.SetFillStyle (0)
        self.leg1.SetTextFont(42);    
        self.leg1.SetTextSize(0.04);        
        self.pads=[]
        can.cd()
        if options.do_ratio or options.force_ratio:
            # CAF setup
            ratioPadRatio  = 0.3;
            markerSize = 1;
            lineWidth = 2;
            markerStyle = 20;
            padScaling      = 0.75 / (1. - ratioPadRatio) ;
            ratioPadScaling = 0.75*(1. / ratioPadRatio) ;  
            ROOT.gStyle.SetPadTopMargin(0.065);
            ROOT.gStyle.SetPadRightMargin(0.05);
            ROOT.gStyle.SetPadBottomMargin(0.16);
            ROOT.gStyle.SetPadLeftMargin(0.16);
            ROOT.gStyle.SetTitleXOffset(1.0);
            ROOT.gStyle.SetTitleYOffset(1.28);            
            self.pads.append( ROOT.TPad('pad0','pad0', 0.0, ratioPadRatio, 1.0, 1.0) )
            self.pads.append( ROOT.TPad('pad1','pad1', 0.0, 0.0, 1.0, ratioPadRatio) )

            self.pads[0].SetTopMargin(padScaling * self.pads[0].GetTopMargin());
            self.pads[0].SetBottomMargin(.015);
            self.pads[0].SetTickx(True);
            self.pads[0].SetTicky(True);
            #self.pads[1].SetTopMargin(.01);
            self.pads[1].SetBottomMargin(.4);            
            #self.pads[1].SetBottomMargin(ratioPadScaling * self.pads[1].GetBottomMargin());
            self.pads[1].SetGridy(True);
            self.pads[1].SetTickx(True);
            self.pads[1].SetTicky(True);
            
            if False:
                self.pads[0].SetTicky(0)
                # Margins                                                                                                                               
                tmargin = 0.05
                lmargin = 0.15
                rmargin = 0.28
                bmargin = 0.18              
                
                for pad in self.pads:
                    pad.SetFrameLineColor(0)
                    pad.SetLeftMargin(lmargin)
                    pad.SetRightMargin(rmargin)
                    pad.SetTopMargin(tmargin+bmargin)
                    pad.SetBottomMargin(bmargin-0.03)
                    pad.SetFillColor(0)
                    pad.SetFillStyle(0)
                    pad.Draw()
                if len(self.pads)>1:
                    rmargin_ = 0.2
                    self.pads[0].SetTopMargin(tmargin+bmargin)
                    self.pads[0].SetRightMargin(rmargin_)
                    self.pads[0].SetBottomMargin(0.0)
                    self.pads[1].SetTopMargin(0.0)
                    self.pads[1].SetBottomMargin(tmargin+bmargin)
                    self.pads[1].SetFrameLineColor(1)
                    self.pads[1].SetRightMargin(rmargin_)
                    self.pads[1].SetTicky(1) # RHS ticks 
            else:
                self.pads[0].Draw()
                self.pads[1].Draw()

            ipad = 0
            self.pad = self.pads[ipad]
            self.pad.cd()

        if self.IsLogy():
            can.SetLogy(1)
            if options.do_ratio:
                self.pads[0].SetLogy(1)
        else:
            can.SetLogy(0)

        self.CreateStack()

        if options.draw_norm: self.bkg_sum.DrawNormalized('HIST') 
        else:                 self.stack.Draw('HIST')

        if not options.stack_signal:
            self.UpdateHist(self.sign.hist,self.sign.sample)
            self.sign.DrawHist('SAME HIST', self.leg, True)
        self.UpdateStack()                    
        if options.do_ratio or options.force_ratio:
            #self.UpdateStack()            
            bx = self.stack.GetXaxis();
            by = self.stack.GetYaxis();
            #if not options.draw_norm:
            #    bx = self.bkg_sum.GetXaxis();
            #    by = self.bkg_sum.GetYaxis();                
            bx.SetTitleSize(ROOT.gStyle.GetTitleSize("x") * padScaling);
            bx.SetLabelSize(ROOT.gStyle.GetLabelSize("x") * padScaling);
            by.SetTitleSize(ROOT.gStyle.GetTitleSize("y") * padScaling);
            by.SetTitleOffset(ROOT.gStyle.GetTitleOffset("y") / padScaling  );
            by.SetLabelSize(ROOT.gStyle.GetLabelSize("y") * padScaling);
            bx.SetLabelColor(0);
            bx.SetTickLength(bx.GetTickLength() * padScaling);
            #print 'OFFSET'
            bx.SetLabelOffset(1.2); 
            bx.SetLabelSize(0.03);
            bx.SetTitle("")
            #bx.SetTitle("")            
            by.SetRangeUser(0,80);
            by.SetTitleSize(0.055);
            by.SetTitleOffset(1.28);
            by.SetLabelSize(0.05);
            by.SetLabelOffset(0.01);


        # Add Data
        if self.data != None and not options.blind:
            #self.data.hist.GetXaxis().SetLabelColor(0)
            self.data.hist.GetXaxis().SetTitle("")
            self.data.DrawHist('SAME', None)        

        if True:
            self.bkg_sum.SetLineColor(ROOT.kRed)
            self.bkg_sum.SetFillColor(0)
            self.bkg_sum.GetXaxis().SetLabelColor(0)
            if options.draw_norm: self.bkg_sum.DrawNormalized('HIST SAME')
            else: self.bkg_sum.Draw('HIST SAME')
            self.bkg_sum_alt=self.bkg_sum.Clone()
            self.bkg_sum_alt.SetLineColor(ROOT.kRed)
            self.bkg_sum_alt.SetMarkerColor(ROOT.kRed)            
            self.bkg_sum_alt.SetMarkerSize(0)
            self.bkg_sum_alt.SetFillColor(1)
            self.bkg_sum_alt.SetFillStyle(3004)
        self.leg.Draw()
        self.leg1.Draw()        

        self.texts = getATLASLabels(can, 0.19, 0.86, selkey=self.selkey)
        for text in self.texts:
            text.Draw()

        if self.data.text1st != None:
            log.info('Draw 1st bin text...')
            self.data.text1st.Draw()

        #
        # Draw systematics error band around total background stack
        #
        if options.draw_syst:
            bkg_herr = self.stack.GetHistogram().Clone()
            bkg_herr.GetXaxis().SetLabelColor(0)
            bkg_herr.GetXaxis().SetTitle("")
            for ibin in range(1, bkg_herr.GetNbinsX()+1):
                val, err = self.GetBkgSystBinError(ibin)
                bkg_herr.SetBinContent(ibin, val)
                bkg_herr.SetBinError  (ibin, err)
                
            self.stackeg = ROOT.TGraphAsymmErrors(bkg_herr)

            #self.stackeg.SetFillStyle(3005)
            self.stackeg.SetFillStyle(3004)
            self.stackeg.SetFillColor(1)
            self.stackeg.GetXaxis().SetLabelColor(0)            
            #self.stackeg.Draw('2')
        #
        # Draw chi2 for stack and data
        #
        if True and not options.blind:
            chi2 = self.data.hist.Chi2Test      (self.bkg_sum, 'UW CHI2')
            kval = self.data.hist.KolmogorovTest(self.bkg_sum, '')
            
            log.info('Draw - %s: chi2 = %.2f' %(self.name, chi2))
            log.info('Draw - %s: KS   = %.2f' %(self.name, kval))
            
            self.ks_text = ROOT.TLatex(0.3, 0.95, 'KS: %.2f' %kval)
            self.ks_text.SetNDC()
            self.ks_text.SetTextSize(0.045)
            self.ks_text.SetTextAlign(11)    
            self.ks_text.SetTextColor(ROOT.kBlack)

        # Plot - calculating the systematic error bands
        norm_hists_bkg=[]
        for hk,hg in self.bkgs.iteritems(): norm_hists_bkg+=[hg.hist.Clone()]
        syst_hist_bkg=ROOT.TGraphAsymmErrors(self.bkg_sum); self.err_bands+=[syst_hist_bkg]
        syst_ratio=syst_hist_bkg.Clone();                   self.err_bands+=[syst_ratio]
        self.SystBand(norm_hists_bkg, syst=syst_hist_bkg, syst_ratio=syst_ratio, linestyle=0, tot_bkg=self.bkg_sum, other_syst=self.stackeg)

        # Setting the draw options
        syst_hist_bkg.SetFillStyle(3004)
        syst_hist_bkg.SetFillColor(12)
        syst_hist_bkg.SetMarkerColor(1)
        syst_hist_bkg.SetLineColor(1)
        syst_hist_bkg.GetXaxis().SetLabelColor(0)
        self.error_map['bkg']=syst_hist_bkg.Clone()
        self.error_map['bkg'].GetXaxis().SetLabelColor(0)        
        if options.draw_norm: pass #self.error_map['bkg'].DrawNormalized('SAMEE2')
        else: self.error_map['bkg'].Draw('SAMEE2')

        # Draw Arrow
        if self.name in ['mjj','ptll_over_met','ptj0_over_met']:
            cut = 1.9
            if self.name=='mjj':
                cut=350.0
            if self.name=='ptll_over_met':
                cut=0.4
            if self.name=='ptj0_over_met':
                cut=1.9                               
            self.arrow = ROOT.TArrow( cut, 0.2, cut, 0.0, 0.04, '|>' )
            self.arrow.SetFillStyle( 1001 )
            self.arrow.SetLineColor( ROOT.kRed )
            self.arrow.SetFillColor( ROOT.kRed )        
            self.arrow.Draw()
            self.my_line2 = ROOT.TLine(cut,0.0,cut,0.3*self.stack.GetMaximum())
            if options.do_logy:
                self.my_line2 = ROOT.TLine(cut,0.0,cut,0.06*self.stack.GetMaximum())            
            self.my_line2.SetLineColor(ROOT.kRed)
            self.my_line2.SetLineWidth(2)
            self.my_line2.SetLineStyle(1)
            self.my_line2.Draw('same')
        
        if options.do_ratio or options.force_ratio:
            # Ratio
            ipad = 1
            #self.pad = self.pads[ipad]
            #self.pad.cd()
            self.pads[ipad].cd()
            self.ratio=self.data.hist.Clone()
            self.UpdateHist(self.ratio)
            self.ratio.SetMinimum(0.25)
            self.ratio.SetMaximum(1.75)
            #self.ratio.SetMinimum(0.0)
            #self.ratio.SetMaximum(2.0)

            if options.do_nf!=None:
                samples = options.do_nf.split(',')
                self.ratio=self.data.hist.Clone()
                den=None
                tot_bkg=0.0; tot_data=0.0; tot_zgam=0.0
                tot_data=self.ratio.Integral(4,101)                

                for bkg, ent in self.bkgs.iteritems():
                    if bkg in samples:                        
                        if den==None:
                            den=ent.hist.Clone()
                        else:
                            den.Add(ent.hist)
                        tot_zgam+=ent.hist.Integral(4,101)
                    else:
                        self.ratio.Add(ent.hist, -1.0)
                        tot_bkg+=ent.hist.Integral(4,101)
                # Divide
                self.ratio.Divide(den)
                for i in range(0,self.ratio.GetNbinsX()+1):
                    if i<6:
                        print self.ratio.GetXaxis().GetBinLowEdge(i),' mean: ',self.ratio.GetBinContent(i),' +/- ',self.ratio.GetBinError(i)

                #print:
                print (tot_data-tot_bkg)/tot_zgam,' +/- ',math.sqrt(tot_data)/tot_zgam*(tot_data-tot_bkg)/tot_zgam,
            else:
                self.ratio.Divide(self.bkg_sum)                
            
            # Set Names
            pars = getHistPars(self.name)
            if 'xtitle' in pars and self.bkg_sum.GetXaxis() != None:
                self.ratio.GetXaxis().SetTitle(pars['xtitle'])
            self.ratio.GetYaxis().SetTitle('Data / SM ')

            if options.blind:
                for i in range(0,self.ratio.GetNbinsX()+1):
                    self.ratio.SetBinError(i,0.0)
                    self.ratio.SetBinContent(i,0.0)
                    
            # Setting the size of ratio font        
            bx = self.ratio.GetXaxis();
            by = self.ratio.GetYaxis();
            self.ratio.SetMarkerSize(1.2);
            self.ratio.SetMarkerStyle(20);
            self.ratio.SetLineColor(ROOT.kBlack);
            self.ratio.SetLineWidth(2);
            
            #print 'Y:',ROOT.gStyle.GetTitleY();
            #ROOT.gStyle.SetTitleY(0.5);
            bx.SetTitleSize(ROOT.gStyle.GetTitleSize("x") * ratioPadScaling);
            bx.SetLabelSize(ROOT.gStyle.GetLabelSize("x") * ratioPadScaling);
            by.SetTitleSize(ROOT.gStyle.GetTitleSize("y") * ratioPadScaling);
            #by.SetTitleOffset(ROOT.gStyle.GetTitleOffset("y") / ratioPadScaling  );
            by.SetTitleOffset(ROOT.gStyle.GetTitleOffset("y") / ratioPadScaling  );
            #by.	CenterTitle(True);
            by.SetLabelSize(ROOT.gStyle.GetLabelSize("y") * ratioPadScaling);
            bx.SetTickLength(ROOT.gStyle.GetTickLength() * ratioPadScaling);

            #bx.SetTitle("Observable");
            #bx.SetTitle("Data/SM");
            bx.SetLabelSize(0.13);
            bx.SetLabelOffset(0.02);
            bx.SetTitleSize(0.14);
            bx.SetTitleOffset(1.2);
            
            by.SetRangeUser(0,2);
            by.SetLabelSize(0.13);
            by.SetLabelOffset(0.0125);
            by.SetTitleSize(0.14);
            by.SetTitleOffset(0.5);
            by.SetNdivisions(5);            
            
            self.ratio.DrawCopy()

            #
            # Draw ratio error band                                              
            #
            self.error_map['bkg_ratio'] = syst_ratio.Clone()
            #self.error_map['bkg_ratio'].SetFillStyle(3354)
            self.error_map['bkg_ratio'].SetFillStyle(3004)
            self.error_map['bkg_ratio'].SetFillColor(ROOT.kBlack)
            self.error_map['bkg_ratio'].SetMarkerColor(1)
            self.error_map['bkg_ratio'].SetMarkerSize(0)
            self.error_map['bkg_ratio'].SetLineColor(1)

            self.error_map['bkg_ratio'].Draw('SAME E2')

            # Overlay the ratio plot on top of errors
            self.ratio.Draw('same')

            self.pads[ipad].RedrawAxis()
            self.pads[ipad].Update()

    #-----------------------------
    def SystBand(self, hists=[], syst=None, syst_ratio=None, linestyle=0, tot_bkg=None,other_syst=None):

        if len(hists)<2:
            log.info('MvaPlot - ERROR plot_syst_err_band does not have enough histograms to compute uncertainity: %s' %(len(hists)))
        
        # Draw
        nom=None
        for i, hist in enumerate(hists):
            #self.format_syst(hist, i, linestyle)

            if i==0 or True: # HACKING TO RUN only statistical error
                if not nom:
                    nom=hist.Clone()                
                    for j in range(1,nom.GetNbinsX()+1):
                        syst.SetPointEYhigh(j-1,nom.GetBinError(j))
                        syst.SetPointEYlow(j-1,nom.GetBinError(j))                        
                else:
                    nom.Add(hist)
                    for j in range(1,hist.GetNbinsX()+1):
                        e1=hist.GetBinError(j)
                        e2=syst.GetErrorYhigh(j-1)
                        err_quad=math.sqrt(e1*e1+e2*e2)
                        syst.SetPointEYhigh(j-1,err_quad)
                        syst.SetPointEYlow(j-1,err_quad)

                continue
            
            # HACKING TO RUN only statistical error
            if False: # HACKING TO RUN only statistical error
                for m in range(1,nom.GetNbinsX()+1):
                    e1=(nom.GetBinContent(m)-hist.GetBinContent(m))
                    if e1>0:
                        e2=syst.GetErrorYhigh(m-1)
                        new_e = ROOT.Double(math.sqrt(e1*e1+e2*e2))
                        syst.SetPointEYhigh(m-1,new_e)
                    elif e1<0:
                        e2=syst.GetErrorYlow(m-1)
                        new_e = ROOT.Double(math.sqrt(e1*e1+e2*e2))
                        syst.SetPointEYlow(m-1,new_e)

        #if other_syst!=None and False:
        #if True:
            #print 'drawing this symmetric error: '
            for m in range(1,nom.GetNbinsX()+1):
                #adding 50\% error
                print 'bins: ',m
                #if nom.GetXaxis().GetBinUpEdge(m)<=12.0 and False:
                #    #syst.SetPointEYhigh(m-1,math.sqrt(syst.GetErrorYhigh(m-1)**2+(3.5*nom.GetBinContent(m))**2))
                #    #syst.SetPointEYlow(m-1,math.sqrt(syst.GetErrorYlow(m-1)**2+(3.5*nom.GetBinContent(m))**2))
                #
                #    syst.SetPointEYhigh(m-1,math.sqrt((3.5*nom.GetBinContent(m))**2))
                #    syst.SetPointEYlow(m-1,math.sqrt((3.5*nom.GetBinContent(m))**2))                    
                #else:
                #    #syst.SetPointEYhigh(m-1,math.sqrt(syst.GetErrorYhigh(m-1)**2+(0.25*nom.GetBinContent(m))**2))
                #    #syst.SetPointEYlow(m-1,math.sqrt(syst.GetErrorYlow(m-1)**2+(0.25*nom.GetBinContent(m))**2))
                #    syst.SetPointEYhigh(m-1,math.sqrt((0.25*nom.GetBinContent(m))**2))
                #    syst.SetPointEYlow(m-1,math.sqrt((0.25*nom.GetBinContent(m))**2))                                    
                if other_syst:
                    e1=other_syst.GetErrorYhigh(m-1)
                    e2=syst.GetErrorYhigh(m-1)
                    new_e = ROOT.Double(math.sqrt(e1*e1+e2*e2))
                    syst.SetPointEYhigh(m-1,new_e)
                    e2=syst.GetErrorYlow(m-1)
                    new_e = ROOT.Double(math.sqrt(e1*e1+e2*e2))
                    syst.SetPointEYlow(m-1,new_e)

        for sys, ent in self.sys_bkgs.iteritems():
            #if ibin >= 0 and ibin <= ent.hist.GetNbinsX()+1:                
            #    sval = ent.hist.GetBinContent(ibin)
            #    cerr += (cval-sval)*(cval-sval)
            if True: # HACKING TO RUN only statistical error
                for m in range(1,nom.GetNbinsX()+1):
                    nom_val=nom.GetBinContent(m)
                    e1=(ent.hist.GetBinContent(m)-nom_val)
                    #print 'e1: ',e1,' nom_val: ',nom_val,' variation: ',ent.hist.GetBinContent(m)
                    #print 'stat error: ',nom.GetBinError(m),' asym: ',syst.GetErrorYhigh(m-1)
                    if e1>0:
                        e2=syst.GetErrorYhigh(m-1)
                        new_e = ROOT.Double(math.sqrt(e1*e1+e2*e2))
                        syst.SetPointEYhigh(m-1,new_e)
                    elif e1<0:
                        e2=syst.GetErrorYlow(m-1)
                        new_e = ROOT.Double(math.sqrt(e1*e1+e2*e2))
                        syst.SetPointEYlow(m-1,new_e)
        #    
        # Calculate the systematic band for a ratio plot  
        #  
        x1=ROOT.Double()
        y1=ROOT.Double()
        for j in range(1,tot_bkg.GetNbinsX()+1):
            # Set Y value to 1  
            syst_ratio.GetPoint(j-1,x1,y1)
            syst_ratio.SetPoint(j-1,x1,1.0)
            val=tot_bkg.GetBinContent(j)
            if val==0.0:
                continue

            #  
            # Normalize error  
            #   
            eyu=syst.GetErrorYhigh   (j-1)/val
            eyd=syst.GetErrorYlow    (j-1)/val
            syst_ratio.SetPointEYhigh(j-1,eyu)
            syst_ratio.SetPointEYlow (j-1,eyd)
            #print 'err up: ',eyu,' down: ',eyd

        return

    def CreateStack(self):
        self.stack   = ROOT.THStack(self.name, self.name)
        self.bkg_sum = None
    
        for bkg in sorted(self.bkgs.keys(), key=getSampleSortKey):

            if self.bkgs[bkg].sample=='smww' or self.bkgs[bkg].sample=='wzzz': ## doug wzzz
                for bb in range(0,self.bkgs[bkg].hist.GetNbinsX()):
                    my_err = self.bkgs[bkg].hist.GetBinError(bb)
                    my_int = self.bkgs[bkg].hist.GetBinContent(bb)
                    self.bkgs[bkg].hist.SetBinError(bb,math.sqrt(my_err**2+(0.09*my_int)**2))
            
            he = self.bkgs[bkg]
            self.stack.Add(he.hist)


            if self.bkg_sum == None:
                self.bkg_sum = he.hist.Clone()
                if options.draw_norm:
                    self.bkg_sum.SetFillColor  (219)
                    self.bkg_sum.SetMarkerColor(219)
                    self.bkg_sum.SetLineColor  (219)
            else:
                self.bkg_sum.Add(he.hist)

        if self.data != None and not options.blind:
            self.leg.AddEntry(self.data.hist,'Data')
            self.bkg_sum_altb=self.data.hist.Clone()
            self.bkg_sum_altb.SetLineColor(ROOT.kRed)
            self.bkg_sum_altb.SetMarkerColor(ROOT.kRed)            
            self.bkg_sum_altb.SetMarkerSize(0)
            self.bkg_sum_altb.SetFillColor(1)
            #self.bkg_sum_altb.SetFillStyle(3005)
            self.bkg_sum_altb.SetFillStyle(3004)            
                        
        for bkg in sorted(self.bkgs.keys(), key=getLabelSortKey):
            he = self.bkgs[bkg]
            he.DrawHist(None, self.leg)

    #---------------------
    def UpdateStack(self):

        pars = getHistPars(self.name)
        
        if 'xtitle' in pars and self.stack.GetXaxis() != None:
            self.stack.GetXaxis().SetTitle(pars['xtitle'])
        
        if 'ytitle' in pars and self.stack.GetYaxis() != None:
            self.stack.GetYaxis().SetTitle(pars['ytitle'])

        ymax = self.GetYaxisMax()
        if ymax > 0.0:
            if self.IsLogy():
                self.stack.SetMaximum(25.0*ymax)
                self.stack.SetMinimum(0.1)
            else:
                self.stack.SetMaximum( 1.8*ymax)
                self.stack.SetMinimum(0.0)
                
        if 'ymin' in pars:
            self.stack.SetMinimum(pars['ymin'])
        elif options.ymin != None:
            self.stack.SetMinimum(options.ymin)
        if 'bin_labels' in pars:
            n=1
            for labeli in pars['bin_labels']:
                self.stack.GetXaxis().SetBinLabel(n,labeli)
                n+=1
        if 'ymax' in pars:
            self.stack.SetMaximum(pars['ymax'])
        elif options.ymax != None:
            self.stack.SetMaximum(options.ymax)
            pars['ymax']=options.ymax
        #else:
        #    ['ymax']=self.stack.GetMaximum()
        if options.do_logy:
            self.stack.SetMinimum(0.1)
        if 'xmax' in pars:
            self.stack.GetXaxis().SetRangeUser(0.0,pars['xmax'])
        elif options.xmax != None:
            self.stack.GetXaxis().SetRangeUser(options.xmin,options.xmax)
    #--------------------
    def UpdateHist(self,h, sample=None):

        pars = getHistPars(self.name)
        if 'xtitle' in pars and h.GetXaxis() != None:
            h.GetXaxis().SetTitle(pars['xtitle'])
        
        if 'ytitle' in pars and h.GetYaxis() != None:
            h.GetYaxis().SetTitle(pars['ytitle'])

        ymax = self.GetYaxisMax()
        if ymax > 0.0:
            if self.IsLogy():
                h.SetMaximum(15.0*ymax)
                h.SetMinimum(0.1)
            else:
                h.SetMaximum( 1.3*ymax)
                h.SetMinimum(0.0)
                
        if 'ymin' in pars:
            h.SetMinimum(pars['ymin'])
        elif options.ymin != None:
            h.SetMinimum(options.ymin)
        if 'bin_labels' in pars:
            n=1
            for labeli in pars['bin_labels']:
                h.GetXaxis().SetBinLabel(n,labeli)
                n+=1
        if 'ymax' in pars:
            h.SetMaximum(pars['ymax'])
        elif options.ymax != None:
            h.SetMaximum(options.ymax)

        if sample!=None:
            style = getStyle(sample)
            if 'line_width' in style:
                h.SetLineWidth(style['line_width'])
            if 'line_style' in style:
                h.SetLineStyle(style['line_style'])
            
        if 'xmax' in pars:
            h.GetXaxis().SetRangeUser(0.0,pars['xmax'])
        elif options.xmax != None:
            h.GetXaxis().SetRangeUser(options.xmin,options.xmax)

    #--------------------
    def GetYaxisMax(self):
        ymax = 0.0
        
        ymax = max([ymax, self.GetHistMax(self.data.hist)])
        ymax = max([ymax, self.GetHistMax(self.sign.hist)])
        
        if self.stack != None:
            ymax = max([ymax, self.stack.GetMaximum()])

        return ymax

    #---------------------------
    def GetHistMax(self, hist):
        ymax = None

        for ibin in range(1, hist.GetNbinsX()+1):
            val = hist.GetBinContent(ibin)
            err = hist.GetBinError  (ibin)
            
            if val > 0.0:
                if ymax == None:
                    ymax = val + err
                else:
                    ymax = max([ymax, val+err])

        return ymax

#-------------------------------------------------------------------------
def getSystFileList(rpath):
    
    paths = {}
    vetos = ['MuRescaleUp','MuRescaleDown']
    
    #systs = ['el_fr_n','el_fr_p','mu_fr_n','mu_fr_p'] #hstudy.getSystVarHWWWinter(options,returnVals=True)
    systs = ['btag_cj_p','btag_cj_n','btag_lj_n','btag_lj_p','eer_n','eer_p','ees_low_n','ees_low_p','ees_mat_n','ees_mat_n','ees_mat_p','ees_ps_n','ees_z_n','ees_z_p','el_eff_n','el_eff_p','id_n','id_p','jer','jes_n','jes_p','jvf_n','jvf_p','ms_n','ms_p','mu_eff_n','mu_eff_p','pileup_n','pileup_p','tau_eff_n','tau_eff_p','qflip_n','qflip_p','btag_bj_n','btag_bj_p','el_stat_fr_p', 'el_stat_fr_n', 'mu_stat_fr_p', 'mu_stat_fr_n', 'lep_corr_fr_p',
        'lep_corr_fr_n','bch_up','bch_dn','scalest_p','scalest_n','resost']#'xsec_n','xsec_p','nom','el_fr_n','el_fr_p','mu_fr_p','mu_fr_n',
    #systs = ['el_fr_n','el_fr_p','mu_fr_p'] #hstudy.getSystVarHWWWinter(options,returnVals=True)    
    if rpath.count('%s/' %options.syst_sel) != 1 or not options.draw_syst:
        log.info('getSystFileList - ignore path with incorrect format: %s' %rpath)
        return {}

    for syst in sorted(systs):
        if syst in vetos:
            continue

        if syst != options.syst_sel:
            npath = rpath.replace(options.syst_sel, syst)

            if os.path.isfile(npath):
                rfile  = ROOT.TFile(npath, 'READ')
                paths[syst] = rfile
                log.info('getSystFileList - %-20s path: %s' %(syst, npath))
            else: log.error('getSystFileList - %-20s path: %s' %(syst, npath))
                
    return paths

#---
def syst_names():

    syst_name_map={'jes_n':'JES Down',
                   'jvf_n':'JVF Down',
                   'jes_p':'JES Up',
                   'jvf_p':'JVF Up',
                   'qflip_p':'Charge Flip Up',
                   'qflip_n':'Charge Flip Down',
                   'ms_p':'Muon Scale Up',
                   'ms_n':'Muon Scale Down',
                   'mu_eff_p':'Muon Eff Up',
                   'mu_eff_n':'Muon Eff Down',
                   'tau_eff_n':'Tau Eff Down',
                   'tau_eff_p':'Tau Eff Up',
                   'el_eff_n':'Electron Eff Down',
                   'el_eff_p':'Electron Eff Up',
                   'ees_low_p': 'Electron Scale Low p_{T} Up',
                   'ees_low_n': 'Electron Scale Low p_{T} Down',                   
                   'btag_cj_p':'Btag Charm Up',
                   'btag_cj_n':'Btag Charm Down',
                   'btag_lj_n':'Btag Light Down',
                   'btag_lj_p':'Btag Light Up',
                   'btag_bj_n':'Btag Bottom Down',
                   'btag_bj_p':'Btag Bottom Up',
                    'scalest_p':'MET Scale Up',
                    'scalest_n':'MET Scale Down',
                    'resost':'MET Resolution',

                    'ees_z_p':'Electron Scale Up',
                    'ees_z_n':'Electron Scale Down',
                    'ees_mat_p':'Electron Material Up',
                    'ees_mat_n':'Electron Material Down',
                    'ees_ps_p':'Electron Presampler Up',
                    'ees_ps_n':'Electron Presampler Down',

                    'eer_p':'Electron Resolution Up',
                    'eer_n':'Electron Resolution Down',
                    'bch_up' : 'BCH Up',
                    'bch_dn' : 'BCH Down',
                    
                   'jer':'JER',
                   'pileup_p':'Pileup Up',
                   'pileup_n':'Pileup Down',
                   'id_p':'Muon ID Resolution Up',
                   'id_n':'Muon ID Resolution Down',
                   'mu_fr_n':'ID Resolution Down',
                   'el_stat_fr_p':'Electron FR Stat Up',
                   'el_stat_fr_n':'Electron FR Stat Down',
                   'mu_stat_fr_p':'Muon FR Stat Up',
                   'mu_stat_fr_n':'Muon FR Stat Down',                   
                    'lep_corr_fr_p':'FR Closure Up',
                    'lep_corr_fr_n':'FR Closure Down',
                   }
    return syst_name_map

#-------------------------------------------------------------------------
def writeSystTex(table_name, stack):

    try:
        out = open(table_name+'.table','w')
    except:
        print 'table_name: ',table_name,' does not exist'


    out.write('\\resizebox{\\textwidth}{!} { \n')
    out.write('\\begin{tabular}{l||llll|l}\n')
    out.write('\\hline\\hline\n')
        
    syst_name_map=syst_names()
    
    bkg_herr =  stack.sys_bkgs
    deleteme,hnom = stack.GetErrorHists()
    nom_err=ROOT.Double(0.0)
    nom_val = hnom.IntegralAndError(0,2001,nom_err)
    systs=[]
    total_uncer_up=0.0
    total_uncer_down=0.0    
    for sys, ent in bkg_herr.iteritems():
        if nom_val<=0.0:
            nom_val=1.0
        my_ratio=(ent.hist.Integral(0,1001)-nom_val)/nom_val
        print sys,' ',ent.hist.Integral(0,1001),' nom: ',nom_val,' frac: ',my_ratio
        sys_name = sys
        if sys in syst_name_map:
            sys_name=syst_name_map[sys]
        systs+=[[sys_name,my_ratio]]
        if my_ratio>0.0:
            total_uncer_up+=my_ratio*my_ratio
        else:
            total_uncer_down+=my_ratio*my_ratio            
   
    # Sort systematics
    for i in range(0,len(systs)):

        for j in range(i+1,len(systs)):
            if systs[i][1]*systs[i][1]<systs[j][1]*systs[j][1]:
                tmp=systs[i]
                systs[i]=systs[j]
                systs[j]=tmp

    my_order=["lep_corr_fr_p",
    "lep_corr_fr_n",
    "jes_n",
    "jes_p",
    "jer",
    "el_stat_fr_p",
    "el_stat_fr_n",
    "el_eff_p",
    "el_eff_n",
    "ees_mat_n",
    "ees_low_p",
    "eer_p",
    "jvf_p",
    "pileup_p",
    "ees_z_p",
    "ees_z_n",
    "mu_stat_fr_p",
    "pileup_n",
    "mu_stat_fr_n",
    "mu_eff_p",
    "mu_eff_n",
    "eer_n",
    "id_n",
    "ees_low_n",
    "ms_n",
    "qflip_p",
    "qflip_n",
    "ees_mat_p",
    "ms_p",
    "ees_ps_n",
    "btag_cj_p",
    "btag_cj_n",    
    "btag_lj_n",
    "tau_eff_p",
    "btag_bj_n",
    "tau_eff_n",
    "jvf_n",
    "ees_ps_p",
    "btag_lj_p",
    "id_p",
    "btag_bj_p",'bch_up','bch_dn','scalest_p','scalest_n','resost']

    my_order=['jes_n',
'btag_bj_n',
'jvf_n',
'ees_z_p',
'mu_stat_fr_p',
'ees_ps_n',
'tau_eff_p',
'mu_stat_fr_n',
'bch_up',
'jvf_p',
'btag_bj_p',
'jes_p',
'pileup_n',
'ms_n',
'bch_dn',
'id_n',
'ees_z_n',
'id_p',
'btag_lj_p',
'ms_p',
'pileup_p',
'btag_lj_n',
'ees_low_n',
'scalest_n',
'mu_eff_p',
'ees_low_p',
'scalest_p',
'tau_eff_n',
'jer',
'el_eff_n',
'lep_corr_fr_n',
'btag_cj_p',
'btag_cj_n',
'eer_p',
'el_stat_fr_p',
'ees_mat_n',
'mu_eff_n',
'resost',
'ees_mat_p',
'el_stat_fr_n',
'eer_n',
'el_eff_p',
'lep_corr_fr_p',]
        
    if True:
        for key in my_order:
            for s in systs:
                #print s
                tmp_key=''
                for kk,ll in syst_name_map.iteritems():
                    if s[0]==ll:
                        tmp_key=kk
                        break
                if s[0]==key or key==tmp_key:
                    my_space=''
                    for nnn in range(0,25-len(s[0])):
                        my_space+=' '
                    line= s[0]+my_space+' & '+'%0.4f \\\\' %(s[1])                    
                    #line=' & '+'%0.4f ' %(s[1])
                    out.write('%s\n' %line)            
    else:

        for s in systs:
            #print '"%s",' %s[0]
            my_space=''
            for nnn in range(0,25-len(s[0])):
                my_space+=' '
            line= s[0]+my_space+' & '+'%0.4f \\\\' %(s[1])
            #line= s[0]
            #line='%s & '+'%0.4f ' %(s[0],s[1])
            out.write('%s\n' %line)        
    # Print errors
    my_err_up=math.sqrt(total_uncer_up)
    my_err_dw=math.sqrt(total_uncer_down)    
    syst_err_up=my_err_up*nom_val
    syst_err_dw=my_err_dw*nom_val    
    data_val= stack.data.hist.Integral(0,1001)
    data_err = math.sqrt(data_val)

    out.write('Total Uncertainty & $\\pm_{%0.4f}^{%0.4f}$ \\\\ ' %(my_err_dw,my_err_up))
    out.write('\\hline \\hline\n')
    out.write('Total Bkg & %0.2f $\\pm$ %0.2f (stat)$\\pm_{%0.2f}^{%0.2f}$ (syst) \\\\ \n' %(nom_val,nom_err,syst_err_dw,syst_err_up))
    out.write('Observed & %0.0f $\\pm$ %0.2f \\\\ \n' %(data_val,data_err))
    out.write('\\end{tabular}\n')
    out.write('}\n')
    out.close()
    
#-------------------------------------------------------------------------
def main():

    if len(args) != 1:
        log.error('Need exactly one input argument: %s' %str(args))
        sys.exit(1)

    if options.blind:
        options.do_ratio=False
        log.info('Ratio turned off because histogram is blinded!')

    rpath = args[0]

    if not os.path.isfile(rpath):
        log.error('Input argument is not a valid file: %s' %rpath)
        sys.exit(1)

    if options.selkey == None:
        log.error('Missing required option: --selkey=<directory name>')
        sys.exit(1)

    rfile  = ROOT.TFile(rpath, 'READ')
    sfiles={}    
    sfiles = getSystFileList(rpath) # Turned off.
    
    #
    # Select histograms and samples for stacks
    #
    #bkgs = ['zewk', 'zqcd','wewk','wqcd','top1','top2']
    bkgs = ['zewk', 'zqcd','wewk','wqcd','tall']  

    if options.stack_signal:
        if not 'higgs' in bkgs: bkgs+=['higgs']

    # Signal events to extract
    extract_sig=[]
    if options.extract_sig!=None:
        extract_sig = options.extract_sig.split(',')
        
    vars = ['mll', 'ptll', 'pttot', 'mt', 'dphill', 'outbdt', 'outknn']
    nf_map={}
    if options.sf_file!=None:
        sf_file=open(options.sf_file,'r')
        for l in sf_file:
            sfs1=l.split(' ')
            try:
            #if sfs1[0]==_opts.weight: pass
            #else: continue                
                if sfs1[0].strip()=='top':
                    nf_map['top2']=float(sfs1[1].strip())
                    nf_map['top1']=float(sfs1[1].strip())
                elif sfs1[0].strip()=='z' or sfs1[0].strip()=='zSF' or sfs1[0].strip()=='zOF':
                    nf_map['zjet']=float(sfs1[1].strip())
                else: nf_map[sfs1[0].strip()]=float(sfs1[1].rstrip('\n').strip())
            except:  print 'Could not read: ',sfs1
        log.info('NF map: %s' %nf_map)
        sf_file.close()

    if options.vars != None:
        vars = options.vars.split(',')

    #config.setPlotDefaults(ROOT)
    Style()
    can = ROOT.TCanvas('stack', 'stack', 500, 500)
    can.Draw()
    can.cd()

    stacks = []

    for var in vars:

        stack = DrawStack(var, rfile, 'higgs', 'data', bkgs, nf_map, extract_sig)  
        if options.draw_syst:
            if len(sfiles):
                stack.ReadSystFiles(sfiles)
            
        stack.Draw(can)
        stacks += [stack]

        if options.syst == 'SysAll':
            cname='%s_%s_Nominal' %(getSelKeyPath(), var)
        else:
            cname='%s_%s_%s' %(getSelKeyPath(), var, options.syst)

        updateCanvas(can, name=cname)

        if options.syst_see == 'allsyst':
            stack.PlotManySyst(sfiles.keys(), can, isSignal=True)
            stack.PlotManySyst(sfiles.keys(), can, fillData=(not options.blind))

        for syst in sorted(sfiles.keys()):
            if options.syst_see == 'all' or options.syst_see == syst:
                stack.PlotSystSig(syst, can)
                stack.PlotSystBkg(syst, can)

    if options.syst == 'SysAll' and options.make_syst_table:
        
        ROOT.gStyle.SetPadLeftMargin  (0.28)
        ROOT.gStyle.SetPadRightMargin (0.08)
        ROOT.gStyle.SetPadBottomMargin(0.10)
        
        can = ROOT.TCanvas('table', 'table', 600, 850)
        can.Draw()
        can.cd()
        
        for stack in stacks:
            stack.PlotSystTables(can)
    if options.syst_table:
        writeSystTex(options.syst_table, stack)
            
    # Delete Memory
    can.Clear()
    del stacks
    rfile.Close()
    del rfile
    return

###########################################################################
# Main function for command line execuation
#
if __name__ == "__main__":
    main()