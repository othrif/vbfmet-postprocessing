#!/usr/bin/env python 

import os
import argparse
import ROOT
import math
import sys

parser = argparse.ArgumentParser( description = "Looping over sys and samples for HF Input Alg", add_help=True , fromfile_prefix_chars='@')
parser.add_argument( "-i", "--input", type = str, dest = "input", default = "/tmp/HFALL_nom_v37.root", help = "input file name" )
parser.add_argument( "-t", "--unblind", action = "store_true", dest = "unblind", default = False, help = "unblind the tables");
args, unknown = parser.parse_known_args()

regions=[
'VBFjetSel_XNom_SRX_obs_cuts',
'VBFjetSel_XNom_twoEleCRX_obs_cuts',
'VBFjetSel_XNom_twoMuCRX_obs_cuts',
'VBFjetSel_XNom_oneElePosCRX_obs_cuts',
'VBFjetSel_XNom_oneEleNegCRX_obs_cuts',
'VBFjetSel_XNom_oneMuPosCRX_obs_cuts',
'VBFjetSel_XNom_oneMuNegCRX_obs_cuts',
'VBFjetSel_XNom_oneElePosLowSigCRX_obs_cuts',
'VBFjetSel_XNom_oneEleNegLowSigCRX_obs_cuts',
]
unblind=args.unblind
#hdata_NONE_twoEleCR3_obs_cuts
samples =['hVBFH125_',
          'hggFH125_',
          'hVH125_',
          'hZ_strong_',
          'hZ_EWK_',
          'hW_strong_',
          'hW_EWK_',
          'httbar_',
          #'hQCDw_',
          'heleFakes_',
          'hmultijet_',
          'hdata_',
]

samplesPrint =['Samples','VBFH125',
          'ggFH125',
          'VH125',
          'Z QCD',
          'Z EWK',
          'W QCD',
          'W EWK',
          'Top/VV/VVV/VBFWW',
          #'QCD',
          'eleFakes',
          'multijet',
          'data',
          #'Signal',
          'total bkg','data/bkg'
]

if not os.path.exists(args.input):
    print 'input file does not exist: ',args.input
    sys.exit(0)
    
f=ROOT.TFile.Open(args.input)

SumList=[]
SumErrList=[]
line='Region\t'
for s in samples:
    line+=s+'\t'
    SumList+=[0.0]
    SumErrList+=[0.0]
print line

bins=[1,2,3,4,5,6,7,8,9,10,11,12,13]
nRegion=0
sTot=0
for bin_num in bins:
    r=regions[0].replace('X','%s' %bin_num)
    histname=samples[0]+r
    h=f.Get(histname)
    if not h:
        sTot=bin_num-1
        break

