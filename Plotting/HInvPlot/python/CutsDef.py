
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

        if Analysis not in ['LowMETQCDSR','LowMETQCDVR','LowMETQCD','LowMETQCDSRFJVT','LowMETQCDVRFJVT','LowMETQCDFJVT','deta25','LowMETSR','mjjLow200','allmjj','mjj800','mjj1000','mjj1500','mjj2000','mjj3000','mjj3500','mjj1000dphijj1','mjj1500dphijj1','mjj2000dphijj1','mjj1000dphijj2','mjj1500dphijj2','mjj2000dphijj2','mjj1500TrigTest','mjj2000TrigTest','mjj1000TrigTest','mjj800dphijj1','mjj800dphijj2','mjj3000dphijj2','mjj3500dphijj2','mjj3000dphijj1','mjj3500dphijj1',
			    'mjjLowNjet','mjjLowNjet2','mjjLowNjetFJVT','njgt','njgt4',
                            'mjj1000dphijj1nj2','mjj1500dphijj1nj2','mjj2000dphijj1nj2','mjj1000dphijj2nj2','mjj1500dphijj2nj2','mjj2000dphijj2nj2',
                                'njgt2','njgt2lt5','njgt3lt5',
                                'metsf','metsfxe70','metsfxe90','metsfxe110','metsftrig','metsftrigxe70','metsftrigxe90','metsftrigxe70J400','metsftrigxe110','metsftrigxe110J400','metsftrigxe90J400',
                            'metsfVBFTopo','metsfxe110XE70','metsfxe110XE65',
                            'metsfxe90','metsfxe100','metsfxe110L155','metsfxe100L150',
                            'metsfVBFTopotrigOR','metsfxe110XE70trig','metsfxe110XE65trig',
                            'metsfxe90trig','metsfxe100trig','metsfxe110L155trig','metsfxe100L150trig',]:
            raise NameError('BasicCuts - unknown analysis string: %s' %Analysis)

        self.analysis = Analysis
        self.chan     = Chan
        self.SameSign = SameSign
        self.MjjLowerCut   = 800.0
        self.MjjUpperCut   = -1.0
        self.DPhijjLowerCut   = -1.0
        self.DPhijjUpperCut   = 2.0
        self.DEtajjLowerCut   = 3.8
        self.DEtajjUpperCut   = -1.0
        self.NjetCut   = 'n_jet > 1 && n_jet < 5'
        #self.NjetCut   = 'n_jet == 2'
        self.JetEta = ''
        if Analysis.count('metsf'):
            self.DEtajjLowerCut   = 3.5 # was 3.5
            self.MjjLowerCut   = 1500.0
            if Analysis.count('VBFTopo'):
                self.JetEta = '(jetEta0 < 3.2 && jetEta0 > -3.2) || (jetEta1 < 3.2 && jetEta1 > -3.2)'
                self.DEtajjLowerCut   = 4.2 # was 3.5
                self.MjjLowerCut   = 1500.0
            #self.NjetCut   = 'n_jet == 3'
        if Analysis.count('mjj1000'):
            self.MjjLowerCut   = 1000.0
            self.MjjUpperCut   = 1500.0
        if Analysis.count('mjj800'):
            self.MjjLowerCut   = 800.0
            self.MjjUpperCut   = 1000.0
        if Analysis.count('LowMETQCDVR'):
            self.MjjLowerCut   = 200.0
            self.MjjUpperCut   = -1
            self.DEtajjLowerCut   = 2.8
            self.DEtajjUpperCut   = 3.8
            self.NjetCut = 'n_jet == 2'
        if Analysis.count('LowMETQCDSR'):
            self.MjjLowerCut   = 800.0
            self.MjjUpperCut   = -1
            self.DEtajjLowerCut   = 3.8
            self.DEtajjUpperCut   = -1
            self.NjetCut = 'n_jet == 2'
        if Analysis.count('deta25'):
            self.DEtajjLowerCut = 2.5
            self.DEtajjUpperCut = 3.8
            self.MjjLowerCut   = 200.0
        if Analysis.count('mjjLow200'):
            self.MjjLowerCut   = 200.0
            self.MjjUpperCut   = 800.0
        if Analysis.count('mjj1500'):
            self.MjjLowerCut   = 1500.0
            self.MjjUpperCut   = 2000.0
        if Analysis.count('mjj1000TrigTest'):
            self.MjjLowerCut   = 1000.0
            self.MjjUpperCut   = -1
            self.DEtajjLowerCut = 4.2 # remove
            self.DPhijjUpperCut = 2.0
            self.JetEta = '(jetEta0 < 3.2 && jetEta0 > -3.2) || (jetEta1 < 3.2 && jetEta1 > -3.2)'
        if Analysis.count('mjj1500TrigTest'):
            self.MjjLowerCut   = 1500.0
            self.MjjUpperCut   = -1
            self.DEtajjLowerCut = 4.2 # remove
            self.DPhijjUpperCut = 2.0
            self.JetEta = '(jetEta0 < 3.2 && jetEta0 > -3.2) || (jetEta1 < 3.2 && jetEta1 > -3.2)'
        if Analysis.count('mjj2000TrigTest'):
            self.MjjLowerCut   = 2000.0
            self.MjjUpperCut   = -1
            self.DEtajjLowerCut = 4.2 # remove
            self.DPhijjUpperCut = 2.0
            self.JetEta = '(jetEta0 < 3.2 && jetEta0 > -3.2) || (jetEta1 < 3.2 && jetEta1 > -3.2)'
        if Analysis.count('mjj2000'):
            self.MjjLowerCut   = 2000.0
            self.MjjUpperCut   = -1.0
        if Analysis.count('mjj3000'):
            self.MjjLowerCut   = 3000.0
            self.MjjUpperCut   = -1.0
        if Analysis.count('mjj3500'):
            self.MjjLowerCut   = 3500.0
            self.MjjUpperCut   = -1.0
        if Analysis.count('dphijj1'):
            self.DPhijjLowerCut   = -1
            self.DPhijjUpperCut   = 1.0
        if Analysis.count('dphijj2'):
            self.DPhijjLowerCut   = 1.0
            self.DPhijjUpperCut   = 2.0
        if Analysis.count('njgt2'): # single bin
            self.MjjLowerCut   = 800.0
            self.MjjUpperCut   = -1.0
            self.DPhijjLowerCut   = -1.0
            self.DPhijjUpperCut   = 2.0
            self.NjetCut = 'n_jet > 2 && n_jet < 5'
        if Analysis.count('mjjLowNjet2'): # single bin
            self.MjjLowerCut   = 200.0
            self.MjjUpperCut   = 800.0
            self.DPhijjLowerCut   = -1.0
            self.DPhijjUpperCut   = 2.0
            self.NjetCut = 'n_jet > 2 && n_jet < 5'
        if Analysis.count('mjjLowNjet') or Analysis.count('mjjLowNjetFJVT'): # single bin
            self.MjjLowerCut   = 200.0
            self.MjjUpperCut   = 800.0
            self.DPhijjLowerCut   = -1.0
            self.DPhijjUpperCut   = 2.0
        if Analysis.count('njgt3'): # single bin
            self.MjjLowerCut   = 800.0
            self.MjjUpperCut   = -1.0
            self.DPhijjLowerCut   = -1.0
            self.DPhijjUpperCut   = 2.0
            self.NjetCut = 'n_jet > 3 && n_jet < 5'
        if Analysis.count('nj2'):
            self.NjetCut = 'n_jet == 2'

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

    def GetMjjCut(self):
        cutMjj = CutItem('CutMjj')
        cutMjj.AddCut(CutItem('Low',  'jj_mass > %s' %(self.MjjLowerCut)), 'AND')
        if self.MjjUpperCut>0.0:
            cutMjj.AddCut(CutItem('High', 'jj_mass < %s' %(self.MjjUpperCut)), 'AND')
        return [cutMjj]

    def GetDPhijjCut(self):
        cutDPhijj = CutItem('CutDPhijj')
        if self.DPhijjLowerCut>0.0:
            cutDPhijj.AddCut(CutItem('Low',  'jj_dphi > %s' %(self.DPhijjLowerCut)), 'AND')
        if self.DPhijjUpperCut>0.0:
            cutDPhijj.AddCut(CutItem('High', 'jj_dphi < %s' %(self.DPhijjUpperCut)), 'AND')
        return [cutDPhijj]

    def GetDEtajjCut(self):
        cutDEtajj = CutItem('CutDEtajj')
        if self.DEtajjLowerCut>0.0:
            cutDEtajj.AddCut(CutItem('Low',  'jj_deta > %s' %(self.DEtajjLowerCut)), 'AND')
        if self.DEtajjUpperCut>0.0:
            cutDEtajj.AddCut(CutItem('High', 'jj_deta < %s' %(self.DEtajjUpperCut)), 'AND')
        return [cutDEtajj]

    def GetNjetCut(self):
        cutNjet = CutItem('CutNjet', self.NjetCut)
        return [cutNjet]

    def GetLeadJetEtaCut(self):
        if self.JetEta!='':
            if self.JetEta=='(jetEta0 < 3.2 && jetEta0 > -3.2) || (jetEta1 < 3.2 && jetEta1 > -3.2)':
                cutJetEta0 = CutItem('CutJetEta01')
                cutJetEta0.AddCut(CutItem('Low',   'jetEta0 < 3.2 && jetEta0 > -3.2'), 'OR')
                cutJetEta0.AddCut(CutItem('High',  'jetEta1 < 3.2 && jetEta1 > -3.2'), 'OR')
                return [cutJetEta0]
            else:
                cutJetEta0 = CutItem('CutJetEta0', self.JetEta)
                return [cutJetEta0]
        else:
            return []

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
    if options.mergePTV:
        cuts += [CutItem('CutMergePTV','passVjetsPTV > 0')]
    if options.mergeExt:
        cuts += [CutItem('CutMergeExt','passVjetsFilter > 0')]
    return cuts

