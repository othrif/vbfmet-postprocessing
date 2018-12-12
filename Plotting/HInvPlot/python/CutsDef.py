
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
def ExtraCuts(n_mu=0, n_el=0, isEMu=False):
    cuts = []
    #cuts += [CutItem('CutTruthFilter','TruthFilter < 0.5')]    
    #return cuts
    if isEMu:
        cuts += [CutItem('CutBaseLep','n_baselep == 2')]                
    elif n_mu>=0 and n_el>=0:
        cuts += [CutItem('CutBaseLep','n_baselep == %s' %(n_mu))]        
    elif n_mu>=0 or n_el>=0:
        cuts += [CutItem('CutBaseMu','n_basemu == %s' %(n_mu))]
        cuts += [CutItem('CutBaseEl','n_baseel == %s' %(n_el))]
    else:
        cuts += [CutItem('CutBaseLep','n_baselep == 0')]
    if not isEMu:
        cuts += [CutItem('CutJetMETSoft','met_soft_tst_et < 20.0')]
    cuts += [CutItem('CutFJVT','j0fjvt < 0.5 && j1fjvt < 0.5')]
    cuts += [CutItem('CutJetTiming0','j0timing < 11.0 && j0timing > -11.0')]
    cuts += [CutItem('CutJetTiming1','j1timing < 11.0 && j1timing > -11.0')]
    return cuts

#-------------------------------------------------------------------------
def getJetCuts(isPh=False):
    cuts = [CutItem('CutNjet',  'n_jet == 2')]
    #cuts = [CutItem('CutNjet',  'n_jet < 5')]
    if not isPh:
        #cuts += [CutItem('CutNjetCen',  'n_jet_cenj == 0')]    
        #cuts  = [CutItem('CutNjet',  'n_jet > 1 && n_jet < 5')]
        #cuts += [CutItem('CutMaxCentrality',  'maxCentrality <0.6')]
        #cuts += [CutItem('CutMaxMj3_over_mjj',  'maxmj3_over_mjj <0.05')]

        cuts += [CutItem('CutJ0Pt',  'jetPt0 > 80.0')]
        cuts += [CutItem('CutJ1Pt',  'jetPt1 > 50.0')]
        #cuts += [CutItem('CutJ0Eta',  'jetEta0 > 2.5 || jetEta0 < -2.5')]
        #cuts += [CutItem('CutJ1Eta',  'jetEta1 > 2.5 || jetEta1 < -2.5')]
    else:
        cuts = [CutItem('CutNjet',  'n_jet == 2')]
        cuts += [CutItem('CutJ0Pt',  'jetPt0 > 50.0')]
        cuts += [CutItem('CutJ1Pt',  'jetPt1 > 35.0')]
        
    return cuts

#-------------------------------------------------------------------------
def getVBFCuts(isLep=False):
    
    cuts = [CutItem('CutDPhijj',   'jj_dphi < 1.8')]
    if not isLep:
        cuts += [CutItem('CutDPhiMetj0','met_tst_j1_dphi > 1.0')]
        cuts += [CutItem('CutDPhiMetj1','met_tst_j2_dphi > 1.0')]
    else:
        cuts += [CutItem('CutDPhiMetj0','met_tst_nolep_j1_dphi > 1.0')]
        cuts += [CutItem('CutDPhiMetj1','met_tst_nolep_j2_dphi > 1.0')]
    cuts += [CutItem('CutOppHemi','etaj0TimesEtaj1 < 0.0')]
    cuts += [CutItem('CutDEtajj','jj_deta > 4.8')]
    #cuts += [CutItem('CutDEtajjV','jj_deta > 2.5')]
    cuts += [CutItem('CutMjj','jj_mass > 1000.0')]
    
    return cuts

#-------------------------------------------------------------------------
def getSRCuts(cut = '', options=None, basic_cuts=None, ignore_met=False):

    cuts = []

    cuts += [CutItem('CutTrig',      'trigger_met == 1')]
    cuts += [CutItem('CutJetClean',  'passJetCleanTight == 1')]
    cuts += getLepChannelCuts(basic_cuts)
    cuts += getJetCuts();

    # add the extra cuts
    cuts += ExtraCuts()
    
    if cut == 'BeforeMET':
        return GetCuts(cuts)
    if not ignore_met:
        cuts += [CutItem('CutMet',       '%s > 180.0' %(options.met_choice))]
        #cuts += [CutItem('CutMetLow',       '%s > 100.0' %(options.met_choice))]
        cuts += [CutItem('CutMetCSTJet', 'met_cst_jet > 150.0')]

    # VBF cuts
    cuts+=getVBFCuts(isLep=False)

    return GetCuts(cuts)