table_per_bin={}
for b in bins: table_per_bin[b]={}
region_cf=[]
for rmy in regions:
    if nRegion==0:
        for su in range(0,len(SumList)):
            SumList[su]=0.0
            SumErrList[su]=0.0
    for bin_num in bins:
        r=rmy.replace('X','%s' %bin_num)
        if bin_num<=sTot:
            line =r+'\t'
        else:
            continue
        su=0
        lineBkgErr=0.0
        lineBkg=0.0
        lineSig=0.0
        lineData=0.0
        for s in samples:
            histname=s+r
            if s=='hdata_':
                if bin_num>9:
                    histname=s+'NONE_'+r[len('VBFjetSel_10Nom_'):]
                else:
                    histname=s+'NONE_'+r[len('VBFjetSel_3Nom_'):]
                #print histname
            h=f.Get(histname)
            integral=0.0

            if h!=None:
                e = ROOT.Double(0.0)
                integral=h.IntegralAndError(0,1001,e)
                line+='%0.2f +/- %0.2f\t' %(integral,e)
                #line+='%0.2f\t' %(integral)
                SumList[su]+=integral
                SumErrList[su]+=e**2
                if s=='hVBFH125_' or s=='hggFH125_' or s=='hVH125_':
                    line+=''
                    lineSig+=integral
                elif s!='hdata_':
                    lineBkgErr+=e**2
                    lineBkg+=integral
                else:
                    lineData=integral
            else:
                line+='N/A\t'
            su+=1

        # add stat/MC and data/MC
        bkgFracErr= math.sqrt(lineBkgErr)/lineBkg
        line +='%0.3f\t' %(bkgFracErr)
        #line +='%0.2f\t' %(lineData/lineBkg)
        if lineData<1.0:
            lineData=1.0
        if lineBkg<1.0:
            lineBkg=1.0
        line +='%0.3f +/- %0.3f\t' %(lineData/lineBkg, math.sqrt(1./lineData+bkgFracErr**2)*(lineData/lineBkg))
        print line

        region_name = ['']
        if r.count('twoEle'):  region_name=['Zee']
        elif r.count('twoMu'):  region_name=['Zmm']
        elif r.count('oneEleNegLowSigC'):  region_name=['WenminusLowMetSig']
        elif r.count('oneElePosLowSigC'):  region_name=['WenplusLowMetSig']
        elif r.count('oneEleNeg'):  region_name=['Wenminus']
        elif r.count('oneElePos'):  region_name=['Wenplus']
        elif r.count('oneMuNeg'):  region_name=['Wmnminus']
        elif r.count('oneMuPos'):  region_name=['Wmnplus']
        elif r.count('_SR'):  region_name=['SR']
        table_per_bin[bin_num][region_name[0]]=[lineData,lineSig,lineBkg,'%0.3f $\\pm$ %0.3f\t' %(lineData/lineBkg, math.sqrt(1./lineData+bkgFracErr**2)*(lineData/lineBkg))]
        #[[sreg,totalData,totalBkg,'%0.3f\t%0.3f +/- %0.3f\t' %(totalBkgFracErr, totalData/totalBkg, math.sqrt(totalBkgFracErr**2+1./totalData)*(totalData/totalBkg))]]        
        nRegion+=1
        if nRegion==sTot:
            nRegion=0
            totalData=0
            totalBkg=0
            totalBkgErr=0
            totalSig=0
            totalSigErr=0
            rline='Sum\t' 
            sreg=['Region']
            if r.count('twoEle'):  sreg=['Zee']
            elif r.count('twoMu'):  sreg=['Zmm']
            elif r.count('oneEleNegLowSigC'):  sreg=['WenminusLowMetSig']
            elif r.count('oneElePosLowSigC'):  sreg=['WenplusLowMetSig']
            elif r.count('oneEleNeg'):  sreg=['Wenminus']
            elif r.count('oneElePos'):  sreg=['Wenplus']
            elif r.count('oneMuNeg'):  sreg=['Wmnminus']
            elif r.count('oneMuPos'):  sreg=['Wmnplus']
            elif r.count('_SR'):  sreg=['SR']
            for su in range(0,len(SumList)):
                sreg+=[SumList[su]]
                #rline+='%0.2f\t' %(SumList[su])
                rline+='%0.2f +/- %0.2f\t' %(SumList[su],math.sqrt(SumErrList[su]))
                if samples[su]=='hVBFH125_' or samples[su]=='hggFH125_' or samples[su]=='hVH125_':
                    totalSig+=SumList[su]
                    totalSigErr+=SumErrList[su]
                elif samples[su]!='hdata_':
                    totalBkg+=SumList[su]
                    totalBkgErr+=SumErrList[su]
                else:
                    totalData=SumList[su] 
            sreg+=[totalBkg]
            region_cf+=[sreg]            
            #bkgFracErr
            totalBkgFracErr = math.sqrt(totalBkgErr)/totalBkg
            
            rline+='%0.3f\t%0.3f +/- %0.3f\t' %(totalBkgFracErr, totalData/totalBkg, math.sqrt(totalBkgFracErr**2+1./totalData)*(totalData/totalBkg))
            print rline
            