#-------------------------------------------------------------------------
def ExtraCuts(basic_cuts, options, n_mu=0, n_el=0, isEMu=False, isWCR=False):
    cuts = []

    if options.r207Ana:
        if isEMu:
            cuts += [CutItem('CutSignalLep','n_siglep == 2')]
        elif n_mu>=0 and n_el>=0:
            cuts += [CutItem('CutSignalLep','n_siglep == %s' %(n_mu))]
        elif n_mu>=0 or n_el>=0:
            cuts += [CutItem('CutSignalMu','n_mu == %s' %(n_mu))]
            cuts += [CutItem('CutSignalEl','n_el == %s' %(n_el))]
        else:
            cuts += [CutItem('CutSignalLep','n_baselep == 0')]
        return cuts
    #cuts += [CutItem('CutTruthFilter','TruthFilter < 0.5')]
    #return cuts
    if isEMu:
        cuts += [CutItem('CutBaseLep','n_baselep == 2')]
    elif n_mu==0 and n_el==0: # for the SR
        cuts += [CutItem('CutBaseLep','n_baselep == 0')]
    elif n_mu>0 and n_el>0: # for the WCR
        cuts += [CutItem('CutBaseLep',  'n_baselep == %s' %(n_mu))]
        if isWCR:
            cuts += [CutItem('CutSignalWLep','n_lep_w == %s' %(n_mu))]
        else:
            cuts += [CutItem('CutSignalZLep','n_siglep == %s' %(n_mu))]
    elif n_mu>=0 or n_el>=0: # for Z CR
        cuts += [CutItem('CutBaseLep','n_baselep == %s' %(n_mu+n_el))]
        cuts += [CutItem('CutSignalMu','n_mu == %s' %(n_mu))]
        cuts += [CutItem('CutSignalEl','n_el == %s' %(n_el))]
    else: #other
        cuts += [CutItem('CutBaseLep','n_baselep == 0')]

    # Cut is under discussion
    if not isEMu:
        cuts += [CutItem('CutJetMETSoft','met_soft_tst_et < 20.0')]
    if basic_cuts.analysis!='mjjLowNjetFJVT' and basic_cuts.analysis!='njgt' and basic_cuts.analysis!='njgt4':
        cuts += [CutItem('CutFJVT','j0fjvt < 0.5 && j1fjvt < 0.5')]
    cuts += [CutItem('CutJetTiming0','j0timing < 11.0 && j0timing > -11.0')]
    cuts += [CutItem('CutJetTiming1','j1timing < 11.0 && j1timing > -11.0')]
    return cuts

