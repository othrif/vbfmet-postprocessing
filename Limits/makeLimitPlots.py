#!/usr/bin/env python

#
# Authors: Doug Schaefer, schae@cern.ch
#          Rustem Ospanov, rustem@cern.ch
#

#
# Example usage:
#   export LOUT=/afs/cern.ch/user/t/trigcomm/w0/rates/schae/testarea/PhysicsLimit
#   python makeLimitPlots.py $LOUT/results_lep5_afterPtll:lep5_AfterPtll $LOUT/results_lep5_norm:lep5_BeforePtll --opath=limit-out
#   python makeLimitPlots.py --mva-key=lep5,Ptll --opath=limit-out
#

import os
import sys
import math

from array     import array
from optparse  import OptionParser

# Default path
ipath_default = '/afs/cern.ch/user/t/trigcomm/w0/rates/trigrate/testarea/PhysicsLimit'

p = OptionParser()

p.add_option( '--opath',     type='string',      default=None,                 dest='opath',      help='Specify the output path like ./plots')
p.add_option( '--ipath',     type='string',      default=ipath_default,        dest='ipath',      help='Input path for --mva-key')
p.add_option( '--mass',      type='string',      default=None,                 dest='mass',       help='Run one mass point like 160')
p.add_option( '--mva',       type='string',      default='Cut Based',          dest='mva',        help='MVA Name')
p.add_option( '--analysis',  type='string',      default='hipt',               dest='analysis',   help='Analysis')
p.add_option( '--lumi',      type='string',      default='4.6',                dest='lumi',       help='Integrated Luminosity')
p.add_option( '--mva-key',   type='string',      default=None,                 dest='mva_key',    help='MVA Key to wildcard: separated by , or _')
p.add_option( '--mva-token', type='string',      default=None,                 dest='mva_token',  help='MVA Token to separate --mva-key: , or _ -- try both by default')
p.add_option( '--max-mass',  type='string',      default=None,                 dest='max_mass',   help='Draws up to max mass point')
p.add_option( '--style',     type='string',      default='atlas',              dest='style',      help='Plot style: atlas, tmhong')
p.add_option( '--file-type', type='string',      default='eps',                dest='file_type',  help='Image type: pdf eps png')
p.add_option( '--first',     type='string',      default=None,                 dest='first',      help='Filter for ratio')

p.add_option( '--scaleXS',      action='store_true',default=False,               dest='scaleXS',      help='Scale the XS')
p.add_option( '--debug',      action='store_true',default=False,               dest='debug',      help='Run in debug mode')
p.add_option( '--draw-obs',   action='store_true',default=False,               dest='draw_obs',   help='Draw the observed limit')
p.add_option( '--no-wait',    action='store_true',default=False,               dest='no_wait',    help='Run in batch mode')
p.add_option( '--logy',       action='store_true',default=False,               dest='logy',       help='Use Log y')

(options, args) = p.parse_args()

import ROOT #, PyCintex
import LimitPlotsConfig as plotConfig

log = plotConfig.getLog('makeLimitPlots.py')

#---------------------------------------------------------------------------------------------
#
# Formatting
#
try:
    import LimitPlotsConfig
    LimitPlotsConfig.setATLASDefaults(ROOT)
except ImportError:
    ROOT.gROOT.Reset()
    print 'Failed to import LimitPlotsConfig... continue without ATLAS style'

if options.style == 'atlas':
    testarea=os.getenv('TestArea')
    print '%s/HWWMVACode/atlasstyle/AtlasStyle.C'  %(testarea)
    #ROOT.gROOT.LoadMacro('%s/HWWMVACode/atlasstyle/AtlasStyle.C'  %(testarea))
    #ROOT.gROOT.LoadMacro('%s/HWWMVACode/atlasstyle/AtlasUtils.C'  %(testarea))
    #ROOT.gROOT.LoadMacro('%s/HWWMVACode/atlasstyle/AtlasLabels.C' %(testarea))
    testarea='/Users/schae/testarea/SUSY/JetUncertainties/testingMacros/atlasstyle'
    ROOT.gROOT.LoadMacro('%s/AtlasStyle.C'  %(testarea))
    ROOT.gROOT.LoadMacro('%s/AtlasUtils.C'  %(testarea))
    ROOT.gROOT.LoadMacro('%s/AtlasLabels.C' %(testarea))
    ROOT.SetAtlasStyle()
    ROOT.gStyle.SetFillColor(10)


