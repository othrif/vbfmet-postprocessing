import ROOT
import sys,os
import math
import VBFAnalysis.ATLAS as ATLAS
import VBFAnalysis.Style as Style
from optparse import OptionParser
import HInvPlot.systematics as vbf_syst
import HInvPlot.JobOptions as config

def HistName(histName, regionName, systName, binNum):
    return "h"+histName+"_"+(regionName.replace('X','%s' %binNum)).replace('Nom_',systName+'_')

def DeclareCanvas(options):

    can=ROOT.TCanvas("c1","c1",1600,1000)
    if options.ratio:
        can.Divide(1,2)
        can.cd(1)
        ROOT.gPad.SetBottomMargin(0)
        ROOT.gPad.SetRightMargin(0.1)
        ROOT.gPad.SetPad(0,0.3,1,1)
        can.cd(2)
        ROOT.gPad.SetTopMargin(0)
        ROOT.gPad.SetBottomMargin(0.35)
        ROOT.gPad.SetRightMargin(0.1)
        ROOT.gPad.SetPad(0,0,1,0.3)
        can.cd(1)
    return can

def DrawRatio(options,can,nom, varHist=[]):
    color=1
    drawOpt=''
    for v in varHist:
        v.Divide(nom)
        v.GetYaxis().SetRangeUser(0.9,1.1)
        v.SetLineColor(color)
        color+=1
        v.Draw(drawOpt)
        drawOpt='same'

    can.Update()
    can.WaitPrimitive()
    
def GetLegLabel(options,can):

    #ROOT.gPad.BuildLegend(0.7,0.7,0.9,0.9)
    ROOT.gPad.SetTickx(True);
    ROOT.gPad.SetTicky(True);
    texts = ATLAS.getATLASLabels(can, 0.4, 0.78, options.lumi, selkey="")
    for text in texts:
        text.Draw()

def PrintPulls(rfile,options,can,histName,regions):
    print 'Reading file: ',options.pullsFile
    if not os.path.exists(options.pullsFile):
        print 'file does not exist'
    pullMap={}
    pullList = open(options.pullsFile)
    systFile=open('../listTheorySyst11STv4')
    systMap={}
    key=''
    for l in systFile:
        if l.count('SRup'):
            key='SRup'
            continue
        elif l.count('SRdown'):
            key='SRdown'
            continue
        elif l.count('ZCRdown'):
            key='ZCRdown'
            continue
        elif l.count('ZCRup'):
            key='ZCRup'
            continue
        elif l.count('WCRdown'):
            key='WCRdown'
            continue        
        elif l.count('WCRup'):
            key='WCRup'
            continue
        if not l.strip():
            continue
        sLine=l.strip().split(' ')
        if key not in systMap:
            systMap[key]={}
        #print sLine[0],sLine[1]
        systMap[key][sLine[0]+"_bin1"]=sLine[1].rstrip('\n').split(',')
        
    for i in pullList:
        myList= i.strip().rstrip('\n').split(' ')
        myList=filter(None, myList)
        #print myList
        if myList[0].count('alpha_'):
            pullMap[myList[0].replace('alpha_','')]=[float(myList[2]),float(myList[4])]
    for r in regions:
        rkey='SR'
        if r.count('two'):
            rkey='ZCR'
        if r.count('one'):
            rkey='WCR'
        #for ibin in range(1,options.binNum+1):
        for ibin in [4,9,5,10]:
            print 'Bin: ',ibin
            nomBinH=rfile.Get(HistName(histName, r, 'Nom', ibin))
            nomVal=nomBinH.GetBinContent(1)
            if not nomBinH:
                print 'could not load Nominal: ',HistName(histName, r, 'Nom', ibin)
                continue            
            for systName,pulls in pullMap.iteritems():
                pullValue = pulls[0]/pulls[1]
                sysBinH=rfile.Get(HistName(histName, r, systName+'High', ibin))
                #print systName #,systMap[rkey+'up']
                #print systName+'_bin1'
                if (systName) in systMap[rkey+'up']:
                    #print 'FOUND:',systName
                    if not systName.count(histName):
                        continue
                    upPull=pullValue*(nomVal)*(float(systMap[rkey+'up'][systName][ibin-1])-1.0)
                    dwPull=pullValue*(nomVal)*(float(systMap[rkey+'down'][systName][ibin-1])-1.0)                    
                    if abs(dwPull)>0.01 or  abs(upPull)>0.01:
                        print '%0.2f %0.2f %s %s THEORY %s bin %s' %(upPull, dwPull, systName,histName, r,ibin)
                if not sysBinH:
                    #print 'could not load Syst: ',HistName(histName, r, systName+'High', ibin)
                    continue
                sysBinL=rfile.Get(HistName(histName, r, systName+'Low', ibin))
                if not sysBinL:
                    #print 'could not load Syst: ',HistName(histName, r, systName+'Low', ibin)
                    continue
                upPull=pullValue*(nomVal-sysBinH.GetBinContent(1))
                dwPull=pullValue*(nomVal-sysBinL.GetBinContent(1))
                if abs(dwPull)>0.01 or  abs(upPull)>0.01:
                    if pullValue>0.0:
                        print '%0.2f + %0.2f %s %s' %(nomVal,upPull,systName,histName)
                    else:
                        print '%0.2f - %0.2f %s %s' %(nomVal,dwPull,systName,histName)                        
    pullList.close()
    