#-------------------------------------------------------------------------
def getJetCuts(basic_cuts, options, isPh=False):

    if not isPh:
        if options.r207Ana:
            cuts=[]
            cuts = [CutItem('CutNjet',  'n_jet == 2')]
            #cuts = [CutItem('CutNjet',  'n_jet < 4')]
            cuts += [CutItem('CutJ0Pt',  'jetPt0 > 80.0')]
            cuts += [CutItem('CutJ1Pt',  'jetPt1 > 50.0')]
            return cuts
        else:
            # New Cuts
            #cuts += [CutItem('CutNjetCen',  'n_jet_cenj == 0')]
            #cuts  = [CutItem('CutNjet',             'n_jet == 2')]
            cuts = basic_cuts.GetNjetCut()
            cuts += basic_cuts.GetLeadJetEtaCut()
            if basic_cuts.analysis!='njgt2lt5' and basic_cuts.analysis!='njgt3lt5' and basic_cuts.analysis!='mjjLowNjet' and basic_cuts.analysis!='mjjLowNjetFJVT' and basic_cuts.analysis!='njgt':
                #cuts += [CutItem('CutJ3Pt',    'jetPt3 < 30.0')]
                cuts += [CutItem('CutMaxCentrality',    'maxCentrality <0.6')]
                cuts += [CutItem('CutMaxMj3_over_mjj',  'maxmj3_over_mjj <0.05')]
            if basic_cuts.analysis=='mjj1500TrigTest' or basic_cuts.analysis=='mjj2000TrigTest' or basic_cuts.analysis=='mjj1000TrigTest':
                cuts += [CutItem('CutJ0Pt',  'jetPt0 > 90.0')]
                cuts += [CutItem('CutJ1Pt',  'jetPt1 > 70.0')] # move to 50
            else:
                cuts += [CutItem('CutJ0Pt',  'jetPt0 > 80.0')]#80,50
                cuts += [CutItem('CutJ1Pt',  'jetPt1 > 50.0')] # move to 50
            #cuts += [CutItem('CutJ0Eta',  'jetEta0 > 2.5 || jetEta0 < -2.5')]
            #cuts += [CutItem('CutJ1Eta',  'jetEta1 > 2.5 || jetEta1 < -2.5')]
    else:
        cuts = [CutItem('CutNjet',  'n_jet == 2')]
        cuts += [CutItem('CutJ0Pt',  'jetPt0 > 60.0')]
        cuts += [CutItem('CutJ1Pt',  'jetPt1 > 50.0')]

    # b jet veto
    cuts += [CutItem('CutBVeto',  'n_bjet < 2')]

    return cuts

#-------------------------------------------------------------------------
def getVBFCuts(options, basic_cuts, isLep=False):

    cuts = basic_cuts.GetDPhijjCut()
    if not isLep:
        cuts += [CutItem('CutDPhiMetj0','met_tst_j1_dphi > 1.0')]
        cuts += [CutItem('CutDPhiMetj1','met_tst_j2_dphi > 1.0')]
    else:
        cuts += [CutItem('CutDPhiMetj0','met_tst_nolep_j1_dphi > 1.0')]
        cuts += [CutItem('CutDPhiMetj1','met_tst_nolep_j2_dphi > 1.0')]
    cuts += [CutItem('CutOppHemi','etaj0TimesEtaj1 < 0.0')]
    if options.r207Ana:
        cuts += [CutItem('CutDEtajj','jj_deta > 4.8')]
        cuts += basic_cuts.GetMjjCut()
    else:
        cuts += basic_cuts.GetDEtajjCut()
        cuts += basic_cuts.GetMjjCut()
    #cuts += [CutItem('CutMu40','averageIntPerXing>40.0')]

    return cuts