def GetXSLine(arr_mass):
    xaxis=[10.00  ] ; xss=[1.121E+01   ]
    xaxis+=[15.00 ] ; xss+=[1.074E+01   ]
    xaxis+=[20.00 ] ; xss+=[1.025E+01   ]
    xaxis+=[25.00 ] ; xss+=[9.769E+00   ]
    xaxis+=[30.00 ] ; xss+=[9.299E+00   ]
    xaxis+=[35.00 ] ; xss+=[8.847E+00   ]
    xaxis+=[40.00 ] ; xss+=[8.419E+00   ]
    xaxis+=[45.00 ] ; xss+=[8.011E+00   ]
    xaxis+=[50.00 ] ; xss+=[7.627E+00   ]
    xaxis+=[55.00 ] ; xss+=[7.264E+00   ]
    xaxis+=[60.00 ] ; xss+=[6.924E+00   ]
    xaxis+=[65.00 ] ; xss+=[6.603E+00   ]
    xaxis+=[70.00 ] ; xss+=[6.301E+00   ]
    xaxis+=[75.00 ] ; xss+=[6.016E+00   ]
    xaxis+=[80.00 ] ; xss+=[5.748E+00   ]
    xaxis+=[85.00 ] ; xss+=[5.496E+00   ]
    xaxis+=[90.00 ] ; xss+=[5.258E+00   ]
    xaxis+=[95.00 ] ; xss+=[5.034E+00   ]
    xaxis+=[100.00 ] ; xss+=[	4.822E+00   ]
    xaxis+=[105.00 ] ; xss+=[	4.623E+00   ]
    xaxis+=[110.00 ] ; xss+=[	4.434E+00   ]
    xaxis+=[115.00 ] ; xss+=[	4.255E+00   ]
    xaxis+=[120.00 ] ; xss+=[	4.086E+00   ]
    xaxis+=[125.00 ] ; xss+=[	3.925E+00   ]
    xaxis+=[130.00 ] ; xss+=[	3.773E+00   ]
    xaxis+=[135.00 ] ; xss+=[	3.629E+00   ]
    xaxis+=[140.00 ] ; xss+=[	3.492E+00   ]
    xaxis+=[145.00 ] ; xss+=[	3.362E+00   ]
    xaxis+=[150.00 ] ; xss+=[	3.239E+00   ]
    xaxis+=[160.00 ] ; xss+=[	3.010E+00   ]
    xaxis+=[170.00 ] ; xss+=[	2.802E+00   ]
    xaxis+=[180.00 ] ; xss+=[	2.612E+00   ]
    xaxis+=[190.00 ] ; xss+=[	2.440E+00   ]
    xaxis+=[200.00 ] ; xss+=[	2.282E+00   ]
    xaxis+=[210.00 ] ; xss+=[	2.138E+00   ]
    xaxis+=[220.00 ] ; xss+=[	2.006E+00   ]
    xaxis+=[230.00 ] ; xss+=[	1.884E+00   ]
    xaxis+=[240.00 ] ; xss+=[	1.772E+00   ]
    xaxis+=[250.00 ] ; xss+=[	1.669E+00   ]
    xaxis+=[260.00 ] ; xss+=[	1.573E+00   ]
    xaxis+=[270.00 ] ; xss+=[	1.485E+00   ]
    xaxis+=[280.00 ] ; xss+=[	1.403E+00   ]
    xaxis+=[290.00 ] ; xss+=[	1.326E+00   ]
    xaxis+=[300.00 ] ; xss+=[	1.256E+00   ]
    xaxis+=[310.00 ] ; xss+=[	1.190E+00   ]
    xaxis+=[320.00 ] ; xss+=[	1.128E+00   ]
    xaxis+=[330.00 ] ; xss+=[	1.071E+00   ]
    xaxis+=[340.00 ] ; xss+=[	1.017E+00   ]
    xaxis+=[350.00 ] ; xss+=[	9.666E-01   ]
    xaxis+=[360.00 ] ; xss+=[	9.194E-01   ]
    xaxis+=[370.00 ] ; xss+=[	8.752E-01   ]
    xaxis+=[380.00 ] ; xss+=[	8.337E-01   ]
    xaxis+=[390.00 ] ; xss+=[	7.947E-01   ]
    xaxis+=[400.00 ] ; xss+=[	7.580E-01   ]
    xaxis+=[410.00 ] ; xss+=[	7.235E-01   ]
    xaxis+=[420.00 ] ; xss+=[	6.909E-01   ]
    xaxis+=[430.00 ] ; xss+=[	6.602E-01   ]
    xaxis+=[440.00 ] ; xss+=[	6.312E-01   ]
    xaxis+=[450.00 ] ; xss+=[	6.038E-01   ]
    xaxis+=[460.00 ] ; xss+=[	5.778E-01   ]
    xaxis+=[470.00 ] ; xss+=[	5.533E-01   ]
    xaxis+=[480.00 ] ; xss+=[	5.301E-01   ]
    xaxis+=[490.00 ] ; xss+=[	5.081E-01   ]
    xaxis+=[500.00 ] ; xss+=[	4.872E-01   ]
    xaxis+=[550.00 ] ; xss+=[	3.975E-01   ]
    xaxis+=[600.00 ] ; xss+=[	3.274E-01   ]
    xaxis+=[650.00 ] ; xss+=[	2.719E-01   ]
    xaxis+=[700.00 ] ; xss+=[	2.275E-01   ]
    xaxis+=[750.00 ] ; xss+=[	1.915E-01   ]
    xaxis+=[800.00 ] ; xss+=[	1.622E-01   ]
    xaxis+=[850.00 ] ; xss+=[	1.380E-01   ]
    xaxis+=[900.00 ] ; xss+=[	1.180E-01   ]
    xaxis+=[950.00 ] ; xss+=[	1.013E-01   ]
    xaxis+=[1000.00 ] ; xss+=[	8.732E-02]	 
    xaxis+=[1050.00 ] ; xss+=[	7.551E-02]	 
    xaxis+=[1100.00 ] ; xss+=[	6.550E-02]	 
    xaxis+=[1150.00 ] ; xss+=[	5.698E-02]	 
    xaxis+=[1200.00 ] ; xss+=[	4.970E-02]	 
    xaxis+=[1250.00 ] ; xss+=[	4.345E-02]	 
    xaxis+=[1300.00 ] ; xss+=[	3.807E-02]	 
    xaxis+=[1350.00 ] ; xss+=[	3.343E-02]	 
    xaxis+=[1400.00 ] ; xss+=[	2.941E-02]	 
    xaxis+=[1450.00 ] ; xss+=[	2.592E-02]	 
    xaxis+=[1500.00 ] ; xss+=[	2.288E-02]	 
    xaxis+=[1550.00 ] ; xss+=[	2.023E-02]	 
    xaxis+=[1600.00 ] ; xss+=[	1.791E-02]	 
    xaxis+=[1650.00 ] ; xss+=[	1.588E-02]	 
    xaxis+=[1700.00 ] ; xss+=[	1.410E-02]	 
    xaxis+=[1750.00 ] ; xss+=[	1.253E-02]	 
    xaxis+=[1800.00 ] ; xss+=[	1.115E-02]	 
    xaxis+=[1850.00 ] ; xss+=[	9.926E-03]	 
    xaxis+=[1900.00 ] ; xss+=[	8.849E-03]	 
    xaxis+=[1950.00 ] ; xss+=[	7.896E-03]	 
    xaxis+=[2000.00 ] ; xss+=[	7.052E-03]	 
    xaxis+=[2050.00 ] ; xss+=[	6.303E-03]	 
    xaxis+=[2100.00 ] ; xss+=[	5.638E-03]	 
    xaxis+=[2150.00 ] ; xss+=[	5.046E-03]	 
    xaxis+=[2200.00 ] ; xss+=[	4.520E-03]	 
    xaxis+=[2250.00 ] ; xss+=[	4.051E-03]	 
    xaxis+=[2300.00 ] ; xss+=[	3.633E-03]	 
    xaxis+=[2350.00 ] ; xss+=[	3.259E-03]	 
    xaxis+=[2400.00 ] ; xss+=[	2.925E-03]	 
    xaxis+=[2450.00 ] ; xss+=[	2.627E-03]	 
    xaxis+=[2500.00 ] ; xss+=[	2.360E-03]	 
    xaxis+=[2550.00 ] ; xss+=[	2.122E-03]	 
    xaxis+=[2600.00 ] ; xss+=[	1.908E-03]	 
    xaxis+=[2650.00 ] ; xss+=[	1.717E-03]	 
    xaxis+=[2700.00 ] ; xss+=[	1.545E-03]	 
    xaxis+=[2750.00 ] ; xss+=[	1.391E-03]	 
    xaxis+=[2800.00 ] ; xss+=[	1.252E-03]	 
    xaxis+=[2850.00 ] ; xss+=[	1.128E-03]	 
    xaxis+=[2900.00 ] ; xss+=[	1.016E-03]	 
    xaxis+=[2950.00 ] ; xss+=[	9.156E-04]	 
    xaxis+=[3000.00 ] ; xss+=[	8.253E-04]
    xsMap={}
    xsMap[50]=7.627 #7.627E+00 
    xsMap[75]=6.016 #6.016E+00
    xsMap[100]=4.822 #4.822E+00
    xsMap[125]=3.925 #3.925E+00 
    xsMap[300]=1.256 #1.256E+00 
    xsMap[750]=0.1915 #0.1915
    xsMap[1000]=0.08732 #0.08732
    xsMap[2000]=0.007052 #0.007052
    xsMap[3000]=0.0008253 #0.0008253
    #h=ROOT.TH1F('exclLine','exclLine',10,0.0,1000.0)
    #list_obs=[7.627,6.016,4.822,3.925,1.256,0.1915,0.08732,0.007052,0.0008253]
    arr_xaxis=array('d', xaxis)
    arr_obs=array('d', xss)
    h=ROOT.TGraphAsymmErrors(len(arr_xaxis), arr_xaxis, arr_obs)
    h.SetLineColor(2)
    return h

