
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

    def __init__(self, Analysis, Chan, options, SameSign=0):

        if Analysis not in ['all']:
            raise NameError('BasicCuts - unknown analysis string: %s' %Analysis)

        self.analysis = Analysis
        self.chan     = Chan
        self.SameSign = SameSign
        self.NjetCut  = 'n_jet < 3'
        self.JetEta = ''

        # By default: no special metsig cut.
        # Apply one if running a 'msgt4' or 'mslt4' analysis.
        self.MetsigLowerCut = -0.0001
        self.MetsigUpperCut = -1.0
        if Analysis.count('msgt4'):
            self.MetsigLowerCut = 4.0
        if Analysis.count('mslt4'):
            self.MetsigUpperCut = 4.0

        # Add extra lepton pT cut-- for now, break into bins around the MET cut.
        self.ExtraLepPtLowerCut = 0.0
        self.ExtraLepPtUpperCut = -1.0
        if Analysis.count('lepptlow'):
            self.ExtraLepPtUpperCut = 150.0
        elif Analysis.count('leppthigh'):
            self.ExtraLepPtLowerCut = 150.0

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

    def getMetsigCut(self):
        """ Allow binning in MET significance."""
        cutMetsig = CutItem('CutMetSignificance')
        cutMetsig.AddCut(CutItem('Low',  'alljet_metsig > %s' %(self.MetsigLowerCut)), 'AND')
        if self.MetsigUpperCut>0.0:
            cutMetsig.AddCut(CutItem('High', 'alljet_metsig < %s' %(self.MetsigUpperCut)), 'AND')
        return [cutMetsig]

    def getExtraLepPtCut(self):
        cutExtraLepPt = CutItem('CutLepPtBinning')
        cutExtraLepPt.AddCut(CutItem('Low',  'baselepPt0 > %s' %(self.ExtraLepPtLowerCut)), 'AND')
        if self.ExtraLepPtUpperCut > 0.0:
            cutExtraLepPt.AddCut(CutItem('High', 'baselepPt0 < %s' %(self.ExtraLepPtUpperCut)), 'AND')
        return [cutExtraLepPt]

    def GetNjetCut(self):
        cutNjet = CutItem('CutNjet', self.NjetCut)
        return [cutNjet]

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
    elif basic_cuts.chan == 'e':  cuts += [CutItem('CutChannel', 'chanFlavor==4 || chanFlavor==5')]
    elif basic_cuts.chan == 'u':  cuts += [CutItem('CutChannel', 'chanFlavor==2 || chanFlavor==3')]
    elif basic_cuts.chan == 'l':  cuts += [CutItem('CutChannel', 'chanFlavor==2 || chanFlavor==3 || chanFlavor==4 || chanFlavor==5')]
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
def FilterCuts(options):
    cuts = []
    if options==None:
        return cuts
    if options.mergePTV or options.mergeKTPTV:
        #cuts += [CutItem('CutMergePTV','passVjetsPTV > 0.5')]
        #cuts += [CutItem('CutMergeExt','passVjetsFilter > 0.5')]
        cuts += [CutItem('CutMergeExt','passVjetsFilterTauEl > 0.5')]
    if options.mergeExt or options.mergeMGExt:
        cuts += [CutItem('CutMergeExt','passVjetsFilter > 0')]
    return cuts

#-------------------------------------------------------------------------
def ExtraCuts(options, n_mu=0, n_el=0, isEMu=False, isWCR=False):
    cuts = []

    if isEMu:
        cuts += [CutItem('CutBaseLep','n_baselep == 2')]
    elif n_mu==0 and n_el==0: 
        cuts += [CutItem('CutBaseLep','n_baselep == 0')]
    elif n_mu>0 and n_el>0: 
        cuts += [CutItem('CutBaseLep',  'n_baselep == %s' %(n_mu))]
        if isWCR:
            cuts += [CutItem('CutSignalWLep','n_lep_w == %s' %(n_mu))]
        else:
            cuts += [CutItem('CutSignalZLep','n_siglep == %s' %(n_mu))]
    elif n_mu>=0 or n_el>=0: 
        cuts += [CutItem('CutBaseLep','n_baselep == %s' %(n_mu+n_el))]
        cuts += [CutItem('CutSignalMu','n_mu == %s' %(n_mu))]
        cuts += [CutItem('CutSignalEl','n_el == %s' %(n_el))]
    else: #other
        cuts += [CutItem('CutBaseLep','n_baselep == 0')]

    return cuts

