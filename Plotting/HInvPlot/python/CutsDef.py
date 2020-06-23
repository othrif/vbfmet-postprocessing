
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

        if Analysis not in ['LowMETQCDSR','LowMETQCDVR','LowMETQCD','LowMETQCDSRFJVT','LowMETQCDVRFJVT','LowMETQCDFJVT','deta25','LowMETSR','mjjLow200','allmjj','mjj800','mjj1000','mjj1500','mjj2000','mjj3000','mjj3500','mjj1000dphijj1','mjj1500dphijj1','mjj2000dphijj1','mjj1000dphijj2','mjj1500dphijj2','mjj2000dphijj2','mjj1500TrigTest','mjj2000TrigTest','mjj1000TrigTest','mjj800dphijj1','mjj800dphijj2','mjj3000dphijj2','mjj3500dphijj2','mjj3000dphijj1','mjj3500dphijj1',
                            'mjj800dphijj1nj2','mjj1000dphijj1nj2','mjj1500dphijj1nj2','mjj2000dphijj1nj2','mjj3500dphijj1nj2','mjj800dphijj2nj2','mjj1000dphijj2nj2','mjj1500dphijj2nj2','mjj2000dphijj2nj2','mjj3500dphijj2nj2','antiEHighMET','antiELowMET',

                            'mjj800nj2', 'mjj1000nj2', 'mjj1500nj2', 'mjj2000nj2', 'mjj3500nj2',
                                'njgt2','njgt2lt5','njgt3lt5','nj3','lowmet','revfjvt','njgt3','nj2',
                                'nj2dphijj1','nj2dphijj2','dphijj1','dphijj2',
                                'LowMETQCDRevFJVT','highmjjMidMETnj2',
                                'metsf','metsfxe70','metsfxe90','metsfxe110','metsftrig','metsftrigxe70','metsftrigxe90','metsftrigxe70J400','metsftrigxe110','metsftrigxe110J400','metsftrigxe90J400',
                            'metsfVBFTopo','metsfxe110XE70','metsfxe110XE65',
                            'metsfxe90','metsfxe100','metsfxe110L155','metsfxe100L150',
                            'metsfVBFTopotrigOR','metsfxe110XE70trig','metsfxe110XE65trig',
                            'metsfxe90trig','metsfxe100trig','metsfxe110L155trig','metsfxe100L150trig',
                            'allmjjmslt4', 'allmjjmsgt4',
                                'mjj800nj2mslt4', 'mjj800nj2msgt4', 'mjj1000nj2mslt4', 'mjj1000nj2msgt4', 'mjj1500nj2mslt4', 'mjj1500nj2msgt4',
                                'mjj2000nj2mslt4', 'mjj2000nj2msgt4', 'mjj3500nj2mslt4', 'mjj3500nj2msgt4', 'njgt2mslt4', 'njgt2msgt4',
                            'allmjjlepptlow', 'allmjjleppthigh', 'mjj800nj2lepptlow', 'mjj800nj2leppthigh', 'mjj1000nj2lepptlow', 'mjj1000nj2leppthigh',
                                'mjj1500nj2lepptlow', 'mjj1500nj2leppthigh', 'mjj2000nj2lepptlow', 'mjj2000nj2leppthigh', 'mjj3500nj2lepptlow',
                                'mjj3500nj2leppthigh', 'njgt2lepptlow', 'njgt2leppthigh',
                            'allmjjdphijj3', 'mjj800dphijj3nj2', 'mjj1000dphijj3nj2', 'mjj1500dphijj3nj2', 'mjj2000dphijj3nj2', 'mjj3500dphijj3nj2', 'dphijj3njgt2',
                            'mjjLow200dphijj3', 'LowMETQCDSRdphijj3', 'LowMETQCDVRdphijj3', 'LowMETQCDdphijj3', 'LowMETQCDSRFJVTdphijj3', 'LowMETQCDVRFJVTdphijj3', 'LowMETQCDFJVTdphijj3']:
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
            self.MjjLowerCut   = 600.0 # was 600
            if options.OverlapPh:
                self.DEtajjLowerCut   = 3.0 
                self.MjjLowerCut   = 250.0 
            if Analysis.count('VBFTopo'):
                self.JetEta = '(jetEta0 < 3.2 && jetEta0 > -3.2) || (jetEta1 < 3.2 && jetEta1 > -3.2)'
                self.DEtajjLowerCut   = 4.2 # was 3.5
                self.MjjLowerCut   = 1500.0
            if options.metsf_cuts==1:
                self.NjetCut   = 'n_jet == 3'
        if Analysis.count('mjj1000'):
            self.MjjLowerCut   = 1000.0
            self.MjjUpperCut   = 1500.0
        if Analysis.count('highmjjMidMETnj2'):
            self.MjjLowerCut   = 1500.0
            self.MjjUpperCut   = -1.0
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
        if Analysis=='nj3':
            self.NjetCut = 'n_jet == 3'
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
        if Analysis.count('njgt3'): # single bin
            self.MjjLowerCut   = 800.0
            self.MjjUpperCut   = -1.0
            self.DPhijjLowerCut   = -1.0
            self.DPhijjUpperCut   = 2.0
            self.NjetCut = 'n_jet > 3 && n_jet < 5'
        if Analysis.count('nj2'):
            self.NjetCut = 'n_jet == 2'

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

        if Analysis.count('dphijj3'):
            self.DPhijjLowerCut   = 2.0
            # limited to 2.5 due to multijet estimate.
            self.DPhijjUpperCut   = 2.5
        if options.TwoJet:
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
            if basic_cuts.analysis!='njgt2lt5' and basic_cuts.analysis!='njgt3lt5' and basic_cuts.analysis!='nj3':
                #cuts += [CutItem('CutJ3Pt',    'jetPt3 < 30.0')]
                if options.metsf_cuts==0:
                    cuts += [CutItem('CutMaxCentrality',    'maxCentrality <0.6')]
                    #cuts += [CutItem('CutMaxCentrality',    'maxCentrality <0.35')]
                    if options.ReverseLeadFJVT and options.CutFJVTVal>0.25 and (basic_cuts.analysis=='dphijj2' or basic_cuts.analysis=='nj2dphijj2'):
                        cutMaxMj3_over_mjj = CutItem('CutMaxMj3_over_mjj')
                        cutMaxMj3_over_mjj.AddCut(CutItem('highdphijj',  'jj_dphi>1.0'), 'OR')
                        cutMaxMj3_over_mjj.AddCut(CutItem('mjj',         'maxmj3_over_mjj <0.05'), 'OR')
                        cuts += [cutMaxMj3_over_mjj]
                    else:
                        cuts += [CutItem('CutMaxMj3_over_mjj',  'maxmj3_over_mjj <0.05')]
            elif basic_cuts.analysis=='nj3': #OR
                cutCent = CutItem('CutJetCent')
                cutCent.AddCut(CutItem('Cen',  'maxCentrality >0.6'), 'OR')
                cutCent.AddCut(CutItem('mjj',  'maxmj3_over_mjj >0.05'), 'OR')
                cuts += [cutCent]
            if basic_cuts.analysis=='mjj1500TrigTest' or basic_cuts.analysis=='mjj2000TrigTest' or basic_cuts.analysis=='mjj1000TrigTest':
                cuts += [CutItem('CutJ0Pt',  'jetPt0 > 90.0')]
                cuts += [CutItem('CutJ1Pt',  'jetPt1 > 70.0')] # move to 50
            else:
                cuts += [CutItem('CutJ0Pt',  'jetPt0 > 80.0')]#80,50
                cuts += [CutItem('CutJ1Pt',  'jetPt1 > 50.0')] # move to 50
            #cuts += [CutItem('CutJ0Eta',  'jetEta0 > 2.5 || jetEta0 < -2.5')]
            #cuts += [CutItem('CutJ1Eta',  'jetEta1 > 2.5 || jetEta1 < -2.5')]
    else:
        
        cuts = [CutItem('CutNjet',  'n_jet > 1 && n_jet<4')]        
        #cuts += [CutItem('CutMaxCentrality',    'maxCentrality <0.6')]
        #cuts += [CutItem('CutMaxMj3_over_mjj',  'maxmj3_over_mjj <0.05')]
        #cuts = [CutItem('CutNjet',  'n_jet == 2')]
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
    #cuts += [CutItem('CutOneHSJet',  'nTruthJetMatch == 1')] 
    return cuts