def getATLASLabels(pad, x, y, text=None, selkey=None):
    l = ROOT.TLatex(x, y, 'ATLAS')
    l.SetNDC()
    l.SetTextFont(72)
    l.SetTextSize(0.07)
    l.SetTextAlign(11)
    l.SetTextColor(ROOT.kBlack)
    l.Draw()

    #delx = 0.05*pad.GetWh()/(pad.GetWw())
    labs = [l]

    if True:
        p = ROOT.TLatex(x+0.11, y, ' Internal') #
        #p = ROOT.TLatex(x+0.11, y, ' Preliminary') #
        p.SetNDC()
        p.SetTextFont(42)
        p.SetTextSize(0.065)
        p.SetTextAlign(11)
        p.SetTextColor(ROOT.kBlack)
        p.Draw()
        labs += [p]

        a = ROOT.TLatex(x, y-0.04, '#sqrt{#it{s}} = 13 TeV, %.0f fb^{-1}' %(139e3/1.0e3))
        a.SetNDC()
        a.SetTextFont(42)
        a.SetTextSize(0.05)
        a.SetTextAlign(12)
        a.SetTextColor(ROOT.kBlack)
        a.Draw()
        labs += [a]

        
        d = ROOT.TLatex(x, y-0.1, 'Limits at 95% CL')
        d.SetNDC()
        d.SetTextFont(42)
        d.SetTextSize(0.05)
        d.SetTextAlign(12)
        d.SetTextColor(ROOT.kBlack)
        labs += [d]
        
    if text != None:

        c = ROOT.TLatex(x, y-0.1, text)
        c.SetNDC()
        c.SetTextFont(42)
        c.SetTextSize(0.05)
        c.SetTextAlign(12)
        c.SetTextColor(ROOT.kBlack)
        labs += [c]
        
        
    for l in labs:
        l.Draw()
    return labs
#---------------------------------------------------------------------------------------------
def MeanAndError(list):


    num = float(len(list))
    if num==0: return 0.0,0.0

    avg=sum(list)/num
    
    chi2=0.0
    for i in list: chi2+=(i-avg)*(i-avg)
    rms=math.sqrt(chi2/num)

    return avg,rms

#---------------------------------------------------------------------------------------------
def GetLumi(name, lumi=options.lumi):

    if name==None:
        return lumi

    if   name.count('BtoK') and not name.count('LtoM'): return '2.3'
    elif name.count('LtoM') and not name.count('BtoK'): return '2.4'

    return int(lumi)

#---------------------------------------------------------------------------------------------
def GetAnalysis(name): 

    ana_type = 'H#rightarrowWW#rightarrow'

    if name==None:
        return ana_type

    if   name.count('ee'):   ana_type+='e#nue#nu'
    elif name.count('eu'):   ana_type+='e#nu#mu#nu'
    elif name.count('uu'):   ana_type+='#mu#nu#mu#nu'
    else:                    ana_type+='l#nul#nu'
    
    if  name.count('0j'):    ana_type+=', 0j'
    elif name.count('1j'):   ana_type+=', 1j'
    elif name.count('2j'):   ana_type+=', 2j'
    
    return "" #ana_type

#---------------------------------------------------------------------------------------------
def GetType(name): 

    ana_type = 'Cut Based'

    if name==None:
        return ana_type

    if   name.count('aaron'):    ana_type='Aaron'
    elif name.count('bdt'):      ana_type='BDT'
    elif name.count('knn'):      ana_type='kNN'
    elif name.count('ptll'):     ana_type='P_{T}>40'
    elif name.count('MTCut'):    ana_type='M_T Cut'
    elif name.count('MT100'):    ana_type='M_T Cut'
    elif name.count('MTFit'):    ana_type='M_T Fit'
    elif name.count('_withstat'):    ana_type+=' With Stat Errors'    
    elif name.count('loptonly'): ana_type+=' Low P_{T} Only'
    elif name.count('lopt130'):  ana_type+=' With Low P_{T} MTCut'    
    elif name.count('lopt'):     ana_type+=' With Low P_{T}'    
    elif not name.count('lopt'): ana_type+=' High P_{T} Only'


    if name.count('pt15'):       ana_type+=', 15GeV'
    elif name.count('pt20'):     ana_type+=', 20GeV'
    elif name.count('pt25'):     ana_type+=', 25GeV'
    elif name.count('pt30'):     ana_type+=', 30GeV'

    if name.count('subl15'):       ana_type+=', switch 15GeV'
    elif name.count('subl20'):     ana_type+=', switch 20GeV'
    elif name.count('subl25'):     ana_type+=', switch 25GeV'
    elif name.count('subl30'):     ana_type+=', switch 30GeV'

    if name.count('subliso15'):       ana_type+=', subl Iso 15GeV'
    elif name.count('subliso20'):     ana_type+=', subl Iso 20GeV'
    elif name.count('subliso25'):     ana_type+=', subl Iso 25GeV'
    elif name.count('subliso30'):     ana_type+=', subl Iso 30GeV'

    if   name.count('BtoK') and not name.count('LtoM'): ana_type+=', BtoK'
    elif name.count('LtoM') and not name.count('BtoK'): ana_type+=', LtoM'
    elif name.count('LtoM') and     name.count('BtoK'): ana_type+=', Split Periods'            

    if name.count('Reanalysis'): ana_type='Reanalysis'
    if name.count('Pub'): ana_type='Publication'

    return "" #"VBF+MET"#ana_type

#---------------------------------------------------------------------------------------------
def GetTypeName(name):
    typ = GetType(name)
    typ+=' '
    typ+=GetAnalysis(name)
    return typ