#-------------------------------------------------------------------------
def getJetCuts(basic_cuts, options):
    cuts=[]
    
    cuts = [CutItem('CutNjet',  'n_jet <= 2')]
    return cuts
    
    # b jet veto
    cuts += [CutItem('CutBVeto',  'n_bjet < 2')]

    return cuts

#-------------------------------------------------------------------------
def metCuts(basic_cuts, options, isLep=False, metCut=150.0, cstCut=130.0, maxMET=-1):

    highMET=180.0
    if metCut>180.0:
        highMET=metCut

    met_choice = options.met_choice # the met_choice is filled into this variable
    if isLep:
        met_choice=met_choice.replace('_tst','_tst_nolep')
    cuts += [CutItem('CutMet','%s > 50.0' %(met_choice))]

    return cuts

#-------------------------------------------------------------------------
def getGamCuts(cut = '', options=None, basic_cuts=None, ignore_met=False, Region='SR', syst='Nominal'):

    cuts = FilterCuts(options)
    cuts += [CutItem('CutMCOverlap','in_vy_overlapCut > 0')]
        
    if basic_cuts.chan in ['nn']:
        cuts += getMETTriggerCut(cut, options, basic_cuts, Localsyst=syst)
    elif basic_cuts.chan in ['uu','ee','ll','eu']:
        cuts += [CutItem('CutTrig',      'trigger_lep > 0')]

    cuts += [CutItem('CutJetClean',  'passJetCleanTight == 1')]
    cuts += getLepChannelCuts(basic_cuts)
    cuts += getJetCuts(basic_cuts,options)
    cuts += [CutItem('CutMet', '%s > 50.0' %(options.met_choice))]
    
    cutNumLep = CutItem('CutNumLep')    
    
    if Region=='SR':
        cuts += [CutItem('CutNumPho','n_ph == 1')] 
        
        if basic_cuts.chan=='ee':
            cutNumLep.AddCut(CutItem('CutNumEle','n_el == 2'), 'AND')
        elif basic_cuts.chan=='uu':
            cutNumLep.AddCut(CutItem('CutNumMu','n_mu == 2'), 'AND')

        cuts += [cutNumLep]
        cuts += [CutItem('CutL0Pt', 'lepPt0 > 26.0')]
        cuts += [CutItem('CutL1Pt', 'lepPt1 > 7.0')]
        cuts += [CutItem('CutMass', 'mll < 116.0 && mll > 66.0')]
        cuts += [CutItem('CutVetoBjets','n_bjet == 0')]

    elif Region=='CRtt':
        cuts += [CutItem('CutNumPho','n_ph == 1')] 

        cutNumLep.AddCut(CutItem('CutNumEle','n_el == 1'), 'AND')
        cutNumLep.AddCut(CutItem('CutNumMu','n_mu == 1'), 'AND')

        cuts += [cutNumLep]
        cuts += [CutItem('CutL0Pt', 'lepPt0 > 26.0')]
        cuts += [CutItem('CutL1Pt', 'lepPt1 > 7.0')]
        cuts += [CutItem('CutMass', 'mll < 116.0 && mll > 66.0')]
        cuts += [CutItem('CutNumBjetsGt1','n_bjet >= 1')]

    elif Region=='CRWZ':

        if basic_cuts.chan=='uu':
            cutNumLep.AddCut(CutItem('CutNumMu', 'n_mu == 2'), 'AND')
            #cutNumLep.AddCut(CutItem('CutNumBaseEle', 'n_baseel == 1'), 'AND')
        
        cuts += [cutNumLep]
        cuts += [CutItem('CutL0Pt', 'lepPt0 > 26.0')]
        cuts += [CutItem('CutL1Pt', 'lepPt1 > 7.0')]
        cuts += [CutItem('CutMass', 'mll < 116.0 && mll > 66.0')]
        cuts += [CutItem('CutVetoBjets','n_bjet == 0')]

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
    sigs['higgs'] = ['hyGr','hggf','hvh','hvbf','tth']
    sigs['hggf']  = ['hggf']
    sigs['hvh']   = ['hvh']
    sigs['hyGr']  = ['hyGr']
    sigs['hvbf']  = ['hvbf']
    sigs['tth']  = ['tth']

    bkgs = {}
    bkgs['wqcd'] = ['wqcd']
    bkgs['zqcd'] = ['zqcd']
    bkgs['wewk'] = ['wewk']
    bkgs['zewk'] = ['zewk']
    bkgs['top'] = ['top1']
    bkgs['vvv'] =['vvv']
    bkgs['vv']  =['vv']
    bkgs['vvy']  =['vvy']
    bkgs['vvewk'] = ['vvewk']
    bkgs['ttv'] = ['ttv']
    bkgs['hzy'] = ['hzy']
    bkgs['zgam'] = ['zgam','vgg']
    bkgs['zgamewk'] = ['zgamewk']

    # other={}
    # other['dqcd']    = ['dqcd']
    # other['zqcdMad'] = ['zqcdMad']
    # other['wqcdMad'] = ['wqcdMad']
    # other['zqcdPow'] = ['zqcdPow']
    #if not options.OverlapPh:
    #    other['ttg']  = ['ttg']
    #    other['pho']  = ['pho']
    #    other['phoAlt']  = ['phoAlt']
    #    other['wgam'] = ['wgam']
    #    other['zgam'] = ['zgam']
    #    other['wgamewk'] = ['wgamewk']
    #    other['zgamewk'] = ['zgamewk']

    samples = {}
    samples.update(sigs)
    samples.update(bkgs)