#-------------------------------------------------------------------------
def getGamSRCuts(cut = '', options=None, basic_cuts=None, ignore_met=False):

    cuts = []

    cuts += [CutItem('CutTrig',      'trigger_met == 1')]
    cuts += [CutItem('CutJetClean',  'passJetCleanTight == 1')]
    cuts += getLepChannelCuts(basic_cuts)
    cuts += [CutItem('CutPh',       'n_ph==1')]
    cuts += getJetCuts(isPh=True);

    # add the extra cuts
    cuts += ExtraCuts()
    
    if cut == 'BeforeMET':
        return GetCuts(cuts)
    if not ignore_met:
        cuts += [CutItem('CutMet',       '%s > 150.0' %(options.met_choice))]
        #cuts += [CutItem('CutMetLow',       '%s > 100.0' %(options.met_choice))]
        #cuts += [CutItem('CutMetCSTJet', 'met_cst_jet > 150.0')]
        
    cuts += [CutItem('CutDPhiMetPh','met_tst_ph_dphi > 1.8')]
    cuts += [CutItem('CutPhCentrality','phcentrality > 0.4')]
    # VBF cuts
    #cuts+=getVBFCuts(isLep=False)
    cuts += [CutItem('CutOppHemi','etaj0TimesEtaj1 < 0.0')]
    cuts += [CutItem('CutDEtajj','jj_deta > 2.5')]
    cuts += [CutItem('CutMjj','jj_mass > 250.0')]

    return GetCuts(cuts)

#-------------------------------------------------------------------------
def getZCRCuts(cut = '', options=None, basic_cuts=None, ignore_met=False):

    cuts = []

    cuts += [CutItem('CutTrig',      'trigger_lep == 1')]
    cuts += [CutItem('CutJetClean',  'passJetCleanTight == 1')]
    cuts += getLepChannelCuts(basic_cuts)
    cuts += getJetCuts();
    if basic_cuts.chan=='eu':
        cuts += [CutItem('CutL0Pt',  'lepPt0 > 26.0')]
        cuts += [CutItem('CutNbjet',  'n_bjet < 0.5')]        
        cuts += [CutItem('CutMass',   'Mtt < 116.0 && Mtt > 76.0')]
    else:
        cuts += [CutItem('CutL0Pt',  'lepPt0 > 30.0')]
        #cuts += [CutItem('CutMll',   'mll < 116.0 && mll > 76.0')]
        cutMass = CutItem('CutMass')
        cutMass.AddCut(CutItem('Mll',  'mll < 116.0 && mll > 76.0'), 'OR')
        #cutMass.AddCut(CutItem('Mtt', 'Mtt < 116.0 && Mtt > 76.0'), 'OR')
        cuts += [cutMass]

    # add the extra cuts
    n_mu=2
    n_el=2;
    isEMu=False
    if basic_cuts.chan=='ee':
        n_mu=2; n_el=0; #note that the muon is used
    if basic_cuts.chan=='uu':
        n_mu=2; n_el=0;
    if basic_cuts.chan=='eu':
        n_mu=1; n_el=1; isEMu=True;        
    cuts += ExtraCuts(n_mu,n_el,isEMu)
    
    if cut == 'BeforeMET':
        return GetCuts(cuts)    
    if not ignore_met:
        cuts += [CutItem('CutMet',       'met_tst_nolep_et > 180.0')]
        #cuts += [CutItem('CutMetLow',       'met_tst_nolep_et > 100.0')]        
        cuts += [CutItem('CutMetCSTJet', 'met_cst_jet > 150.0')]

    if basic_cuts.chan=='ee':
        cuts += [CutItem('CutLepVeto',   'n_mu == 0')]        
    if basic_cuts.chan=='uu':
        cuts += [CutItem('CutLepVeto',   'n_el == 0')]        
        
    # VBF cuts
    cuts+=getVBFCuts(isLep=True)

    return GetCuts(cuts)