print 'done'

print table_per_bin
keys_regions = ['SR','Zee','Zmm','Wmnminus','Wmnplus','Wenminus','Wenplus']
print ''
print '\\resizebox{\\textwidth}{!}{ '
print '\\begin{tabular}{ll|ccccccc}'
table_per_bin_line='Bin Number & Yield '
for keyn in keys_regions:
    table_per_bin_line+=' & %s'  %keyn
print table_per_bin_line,' \\\\\\hline\\hline'
for b in bins:
    if b>11:
        continue
    for v in [0,1,2,3]:
        table_per_bin_line='%s ' %b
        if v==0: table_per_bin_line+=' & Data'
        if v==1: table_per_bin_line+=' & Signal'
        if v==2: table_per_bin_line+=' & Bkg'
        if v==3: table_per_bin_line+=' & Data/Bkg'
            
        for keyn in keys_regions:
            if v==0:
                if keyn=='SR':
                    if unblind:
                        table_per_bin_line+=' & %i ' %(table_per_bin[b][keyn][v])
                    else:
                        table_per_bin_line+=' & - ' 
                else:
                    table_per_bin_line+=' & %i ' %(table_per_bin[b][keyn][v])
            elif v==1 or v==2:
                table_per_bin_line+=' & %0.1f ' %(table_per_bin[b][keyn][v])                
            elif v==3:
                if keyn=='SR' and not unblind:
                    table_per_bin_line+=' & - ' #%(table_per_bin[b][keyn][v])
                else:
                    table_per_bin_line+=' & %s ' %(table_per_bin[b][keyn][v])
        print table_per_bin_line,'\\\\'
    
print '\\end{tabular}'
print '}'

print ''
print '\\resizebox{\\textwidth}{!}{ '
print '\\begin{tabular}{l|ccccccccc}'
cline=''
#print region_cf
for b in range(0,len(region_cf[0])+1): # bins
    cline=samplesPrint[b]+'\t& '
    for r in range(0,len(region_cf)):
    #for b in range(0,len(samples)+2):
        extra=''
        if b==0:
            cline+='%s\t& ' %(region_cf[r][b])
            extra='\\hline\\hline'
        elif b>=len(region_cf[0]):
            if unblind or region_cf[r][0]!="SR":
                cline+='%0.3f\t& ' %(region_cf[r][b-2]/region_cf[r][b-1] )
            else:
                cline+=' - \t& '
        elif b==len(region_cf[0])-2:# data
            if unblind or region_cf[r][0]!="SR":
                cline+='%0.0f\t& ' %(region_cf[r][b])
            else:
                cline+=' - \t& ' #%(region_cf[r][b])
        else:
            cline+='%0.1f\t& ' %(region_cf[r][b] )
            if b==len(region_cf[0])-3:# mj
                extra='\\hline\\hline'
            if b==len(region_cf[0])-1:# total bkg
                extra='\\hline'
    print cline.rstrip().rstrip('&')+'\\\\'+extra
    cline=''
print '\\end{tabular}'
print '}'
#sys.exit(0)
# Collect systematics
tobj = f.GetListOfKeys()
mye=ROOT.Double(0.0)
for sample in samples:
    for i in tobj:
    
        vname=i.GetName()
        #print vname
        #if vname.count('VBFjetSel') and vname.count('_SR1_obs_cuts') and vname.count(sample):
        #if vname.count('VBFjetSel') and vname.count('_oneEleNegLowSigCR3_') and vname.count(sample):
        #if vname.count('VBFjetSel') and vname.count('_SR11') and vname.count(sample):
        if vname.count('VBFjetSel') and vname.count('_twoEleCR5') and vname.count(sample):
            h=f.Get(vname)
            intBkg=h.IntegralAndError(0,1001,mye)
            #print '%0.2f ' %(intBkg)+vname 
            print '%0.2f +/- %0.2f ' %(intBkg,mye)+vname 