#---------------------------------------------------------------------------------------------
def GetLegend(name,wide=0.50):
    leg = ROOT.TLegend(0.2, 0.6, wide, 0.87)
    if name!=None:
        leg.SetHeader(name)
    leg.SetBorderSize(0)
    leg.SetTextFont(42)
    leg.SetFillColor(0)
    #leg.SetTextSize(0)
    return leg

#---------------------------------------------------------------------------------------------
def AddAtlasName(name):
    
    try:
        from ROOT import ATLASLabel,myText
        ATLASLabel(0.2,0.88); myText(0.28,0.88,1,'Private');
        myText(0.70,0.88,1,GetAnalysis(name));
        myText(0.70,0.78,1,'#intL dt = %s fb^{-1}' %(GetLumi(name,options.lumi)));
        myText(0.70,0.68,1,'#sqrt{s} = 7 TeV');            
    except ImportError:
        print 'ERROR could not import ATLAS title'

#---------------------------------------------------------------------------------------------
class FitPoint:

    def __init__(self, mass):

        self.mass     = mass
        self.obs_mu   = None
        self.exp_mu   = None
        self.pos_2sig = None
        self.pos_1sig = None
        self.neg_2sig = None
        self.neg_1sig = None
        self.xsMap={}
        if options.scaleXS:
            self.xsMap[50]=(7.4355) #7.627E+00 
            self.xsMap[75]=(5.8396) #6.016E+00
            self.xsMap[100]=(4.6674) #4.822E+00
            self.xsMap[125]=(3.782) #3.925E+00 
            self.xsMap[300]=(0.024186) #1.256E+00 
            self.xsMap[750]=(0.00018346) #0.1915
            self.xsMap[1000]=(4.9409e-05) #0.08732
            self.xsMap[2000]=(8.013e-06) #0.007052
            self.xsMap[3000]=(2.4363e-06) #0.0008253
        else:
            self.xsMap[50]=(7.4355)/7.627 #7.627E+00 
            self.xsMap[75]=(5.8396)/6.016 #6.016E+00
            self.xsMap[100]=(4.6674)/4.822 #4.822E+00
            self.xsMap[125]=(3.782)/3.925 #3.925E+00 
            self.xsMap[300]=(0.024186)/1.256 #1.256E+00 
            self.xsMap[750]=(0.00018346)/0.1915 #0.1915
            self.xsMap[1000]=(4.9409e-05)/0.08732 #0.08732
            self.xsMap[2000]=(8.013e-06)/0.007052 #0.007052
            self.xsMap[3000]=(2.4363e-06)/0.0008253 #0.0008253
    def ScaleXS(self):
        
        if self.mass in self.xsMap:
            scaleXS=self.xsMap[self.mass]
            self.obs_mu*=scaleXS
            self.exp_mu   *=scaleXS
            self.pos_2sig *=scaleXS
            self.pos_1sig *=scaleXS
            self.neg_2sig *=scaleXS
            self.neg_1sig *=scaleXS
    def IsValid(self):
        vars = [self.obs_mu,
                self.exp_mu,
                self.pos_2sig,
                self.pos_1sig,
                self.neg_2sig,
                self.neg_1sig]                
        
        return self.IsValidVars(vars)

    def IsValidVars(self, vars):
        for v in vars:
            if not self.IsValidVar(v):
                return False
        return len(vars) > 0

    def IsValidVar(self, var):
        try:
            from math import isnan
            if type(var) != type(1.0) or math.isnan(var) or math.isinf(var):
                return False
        except ImportError:
            if type(var) != type(1.0) or ('%s' %var == 'nan') or not var or  ('%s' %var == 'inf') or  var>15.0  or  var<0.0:
                return False
        return True

    def Print(self):
        print 'hmass:   ',self.mass
        print 'observ:  ',self.obs_mu
        print 'expect:  ',self.exp_mu
        print '+2sig:   ',self.pos_2sig
        print '+1sig:   ',self.pos_1sig
        print '-1sig:   ',self.neg_2sig
        print '-2sig:   ',self.neg_1sig    