#-------------------------------------------------------------------------
def metCuts(basic_cuts, options, isLep=False, metCut=150.0, cstCut=120.0, maxMET=-1):

    met_choice = options.met_choice # the met_choice is filled into this variable
    if isLep:
        met_choice=met_choice.replace('_tst','_tst_nolep')
    cutMET = CutItem('CutMet')
    if options.r207Ana:
        cutMET.AddCut(CutItem('HighMET', '%s > 180.0' %(met_choice)), 'OR')
        cuts = [cutMET]
        cuts += [CutItem('CutMetCSTJet', 'met_cst_jet > 150.0')]
    else:
        if basic_cuts.analysis.count('LowMETQCD'):
            cutMET.AddCut(CutItem('HighMET', '%s < 150.0 && %s > 100.0' %(met_choice,met_choice)), 'AND')
            if basic_cuts.analysis.count('FJVT'):
                cutMET.AddCut(CutItem('FJVT', 'j0fjvt < 0.2 && j1fjvt < 0.2'), 'AND')
            cuts = [cutMET]
        else:
            cutMET.AddCut(CutItem('HighMET', '%s > 180.0' %(met_choice)), 'OR')
	    if basic_cuts.analysis!='mjjLowNjetFJVT' and basic_cuts.analysis!='njgt' and basic_cuts.analysis!='njgt4':
                cutMET.AddCut(CutItem('LowMET', '%s > %s && j0fjvt < 0.2 && j1fjvt < 0.2' %(met_choice, metCut)), 'OR')
            cuts = [cutMET]
            #cuts += [CutItem('CutMetLow',       '%s > 100.0' %(options.met_choice))]
            cuts += [CutItem('CutMetCSTJet', 'met_cst_jet > %s' %(cstCut))]
    if maxMET>0.0:
        cuts +=  [CutItem('CutMetMaxMET', '%s < %s' %(met_choice,maxMET))]

    return cuts

#-------------------------------------------------------------------------
def getMETTriggerCut(cut = '', options=None, basic_cuts=None, Localsyst=None, ORTrig=''):
    cuts=[]
    apply_weight=None
    if Localsyst!=None and Localsyst!='NOXESF':
        apply_weight='xeSFTrigWeight'
    if Localsyst=='xeSFTrigWeight__1up':
        apply_weight='xeSFTrigWeight__1up'
    elif Localsyst=='xeSFTrigWeight__1down':
        apply_weight='xeSFTrigWeight__1down'
    if apply_weight!=None and ORTrig!='':
        apply_weight=apply_weight.replace('xeSFTrigWeight','xeSFTrigWeight_nomu')

    if options.year==2017:
        cuts += [CutItem('CutTrig',      'trigger_met_encodedv2 == 4'+ORTrig, weight=apply_weight)]
    elif options.year==2018:
        #cuts += [CutItem('CutTrig',      'trigger_met_encodedv2 == 3', weight=apply_weight)]
        #cuts += [CutItem('CutTrig',      'trigger_met_encodedv2 == 5')]
        #cuts += [CutItem('CutTrig',      'trigger_met_encodedv2 == 11')]
        if basic_cuts.analysis=='mjj1500TrigTest' or basic_cuts.analysis=='mjj2000TrigTest' or basic_cuts.analysis=='mjj1000TrigTest':
            cuts += [CutItem('CutTrig',      'trigger_met_encodedv2 == 11 || trigger_met_encodedv2 == 5'+ORTrig)]
        else:
            cuts += [CutItem('CutTrig',      'trigger_met_encodedv2 == 5'+ORTrig, weight=apply_weight)] # use this one
    else:
        cuts += [CutItem('CutTrig',      'trigger_met == 1'+ORTrig, weight=apply_weight)]
    return cuts

#-------------------------------------------------------------------------
def getSRCuts(cut = '', options=None, basic_cuts=None, ignore_met=False, syst='Nominal'):

    cuts = FilterCuts(options)

    # special setup for the trigger SF in the signal region
    cuts += getMETTriggerCut(cut, options, basic_cuts, syst)
    cuts += [CutItem('CutJetClean',  'passJetCleanTight == 1')]
    cuts += getLepChannelCuts(basic_cuts)
    cuts += [CutItem('CutPh', 'n_ph==0')]
    cuts += getJetCuts(basic_cuts, options);

    # add the extra cuts
    cuts += ExtraCuts(basic_cuts,options)

    if cut == 'BeforeMET':
        return GetCuts(cuts)
    if not ignore_met:
        if basic_cuts.analysis=='mjj1500TrigTest' or basic_cuts.analysis=='mjj2000TrigTest' or basic_cuts.analysis=='mjj1000TrigTest':
            cuts += metCuts(basic_cuts,options,metCut=120.0, cstCut=100.0)#, maxMET=150.0)
        else:
            cuts += metCuts(basic_cuts,options,metCut=150.0, cstCut=120.0)
            #cuts += metCuts(basic_cuts,options,metCut=100.0, cstCut=100.0)

    # VBF cuts
    cuts+=getVBFCuts(options, basic_cuts, isLep=False)
    #cuts += [CutItem('CutOneHSJet',  'nTruthJetMatch == 1')]

    return GetCuts(cuts)