#-------------------------------------------------------------------------
def metCuts(basic_cuts, options, isLep=False, metCut=200.0, cstCut=180.0, maxMET=-1, maxcstORCut=-1.0):

    if basic_cuts.analysis=='mjjLow200' or basic_cuts.analysis=='deta25':
        metCut=150.0
        cstCut=130.0

    highMET=200.0
    if metCut>200.0:
        highMET=metCut

    # this will select mid met 160-200 OR CSTJETMET<180 GeV
    if basic_cuts.analysis.count('MidMET'):
        metCut=160.0
        cstCut=140.0
        maxMET=200.0
        maxcstORCut=cstCut

    met_choice = options.met_choice # the met_choice is filled into this variable
    if isLep:
        met_choice=met_choice.replace('_tst','_tst_nolep')
    cutMET = CutItem('CutMet')
    if options.r207Ana:
        cutMET.AddCut(CutItem('HighMET', '%s > 180.0' %(met_choice)), 'OR')
        cuts = [cutMET]
        cuts += [CutItem('CutMetCSTJet', 'met_cst_jet > 150.0')]
    else:
        cuts = []
        if not options.ReverseFJVT and not options.ReverseLeadFJVT and not basic_cuts.analysis.count('LowMETQCD'):
            cuts += [CutItem('CutFJVT','j0fjvt < 0.5 && j1fjvt < 0.5')]
            
        if basic_cuts.analysis.count('LowMETQCDRevFJVT'):
            cutMET.AddCut(CutItem('HighMET', '%s < 180.0 && %s > 150.0' %(met_choice,met_choice)), 'AND')
            if basic_cuts.analysis.count('FJVT'):
                cutMET.AddCut(CutItem('FJVT', 'j0fjvt > %s || j1fjvt > %s' %(options.CutFJVTVal,options.CutFJVTVal)), 'AND')
            cuts += [cutMET]
            cuts += [CutItem('CutMetCSTJet', 'met_cst_jet > 130.0')]
        elif basic_cuts.analysis.count('LowMETQCD'):
            cutMET.AddCut(CutItem('HighMET', '%s < 150.0 && %s > 100.0' %(met_choice,met_choice)), 'AND')
            if basic_cuts.analysis.count('FJVT'):
                if options.ReverseFJVT:
                    cutMET.AddCut(CutItem('FJVT', 'j0fjvt > %s || j1fjvt > %s' %(options.CutFJVTVal,options.CutFJVTVal)), 'AND')
                elif options.ReverseLeadFJVT:
                    cutMET.AddCut(CutItem('FJVT', 'j0fjvt > %s' %(options.CutFJVTVal)), 'AND')
                else:
                    cutMET.AddCut(CutItem('FJVT', 'j0fjvt < %s && j1fjvt < %s' %(options.CutFJVTVal,options.CutFJVTVal)), 'AND')
            cuts += [cutMET]
            cuts += [CutItem('CutMetCSTJet', 'met_cst_jet > 100.0')]
        else:
            if options.ReverseFJVT:
                cutMET.AddCut(CutItem('HighMET1', '%s > %s && j0fjvt > 0.5' %(met_choice,highMET)), 'OR')
                cutMET.AddCut(CutItem('HighMET2', '%s > %s && j1fjvt > 0.5' %(met_choice,highMET)), 'OR')
            elif options.ReverseLeadFJVT:
                cutMET.AddCut(CutItem('HighMET1', '%s > %s && j0fjvt > 0.5' %(met_choice,highMET)), 'OR')
            else:
                cutMET.AddCut(CutItem('HighMET', '%s > %s' %(met_choice,highMET)), 'OR')
            if options.ReverseFJVT:
                cutMET.AddCut(CutItem('LowMETfjvt1', '%s > %s && j0fjvt > %s' %(met_choice, metCut, options.CutFJVTVal)), 'OR')
                cutMET.AddCut(CutItem('LowMETfjvt2', '%s > %s && j1fjvt > %s' %(met_choice, metCut, options.CutFJVTVal)), 'OR')
            elif options.ReverseLeadFJVT:
                cutMET.AddCut(CutItem('LowMETfjvt1', '%s > %s && j0fjvt > %s' %(met_choice, metCut, options.CutFJVTVal)), 'OR')
            else:
                cutMET.AddCut(CutItem('LowMET', '%s > %s && j0fjvt < %s && j1fjvt < %s' %(met_choice, metCut, options.CutFJVTVal, options.CutFJVTVal)), 'OR')
            cuts += [cutMET]
            #cuts += [CutItem('CutMetLow',       '%s > 100.0' %(options.met_choice))]
            cuts += [CutItem('CutMetCSTJet', 'met_cst_jet > %s' %(cstCut))]
    if maxMET>0.0:
        cutMetMaxMET = CutItem('CutMetMaxMET')
        cutMetMaxMET.AddCut(CutItem('MaxMET', '%s < %s' %(met_choice,maxMET)), 'OR')
        if maxcstORCut>0.0:
            cutMetMaxMET.AddCut(CutItem('MaxCST', 'met_cst_jet < %s' %(maxcstORCut)), 'OR')            
        cuts +=  [cutMetMaxMET]

    # cuts met angular
    #cuts +=  [CutItem('CutMetAngle', 'met_tst_cut > 0.5')]
    #cuts +=  [CutItem('CutMetmax', 'met_tst_cut > 0.5')]
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
    if apply_weight!=None and (ORTrig!='' or basic_cuts.chan in ['u','uu']):
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
    cuts += ExtraCuts(options)

    if cut == 'BeforeMET':
        return GetCuts(cuts)
    if not ignore_met:
        if basic_cuts.analysis=='mjj1500TrigTest' or basic_cuts.analysis=='mjj2000TrigTest' or basic_cuts.analysis=='mjj1000TrigTest':
            cuts += metCuts(basic_cuts,options,metCut=130.0, cstCut=100.0)#, maxMET=150.0)
        else:
            #cuts += metCuts(basic_cuts,options,metCut=100.0, cstCut=-1.0)
            #cuts += metCuts(basic_cuts,options,metCut=150.0, cstCut=130.0,maxMET=200.0)
            #cuts += metCuts(basic_cuts,options,metCut=200.0, cstCut=180.0)
            cuts += metCuts(basic_cuts,options,metCut=options.metCut, cstCut=(options.metCut - 20.0),maxMET=options.maxMET)
            #cuts += metCuts(basic_cuts,options,metCut=180.0, cstCut=150.0)
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
            #cuts += [CutItem('CutMETTrigRuns30', 'runPeriod == 30')]
            if basic_cuts.GetSelKey().count('trig'):
                cuts += [CutItem('CutMETTrigMET', 'trigger_met_encodedv2 == 5')]
        elif basic_cuts.GetSelKey().count('metsfxe110XE65'):
            cuts += [CutItem('CutMETTrigRuns31', 'runPeriod == 31 || runPeriod == 20')]
            if basic_cuts.GetSelKey().count('trig'):
                cuts += [CutItem('CutMETTrigMET', 'trigger_met_encodedv2 == 5')]
    elif options.year==2017:
        if basic_cuts.GetSelKey().count('metsfxe90'):
            cuts += [CutItem('CutMETTrigRuns10', 'runPeriod == 10')]
        elif basic_cuts.GetSelKey().count('metsfxe110L155'): # ran all year
            cuts += [CutItem('CutMETTrigRuns10to13', 'runPeriod == 13 || runPeriod == 12 || runPeriod == 11 || runPeriod == 10')]
        elif basic_cuts.GetSelKey().count('metsfxe100'):
            cuts += [CutItem('CutMETTrigRuns11', 'runPeriod == 11')]
        elif basic_cuts.GetSelKey().count('metsfxe100L150'):
            cuts += [CutItem('CutMETTrigRuns10to13', 'runPeriod == 13')]
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
    if options.OverlapPh:
        cuts += [CutItem('CutPh', 'n_ph==1')]        
    else:
        cuts += [CutItem('CutPh', 'n_ph==0')]

    cuts += getJetCuts(basic_cuts, options, isPh=options.OverlapPh);
    cuts += [CutItem('CutMet',       '%s > 100.0' %(met_choice))]
    cuts += [CutItem('CutFJVT','j0fjvt < 0.5 && j1fjvt < 0.5')]
    # does the vertex matter? does the CST met cut matter? does the fjvt cuts matter?
    #cuts += metCuts(basic_cuts,options, metCut=100.0, cstCut=0.0)
    #cuts += metCuts(basic_cuts,options, metCut=100.0, cstCut=130.0)
    # VBF cuts
    cuts += getVBFCuts(options, basic_cuts, isLep=isLep)

    return GetCuts(cuts)