def Smooth(rfile,options,can,systName,histName,regions):

    smoothSyle=1
    if systName.count('EL_'):
        smoothSyle=1
    elif systName.count('JET_'):
        smoothSyle=3
    elif systName.count('MET_'):
        smoothSyle=3
    elif systName.count('PRW_'):
        smoothSyle=3        
    nomMap={}
    sysUpMap={}
    sysDwMap={}
    binOrder=[1,3,5,7,9,2,4,6,8,10,11]
    for r in regions:
        hName  =HistName(histName, r, 'Nom', options.binNum+1)
        hNameUp=HistName(histName, r, 'Up', options.binNum+1)        
        hNameDw=HistName(histName, r, 'Dw', options.binNum+1)        
        hSaveName=hName.replace('12Nom_oneEleNegLowSigCR12_obs_cuts','')
        hSaveName=hName.replace('12Nom_oneMuNegCR12_obs_cuts','')
        h=ROOT.TH1F(hName,hName,options.binNum,0.5,0.5+options.binNum)
        hsys=ROOT.TH1F(hNameUp,hNameUp,options.binNum,0.5,0.5+options.binNum)        
        hsysdw=ROOT.TH1F(hNameDw,hNameDw,options.binNum,0.5,0.5+options.binNum)        
        for ibin in range(1,options.binNum+1):
            nomBinH=rfile.Get(HistName(histName, r, 'Nom', ibin))
            if not nomBinH:
                print 'could not load Nominal: ',HistName(histName, r, 'Nom', ibin)
                continue
            h.SetBinContent(binOrder[ibin-1], nomBinH.GetBinContent(1))
            h.SetBinError  (binOrder[ibin-1], 0.001*nomBinH.GetBinError  (1))
            sysBinH=rfile.Get(HistName(histName, r, systName+'High', ibin))
            if not sysBinH:
                print 'could not load up variation: ',HistName(histName, r, systName+'High', ibin)
            else:
                hsys.SetBinContent(binOrder[ibin-1], sysBinH.GetBinContent(1))
                hsys.SetBinError  (binOrder[ibin-1], 0.0)
            # down variation
            sysdwBinH=rfile.Get(HistName(histName, r, systName+'Low', ibin))
            if not sysdwBinH:
                print 'could not load down variation: ',HistName(histName, r, systName+'Low', ibin)
            else:
                hsysdw.SetBinContent(binOrder[ibin-1], sysdwBinH.GetBinContent(1))
                hsysdw.SetBinError  (binOrder[ibin-1], 0.0)            
        nomMap[r]=h.Clone()
        sysUpMap[r]=hsys.Clone()
        sysDwMap[r]=hsysdw.Clone()

    # takes the integral in the region. Then scales by the integral over all regions
    updateHist=[]
    #rNewfile=ROOT.TFile(options.input,'UPDATE')
    rNewfile=ROOT.TFile('/tmp/HFALL_feb5_sysUPDATE.root','UPDATE')
    if options.smooth==1 or (options.smooth==5 and smoothSyle==1):
        print 'smoothing option 1'
        for r in regions:
            nomInt = nomMap[r].Integral(1,options.binNum)
            upInt  = sysUpMap[r].Integral(1,options.binNum)
            dwInt  = sysDwMap[r].Integral(1,options.binNum)
            for ibin in range(1,options.binNum+1):
                currentNomV=nomMap[r].GetBinContent(binOrder[ibin-1])
                if upInt!=0.0 and nomInt!=0.0:
                    sysBinH=rNewfile.Get(HistName(histName, r, systName+'High', ibin))
                    if not sysBinH:
                        continue
                    #sysBinH.Scale(upInt/nomInt)
                    sysbef=sysBinH.GetBinContent(1)
                    sysBinH.SetBinContent(1,upInt/nomInt*currentNomV)
                    #print 'after: ',nomInt,upInt,currentNomV,sysBinH.GetBinContent(1),sysbef
                    updateHist+=[sysBinH]
                if dwInt!=0.0 and nomInt!=0.0:
                    sysBinH=rNewfile.Get(HistName(histName, r, systName+'Low', ibin))
                    if not sysBinH:
                        continue
                    #sysBinH.Scale(upInt/nomInt)
                    sysBinH.SetBinContent(1,dwInt/nomInt*currentNomV)
                    updateHist+=[sysBinH]
    elif options.smooth==2 or (options.smooth==5 and smoothSyle==2):
        print 'smoothing option 2 - parabolic smoothing'
        smooth_tool=ROOT.SmoothHist()
        smooth_tool.setNmax(1)
        for r in regions:
            sysBefore=sysUpMap[r].Clone()
            hSmoothed = smooth_tool.smoothHistogram(nomMap[r], sysUpMap[r], True)
            smooth_tool.smoothHistogram(nomMap[r], sysDwMap[r], True)            

            if options.wait:
                rhSmoothed = hSmoothed.Clone()                
                DrawRatio(options,can,nomMap[r], varHist=[sysBefore,rhSmoothed])
            for ibin in range(1,options.binNum+1):
                sysBinH=rNewfile.Get(HistName(histName, r, systName+'High', ibin))
                if not sysBinH:
                    continue
                sysBinH.SetBinContent(1,sysUpMap[r].GetBinContent(binOrder[ibin-1]))
                updateHist+=[sysBinH]
                sysBinH=rNewfile.Get(HistName(histName, r, systName+'Low', ibin))
                if not sysBinH:
                    continue
                sysBinH.SetBinContent(1,sysDwMap[r].GetBinContent(binOrder[ibin-1]))
                updateHist+=[sysBinH]
    elif options.smooth==3 or (options.smooth==5 and smoothSyle==3):
        print 'smoothing option 3 - combine regions'
        smooth_tool=ROOT.SmoothHist()
        smooth_tool.setNmax(1)
        
        # first add the regions
        CombineSysNomMap={}
        CombineSysUpMap={}
        CombineSysDwMap={}
        for r in regions:
            CombineSysNomMap[r]= nomMap[r].Clone()
            CombineSysUpMap[r] = sysUpMap[r].Clone()
            CombineSysDwMap[r] = sysDwMap[r].Clone()            
            for r2 in regions:
                if r==r2:
                    continue
                if r.count('two') and r2.count('two'):
                    CombineSysNomMap[r].Add( nomMap[r2])
                    CombineSysUpMap[r]. Add( sysUpMap[r2])
                    CombineSysDwMap[r]. Add( sysDwMap[r2])
                if r.count('one') and r2.count('one'):
                    CombineSysNomMap[r].Add( nomMap[r2])
                    CombineSysUpMap[r]. Add( sysUpMap[r2])
                    CombineSysDwMap[r]. Add( sysDwMap[r2])
                    
        # smooth with the added regions
        for r in regions:
            sysBefore=sysUpMap[r].Clone()
            hSmoothed = smooth_tool.smoothHistogram(CombineSysNomMap[r], CombineSysUpMap[r], True)
            smooth_tool.smoothHistogram(CombineSysNomMap[r], CombineSysDwMap[r], True)            

            if options.wait:
                rhSmoothed = hSmoothed.Clone()                
                DrawRatio(options,can,nomMap[r], varHist=[sysBefore,rhSmoothed])
            for ibin in range(1,options.binNum+1):
                nomBinH=rNewfile.Get(HistName(histName, r, 'Nom', ibin))
                nomV=nomBinH.GetBinContent(1)
                sysBinH=rNewfile.Get(HistName(histName, r, systName+'High', ibin))
                if not sysBinH:
                    continue
                if nomV!=0.0:
                    sysBinH.SetBinContent(1,nomV*CombineSysUpMap[r].GetBinContent(binOrder[ibin-1])/CombineSysNomMap[r].GetBinContent(binOrder[ibin-1]))
                updateHist+=[sysBinH]
                sysBinH=rNewfile.Get(HistName(histName, r, systName+'Low', ibin))
                if not sysBinH:
                    continue
                if nomV!=0.0:
                    #print nomV,(nomV*CombineSysDwMap[r].GetBinContent(binOrder[ibin-1])/CombineSysNomMap[r].GetBinContent(binOrder[ibin-1]))
                    sysBinH.SetBinContent(1,nomV*CombineSysDwMap[r].GetBinContent(binOrder[ibin-1])/CombineSysNomMap[r].GetBinContent(binOrder[ibin-1]))
                updateHist+=[sysBinH] 
                    
    # write the updated histograms
    for ha in updateHist:
        rNewfile.cd()
        ha.Write(ha.GetName(),ROOT.TObject.kOverwrite)
    rNewfile.Close()
        