#-------------------------------------------------------------------------
def getMETSFCuts(cut = '', options=None, basic_cuts=None, ignore_met=False, Region='SR'):

    cuts = FilterCuts(options)
    if options.year==2018:
        if basic_cuts.GetSelKey().count('metsfVBFTopo'):
            cuts += [CutItem('CutMETTrigRuns20', 'runPeriod == 20')]
            if basic_cuts.GetSelKey().count('trigOR'):
                cuts += [CutItem('CutMETTrigVBFTopo', 'trigger_met_encodedv2 == 11 || trigger_met_encodedv2 == 5')]
                #cuts += [CutItem('CutMETTrigVBFTopo', 'trigger_met_encodedv2 == 5')]
            elif basic_cuts.GetSelKey().count('trig'): # this is broken!!!
                cuts += [CutItem('CutMETTrigVBFTopo', 'trigger_met_encodedv2 == 11')]
        elif basic_cuts.GetSelKey().count('metsfxe110XE70'):
            cuts += [CutItem('CutMETTrigRuns30', 'runPeriod == 30')]
            if basic_cuts.GetSelKey().count('trig'):
                cuts += [CutItem('CutMETTrigMET', 'trigger_met_encodedv2 == 5')]
        elif basic_cuts.GetSelKey().count('metsfxe110XE65'):
            cuts += [CutItem('CutMETTrigRuns31', 'runPeriod == 31 || runPeriod == 20')]
            if basic_cuts.GetSelKey().count('trig'):
                cuts += [CutItem('CutMETTrigMET', 'trigger_met_encodedv2 == 5')]
    elif options.year==2017:
        if basic_cuts.GetSelKey().count('metsfxe90'):
            cuts += [CutItem('CutMETTrigRuns10', 'runPeriod == 10')]
        elif basic_cuts.GetSelKey().count('metsfxe100'):
            cuts += [CutItem('CutMETTrigRuns11', 'runPeriod == 11')]
        elif basic_cuts.GetSelKey().count('metsfxe110L155'):
            cuts += [CutItem('CutMETTrigRuns12', 'runPeriod == 12')]
        elif basic_cuts.GetSelKey().count('metsfxe100L150'):
            cuts += [CutItem('CutMETTrigRuns13', 'runPeriod == 13')]
        # apply the trigger
        if basic_cuts.GetSelKey().count('trig'):
            cuts += [CutItem('CutMETTrigVBFTopo', 'trigger_met_encodedv2 == 4')]

    else: # 2015+2016
        if basic_cuts.GetSelKey().count('trigxe70J400'):
            cuts += [CutItem('CutMETTrigxe70J400', 'trigger_met_byrun == 1 || trigger_met_byrun == 4')]
        elif basic_cuts.GetSelKey().count('trigxe70'):
            cuts += [CutItem('CutMETTrigxe70', 'trigger_met_byrun == 1')]
        elif basic_cuts.GetSelKey().count('trigxe90J400'):
            cuts += [CutItem('CutMETTrigxe90J400', 'trigger_met_byrun == 2 || trigger_met_byrun == 5')]
        elif basic_cuts.GetSelKey().count('trigxe110J400'):
            cuts += [CutItem('CutMETTrigxe110J400', 'trigger_met_byrun == 3 || trigger_met_byrun == 6')]
        elif basic_cuts.GetSelKey().count('trigxe90'):
            cuts += [CutItem('CutMETTrigxe90', 'trigger_met_byrun == 2')]
        elif basic_cuts.GetSelKey().count('trigxe110'):
            cuts += [CutItem('CutMETTrigxe110', 'trigger_met_byrun == 3')]
        elif basic_cuts.GetSelKey().count('metsfxe70'):
            cuts += [CutItem('CutMETTrigRuns1', 'runPeriod == 1')]
        elif basic_cuts.GetSelKey().count('metsfxe90'):
            cuts += [CutItem('CutMETTrigRuns2', 'runPeriod == 2')]
        elif basic_cuts.GetSelKey().count('metsfxe110'):
            cuts += [CutItem('CutMETTrigRuns3', 'runPeriod == 3')]

    cuts += [CutItem('CutJetClean',  'passJetCleanTight == 1')]
    met_choice=options.met_choice
    isLep=False
    #cuts += [CutItem('CutJ0Eta',  'jetEta0 > 2.5 || jetEta0 < -2.5')]
    #cuts += [CutItem('CutJ1Eta',  'jetEta1 > 2.5 || jetEta1 < -2.5')]

    if basic_cuts.chan=='e':
        cuts += [CutItem('CutLepTrig', 'trigger_lep == 1')]
        cuts += [CutItem('CutEl','n_el == 1')]
        cuts += [CutItem('CutBaseLep','n_baselep == 1')]
    elif basic_cuts.chan=='u':
        cuts += [CutItem('CutLepTrig', 'trigger_lep == 1')]
        cuts += [CutItem('CutMu','n_mu == 1')]
        cuts += [CutItem('CutBaseLep','n_baselep == 1')]
        met_choice=options.met_choice.replace('_tst','_tst_nolep')
        isLep=True
    elif basic_cuts.chan=='nn':
        cuts += [CutItem('CutBaseLep','n_baselep == 0')]
    # cuts
    cuts += [CutItem('CutPh', 'n_ph==0')]

    cuts += getJetCuts(basic_cuts, options);
    cuts += [CutItem('CutMet',       '%s > 100.0' %(met_choice))]
    # does the vertex matter? does the CST met cut matter? does the fjvt cuts matter?
    #cuts += metCuts(basic_cuts,options, metCut=100.0, cstCut=0.0)
    #cuts += metCuts(basic_cuts,options, metCut=100.0, cstCut=120.0)
    # VBF cuts
    cuts += getVBFCuts(options, basic_cuts, isLep=isLep)

    return GetCuts(cuts)

