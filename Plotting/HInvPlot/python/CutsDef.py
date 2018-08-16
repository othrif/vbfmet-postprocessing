
import os
import sys
#import PyCintex
import ROOT

import HInvPlot.JobOptions as config

from HInvPlot.Base import ExecBase
from HInvPlot.Base import CutItem
import HInvPlot.Vars as get_vars

log = config.getLog('CutsDef.py')

#-------------------------------------------------------------------------
class BasicCuts:
    """
    Basic analysis selection:
      Required parameters:
        - analysis type and channel

      Optional parameters:
    """
        
    def __init__(self, Analysis, Chan, SameSign=0):

        if Analysis != 'allmjj':
            raise NameError('BasicCuts - unknown analysis string: %s' %Analysis)
        
        self.analysis = Analysis
        self.chan     = Chan
        self.SameSign = SameSign
        
    def PadKey(self, key, val, pf=None, sf=None):
        if len(key) > 0: key += '_'
        if pf != None: key += pf
        key += '%s' %val
        if sf != None: key += sf
        return key

    def GetSelKey(self, chan=None):

         key = ''
    
         if self.analysis !=None: key = self.PadKey(key, self.analysis)
         if self.SameSign == 1:   key = self.PadKey(key, 'ss')

         if chan != None:
             if      chan !=None: key = self.PadKey(key,      chan)
         else:
             if self.chan !=None: key = self.PadKey(key, self.chan)
         
         return key

    def GetChan(self):
        return self.chan

    def IsSameFlavor(self):
        if self.chan in ['uu','ee','ll']:
            return True
        return False

#-------------------------------------------------------------------------
def getLepChannelCuts(basic_cuts):

    cuts = [] 

    if   basic_cuts.chan == None or basic_cuts.chan == 'aa':  pass
    elif basic_cuts.chan == 'nn': cuts += [CutItem('CutChannel', 'chanFlavor==1')]
    elif basic_cuts.chan == 'eu': cuts += [CutItem('CutChannel', 'chanFlavor==11')]
    elif basic_cuts.chan == 'uu': cuts += [CutItem('CutChannel', 'chanFlavor==7')]
    elif basic_cuts.chan == 'ee': cuts += [CutItem('CutChannel', 'chanFlavor==9')]
    elif basic_cuts.chan == 'ss': cuts += [CutItem('CutChannel', 'chanFlavor==8 || chanFlavor==6')]
    elif basic_cuts.chan == 'ep': cuts += [CutItem('CutChannel', 'chanFlavor==4')]
    elif basic_cuts.chan == 'e': cuts += [CutItem('CutChannel', 'chanFlavor==4 || chanFlavor==5')]
    elif basic_cuts.chan == 'u': cuts += [CutItem('CutChannel', 'chanFlavor==2 || chanFlavor==3')]
    elif basic_cuts.chan == 'l': cuts += [CutItem('CutChannel', 'chanFlavor==2 || chanFlavor==3 || chanFlavor==4 || chanFlavor==5')]           
    elif basic_cuts.chan == 'em': cuts += [CutItem('CutChannel', 'chanFlavor==5')]
    elif basic_cuts.chan == 'up': cuts += [CutItem('CutChannel', 'chanFlavor==2')]
    elif basic_cuts.chan == 'um': cuts += [CutItem('CutChannel', 'chanFlavor==3')]
    elif basic_cuts.chan == 'll': cuts += [CutItem('CutChannel', 'chanFlavor==7 || chanFlavor==9')]
    else:
        raise KeyError('getHInvBasicCuts - invalid channel configuration: %s' %basic_cuts.chan)

    #
    # Find matching cuts
    #
    return GetCuts(cuts)