def DrawRatio(rfile,options,can,systName,histName,regions):

    #ATLAS.Style()
    nomMap={}
    sysUpMap={}
    sysDwMap={}
    hSaveName=''
    nLoaded=0
    binOrder=[1,3,5,7,9,2,4,6,8,10,11]
    #binOrder=[1,2,3,4,5,6,7,8,9,10,11]
    for r in regions:
        #print r
        hName  =HistName(histName, r, 'Nom', options.binNum+1)
        hNameUp=HistName(histName, r, 'Up', options.binNum+1)        
        hNameDw=HistName(histName, r, 'Dw', options.binNum+1)        
        hSaveName=hName.replace('12Nom_oneEleNegLowSigCR12_obs_cuts','')
        hSaveName=hName.replace('12Nom_oneMuNegCR12_obs_cuts','')
        h=ROOT.TH1F(hName,hName,options.binNum,0.5,0.5+options.binNum)
        hsys=ROOT.TH1F(hNameUp,hNameUp,options.binNum,0.5,0.5+options.binNum)        
        hsysdw=ROOT.TH1F(hNameDw,hNameDw,options.binNum,0.5,0.5+options.binNum)        
        for ibin in range(1,options.binNum+1):
            nomBinH=rfile.Get(HistName(histName, r, 'Nom', ibin))
            if not nomBinH:
                print 'could not load: ',HistName(histName, r, 'Nom', ibin)
                continue
            else:
                nLoaded+=1
            h.SetBinContent(binOrder[ibin-1], nomBinH.GetBinContent(1))
            h.SetBinError  (binOrder[ibin-1], 0.001*nomBinH.GetBinError  (1))
            #*nomBinH.GetBinError  (1)
            # up variation
            sysBinH=rfile.Get(HistName(histName, r, systName+'High', ibin))
            if not sysBinH:
                print 'could not load: ',HistName(histName, r, systName+'High', ibin)
                continue
            hsys.SetBinContent(binOrder[ibin-1], sysBinH.GetBinContent(1))
            hsys.SetBinError  (binOrder[ibin-1], 0.0)
            # down variation
            sysdwBinH=rfile.Get(HistName(histName, r, systName+'Low', ibin))
            if not sysdwBinH:
                print 'could not load: ',HistName(histName, r, systName+'Low', ibin)
                continue
            hsysdw.SetBinContent(binOrder[ibin-1], sysdwBinH.GetBinContent(1))
            hsysdw.SetBinError  (binOrder[ibin-1], 0.0)            
        nomMap[r]=h.Clone()
        sysUpMap[r]=hsys.Clone()
        sysDwMap[r]=hsysdw.Clone()

    color=1
    drawOpt=''
    leg=ROOT.TLegend(0.2,0.13,0.4,0.25)
    leg.SetNColumns(2);
    leg.SetBorderSize(0)
    leg.SetFillColor(0)
    legr=ROOT.TLegend(0.4,0.13,0.6,0.25)
    legr.SetBorderSize(0)
    legr.SetFillColor(0)
    totalMax=1.0
    # create hists and divide
    for r in regions:
        sysUpMap[r].Divide(nomMap[r])
        sysDwMap[r].Divide(nomMap[r])
        max1=sysUpMap[r].GetMaximum()
        max2=sysDwMap[r].GetMaximum()
        if max1>totalMax:
            totalMax=max1
        if max2>totalMax:
            totalMax=max2
    # label the bins
    for r in regions:
        sysUpMap[r].GetXaxis().SetBinLabel(1,'0.8<M_{jj}<1.0')
        sysUpMap[r].GetXaxis().SetBinLabel(3,'1<M_{jj}<1.5')
        sysUpMap[r].GetXaxis().SetBinLabel(5,'1.5<M_{jj}<2')
        sysUpMap[r].GetXaxis().SetBinLabel(7,'2<M_{jj}<3.5')
        sysUpMap[r].GetXaxis().SetBinLabel(9,'3.5<M_{jj}')
        sysUpMap[r].GetXaxis().SetBinLabel(11,'n_{j}>2')   

    # check the region
    color_vec=[1,2, 3, 4, 5, 6,
               #ROOT.kBlue   -9,
               #ROOT.kGreen  -3,
               #ROOT.kCyan   -9,
               17,
               ROOT.kCyan  ,
               #ROOT.kYellow +2,
               #ROOT.kYellow +1,
               ROOT.kMagenta-3,
               ROOT.kOrange,
               ROOT.kOrange-3,
               ]

    yup=1.1
    if totalMax<1.01:
        yup=1.01
    elif totalMax<1.02:
        yup=1.02
    elif totalMax<1.05:
        yup=1.05
    elif totalMax<1.1:
        yup=1.1
    elif totalMax<1.25:
        yup=1.25
    elif totalMax<1.5:
        yup=1.5
    ydw=2.0-yup
    # draw
    for r in regions:
        sysUpMap[r].SetStats(0)
        sysUpMap[r].SetLineStyle(1)
        sysUpMap[r].GetYaxis().SetTitle(systName+' / Nominal')
        sysUpMap[r].GetXaxis().SetTitle('Fit Bins [ordered in m_{jj}]')
        sysUpMap[r].GetYaxis().SetRangeUser(ydw,yup)
        sysUpMap[r].SetLineColor(color_vec[color-1])
        sysUpMap[r].SetMarkerColor(color_vec[color-1])
        sysUpMap[r].Draw(drawOpt)
        drawOpt='same'
        leg.AddEntry(sysUpMap[r],(r.replace('X_obs_cuts','')).replace('VBFjetSel_XNom_',''))

        sysDwMap[r].SetStats(0)
        sysDwMap[r].GetYaxis().SetRangeUser(ydw,yup)
        sysDwMap[r].SetLineColor(color_vec[color-1])
        sysDwMap[r].SetMarkerColor(color_vec[color-1])
        sysDwMap[r].SetLineStyle(2)
        sysDwMap[r].Draw(drawOpt)
        if color==1:
            legr.AddEntry(sysUpMap[r],'Up variation')
            legr.AddEntry(sysDwMap[r],'Down variation')
        color+=1
        drawOpt='same'
    leg.Draw()
    legr.Draw()
    can.Update()
    
    GetLegLabel(options,can)
    if options.wait:
        can.WaitPrimitive()
    if options.saveAs:
        print 'Saving: ',hSaveName
        can.SaveAs(hSaveName+systName+"."+options.saveAs)
        