#-------------------------------------------------------------------------
def getGamCuts(cut = '', options=None, basic_cuts=None, ignore_met=False, Region='SR', syst='Nominal'):

    cuts = FilterCuts(options)
    if options.OverlapPh:
        cuts += [CutItem('CutMCOverlap','in_vy_overlapCut > 0')]

    if basic_cuts.chan in ['nn']:
        cuts += getMETTriggerCut(cut, options, basic_cuts, syst)
    elif basic_cuts.chan in ['uu','u','up','um']:
        cuts += getMETTriggerCut(cut, options, basic_cuts, None, ORTrig=' || trigger_lep > 0')
    elif basic_cuts.chan in ['ee','ll','eu']:
        cuts += [CutItem('CutTrig',      'trigger_lep > 0')]        
    else:
        cuts += [CutItem('CutTrig',      'trigger_lep == 1')]
    cuts += [CutItem('CutJetClean',  'passJetCleanTight == 1')]
    if Region=='SR':
    #    cuts += getLepChannelCuts(basic_cuts)
        print ''
    elif Region=='ZCR':
        if basic_cuts.chan=='ee':
            cuts += [CutItem('CutEl','n_el == 2')]
        if basic_cuts.chan=='uu':
            cuts += [CutItem('CutMu','n_mu == 2')]
        cuts += [CutItem('CutSignalZLep','n_siglep == 2')]
    elif Region=='WCR':
        if basic_cuts.chan=='e':
            cuts += [CutItem('CutEl','n_el == 1')]
        if basic_cuts.chan=='u':
            cuts += [CutItem('CutMu','n_mu == 1')]
        cuts += [CutItem('CutSignalWLep','n_siglep == 1')]

    cuts += [CutItem('CutPh',       'n_ph==1')]
    cuts += getJetCuts(basic_cuts, options, isPh=True);

    # add the extra cuts...decide if we want these
    #cuts += ExtraCuts(options)
    cuts += [CutItem('CutFJVT','j0fjvt < 0.4 && j1fjvt < 0.4')]
    cuts += [CutItem('CutJetTiming0','j0timing < 11.0 && j0timing > -11.0')]
    cuts += [CutItem('CutJetTiming1','j1timing < 11.0 && j1timing > -11.0')]

    if cut == 'BeforeMET':
        return GetCuts(cuts)
    if not ignore_met:
        if Region=='SR':
            met_choice=options.met_choice
        elif Region=='WCR' or Region=='ZCR':
            met_choice=options.met_choice.replace('_tst','_tst_nolep')
        cuts += [CutItem('CutMet',       '%s > 150.0' %(met_choice))]

    cuts += [CutItem('CutDPhiMetPh','met_tst_ph_dphi > 1.8')]
    cuts += [CutItem('CutPhCentrality','phcentrality > 0.4')]
    # VBF cuts
    cuts += [CutItem('CutOppHemi','etaj0TimesEtaj1 < 0.0')]
    cuts += [CutItem('CutDEtajj','jj_deta > 3.0')]
    cuts += [CutItem('CutDPhijj','jj_dphi < 2.0')]
    cuts += [CutItem('CutMjj','jj_mass > 250.0')]

    return GetCuts(cuts)

#-------------------------------------------------------------------------
def getZCRCuts(cut = '', options=None, basic_cuts=None, ignore_met=False, syst='Nominal'):

    cuts = FilterCuts(options)

    if options.r207Ana:
        cuts += [CutItem('CutTrig',      'trigger_lep == 1')]
    else:
        if basic_cuts.chan=='uu':
            cuts += getMETTriggerCut(cut, options, basic_cuts, Localsyst='NOXESF', ORTrig=' || trigger_lep > 0')   
        else:
            cuts += [CutItem('CutTrig',      'trigger_lep > 0')]
    cuts += [CutItem('CutJetClean',  'passJetCleanTight == 1')]
    cuts += [CutItem('CutPh', 'n_ph==0')]
    cuts += getLepChannelCuts(basic_cuts)
    cuts += getJetCuts(basic_cuts, options);
    if basic_cuts.chan=='eu':
        cuts += [CutItem('CutL0Pt',  'lepPt0 > 26.0')]
        cuts += [CutItem('CutNbjet',  'n_bjet < 0.5')]
        cuts += [CutItem('CutMass',   'Mtt < 116.0 && Mtt > 66.0')]
    else:
        cuts += [CutItem('CutL0Pt',  'lepPt0 > 30.0')]
        cuts += [CutItem('CutL1Pt',  'lepPt1 > 7.0')]
        #cuts += [CutItem('CutMll',   'mll < 116.0 && mll > 76.0')]
        cutMass = CutItem('CutMass')
        cutMass.AddCut(CutItem('Mll',  'mll < 116.0 && mll > 66.0'), 'OR')
        #cutMass.AddCut(CutItem('Mtt', 'Mtt < 116.0 && Mtt > 76.0'), 'OR')
        cuts += [cutMass]

    # add the extra cuts
    n_mu=2
    n_el=2;
    isEMu=False
    if basic_cuts.chan=='ee':
        n_mu=0; n_el=2; 
    if basic_cuts.chan=='uu':
        n_mu=2; n_el=0;
    if basic_cuts.chan=='eu':
        n_mu=1; n_el=1; isEMu=True;
    cuts += ExtraCuts(basic_cuts,options, n_mu,n_el,isEMu)

    if cut == 'BeforeMET':
        return GetCuts(cuts)
    if not ignore_met:
        if basic_cuts.analysis=='mjj1500TrigTest' or basic_cuts.analysis=='mjj2000TrigTest' or basic_cuts.analysis=='mjj1000TrigTest':
            cuts += metCuts(basic_cuts,options, True, metCut=120.0, cstCut=100.0, maxMET=150.0)
        else:
            cuts += metCuts(basic_cuts, options, True)

    if not options.LoadBaseLep:
        if basic_cuts.chan=='ee':
            cuts += [CutItem('CutLepVeto',   'n_mu == 0')]
        if basic_cuts.chan=='uu':
            cuts += [CutItem('CutLepVeto',   'n_el == 0')]

    # VBF cuts
    cuts+=getVBFCuts(options, basic_cuts, isLep=True)

    return GetCuts(cuts)