#-------------------------------------------------------------------------
def getGamCuts(cut = '', options=None, basic_cuts=None, ignore_met=False, Region='SR', syst='Nominal'):

    cuts = FilterCuts(options)
    if options.OverlapPh and not options.v41:
        cuts += [CutItem('CutMCOverlap','in_vy_overlapCut > 0')]
        
    if basic_cuts.chan in ['nn']:
        cuts += getMETTriggerCut(cut, options, basic_cuts, Localsyst=syst)
    elif basic_cuts.chan in ['uu','u','up','um','l']:
        cuts += getMETTriggerCut(cut, options, basic_cuts, Localsyst=syst, ORTrig=' || trigger_lep > 0')
        # trigger fix for electron channel
        cutElTrig = CutItem('CutElTrig')
        cutElTrig.AddCut(CutItem('Electron',  'n_el_w > 0 && trigger_lep==1'), 'OR')
        #cutElTrig.AddCut(CutItem('Electron',  'n_el > 0 && trigger_lep==1'), 'OR')
        if not options.doAntiID:
            cutElTrig.AddCut(CutItem('Muon', 'n_mu>0 || n_mu_w>0'), 'OR')
        else:
            cutElTrig.AddCut(CutItem('Muon', 'n_basemu>0 || n_mu_w>0'), 'OR')
        cuts += [cutElTrig]
    elif basic_cuts.chan in ['ee','ll','eu']:
        cuts += [CutItem('CutTrig',      'trigger_lep > 0')]
    else:
        cuts += [CutItem('CutTrig',      'trigger_lep == 1')]
    cuts += [CutItem('CutJetClean',  'passJetCleanTight == 1')]
    if not options.doAntiID:
        cuts += getLepChannelCuts(basic_cuts)
    elif  basic_cuts.chan in ['ee','e','ep','em']:
        cuts += [CutItem('CutLepAntiID',  'n_baseel > 0 && n_basemu == 0')]
    elif  basic_cuts.chan in ['uu','u','up','um']:
        cuts += [CutItem('CutLepAntiID',  'n_baseel == 0 && n_basemu > 0')]
        
    if Region=='SR':
        cuts += [CutItem('CutBaseLep','n_baselep == 0')]
    elif Region=='ZCR':
        if basic_cuts.chan=='ee':
            cuts += [CutItem('CutEl','n_el == 2')]
        if basic_cuts.chan=='uu':
            cuts += [CutItem('CutMu','n_mu == 2')]
        cuts += [CutItem('CutSignalZLep','n_siglep == 2')]
        cuts += [CutItem('CutBaseLep','n_baselep == 2')]
        cuts += [CutItem('CutL0Pt',  'lepPt0 > 30.0')]
        cuts += [CutItem('CutL1Pt',  'lepPt1 > 7.0')]
        cutMass = CutItem('CutMass')
        cutMass.AddCut(CutItem('Mll',  'mll < 116.0 && mll > 66.0'), 'OR')
        #cutMass.AddCut(CutItem('Mtt', 'Mtt < 116.0 && Mtt > 76.0'), 'OR')
        cuts += [cutMass]
        cuts += [CutItem('CutMETForTop',  'met_tst_et < 70.0')]
    elif Region=='WCR':
        if basic_cuts.chan=='e':
            #cuts += [CutItem('CutEl','n_el_w == 1')]
            if not options.doAntiID:
                cuts += [CutItem('CutEl','n_el == 1')]
            else:
                cuts += [CutItem('CutEl','n_baseel == 1')]
        if basic_cuts.chan=='u':
            #cuts += [CutItem('CutMu','n_mu_w == 1')]
            if not options.doAntiID:
                cuts += [CutItem('CutMu','n_mu == 1')]
            else:
                cuts += [CutItem('CutMu','n_basemu == 1')]                
        #cuts += [CutItem('CutSignalWLep','n_siglep == 1')]
        if not options.doAntiID:
            cuts += [CutItem('CutSignalWLep','n_lep_w == 1')]
            cuts += [CutItem('CutBaseLep','n_baselep == 1')]
            cuts += [CutItem('CutL0Pt',  'lepPt0 > 30.0')]
            #cuts += [CutItem('CutL0Pt',  'lepPt0 > 26.0')]
            cuts += [CutItem('CutMETW',  'met_tst_et > 80.0')]
        else:
            cuts += [CutItem('CutSignalWLep','n_siglep == 0')]
            cuts += [CutItem('CutBaseLep','n_baselep == 1')]
            cuts += [CutItem('CutL0Pt',  'baselepPt0 > 30.0')]
            if basic_cuts.analysis in ['antiEHighMET']:
                cuts += [CutItem('CutMETW',  'met_tst_et > 80.0')]
            elif basic_cuts.analysis in ['antiELowMET']:
                cuts += [CutItem('CutMETW',  'met_tst_et < 80.0')]
                
    cuts += [CutItem('CutPh',       'n_ph==1')]
    #cuts += [CutItem('CutPhMETCleaning',       'n_ph_crackVetoCleaning>1')]     # photon met cleaning
    #cuts += [CutItem('CutPhPointing','ph_pointing_z<250.0')]    # 250 mm of the primary vertex. variable is not absolute value
    #cutPhPointing = CutItem('CutPhPointing')
    #cutPhPointing.AddCut(CutItem('High',  'ph_pointing_z<250.0'), 'AND')
    #cutPhPointing.AddCut(CutItem('Low', 'ph_pointing_z>-250.0'), 'AND')
    #cuts += [cutPhPointing]
    cuts += [CutItem('CutPhPt', 'phPt>15.0')] 
    if basic_cuts.analysis not in ['lowmet']:
        cuts += [CutItem('CutPhPtHig', 'phPt<110.0')] 
    cuts += getJetCuts(basic_cuts, options, isPh=True);

    # add the extra cuts...decide if we want these
    #cuts += ExtraCuts(options)
    if options.ReverseFJVT:
        cuts += [CutItem('CutFJVT','j0fjvt > 0.4 || j1fjvt > 0.4')]
    elif options.ReverseLeadFJVT:
        cuts += [CutItem('CutFJVT','j0fjvt > 0.4')]
    else:
        if basic_cuts.analysis in ['revfjvt']:
            #cuts += [CutItem('CutFJVT','j0fjvt > 0.4 || j1fjvt > 0.4')]
            cuts += [CutItem('CutFJVT','j0fjvt > 0.4')]
            #cuts += [CutItem('CutMjjLow','jj_mass < 1000.0')]
        else:
            cuts += [CutItem('CutFJVT','j0fjvt < 0.4 && j1fjvt < 0.4')]
    cuts += [CutItem('CutJetTiming0','j0timing < 11.0 && j0timing > -11.0')]
    cuts += [CutItem('CutJetTiming1','j1timing < 11.0 && j1timing > -11.0')]
    #cuts += [CutItem('CutJetMETSoft','met_soft_tst_et < 20.0')]
    
    if cut == 'BeforeMET':
        return GetCuts(cuts)
    if not ignore_met:
        if Region=='SR':
            met_choice=options.met_choice
        elif Region=='WCR' or Region=='ZCR':
            met_choice=options.met_choice.replace('_tst','_tst_nolep')
        if basic_cuts.analysis in ['lowmet']:
            cuts += [CutItem('CutMjjLow','jj_mass < 1000.0')]
            cuts += [CutItem('CutMet',       '%s > 110.0 && %s < 150.0' %(met_choice,met_choice))]
        else:
            cuts += [CutItem('CutMet',       '%s > 150.0' %(met_choice))]
            cuts += [CutItem('CutMetCST',    'met_cst_jet > 120.0')]

    if not options.nodphimetgam:
        cuts += [CutItem('CutDPhiMetPh','met_tst_nolep_ph_dphi > 1.8')]
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
        if basic_cuts.chan in ['uu','ll']:
            #cuts += getMETTriggerCut(cut, options, basic_cuts, Localsyst='NOXESF', ORTrig=' || trigger_lep > 0')
            cuts += getMETTriggerCut(cut, options, basic_cuts, Localsyst=syst, ORTrig=' || trigger_lep > 0')
            #cuts += getMETTriggerCut(cut, options, basic_cuts, Localsyst=syst, ORTrig='')
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
        cuts += [CutItem('CutMETForTop',  'met_tst_et < 70.0')]

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
    cuts += ExtraCuts(options, n_mu,n_el,isEMu)

    if cut == 'BeforeMET':
        return GetCuts(cuts)
    if not ignore_met:
        if basic_cuts.analysis=='mjj1500TrigTest' or basic_cuts.analysis=='mjj2000TrigTest' or basic_cuts.analysis=='mjj1000TrigTest':
            cuts += metCuts(basic_cuts,options, True, metCut=120.0, cstCut=100.0, maxMET=150.0)
        else:
            #cuts += metCuts(basic_cuts, options, True)
            cuts += metCuts(basic_cuts,options,isLep=True,metCut=options.metCut, cstCut=(options.metCut - 20.0),maxMET=options.maxMET)
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
    if basic_cuts.chan in ['u','um','up','l']:
        #cuts += getMETTriggerCut(cut, options, basic_cuts, Localsyst='NOXESF', ORTrig=' || trigger_lep > 0')
        cuts += getMETTriggerCut(cut, options, basic_cuts, Localsyst=syst, ORTrig=' || trigger_lep > 0')
        #cuts += getMETTriggerCut(cut, options, basic_cuts, Localsyst=syst)
    else:
        cuts += [CutItem('CutTrig',      'trigger_lep == 1')]

    cuts += [CutItem('CutJetClean',  'passJetCleanTight == 1')]
    cuts += [CutItem('CutPh', 'n_ph==0')]
    cuts += getLepChannelCuts(basic_cuts)
    cuts += getJetCuts(basic_cuts, options);
    cuts += [CutItem('CutL0Pt',  'lepPt0 > 30.0')]

    # add the extra cuts
    cuts += ExtraCuts(options, 1,1, isWCR=True)

    if cut == 'BeforeMET':
        return GetCuts(cuts)
    if not ignore_met:
        if basic_cuts.analysis=='mjj1500TrigTest' or basic_cuts.analysis=='mjj2000TrigTest' or basic_cuts.analysis=='mjj1000TrigTest':
            cuts += metCuts(basic_cuts,options, True, metCut=120.0, cstCut=100.0, maxMET=150.0)
        else:
            #cuts += metCuts(basic_cuts,options, True)
            cuts += metCuts(basic_cuts,options,isLep=True,metCut=options.metCut, cstCut=(options.metCut - 20.0),maxMET=options.maxMET)
    if do_met_signif:
        #cuts += [CutItem('CutMetSignif','met_significance > 4.0')]
        cutMetSignif = CutItem('CutMetSignif')
        cutMetSignif.AddCut(CutItem('Muon',  'n_mu_w>0'), 'OR')
        cutMetSignif.AddCut(CutItem('METSig', 'met_significance > 4.0'), 'OR')
        cuts += [cutMetSignif]
        cutWMT = CutItem('CutWMT')
        cutWMT.AddCut(CutItem('Electron',  'n_el_w>0'), 'OR')
        if basic_cuts.analysis.count('LowMETQCD'):
            cutWMT.AddCut(CutItem('MTW', 'mt > 40.0'), 'OR')
        else:
            cutWMT.AddCut(CutItem('MTW', 'mt > 20.0'), 'OR')
        cuts += [cutWMT]
    # VBF cuts
    cuts+=getVBFCuts(options, basic_cuts, isLep=True)

    return GetCuts(cuts)