#-------------------------------------------------------------------------
def getSRCuts(cut = '', basic_cuts=None, ignore_met=False):

    cuts = []

    cuts += [CutItem('CutTrig',      'trigger_met == 1')]
    cuts += [CutItem('CutJetClean',  'passJetCleanTight == 1')]
    cuts += getLepChannelCuts(basic_cuts)    
    cuts += [CutItem('CutNjet',  'n_jet == 2')]
    cuts += [CutItem('CutJ0Pt',  'jetPt0 > 80.0')]        
    cuts += [CutItem('CutJ1Pt',  'jetPt1 > 50.0')]
    #cuts += [CutItem('CutMetSig', 'mll < 116.0 && mll > 76.0')]
    
    if cut == 'BeforeMET':
        return GetCuts(cuts)    
    if not ignore_met:
        cuts += [CutItem('CutMet',  'met_tst_et > 180.0')]

    cuts += [CutItem('CutDPhijj',   'jj_dphi < 1.8')]        
    cuts += [CutItem('CutDPhiMetj0','met_tst_j1_dphi > 1.0')]        
    cuts += [CutItem('CutDPhiMetj1','met_tst_j2_dphi > 1.0')]        
    cuts += [CutItem('CutOppHemi','etaj0TimesEtaj1 < 0.0')] 
    cuts += [CutItem('CutDEtajj','jj_deta > 4.8')] 
    #cuts += [CutItem('CutMjj','jj_mass > 500.0')]

    return GetCuts(cuts)

#-------------------------------------------------------------------------
def getZCRCuts(cut = '', basic_cuts=None, ignore_met=False):

    cuts = []

    cuts += [CutItem('CutTrig',      'trigger_lep == 1')]
    cuts += [CutItem('CutJetClean',  'passJetCleanTight == 1')]
    cuts += getLepChannelCuts(basic_cuts)    
    cuts += [CutItem('CutNjet',  'n_jet == 2')]
    cuts += [CutItem('CutJ0Pt',  'jetPt0 > 80.0')]        
    cuts += [CutItem('CutJ1Pt',  'jetPt1 > 50.0')]
    cuts += [CutItem('CutL0Pt',  'lepPt0 > 30.0')]
    cuts += [CutItem('CutMll',   'mll < 116.0 && mll > 76.0')]
    #cuts += [CutItem('CutMetSig', 'mll < 116.0 && mll > 76.0')]    
    
    if cut == 'BeforeMET':
        return GetCuts(cuts)    
    if not ignore_met:
        cuts += [CutItem('CutMet',  'met_tst_nolep_et > 180.0')]

    if basic_cuts.chan=='ee':
        cuts += [CutItem('CutLepVeto',   'n_mu == 0')]        
    if basic_cuts.chan=='uu':
        cuts += [CutItem('CutLepVeto',   'n_el == 0')]        
        
    cuts += [CutItem('CutDPhijj',   'jj_dphi < 1.8')]        
    cuts += [CutItem('CutDPhiMetj0','met_tst_nolep_j1_dphi > 1.0')]        
    cuts += [CutItem('CutDPhiMetj1','met_tst_nolep_j2_dphi > 1.0')]        
    cuts += [CutItem('CutOppHemi','etaj0TimesEtaj1 < 0.0')] 
    cuts += [CutItem('CutDEtajj','jj_deta > 4.8')] 
    #cuts += [CutItem('CutMjj','jj_mass > 500.0')]

    return GetCuts(cuts)