#-------------------------------------------------------------------------
def getWCRCuts(cut = '', options=None, basic_cuts=None, ignore_met=False, do_met_signif=False,syst='Nominal'):

    cuts = FilterCuts(options)
    if basic_cuts.chan in ['u','um','up']:
        cuts += getMETTriggerCut(cut, options, basic_cuts, Localsyst='NOXESF', ORTrig=' || trigger_lep > 0')
    else:
        cuts += [CutItem('CutTrig',      'trigger_lep == 1')]

    cuts += [CutItem('CutJetClean',  'passJetCleanTight == 1')]
    cuts += [CutItem('CutPh', 'n_ph==0')]
    cuts += getLepChannelCuts(basic_cuts)
    cuts += getJetCuts(basic_cuts, options);
    cuts += [CutItem('CutL0Pt',  'lepPt0 > 30.0')]

    # add the extra cuts
    cuts += ExtraCuts(basic_cuts,options, 1,1, isWCR=True)

    if cut == 'BeforeMET':
        return GetCuts(cuts)
    if not ignore_met:
        if basic_cuts.analysis=='mjj1500TrigTest' or basic_cuts.analysis=='mjj2000TrigTest' or basic_cuts.analysis=='mjj1000TrigTest':
            cuts += metCuts(basic_cuts,options, True, metCut=120.0, cstCut=100.0, maxMET=150.0)
        else:
            cuts += metCuts(basic_cuts,options, True)
    if do_met_signif:
        cuts += [CutItem('CutMetSignif','met_significance > 4.0')]
    # VBF cuts
    cuts+=getVBFCuts(options, basic_cuts, isLep=True)

    return GetCuts(cuts)

def getWCRAntiIDCuts(cut = '', options=None, basic_cuts=None, ignore_met=False):
    cuts = getWCRCuts(cut, options, basic_cuts, ignore_met)

    # Loop through the WCR cuts. Replace some of them to create the anti-ID region.
    # By doing it this way, the anti-ID region is always updated with regard to
    # other changes in the analysis.

    new_cuts = []
    for cutobj in cuts:

        # Rewrite the lepton pT cut to use base lepton pT.
        if cutobj.GetCutName() == "CutL0Pt":
            new_lep_pt = cutobj.cut_conf.replace("lepPt", "baselepPt")
            lep_pt_cut = CutItem("CutL0Pt", conf=new_lep_pt, weight=cutobj.cut_wkey)
            new_cuts.append(lep_pt_cut)

        # Rewrite the "channel" cut to explicitly look at n_baselep and n_basemu.
        # this short-circuits the "channel" computation in the C++ code to always
        # use baseline leptons-- as desired for the anti-ID region.
        elif cutobj.GetCutName() == "CutChannel":
            chan_conf = ""

            # If this is an electron channel, requre at least 1 baseline electron, no muons.
            # And vice versa for muon channels.
            if basic_cuts.chan[0] == 'e':
                chan_conf += "n_baseel > 0 && n_basemu == 0"
            else:
                chan_conf += "n_basemu > 0 && n_baseel == 0"

            # Now consider the possibility that we want an e+/e- channel (or the same for muons).
            # Add a cut on baselepCh0.
            if len(basic_cuts.chan) == 2:
                if basic_cuts.chan[1] == "p":
                    chan_conf += " && baselepCh0>0"
                else:
                    chan_conf += " && baselepCh0<0"

            chan_cut = CutItem("CutChannel", conf=chan_conf, weight=cutobj.cut_wkey)
            new_cuts.append(chan_cut)

        # I believe we need a special case for the 20.7 cuts.
        # There, we require that there be exactly one signal lepton-- and do not
        # put requirements on the base leptons beyond this. Thus, there can be
        # more than one base lepton.
        # So, in the anti-ID region for r20.7 cuts, replace this with a cut
        # requiring n_baseleps > 0.
        elif cutobj.GetCutName() == "CutBaseLep" and options.r207Ana:
            r207_base_cut = CutItem("CutBaseLep", "n_baselep > 0")
            new_cuts.append(r207_base_cut)

        # We need to *remove* this cut (we don't want to require signal leptons).
        elif cutobj.GetCutName() == "CutSignalWLep":
            pass

        # Otherwise-- just add the cut.
        else:
            new_cuts.append(cutobj)

    # Add a cut to veto signal leptons.
    new_cuts.append(CutItem("CutNoSigLeps", "n_lep_w == 0"))

    # Add the trigger isolation: ptvarcone30/pt < 0.07 for mu, ptvarcone20/pt<0.1
    # TODO: make this one optional!
    if basic_cuts.chan[0] == 'e':
        new_cuts.append(CutItem("CutPtVarCone", "baselep_ptvarcone_0 < 0.1"))
    else:
        new_cuts.append(CutItem("CutPtVarCone", "baselep_ptvarcone_0 < 0.07"))

    # Debugging: print out the cuts.
    #print("Selection in anti-ID region (%s):" % (basic_cuts.chan))
    #for cutobj in new_cuts:
    #    print("%s: %s" % (cutobj.cut_name, cutobj.cut_conf))
    #sys.exit(1)

    # Return the modified cuts.
    return new_cuts

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
    sigs['higgs'] = ['hggf','hvh','hvbf','tth']
    sigs['hggf']  = ['hggf']
    #sigs['whww']  = ['whww']
    sigs['hvh']   = ['hvh']
    sigs['hvbf']  = ['hvbf']
    sigs['tth']  = ['tth']

    bkgs = {}

    bkgs['wqcd'] = ['wqcd']
    bkgs['zqcd'] = ['zqcd']
    bkgs['wewk'] = ['wewk']
    bkgs['zewk'] = ['zewk']
    bkgs['tall'] = ['top2','vvv']
    bkgs['dqcd'] = ['dqcd']
    bkgs['mqcd'] = ['mqcd']
    if options.OverlapPh:
        sigs['vbfg'] = ['vbfg']
        sigs['higgs'] += ['vbfg']
        bkgs['ttg']  = ['ttg']
        bkgs['pho']  = ['pho']
        bkgs['phoAlt']  = ['phoAlt']
        bkgs['wgam'] = ['wgam']
        bkgs['zgam'] = ['zgam']
        bkgs['wgamewk'] = ['wgamewk']
        bkgs['zgamewk'] = ['zgamewk']        

    other={}
    other['dqcd']    = ['dqcd']
    other['zqcdMad'] = ['zqcdMad']
    other['wqcdMad'] = ['wqcdMad']
    other['zqcdPow'] = ['zqcdPow']
    if not options.OverlapPh:
        other['ttg']  = ['ttg']
        other['pho']  = ['pho']
        other['phoAlt']  = ['phoAlt']
        other['wgam'] = ['wgam']
        other['zgam'] = ['zgam']
        other['wgamewk'] = ['wgamewk']
        other['zgamewk'] = ['zgamewk']

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
        if options.OverlapPh:
            reg.SetVal(key, 'higgs,tall,wqcd,wewk,zqcd,zewk,mqcd,ttg,pho,phoAlt,wgam,zgam,zgamEWK,wgamEWK,bkgs,data')
        else:
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
def preparePassEventForSR(alg_name, options, basic_cuts, cut='BASIC',syst='Nominal'):

    reg  = ROOT.Msl.Registry()

    cuts = getSRCuts(cut, options, basic_cuts, ignore_met=options.ignore_met, syst=syst)

    #
    # Fill Registry with cuts and samples for cut-flow
    #
    _fillPassEventRegistry(reg, cuts, options, basic_cuts, Debug='no', Print='no')

    return ExecBase(alg_name, 'PassEvent', ROOT.Msl.PassEvent(), reg)