#---------------------------------------------------------------------------------------------
class LimitHists:
 
    def __init__(self, name, points):

        if len(points) < 1:
            print 'LimitHists - need at least obe fit point... expect troubles'
            return

        mass = []
        bins = []

        for fp in points:
            mass += [fp.mass]
            
        mass = sorted(mass)

        if len(mass)==1:
            bins.append(float(mass[0])-2.5)
            bins.append(float(mass[0])+2.5)
        else:
            for m in range(0, len(mass)):
                if m == 0:
                    width=(float(mass[m+1])-float(mass[m]))/2.0
                    bins.append(float(mass[m])-width)
                    bins.append(float(mass[m])+width)
                elif m == len(mass)-1:
                    width=(float(mass[m])-float(mass[m-1]))/2.0
                    bins.append(float(mass[m])+1.0)#+width)                    
                else:
                    width=(float(mass[m+1])-float(mass[m]))/2.0
                    bins.append(float(mass[m])+width)

        if options.debug:
            print 'Print mass and bin arrays:'
            print mass
            print bins            
            for b in bins:
                print 'bin=%f' %b

        list_pos_1sig = []
        list_pos_2sig = []    
        list_neg_1sig = []
        list_neg_2sig = []
        list_exp      = []
        list_obs      = []        
        list_empty    = []
        list_mass     = []
        list_one      = []

        self.name       = name
        self.points     = points
        self.mass       = mass
        self.bins       = bins
        self.bins_array = array('d', bins)
        self.bins_arrayone = array('d', bins+[float(mass[len(mass)-1])+1000.0])        
        self.mass_array = array('d', mass)

        self.color      = None
        self.exclusions = None
        
        self.obs = self.GetTH1('observ', self.bins_array)
        self.exp = self.GetTH1('expect', self.bins_array)
        self.one = self.GetTH1('one',    self.bins_arrayone)
    
        #
        # Filling histograms
        #
        if options.debug:
            for ibin in range(1, self.one.GetNbinsX()+1):
                print 'ibin=%d ledge=%f center=%f' %(ibin, self.one.GetBinLowEdge(ibin), self.one.GetBinCenter(ibin))

        ymax = None
        
        log_buf = '%s -' % name
        for fp in points:
            log_buf = log_buf + ' %s' % str(fp.mass)
        
            self.exp.Fill(fp.mass, fp.exp_mu)
            self.obs.Fill(fp.mass, fp.obs_mu)
            self.one.Fill(fp.mass, 1.0)
            for ib in range(1,self.one.GetNbinsX()+2):
                self.one.SetBinContent(ib,1.0)
            
            list_pos_1sig.append(fp.pos_1sig - fp.exp_mu)
            list_pos_2sig.append(fp.pos_2sig - fp.exp_mu)
            list_neg_1sig.append(fp.exp_mu - fp.neg_1sig)
            list_neg_2sig.append(fp.exp_mu - fp.neg_2sig)
            list_exp     .append(fp.exp_mu)
            list_obs     .append(fp.obs_mu)            
            list_empty   .append(0.0)
            list_mass    .append(fp.mass)
            list_one     .append(1.0)
            if ymax == None: ymax = fp.pos_2sig
            else:            ymax = max([fp.pos_2sig, ymax])

        log.info(log_buf)
        del log_buf

        arr_pos_1sig = array('d', list_pos_1sig)
        arr_pos_2sig = array('d', list_pos_2sig)
        arr_neg_1sig = array('d', list_neg_1sig)
        arr_neg_2sig = array('d', list_neg_2sig)

        arr_ratio_pos_1sig = array('d', self.Ratio(list_exp,list_pos_1sig))
        arr_ratio_pos_2sig = array('d', self.Ratio(list_exp,list_pos_2sig))
        arr_ratio_neg_1sig = array('d', self.Ratio(list_exp,list_neg_1sig))
        arr_ratio_neg_2sig = array('d', self.Ratio(list_exp,list_neg_2sig))        

        arr_obs      = array('d', list_obs)
        arr_exp      = array('d', list_exp)
        arr_empty    = array('d', list_empty)
        arr_mass     = array('d', list_mass)
        arr_one     = array('d', list_one)        

        self.SMoneLine = GetXSLine(arr_mass)
        self.obs_graph       = ROOT.TGraphAsymmErrors(len(arr_mass), arr_mass, arr_obs)
        self.exp_graph       = ROOT.TGraphAsymmErrors(len(arr_mass), arr_mass, arr_exp)
        self.sig1_err        = ROOT.TGraphAsymmErrors(len(arr_mass), arr_mass, arr_exp, arr_empty, arr_empty, arr_neg_1sig,       arr_pos_1sig)
        self.sig2_err        = ROOT.TGraphAsymmErrors(len(arr_mass), arr_mass, arr_exp, arr_empty, arr_empty, arr_neg_2sig,       arr_pos_2sig)
        self.ratio_sig1_err  = ROOT.TGraphAsymmErrors(len(arr_mass), arr_mass, arr_one, arr_empty, arr_empty, arr_ratio_neg_1sig, arr_ratio_pos_1sig)
        self.ratio_sig2_err  = ROOT.TGraphAsymmErrors(len(arr_mass), arr_mass, arr_one, arr_empty, arr_empty, arr_ratio_neg_2sig, arr_ratio_pos_2sig)        
        #
        # Formatting and Drawing Histograms
        #
        self.exp.SetXTitle('Mediator mass [GeV]')
        self.exp.SetYTitle('#sigma/#sigma_{SM}')
        self.obs.SetXTitle('Mediator mass [GeV]')
        self.obs.SetYTitle('#sigma/#sigma_{SM}')
        self.obs.SetMarkerSize(0)
        if options.scaleXS:
            self.obs.SetYTitle('#sigma_{SM}^{VBF} x  #it{B}_{inv} [pb]') 
            self.exp.SetYTitle('#sigma_{SM}^{VBF} x  #it{B}_{inv} [pb]') 
        self.sig2_err      .SetName('TwoSigmaBand')
        self.sig1_err      .SetName('OneSigmaBand')
        self.ratio_sig2_err.SetName('TwoSigmaBand')
        self.ratio_sig1_err.SetName('OneSigmaBand')        
        self.obs           .SetName('Observed')
        self.exp           .SetName('Expected')
        
        self.one.SetLineStyle(2)
        self.one.SetLineWidth(2)
        self.one.SetLineColor(23)
        
        self.exp.SetLineColor(1)
        self.exp.SetLineStyle(2)
        self.exp.SetLineWidth(2)
        self.exp.SetMarkerStyle(0)
        
        self.exp_graph.SetLineColor(1)
        self.exp_graph.SetLineStyle(2)
        self.exp_graph.SetLineWidth(2)
        self.exp_graph.SetMarkerStyle(0)
        
        self.obs_graph.SetLineStyle(1)
        self.obs_graph.SetLineWidth(2)        
        self.obs_graph.SetMarkerStyle(11)
        self.obs_graph.SetMarkerSize(0.80)
        
        self.sig2_err.SetLineColor(ROOT.kYellow)
        self.sig2_err.SetFillColor(ROOT.kYellow)
        self.sig1_err.SetLineColor(ROOT.kGreen)
        self.sig1_err.SetFillColor(ROOT.kGreen)
        self.ratio_sig2_err.SetLineColor(ROOT.kYellow)
        self.ratio_sig2_err.SetFillColor(ROOT.kYellow)
        self.ratio_sig1_err.SetLineColor(ROOT.kGreen)
        self.ratio_sig1_err.SetFillColor(ROOT.kGreen)

        self.obs.SetMaximum(1.1*ymax)
        self.exp.SetMaximum(1.1*ymax)

    def GetFitPoints(self,points):
        points_val=[]
        for fp in points:
            fpn = None
            for i in self.points:
                if i.mass==fp.mass:
                    fpn=i
                    break
            if fpn==None:
                points_val+=[1.0]
                continue
                
            elif fp.IsValid() and fpn.IsValid():
                n=fp.obs_mu
                d=fpn.obs_mu
                if d==0:  points_val+=[1.0]
                else:     points_val+=[n/d]
                
        return points_val

    def GetTH1(self, name, arr):
        
        if len(arr) < 1:
            print 'GetTH1 - invalid nbin=%d' %nbin
            
        h = ROOT.TH1F(name, name, len(arr)-1, arr)
        h.SetStats(False)
        h.SetDirectory(0)
        
        return h

    def Ratio(self,obs,errors):
        ratio_errors=[]
        for i in range(0,len(errors)):
            if   obs[i]==0: ratio_errors+=[0.0]
            else:           ratio_errors+=[errors[i]/obs[i]]

        return ratio_errors

    def Draw(self):

        draw_opts = 'SAME'
        if len(self.mass)>1:
            draw_opts = 'SAME E3'
    
        self.exp.Draw('AXIS')
        self.sig2_err.Draw(draw_opts)
        self.sig1_err.Draw(draw_opts)
        if options.draw_obs:
            self.obs_graph.Draw('L P')
        self.exp_graph.Draw('L')
        self.exp.Draw('AXIS SAME')
        #self.one.Draw('L SAME')
        #onelin=ROOT.TLine(0.0,1.0,300,1.0)
        #onelin.SetLineColor(2)
        #onelin.SetLineWidth(2)
        #onelin.Draw()
        
        self.SMoneLine.Draw('L same')

        self.leg4 = GetLegend(None)

        self.leg4.SetHeader(GetTypeName(self.name)+'') #options.mva
        if options.draw_obs:
            self.leg4.AddEntry(self.obs, self.obs.GetName(), 'pl')

        self.leg4.AddEntry(self.SMoneLine,  '#sigma_{SM}^{VBF} with #it{B}_{inv}=1', 'l')
        self.leg4.AddEntry(self.exp,         self.exp.GetName(), 'l')
        self.leg4.AddEntry(self.sig2_err,   '#pm2#sigma',       'F')
        self.leg4.AddEntry(self.sig1_err,   '#pm1#sigma',       'F')
        self.leg4.Draw()
        labsA=getATLASLabels(None,0.65,0.9)
        for l in labsA:
            l.Draw()
        #AddAtlasName(self.name)

    def DrawRatio(self,hists):

        draw_opts = 'SAME'
        if len(self.mass)>1:
            draw_opts = 'SAME E3'

        self.exp.Draw('AXIS')
        self.ratio_sig2_err.Draw(draw_opts)
        self.ratio_sig1_err.Draw(draw_opts)
        for h in hists:
            h.Draw('L SAME')
        self.one.Draw('L SAME')
        #self.exp.Draw('AXIS SAME')
        self.leg4 = GetLegend(None)

        self.leg4.SetHeader(GetTypeName(self.name)+'') #options.mva
            
        self.leg4.AddEntry(self.exp,            self.exp.GetName(), 'l')
        self.leg4.AddEntry(self.ratio_sig2_err, '#pm2#sigma',       'F')
        self.leg4.AddEntry(self.ratio_sig1_err, '#pm1#sigma',       'F')
        self.leg4.Draw()
        labsA=getATLASLabels(None,0.65,0.9)
        for l in labsA:
            l.Draw()
        #AddAtlasName(self.name)

    def Save(self, fout):
        
        if fout != None:
            fout.cd()
            self.obs.Write()
            self.exp.Write()        
            self.sig1_err.Write()
            self.sig2_err.Write()