#-------------------------------------------------------------------------
def getWCRCuts(cut = '', basic_cuts=None, ignore_met=False):

    cuts = []

    cuts += [CutItem('CutTrig',      'trigger_lep == 1')]
    cuts += [CutItem('CutJetClean',  'passJetCleanTight == 1')]
    cuts += getLepChannelCuts(basic_cuts)    
    cuts += [CutItem('CutNjet',  'n_jet == 2')]
    cuts += [CutItem('CutJ0Pt',  'jetPt0 > 80.0')]        
    cuts += [CutItem('CutJ1Pt',  'jetPt1 > 50.0')]
    cuts += [CutItem('CutL0Pt',  'lepPt0 > 30.0')]
    
    if cut == 'BeforeMET':
        return GetCuts(cuts)    
    if not ignore_met:
        cuts += [CutItem('CutMet',  'met_tst_nolep_et > 180.0')]

    cuts += [CutItem('CutDPhijj',   'jj_dphi < 1.8')]        
    cuts += [CutItem('CutDPhiMetj0','met_tst_nolep_j1_dphi > 1.0')]        
    cuts += [CutItem('CutDPhiMetj1','met_tst_nolep_j2_dphi > 1.0')]        
    cuts += [CutItem('CutOppHemi','etaj0TimesEtaj1 < 0.0')] 
    cuts += [CutItem('CutDEtajj','jj_deta > 4.8')] 
    #cuts += [CutItem('CutMjj','jj_mass > 500.0')]

    return GetCuts(cuts)

#-------------------------------------------------------------------------
def GetCutsObject(reg,cuts,options,alg_name):
    #
    # Fill Registry with cuts and samples for cut-flow
    #
    _fillPassEventRegistry(reg, cuts, options, Debug='no', Print='no')

    return ExecBase(alg_name, 'PassEvent', ROOT.Msl.PassEvent(), reg)

#-------------------------------------------------------------------------
def GetCuts(cuts):

    #
    # Find matching cuts
    #
    res = []

    for cut in cuts:
        res += [cut]
        
        if cut == cut.GetCutName():
            break

    return res
    
#-------------------------------------------------------------------------
def fillSampleList(reg=None, key=None,options=None, basic_cuts=None):
    
    sigs = {}
    sigs['higgs'] = ['hggf','hvh','hvbf']
    sigs['hggf']  = ['hggf']
    sigs['hvh']   = ['hvh']
    sigs['hvbf']  = ['hvbf']
    
    bkgs = {}
    bkgs['wqcd'] = ['wqcd']
    bkgs['zqcd'] = ['zqcd']
    bkgs['wewk'] = ['wewk']
    bkgs['zewk'] = ['zewk']
    bkgs['top1'] = ['top1']
    bkgs['top2'] = ['top2']
    bkgs['tall'] = ['top2','top1']    

    samples = {}
    samples.update(sigs)
    samples.update(bkgs)

    samples['data'] = ['data']
    samples['bkgs'] = []

    for bkg in bkgs.itervalues():
        if bkg not in samples['bkgs']:
            samples['bkgs'] += bkg

    #
    # Save samples (type list by hand to preserve order)
    #
    if reg != None and key != None:
        reg.SetVal(key, 'higgs,top1,top2,wqcd,wewk,zqcd,zewk,bkgs,data')
        for k, v in samples.iteritems():
            reg.SetVal(k, ','.join(v))

    return samples

#-------------------------------------------------------------------------
def _fillPassEventRegistry(reg, cuts, options, basic_cuts=None, *arguments, **keywords):
    #
    # Fill Registry with cuts
    #
    cuts_val = ''

    for cut in cuts:
        cuts_val += '%s ' %cut.GetCutName()
        reg.SetVal('PassEvent::%s' %cut.GetCutName(), cut.GetRegistry())

    reg.SetVal('PassEvent::Cuts',     cuts_val)
    reg.SetVal('PassEvent::WriteAll', 'yes')
    if options.prec:
        reg.SetVal('PassEvent::Precision',11)    

    if options.print_raw:
        reg.SetVal('PassEvent::PrintRaw', 'yes')
    if options.print_evt:
        reg.SetVal('PassEvent::PrintEvents', 'yes')
    for key, var in keywords.iteritems():
        if type(var) == type([]):
            reg.SetVal('PassEvent::%s' %key, ','.join(var))
        elif type(var) == bool:
            if var: reg.SetVal('PassEvent::%s' %key, 'yes')
            else  : reg.SetVal('PassEvent::%s' %key, 'no')
        elif var != None:
            reg.SetVal('PassEvent::%s' %key, var)

    #
    # Fill list of samples for cut-flow tables and histograms
    #
    fillSampleList(reg, 'PassEvent::Sets', options, basic_cuts)