#    samples.update(other)

    samples['data'] = ['data']
    samples['bkgs'] = []

    for bkg in bkgs.itervalues():
        if bkg not in samples['bkgs']:
            samples['bkgs'] += bkg

    #
    # Save samples (type list by hand to preserve order)
    #
    if reg != None and key != None:
        
        reg.SetVal(key, 'hvh,hyGr,vvewk,vv,vvv,vvy,zqcd,zewk,zgam,hzy,top,ttv,bkgs,data')
        
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
def preparePassEventForSR(alg_name, options, basic_cuts, cut='BASIC',syst='Nominal'):

    reg  = ROOT.Msl.Registry()

    cuts = getGamCuts(cut, options, basic_cuts, ignore_met=options.ignore_met,  Region='SR', syst=syst)

    #
    # Fill Registry with cuts and samples for cut-flow
    #
    _fillPassEventRegistry(reg, cuts, options, basic_cuts, Debug='no', Print='no')

    return ExecBase(alg_name, 'PassEvent', ROOT.Msl.PassEvent(), reg)
#-------------------------------------------------------------------------
def preparePassEventForCRtt(alg_name, options, basic_cuts, cut='BASIC',syst='Nominal'):

    reg  = ROOT.Msl.Registry()

    cuts = getGamCuts(cut, options, basic_cuts, ignore_met=options.ignore_met, Region='CRtt', syst=syst)

    #
    # Fill Registry with cuts and samples for cut-flow
    #
    _fillPassEventRegistry(reg, cuts, options, basic_cuts, Debug='no', Print='no')

    return ExecBase(alg_name, 'PassEvent', ROOT.Msl.PassEvent(), reg)
#-------------------------------------------------------------------------
def preparePassEventForCRWZ(alg_name, options, basic_cuts, cut='BASIC',syst='Nominal'):

    reg  = ROOT.Msl.Registry()

    cuts = getGamCuts(cut, options, basic_cuts, ignore_met=options.ignore_met, Region='CRWZ', syst=syst)

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
def preparePlotEvent(alg_name, syst_name, DetailLvl, *arguments, **keywords):

    alg = ROOT.Msl.PlotEvent()
    reg = ROOT.Msl.Registry()

    reg.SetVal('PlotEvent::Debug',       'no')
    reg.SetVal('PlotEvent::Print',       'no')
    reg.SetVal('PlotEvent::VarPref',     'var_')
    reg.SetVal('PlotEvent::DetailLvl',   DetailLvl)
    reg.SetVal('PlotEvent::VarVec',      ','.join((get_vars.GetPltStr(0,syst_name,DetailLvl=DetailLvl))))
    reg.SetVal('PlotEvent::NBinVec',     ','.join((get_vars.GetPltStr(1,syst_name,DetailLvl=DetailLvl))))
    reg.SetVal('PlotEvent::LoVec',       ','.join((get_vars.GetPltStr(2,syst_name,DetailLvl=DetailLvl))))
    reg.SetVal('PlotEvent::HiVec',       ','.join((get_vars.GetPltStr(3,syst_name,DetailLvl=DetailLvl))))

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