#---------------------------------------------------------------------------------------------
def make_txt(fit_points, exclusions, name, output):
    print 'txt'
            
#---------------------------------------------------------------------------------------------
def make_table(fit_points, exclusions, name, output):

    #
    # Check if output directory exists for latex tables
    #
    if not output:
        return

    #
    # Write latex table
    #
    name=name.rstrip('/')
    ifile = open(output.rstrip('/')+'/'+name+'.table','w')
    ifile.write('Mediator mass ($GeV$) & Significance & Observed & $+2\sigma$ & $+\sigma$ & Expected & $-\sigma$ & $-2\sigma$ \\\\ \n')
    
    for fp in fit_points:

        observ  = fp.obs_mu
        expect  = fp.exp_mu
        ptwosig = fp.pos_2sig
        ponesig = fp.pos_1sig
        monesig = fp.neg_1sig
        mtwosig = fp.neg_2sig
        signif  = fp.signif

        if not options.draw_obs:
            observ=-1.0

        ifile.write(str(fp.mass)+' & %.3f & %.3f & %.3f & %.3f & %.3f & %.3f & %.3f \\\\ \n' %(signif,observ,ptwosig,ponesig,expect,monesig,mtwosig))

    ifile.write('\nExclusions\n')
    for ex in exclusions:
        if 'begin' in ex:
            ifile.write('$%.1f-$' %(ex['begin']))
        elif 'end' in ex:
            ifile.write('$%.1f$\n' %(ex['end']))
    ifile.write('\n') 
    ifile.close()

#---------------------------------------------------------------------------------------------
def FindExclusion(hist,sm=1.0):
    #
    # Prints region where the histogram is below 1.0
    #   -- use linear extrapolation or 
    #
    exclusions=[]
    for i in range(1,hist.GetNbinsX()):
        if i < hist.GetNbinsX():
            low_bin=hist.GetBinContent(i)
            hi_bin =hist.GetBinContent(i+1)
            if (low_bin-sm)*(hi_bin-sm) < 0.0:
                x1=hist.GetBinLowEdge(i)
                x2=hist.GetBinLowEdge(i+1)
                m=0.00001
                if (x2-x1)!=0.0:
                    m=(hi_bin-low_bin)/(x2-x1)
                # Solving for the intersection with SM = 1.0
                #     sm-y1=(x-x1)m
                #     x=(sm-y1)/m+x1
                x=(sm-low_bin)/m+x1
                exc = {'end' : x}
                if low_bin > sm:
                    exc = {'begin' : x}

                if options.debug:
                    print 'Passing 1.0: ',x
                exclusions.append(exc)
                
    print exclusions    
    return exclusions

#---------------------------------------------------------------------------------------------
def removeMissingPoints(dpoints):
    
    #
    # Count number of results per mass point
    #
    count_names = {}
    
    for name, points in dpoints.iteritems():
        for fp in points:
            try:
                count_names[fp.mass] += [name]
            except KeyError:
                count_names[fp.mass] = [name]

    #
    # Find minimum number of results across all mass points
    #
    max_count = None
    
    for names in count_names.itervalues():
        if max_count == None:
            max_count = len(names)
        else:
            max_count = max(max_count, len(names))

    #
    # Sanity check - there is at least one mass point with full set of results
    #
    if max_count != len(dpoints):
        log.warning('At least one fit is missing at all mass points... no changes')
        return dpoints

    #
    # Eliminate missing mass points
    #
    for name, points in dpoints.iteritems():
        del_list = []
        
        for fp in points:
            if len(count_names[fp.mass]) != max_count:
                del_list += [fp]
                log.info('Remove mass point: name=%s mass=%s' %(name, fp.mass))
                
        for fp in del_list:
            points.remove(fp)

        points = sorted(points)

    for name, points in dpoints.iteritems():
        log.info('removeMissingPoints: %-20s - number of mass points: %d' %(name, len(points)))

    return dpoints
            
#---------------------------------------------------------------------------------------------
def readFitPoints(path):
    #
    # List of read fit points
    #
    fit_points = []
    match_mass = []

    if options.mass != None:
        for imass in options.mass.split(','):
            match_mass.append(int(imass))
    
    for hmass in range(0, 3001):
        fpath_list = []

        fpath_list.append( path )
        fpath_list.append( '%d.root' % hmass )
        fpath = '/'.join(fpath_list)

        if len(match_mass) > 0 and hmass not in match_mass:
            continue

        if not os.path.isfile(fpath):
            continue

        fin = ROOT.TFile(fpath)
        lim = fin.Get('limit')

        fp = FitPoint(hmass)

        fp.obs_mu   = lim.GetBinContent(1)
        fp.exp_mu   = lim.GetBinContent(2)
        fp.pos_2sig = lim.GetBinContent(3)
        fp.pos_1sig = lim.GetBinContent(4)
        fp.neg_1sig = lim.GetBinContent(5)
        fp.neg_2sig = lim.GetBinContent(6)
        fp.signif   = lim.GetBinContent(7) # TODO verify: May be status now.
        #if options.scaleXS:
        fp.ScaleXS()
        if options.debug:
            fp.Print()

        if not fp.IsValid():
            print 'Ignore invalid fit point with mass=%d' %hmass
            continue

        fit_points += [fp]

    return fit_points