#-------------------------------------------------------------------------
def preparePassEventForMETSF(alg_name, options, basic_cuts, cut='BASIC'):

    reg  = ROOT.Msl.Registry()

    cuts = getMETSFCuts(cut, options, basic_cuts, ignore_met=options.ignore_met, Region='SR')

    #
    # Fill Registry with cuts and samples for cut-flow
    #
    _fillPassEventRegistry(reg, cuts, options, basic_cuts, Debug='no', Print='no')

    return ExecBase(alg_name, 'PassEvent', ROOT.Msl.PassEvent(), reg)

#-------------------------------------------------------------------------
def preparePassEventForGamSR(alg_name, options, basic_cuts, cut='BASIC',syst='Nominal'):

    reg  = ROOT.Msl.Registry()

    cuts = getGamCuts(cut, options, basic_cuts, ignore_met=options.ignore_met, Region='SR', syst=syst)

    #
    # Fill Registry with cuts and samples for cut-flow
    #
    _fillPassEventRegistry(reg, cuts, options, basic_cuts, Debug='no', Print='no')

    return ExecBase(alg_name, 'PassEvent', ROOT.Msl.PassEvent(), reg)

#-------------------------------------------------------------------------
def preparePassEventForGamZCR(alg_name, options, basic_cuts, cut='BASIC'):

    reg  = ROOT.Msl.Registry()

    cuts = getGamCuts(cut, options, basic_cuts, ignore_met=options.ignore_met, Region='ZCR')

    #
    # Fill Registry with cuts and samples for cut-flow
    #
    _fillPassEventRegistry(reg, cuts, options, basic_cuts, Debug='no', Print='no')

    return ExecBase(alg_name, 'PassEvent', ROOT.Msl.PassEvent(), reg)

#-------------------------------------------------------------------------
def preparePassEventForGamWCR(alg_name, options, basic_cuts, cut='BASIC',syst='Nominal'):

    reg  = ROOT.Msl.Registry()

    cuts = getGamCuts(cut, options, basic_cuts, ignore_met=options.ignore_met, Region='WCR')

    #
    # Fill Registry with cuts and samples for cut-flow
    #
    _fillPassEventRegistry(reg, cuts, options, basic_cuts, Debug='no', Print='no')

    return ExecBase(alg_name, 'PassEvent', ROOT.Msl.PassEvent(), reg)

#-------------------------------------------------------------------------
def preparePassEventForZCR(alg_name, options, basic_cuts, cut='BASIC',syst='Nominal'):

    reg  = ROOT.Msl.Registry()

    cuts = getZCRCuts(cut, options, basic_cuts, ignore_met=options.ignore_met,syst=syst)

    #
    # Fill Registry with cuts and samples for cut-flow
    #
    _fillPassEventRegistry(reg, cuts, options, basic_cuts, Debug='no', Print='no')

    return ExecBase(alg_name, 'PassEvent', ROOT.Msl.PassEvent(), reg)

#-------------------------------------------------------------------------
def preparePassEventForWCR(alg_name, options, basic_cuts, cut='BASIC', do_met_signif=False,syst='Nominal'):

    reg  = ROOT.Msl.Registry()

    cuts = getWCRCuts(cut, options, basic_cuts, ignore_met=options.ignore_met, do_met_signif=do_met_signif,syst=syst)

    #
    # Fill Registry with cuts and samples for cut-flow
    #
    _fillPassEventRegistry(reg, cuts, options, basic_cuts, Debug='no', Print='no')

    return ExecBase(alg_name, 'PassEvent', ROOT.Msl.PassEvent(), reg)

def preparePassEventForWCRAntiID(alg_name, options, basic_cuts, cut='BASIC'):
    """ Prepare events for the anti-ID version of the WCR."""
    reg  = ROOT.Msl.Registry()
    cuts = getWCRAntiIDCuts(cut, options, basic_cuts, ignore_met=options.ignore_met)
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