#-------------------------------------------------------------------------
def preparePassEventForSR(alg_name, options, basic_cuts, cut='BASIC'):

    reg  = ROOT.Msl.Registry()

    cuts = getSRCuts(cut, basic_cuts, ignore_met=options.ignore_met)

    #
    # Fill Registry with cuts and samples for cut-flow
    #
    _fillPassEventRegistry(reg, cuts, options, basic_cuts, Debug='no', Print='no')

    return ExecBase(alg_name, 'PassEvent', ROOT.Msl.PassEvent(), reg)

#-------------------------------------------------------------------------
def preparePassEventForZCR(alg_name, options, basic_cuts, cut='BASIC'):

    reg  = ROOT.Msl.Registry()

    cuts = getZCRCuts(cut, basic_cuts, ignore_met=options.ignore_met)

    #
    # Fill Registry with cuts and samples for cut-flow
    #
    _fillPassEventRegistry(reg, cuts, options, basic_cuts, Debug='no', Print='no')

    return ExecBase(alg_name, 'PassEvent', ROOT.Msl.PassEvent(), reg)

#-------------------------------------------------------------------------
def preparePassEventForWCR(alg_name, options, basic_cuts, cut='BASIC'):

    reg  = ROOT.Msl.Registry()

    cuts = getWCRCuts(cut, basic_cuts, ignore_met=options.ignore_met)

    #
    # Fill Registry with cuts and samples for cut-flow
    #
    _fillPassEventRegistry(reg, cuts, options, basic_cuts, Debug='no', Print='no')

    return ExecBase(alg_name, 'PassEvent', ROOT.Msl.PassEvent(), reg)

#-------------------------------------------------------------------------
def prepareFillEvent(alg_name, options):

    reg = ROOT.Msl.Registry()
    reg.SetVal('FillEvent::Name',    alg_name)
    reg.SetVal('FillEvent::Debug',   'no')
    reg.SetVal('FillEvent::Print',   'yes')

    reg.SetVal('FillEvent::Year',    options.year)

    return ExecBase(alg_name, 'FillEvent', ROOT.Msl.FillEvent(), reg)

#-------------------------------------------------------------------------
def preparePlotEvent(alg_name, *arguments, **keywords):

    alg = ROOT.Msl.PlotEvent()
    reg = ROOT.Msl.Registry()
    
    reg.SetVal('PlotEvent::Debug',       'no')
    reg.SetVal('PlotEvent::Print',       'no')
    reg.SetVal('PlotEvent::VarPref',     'var_')
    reg.SetVal('PlotEvent::DetailLvl',   1)
    #reg.SetVal('PlotEvent::Debug',       'yes')    
    reg.SetVal('PlotEvent::VarVec',      ','.join((get_vars.GetPltStr(0)))) 
    reg.SetVal('PlotEvent::NBinVec',     ','.join((get_vars.GetPltStr(1))))
    reg.SetVal('PlotEvent::LoVec',       ','.join((get_vars.GetPltStr(2))))
    reg.SetVal('PlotEvent::HiVec',       ','.join((get_vars.GetPltStr(3))))
    
    pass_algs = []
    
    for key, var in keywords.iteritems():
        if type(var) == type([]):
            reg.SetVal('PlotEvent::%s' %key, ','.join(var))
        elif key == 'PassAlg':
            if var != None:            
                pass_algs += [var]
        else:
            if key != None and var != None:
                reg.SetVal('PlotEvent::%s' %key, var)

    plot_alg = ExecBase(alg_name, 'PlotEvent', alg, reg)
    plot_alg.SetPassAlg(pass_algs)

    return plot_alg