#---------------------------------------------------------------------------------------------
def get_canvas(c1name):

    if options.style=='tmhong':
        c1=ROOT.TCanvas(c1name,c1name,550,400)
        c1.SetRightMargin(0.35)
        c1.SetLeftMargin(0.08)
        c1.SetFillColor(ROOT.kWhite)
        c1.SetTickx()
        c1.SetTicky()
        return c1

    c1=ROOT.TCanvas(c1name,c1name,1200,600)
    if options.logy:
        c1.SetLogy()
    return c1

#---------------------------------------------------------------------------------------------
def make_limit(name, fit_points, output):

    if len(fit_points) < 1:
        print 'make_limit - failed to find any fit points'
        return None

    lh = LimitHists(name, fit_points)
        
    #
    # Draw limit plots
    #
    c1=get_canvas('limit')

    lh.Draw()
    
    c1.Modified()
    labsA=getATLASLabels(None,0.65,0.86)
    for l in labsA:
        l.Draw()

    if not options.scaleXS:
        onelin=ROOT.TLine(50.0,1.0,300,1.0)
        onelin.SetLineColor(23)
        onelin.SetLineWidth(2)
        onelin.SetLineStyle(2)
        onelin.Draw()
        c1.Update()
    if not options.no_wait:
        c1.WaitPrimitive()
    raw_input('waiting...')

    if not c1 or c1.Closed():
        sys.exit(0)

    if output and c1 and not c1.Closed():
        c1.SaveAs(output+'/'+name+'.'+options.file_type)
            
        #
        # Save limit plots
        #
        fout=ROOT.TFile(output+'/'+name+'.root', 'RECREATE')
        lh.Save(fout)
        fout.Write()
        fout.Close()

    #
    # Find the Exclusion region
    #
    lh.exclusions = FindExclusion(lh.exp)

    #
    # Write table
    #
    make_table(fit_points, lh.exclusions, name, output)

    return lh