#-------------------------------------------------------------------------
def getWCRCuts(cut = '', options=None, basic_cuts=None, ignore_met=False, do_met_signif=False):

    cuts = []
    cuts += [CutItem('CutTrig',      'trigger_lep == 1')]
    cuts += [CutItem('CutJetClean',  'passJetCleanTight == 1')]
    cuts += getLepChannelCuts(basic_cuts)    
    cuts += getJetCuts();
    cuts += [CutItem('CutL0Pt',  'lepPt0 > 30.0')]

    # add the extra cuts
    cuts += ExtraCuts(1,1)
    
    if cut == 'BeforeMET':
        return GetCuts(cuts)    
    if not ignore_met:
        cuts += [CutItem('CutMet',       'met_tst_nolep_et > 180.0')]
        #cuts += [CutItem('CutMetLow',       'met_tst_nolep_et > 100.0')]        
        cuts += [CutItem('CutMetCSTJet', 'met_cst_jet > 150.0')]
    if do_met_signif:
        cuts += [CutItem('CutMetSignif','met_significance > 4.0')]
    # VBF cuts
    cuts+=getVBFCuts(isLep=True)

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
    #sigs['whww']  = ['whww']    
    sigs['hvh']   = ['hvh']
    sigs['hvbf']  = ['hvbf']
    
    bkgs = {}
    bkgs['wqcd'] = ['wqcd']
    bkgs['zqcd'] = ['zqcd']
    bkgs['wewk'] = ['wewk']
    bkgs['zewk'] = ['zewk']
    bkgs['top1'] = ['top1']
    bkgs['top2'] = ['top2']
    bkgs['vvv']  = ['vvv']    
    bkgs['zldy'] = ['zldy']    
    bkgs['mqcd'] = ['mqcd']    
    bkgs['tall'] = ['top2','top1']
    #bkgs['tall'] = ['top2','top1']    

    other={}
    other['dqcd']    = ['dqcd']
    other['zqcdMad'] = ['zqcdMad']        
    other['wqcdMad'] = ['wqcdMad']        
    other['zqcdPow'] = ['zqcdPow']    
    
    samples = {}
    samples.update(sigs)
    samples.update(bkgs)
    samples.update(other)    

    samples['data'] = ['data']
    samples['bkgs'] = []

    for bkg in bkgs.itervalues():
        if bkg not in samples['bkgs']:
            samples['bkgs'] += bkg

    #
    # Save samples (type list by hand to preserve order)
    #
    if reg != None and key != None:
        reg.SetVal(key, 'higgs,tall,wqcd,wewk,zqcd,zewk,mqcd,bkgs,data')
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

    cuts = getSRCuts(cut, options, basic_cuts, ignore_met=options.ignore_met)

    #
    # Fill Registry with cuts and samples for cut-flow
    #
    _fillPassEventRegistry(reg, cuts, options, basic_cuts, Debug='no', Print='no')

    return ExecBase(alg_name, 'PassEvent', ROOT.Msl.PassEvent(), reg)

#-------------------------------------------------------------------------
def preparePassEventForGamSR(alg_name, options, basic_cuts, cut='BASIC'):

    reg  = ROOT.Msl.Registry()

    cuts = getGamSRCuts(cut, options, basic_cuts, ignore_met=options.ignore_met)

    #
    # Fill Registry with cuts and samples for cut-flow
    #
    _fillPassEventRegistry(reg, cuts, options, basic_cuts, Debug='no', Print='no')

    return ExecBase(alg_name, 'PassEvent', ROOT.Msl.PassEvent(), reg)

#-------------------------------------------------------------------------
def preparePassEventForZCR(alg_name, options, basic_cuts, cut='BASIC'):

    reg  = ROOT.Msl.Registry()

    cuts = getZCRCuts(cut, options, basic_cuts, ignore_met=options.ignore_met)

    #
    # Fill Registry with cuts and samples for cut-flow
    #
    _fillPassEventRegistry(reg, cuts, options, basic_cuts, Debug='no', Print='no')

    return ExecBase(alg_name, 'PassEvent', ROOT.Msl.PassEvent(), reg)

#-------------------------------------------------------------------------
def preparePassEventForWCR(alg_name, options, basic_cuts, cut='BASIC', do_met_signif=False):

    reg  = ROOT.Msl.Registry()

    cuts = getWCRCuts(cut, options, basic_cuts, ignore_met=options.ignore_met, do_met_signif=do_met_signif)

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