if __name__=='__main__':
    p = OptionParser()

    p.add_option('-i', '--input', type='string', help='input file. Created from plotEvent.py')
    p.add_option('-c', '--compare', type='string', help='Compare any number of input files. Does not support --syst atm. example: --compare rfile1.root,rfile2.root')

    p.add_option('--lumi', type='float', default=139, help='Defines the integrated luminosity shown in the label')
    p.add_option('--batch', action='store_true', default=False, help='Turn on batch mode')    
    p.add_option('--binNum', type='int', default=11, help='number of bins')    
    p.add_option('--nBin', type='int', default=1, help='Defines which bin is plotted')
    p.add_option('--smooth', type='int', default=0, help='Smooth options: 1 average bins, 2 run parabolic smoothing, 3 avg Wln and Zll, 5 determine style of smoothing')    
    p.add_option('-s', '--syst', type='string', default="All", help='NEEDS FIXING. defines the systematics that are plotted. -s all <- will plot all available systematics. Otherwise give a key to the dict in systematics.py')# FIXME
    p.add_option('--pullsFile', type='string', default=None, help='pulls file, print yields')
    p.add_option('-d', '--data', action='store_true', help='Draw data')
    p.add_option('--unBlindSR', action='store_true', help='Unblinds the SR bins')
    p.add_option('--debug', action='store_true', help='Print in debug mode')    
    p.add_option('-r', '--ratio', action='store_true', help='Draw data/MC ratio in case of -i and adds ratios to tables for both -i and -c')
    p.add_option('--yieldTable', action='store_true', help='Produces yield table')
    p.add_option('--wait', action='store_true', help='wait on histogram')    
    p.add_option('--saveAs', type='string', help='Saves the canvas in a given format. example argument: pdf')
    p.add_option('-q', '--quite', action='store_true', help='activates Batch mode')
    p.add_option('--texTables', action='store_true', help='Saves tables as pdf. Only works together with --yieldTable')
    p.add_option('--postFitPickleDir', type='string', default=None, help='Directory of post fit yields pickle files. expects the files end in .pickle')    
    p.add_option('--show-mc-stat-err', action='store_true',  dest='show_mc_stat_err', help='Shows the MC stat uncertainties separately from the data ratio error')    
    p.add_option('--plot', default='', help='Plots a variable in a certain region. HFInputAlg.cxx produces these plots with the --doPlot flag . Only works with -i and not with -c. example: jj_mass,SR,1_2_3')
    (options, args) = p.parse_args()

    histNames=["W_strong", "Z_strong", "W_EWK", "Z_EWK", "ttbar"] # "multijet", "eleFakes"
    regions=[
    'VBFjetSel_XNom_SRX_obs_cuts',
    'VBFjetSel_XNom_twoEleCRX_obs_cuts',
    'VBFjetSel_XNom_twoMuCRX_obs_cuts',
    'VBFjetSel_XNom_oneElePosCRX_obs_cuts',
    'VBFjetSel_XNom_oneEleNegCRX_obs_cuts',
    'VBFjetSel_XNom_oneMuPosCRX_obs_cuts',
    'VBFjetSel_XNom_oneMuNegCRX_obs_cuts',
    #'VBFjetSel_XNom_oneElePosLowSigCRX_obs_cuts',
    #'VBFjetSel_XNom_oneEleNegLowSigCRX_obs_cuts',
    ]
    if options.batch:
        ROOT.gROOT.SetBatch(True)
    # Load libraries
    config.loadLibs(ROOT)
    can=DeclareCanvas(options)
    rfile=ROOT.TFile(options.input,'READ')
    # read in pulls file and print the yields
    if options.pullsFile!=None:
        #for histName in histNames:
        for histName in ["Z_strong", "Z_EWK", "ttbar"]:
            PrintPulls(rfile,options,can,histName,['VBFjetSel_XNom_twoEleCRX_obs_cuts','VBFjetSel_XNom_twoMuCRX_obs_cuts'])
        sys.exit(0)
        
    # which syst
    systName='EL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR'
    systToSmooth=['EL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR',
                      'EL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR',
                      'JET_fJvtEfficiency','JET_JvtEfficiency','JET_JvtEfficiency',
                      'JET_Pileup_OffsetMu',
                      'JET_Pileup_OffsetNPV', # still looks weird. some regions are higher or lower than others
                      'JET_Pileup_PtTerm',
                      'JET_Pileup_RhoTopology',
                      'JET_EffectiveNP_Modelling2',
                      'JET_EffectiveNP_Modelling1',
                      'JET_EffectiveNP_Modelling3',
                      'JET_Flavor_Composition',
                      'JET_JER_DataVsMC_MC16',
                      'JET_JER_EffectiveNP_1',
                      'JET_JER_EffectiveNP_2',
                      'JET_JER_EffectiveNP_3',
                      'JET_JER_EffectiveNP_4',
                      'MET_SoftTrk_Scale',
                      'JET_Flavor_Response',
                      'JET_EtaIntercalibration_TotalStat',
                      'PRW_DATASF', # amanda suggested
                      ]
    allSyst=[]
    if options.syst=='All':
        allSystUpAndDown=vbf_syst.systematics('All').getsystematicsList()
        for s in allSystUpAndDown:
            sSystName=s.rstrip('__1up').rstrip('__1down')
            if sSystName not in allSyst:
                allSyst+=[sSystName]
    elif options.syst=='weird':
        allSyst=systToSmooth
    else:
        allSyst=[options.syst]
    print 'Number of syst:',len(allSyst)
    for systNameA in allSyst:
        for histName in histNames:
            if options.smooth:
                Smooth(rfile,options,can,systNameA,histName,regions+['VBFjetSel_XNom_oneElePosLowSigCRX_obs_cuts','VBFjetSel_XNom_oneEleNegLowSigCRX_obs_cuts'])
            DrawRatio(rfile,options,can,systNameA,histName,regions)
    del can
    print 'done'