#---------------------------------------------------------------------------------------------    
if __name__=="__main__":
    #
    # Split multiple inputs
    #
    #if len(args) < 1 and options.mva_key == None:
    #    print 'Require at least one input path.'
    #    print 'Otherwise, specify --mva-key'
    #    sys.exit(1)

    # Output directory
    if options.opath:
        output = options.opath.rstrip('/')
        
        if not os.path.exists(output):
            try:
                os.mkdir(output)
                print 'Created output directory: %s' %output                
            except IOError:
                print 'Failed to created output directory: %s' %output
                sys.exit(1)
    else:
        output = None

    # List of keys to match
    key_list = []
    if options.mva_key:
        if options.mva_token: key_list = options.mva_key.split(options.mva_token)
        if len(key_list) < 1: key_list = options.mva_key.split(',')
        if len(key_list) < 1: key_list = options.mva_key.split('_')

    limits = []
    points = {}
    name_list = []
    path_list = []
    common_name = None

    # Filter dir listing with keys
    print key_list
    if options.mva_key:

        log.info('using ipath %s' % options.ipath)
        for path in os.listdir(options.ipath):

            # Must begin with results_
            if 'results' == path[:len('results')]:

                # All keys must match
                match = True
                for key in key_list:
                    match = match and (key in path)
                    if key=='5bins': match = match and (not '25bins' in path)
                    if key=='syst' : match = match and (not 'shapesyst' in path)

                if match:
                    path_list.append( '%s/%s' %(options.ipath.rstrip('/'),path) )
                    name_list.append( '%s' %(path) )

        # Print list
        log.info('MVAs matching keys %s are:' % options.mva_key)
        for idx_path, path in enumerate(path_list):
            log.info('%d) %s' % (idx_path, path))

        # Put max on the list
        #if len(path_list) > 10:
        #    log.warning('More than 10 MVAs match, will take the first 10')
        #    name_list = name_list[:10]
        #    path_list = path_list[:10]

    # Arguments w/o options
    else:
        
        for iarg in range(0, len(args)):
            arg = args[iarg]

            # path:name
            parts = arg.split(':')
            
            if len(parts) == 1:
                path = arg
                if arg.rstrip('/').count('/'): name = arg[arg.rstrip('/').rfind('/')+1:]
                elif arg.count('/'):           name = arg[arg.rstrip('/').rfind('/'):]
                else:                          name = arg
                name=name.rstrip('/')
            elif len(parts) == 2:
                path = parts[0]
                name = parts[1]
            else:
                print 'Failed to process argument: %s' %arg
                continue

            if name in points:
                log.warning('Ignore duplicate name: %s' %name)
                continue

            name=name.rstrip('/')
            name_list.append( name )
            path_list.append( path )

            del name, path, arg

    #for i in os.listdir(options.ipath):
    #    print i
    name_list.append( 'Limits' )
    path_list.append( '%s' %(options.ipath) )
            
    if len(path_list) < 1:
        log.error('No matching MVAs')
        sys.exit(1)

    # Get 'points' for each path in the list
    for idx_name, name in enumerate(name_list):
        path = path_list[idx_name]
        points[name] = readFitPoints(path)
        if common_name == None:
            common_name = name
        else:
            common_name += '_%s' %name

    #
    # Remove mass points that miss at least one fit result
    #
    points = removeMissingPoints(points)

    #
    # Fill limit histograms
    #
    rt=None
    for name, fit_points in points.iteritems():
        limit = make_limit(name, fit_points, output)
        if options.first!=None and name.count(options.first):
            rt=limit
        else:
            if limit:
                limits += [limit]
    if rt!=None:
        limits=[rt]+limits
    elif len(limits)>0:
        rt=limits[0]
    
    #
    # Write root file with the resulting expected limit plots
    #
    if output:
        ft=ROOT.TFile(output+'/limit_all.root','RECREATE')
        
        for lim in limits:
            lim.exp.SetName(lim.name)
            lim.exp.Write()
            
        ft.Write()
        ft.Close()    

    c1=get_canvas('limit_combined')
    c1.cd()
    
    #
    # Overlay limit plots
    #
    leg4 = GetLegend(options.mva+' Expected Statistical Limits')
    print 'Overlay limit plots'
    plots=[]
    sys.exit(0)
    for ilimit in range(0, len(limits)):
        lim = limits[ilimit]

        lim.color = ilimit+1
        lim.exp.SetLineStyle(1)
        lim.exp.SetLineColor(lim.color)
        if len(limits)<10:
            leg4.AddEntry(lim.exp, GetTypeName(lim.name), 'lp')
        elif ilimit==0:
            leg4.AddEntry(lim.exp, GetTypeName(lim.name), 'lp')
            
        if options.draw_obs:
            if ilimit == 0: lim.obs.Draw('C')
            else:           lim.obs.Draw('C SAME')
        else:
            if ilimit == 0: lim.exp.Draw('C')
            else:           lim.exp.Draw('C SAME')

    leg4.Draw()
    #AddAtlasName('')
    labsA=getATLASLabels(c1,0.65,0.9)
    for l in labsA:
        l.Draw()
    c1.Update()
    if not options.no_wait:
        c1.WaitPrimitive()
    else:
        c1.WaitPrimitive()
    sys.exit(0)
    
    if output and len(limits)>0:
        if len(common_name)>40:
            common_name='stat'
        c1.SaveAs(output+'/'+common_name+'_overlay.'+options.file_type)

    #
    # Ratio of expected limits relative to first input
    #
    num_hist  = None
    den_hist  = None
    den_name  = None
    max_bin   = 0.0
    lim_ratio = {}
    
    for lim in limits:
        print lim.name
        if den_hist == None:
            if options.draw_obs: den_hist = lim.obs.Clone()
            else:                den_hist = lim.exp.Clone()            
            den_name = lim.name
            continue

        num_hist=lim.exp.Clone()        
        if options.draw_obs: num_hist=lim.obs.Clone()
        new_hist=den_hist.Clone()
        
        num_hist.SetLineColor(lim.color)
        num_hist.SetLineStyle(1)
        new_hist.SetLineColor(lim.color)
        new_hist.SetLineStyle(1)
        if True:
            print 'ERROR dividing computing manually'
            weirdbins=False

            if num_hist.GetNbinsX() != den_hist.GetNbinsX():
                print 'Error bin number is not the same!!!'
                print 'numerator   bins: ',num_hist.GetNbinsX()
                print 'denominator bins: ',den_hist.GetNbinsX()
                weirdbins=True
                #continue
            
            for i in range(1,num_hist.GetNbinsX()+1):

                d=den_hist.GetBinContent(i)
                n=1.0
                if weirdbins:
                    x=den_hist.GetXaxis().GetBinLowEdge(i)
                    for j in range(1,num_hist.GetNbinsX()+1):
                        if x==num_hist.GetXaxis().GetBinLowEdge(j):
                            n=num_hist.GetBinContent(j)
                else:
                    n=num_hist.GetBinContent(i)
                if d==0:
                    d=1.0
                    n=1.0
                    
                if options.debug:
                    print 'den',d
                    print 'num',n
                    print 'ratio:',str(n/d)
                    
                new_hist.SetBinContent(i,n/d)
        else:
            pts=lim.GetFitPoints(rt.points)
            i=1
            for pt in pts:
                new_hist.SetBinContent(i,pt)
                i+=1
        lim_ratio[lim.name] = new_hist
        max_bin=max(num_hist.GetBinContent(new_hist.GetMaximumBin()),max_bin)
    max_bin=2.0
    #
    # loop over list of histograms and plot them
    #
    leg5 = GetLegend(options.mva+' Expected Statistical Limits Ratio over '+GetTypeName(den_name), wide=0.7)
    if options.draw_obs:
        leg5 = GetLegend(options.mva+' Observed Statistical Limits Ratio over '+GetTypeName(den_name), wide=0.7)

    c1.Clear()
    c1.cd()
    c1.SetLogy(0)
    draw_opt = ''
    limit_ratios={}
    limit_ratioh=None
    for num_name, num_hist in lim_ratio.iteritems():
        if len(lim_ratio)<10:
            leg5.AddEntry(num_hist, GetTypeName(num_name)+'/'+GetTypeName(den_name), 'lp')
        elif limit_ratioh==None:
            leg5.AddEntry(num_hist, GetTypeName(num_name)+'/'+GetTypeName(den_name), 'lp')
            
        num_hist.GetYaxis().SetRangeUser(0.5, 1.1*max_bin)
        num_hist.SetYTitle('Ratio #sigma/#sigma_{SM}')
        if options.scaleXS:
            num_hist.SetYTitle('#sigma_{SM}^{VBF} x  #it{B}_{inv} [pb]')            
        if draw_opt=='':
            draw_opt = 'C SAME'
            num_hist.Draw('AXIS')
            limits[0].one.Draw('L SAME')
            #rt.ratio_sig2_err.Draw('SAME E3')
            #rt.ratio_sig1_err.Draw('SAME E3')            
        num_hist.Draw(draw_opt+' C')
        draw_opt = 'C SAME'

        for i in range(1,num_hist.GetNbinsX()+1):
            if i in limit_ratios:  limit_ratios[i]+=[num_hist.GetBinContent(i)]
            else:                  limit_ratios[i] =[num_hist.GetBinContent(i)]
                
        if limit_ratioh==None:
            limit_ratioh=num_hist.Clone()


    leg5.Draw()
    #AddAtlasName('')
    labsA=getATLASLabels(c1,0.65,0.9)
    for l in labsA:
        l.Draw()
    c1.Update()
    if not options.no_wait:
        c1.WaitPrimitive()
    else:
        c1.WaitPrimitive()
        
    if output and len(limits)>1:
        if len(common_name)>40:
            common_name='stat'
        c1.SaveAs(output+'/'+common_name+'_ratio.'+options.file_type)

    #
    # Draw the error band - from statistical fluctuation
    #
    limit_ratioh.SetLineColor(1)
    for i,l in limit_ratios.iteritems():
        avg,rms = MeanAndError(l)
        limit_ratioh.SetYTitle('Ratio #sigma/#sigma_{SM}')
        limit_ratioh.SetBinContent(i,avg)
        limit_ratioh.SetBinError(i,rms)        
    c1.Clear()

    rt.DrawRatio([limit_ratioh])
    labsA=getATLASLabels(c1,0.65,0.9)
    for l in labsA:
        l.Draw()
    c1.Update()
    if not options.no_wait:
        c1.WaitPrimitive()
    else:
        c1.WaitPrimitive()
    raw_input('waiting..')
    
    if output and len(limits)>1:
        if len(common_name)>40:
            common_name='stat'
        c1.SaveAs(output+'/'+common_name+'_rms.'+options.file_type)