def getWCRAntiIDCuts(cut = '', options=None, basic_cuts=None, ignore_met=False, do_met_signif=False):
    # Get WCR cuts. *Don't* use the WCR met significance cut here.
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
    #new_cuts.append(CutItem("CutNoSigLeps", "n_lep_w == 0"))
    new_cuts.append(CutItem("CutNoSigLeps", "n_siglep == 0"))
    # Add the trigger isolation: ptvarcone30/pt < 0.07 for mu, ptvarcone20/pt<0.1
    # Only do for muons. For now, do for none!
    #if basic_cuts.chan[0] != 'e':
    #    new_cuts.append(CutItem("CutPtVarCone", "baselep_ptvarcone_0 > 0.07"))

    # Debugging: print out the cuts.
    #print("Selection in anti-ID region (%s):" % (basic_cuts.chan))
    #for cutobj in new_cuts:
    #    print("%s: %s" % (cutobj.cut_name, cutobj.cut_conf))
    #sys.exit(1)

    # Apply metsig cut. By default, will do nothing.
    # useful for studies of a variable in either low or high met significance.
    new_cuts += basic_cuts.getMetsigCut()

    # Apply extra lepton pT binning if we're running in that mode.
    if basic_cuts.ExtraLepPtLowerCut != 0 or basic_cuts.ExtraLepPtUpperCut != -1:
        new_cuts += basic_cuts.getExtraLepPtCut()

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
    #sigs['hvbf500']  = ['hvbf500']
    #sigs['hvbf1k']  = ['hvbf1k']
    #sigs['hvbf3k']  = ['hvbf3k']

    bkgs = {}

    bkgs['wqcd'] = ['wqcd']
    bkgs['zqcd'] = ['zqcd']
    bkgs['wewk'] = ['wewk']
    bkgs['zewk'] = ['zewk']
    bkgs['tall'] = ['top2','vvv']
    #bkgs['vvv'] =['vvv']
    bkgs['dqcd'] = ['dqcd']
    bkgs['mqcd'] = ['mqcd']
    if options.OverlapPh:
        sigs['vbfg'] = ['vbfg']
        sigs['higgs'] += ['vbfg']
        bkgs['ttg']  = ['ttg']
        bkgs['pho']  = ['pho']
        bkgs['phoAlt']  = ['phoAlt']
        bkgs['wgam'] = ['wgam']
        bkgs['zgam'] = ['zgam','vgg']
        bkgs['wgamewk'] = ['wgamewk']
        bkgs['zgamewk'] = ['zgamewk']
        bkgs['efakeph'] = ['efakeph']
        bkgs['jfakeph'] = ['jfakeph']
        del bkgs['wqcd']
        del bkgs['zqcd']
        del bkgs['wewk']
        del bkgs['zewk']
    other={}
    other['dqcd']    = ['dqcd']
    other['zqcdMad'] = ['zqcdMad']
    other['wqcdMad'] = ['wqcdMad']
    other['zqcdPow'] = ['zqcdPow']
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
            #reg.SetVal(key, 'higgs,tall,wqcd,wewk,zqcd,zewk,mqcd,ttg,pho,phoAlt,wgam,zgam,zgamewk,wgamewk,bkgs,data')
            reg.SetVal(key, 'higgs,tall,mqcd,ttg,pho,phoAlt,wgam,zgam,zgamewk,wgamewk,efakeph,jfakeph,bkgs,data')
        else:
            if options.mergeMGExt:                            
                reg.SetVal(key, 'higgs,tall,wqcdMad,wewk,zqcdMad,zewk,dqcd,bkgs,data')
            else:
                reg.SetVal(key, 'higgs,tall,wqcd,wewk,zqcd,zewk,dqcd,bkgs,data')
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

def preparePassEventForWCRAntiID(alg_name, options, basic_cuts, cut='BASIC', do_met_signif=False):
    """ Prepare events for the anti-ID version of the WCR."""
    reg  = ROOT.Msl.Registry()
    cuts = getWCRAntiIDCuts(cut, options, basic_cuts, ignore_met=options.ignore_met, do_met_signif=do_met_signif)
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
