#!/usr/bin/env python
import os
import sys
import subprocess
import argparse
import ROOT
import math

def check(v,ispdf=False):

    # use inverted uncertainties
    if v<0.9999 and not ispdf:
        return 1./(2.-v)
    return v

def ReturnNewSystScaleUncor(sysname, vals, listV):
    line=''
    debug=False
    new_vals = []
    for h in vals:
        new_vals+=[1.-float(h)]
    newSyst=[]
    vsysname=0
    if sysname.count('Z_EWK'):    vsysname=1
    if sysname.count('W_strong'): vsysname=2
    if sysname.count('W_EWK'):    vsysname=3
    linesys=''
    maxBin=12
    totalSysCorrelated=0.0
    totalSysUncorrelated=0.0
    cordphi={}
    maxBinIter=maxBin
    if args.corrDPhi:
        print 'correlate dphi'
        cordphi[0]=5
        cordphi[1]=6
        cordphi[2]=7
        cordphi[3]=8
        cordphi[4]=9
        maxBinIter=6    
    for  bin_num1Z in range(0,maxBinIter-1):
        sysV=new_vals[bin_num1Z]*listV[bin_num1Z][vsysname]
        if bin_num1Z in cordphi:
            bin_num1ZAlt = cordphi[bin_num1Z]
            sysV+=new_vals[bin_num1ZAlt]*listV[bin_num1ZAlt][vsysname]            
        totalSysCorrelated+=sysV
        totalSysUncorrelated+=(sysV)**2
    print 'totalSysCorrelated: ',totalSysCorrelated,' uncorr: ',math.sqrt(totalSysUncorrelated)
    scaleF = totalSysCorrelated/math.sqrt(totalSysUncorrelated)
    print 'Increase: ',scaleF
    # apply larger syst
    tmp_line=sysname+' '
    for  bin_num1Z in range(0,maxBin-1):
        sysV=new_vals[bin_num1Z]*listV[bin_num1Z][vsysname]*scaleF
        newSystmig11=check(1.-sysV/listV[bin_num1Z][vsysname],ispdf=False)
        tmp_line+='%0.5f,' %newSystmig11
    print tmp_line.rstrip(',')
    line+=tmp_line.rstrip(',')
    return line+'\n'

def ReturnNewSyst(sysname, vals, listV, EWKDecor=True):
    line=''
    debug=False
    new_vals = []
    for h in vals:
        new_vals+=[1.-float(h)]
    
    newSyst=[]
    #print listV
    #print len(listV)
    newSystmig12up=0.0
    newSystmig12dw=0.0
    newSystmig23up=0.0
    newSystmig23dw=0.0
    newSystmig12uphigh=0.0
    newSystmig12dwhigh=0.0
    newSystmig23uphigh=0.0
    newSystmig23dwhigh=0.0
    doDecorrelation=False
    deCorrFactor=0.25
    vsysname=0
    if sysname.count('Z_EWK'):
        vsysname=1
        if EWKDecor:
            doDecorrelation=True
    if sysname.count('W_strong'): vsysname=2
    if sysname.count('W_EWK'):    vsysname=3
    linesys=''
    linesys1=''
    maxBin=12
    tot_err=0.0
    tmp_line=sysname+'_uncbin11 '
    if sysname.count('pdf_'):
        for  bin_num1Z in range(0,maxBin-1):
            newSystmig11=new_vals[bin_num1Z]*listV[bin_num1Z][vsysname]
            newSystmig11=check(1.-newSystmig11/listV[bin_num1Z][vsysname],ispdf=True)
            tmp_line+='%0.5f,' %newSystmig11
        print tmp_line.rstrip(',')
        line+=tmp_line.rstrip(',')
        return line+'\n'
    for  bin_num1Z in range(1,maxBin-1):
        tmp_line+='1.0,'
    newSystmig11=new_vals[10]*listV[10][vsysname]
    newSystmig11=check(1.-newSystmig11/listV[10][vsysname])
    tmp_line+='%0.4f' %newSystmig11
    print tmp_line
    line+=tmp_line+'\n'
    if not args.corrDPhi:
        for  bin_num1 in range(1,maxBin-1):
            linesys=''
            bin_num=maxBin-bin_num1
            for  bin_num1 in range(1,bin_num-1): linesys+='1.0,'
            if debug:
                print bin_num,new_vals[bin_num-1],listV[bin_num-1][vsysname]
            newSystmig23up+=new_vals[bin_num-1]*listV[bin_num-1][vsysname]
            newSystmig23dw-=newSystmig23up
            sysdw = check(1.-newSystmig23dw/listV[bin_num-2][vsysname])
            sysup = check(1.-newSystmig23up/listV[bin_num-1][vsysname])
            linesys+='%0.4f,' %(sysdw)
            linesys+='%0.4f,' %(sysup)
            #newSystmig23up=new_vals[bin_num-2]*listV[bin_num-2][vsysname]+newSystmig23up
            #newSystmig23dw-=newSystmig23up
            for  bin_num1 in range(bin_num,11): linesys+='1.0,'
            tmp_line=sysname+('_mig%s_%s ' %(bin_num-1,bin_num))+linesys.rstrip(',')
            line+=tmp_line+'\n'
            print tmp_line
            if bin_num==2:
                bin1Syst=new_vals[bin_num-2]*listV[bin_num-2][vsysname]
                if debug:
                    print 'low bin: ',bin1Syst,new_vals[bin_num-2],listV[bin_num-2][vsysname]
                bin1Syst+=newSystmig23up
                
                linesys1+=('%0.4f,' %(check(1.-bin1Syst/listV[bin_num-2][vsysname])))
                for  a in range(2,maxBin): linesys1+='1.0,'
                tmp_line=sysname+'_uncbin1 '+linesys1.rstrip(',')
                print tmp_line
                line+=tmp_line+'\n'
    else:

        #binmap={{1,6},{2,7},{3,8},{4,9},{5,10}}
        for  bin_num1 in range(1,maxBin/2-1):
            linesys=''
            linesys_decorr=''
            bin_num=(maxBin/2)-bin_num1
            bin_num_high=(maxBin/2)-bin_num1+(maxBin/2)-1
            for  bin_num1Z in range(1,bin_num-1): linesys+='1.0,'
            if debug:
                print bin_num,new_vals[bin_num-1],listV[bin_num-1][vsysname]
            newSystmig23up+=new_vals[bin_num-1]*listV[bin_num-1][vsysname]
            newSystmig23dw-=newSystmig23up
            newSystmig23uphigh+=new_vals[bin_num_high-1]*listV[bin_num_high-1][vsysname]
            newSystmig23dwhigh-=newSystmig23uphigh
            sysdw = check(1.-newSystmig23dw/listV[bin_num-2][vsysname])
            sysup = check(1.-newSystmig23up/listV[bin_num-1][vsysname])
            sysdwhigh = check(1.-newSystmig23dwhigh/listV[bin_num_high-2][vsysname])
            sysuphigh = check(1.-newSystmig23uphigh/listV[bin_num_high-1][vsysname])
            linesys+='%0.4f,' %(sysdw)
            linesys+='%0.4f,' %(sysup)
            for  bin_numZ in range(1,(maxBin/2)-bin_num): linesys+='1.0,'
            for  bin_num1Z in range(1,bin_num-1): linesys+='1.0,'
            linesys+='%0.4f,' %(sysdwhigh)
            linesys+='%0.4f,' %(sysuphigh)
            for  bin_numZ in range(bin_num_high+1,11): linesys+='1.0,'
            tmp_line=sysname+('_mig%s_%s ' %(bin_num-1,bin_num))+linesys.rstrip(',')
            line+=tmp_line+',1.0'+'\n'
            print tmp_line+',1.0'
            if doDecorrelation:
                
                for  bin_num1Z in range(1,bin_num-1): linesys_decorr+='1.0,'
                sysdw_decorr = check(1.-deCorrFactor*newSystmig23dw/listV[bin_num-2][vsysname])
                sysup_decorr = check(1.-deCorrFactor*newSystmig23up/listV[bin_num-1][vsysname])
                sysdwhigh_decorr = check(1.-deCorrFactor*newSystmig23dwhigh/listV[bin_num_high-2][vsysname])
                sysuphigh_decorr = check(1.-deCorrFactor*newSystmig23uphigh/listV[bin_num_high-1][vsysname])
                linesys_decorr+='%0.1f,' %(1.0)
                linesys_decorr+='%0.4f,' %(sysup_decorr)
                for  bin_numZ in range(1,(maxBin/2)-bin_num): linesys_decorr+='1.0,'
                for  bin_num1Z in range(1,bin_num-1): linesys_decorr+='1.0,'
                linesys_decorr+='%0.1f,' %(1.0)
                linesys_decorr+='%0.4f,' %(sysuphigh_decorr)
                for  bin_numZ in range(bin_num_high+1,11): linesys_decorr+='1.0,'
                tmp_line_decorr=sysname+('_uncbin%s ' %(bin_num))+linesys_decorr.rstrip(',')
                print tmp_line_decorr+',1.0'
                line+=tmp_line_decorr+',1.0'+'\n'
            if bin_num==2:
                # low dphijj
                bin1Syst=new_vals[bin_num-2]*listV[bin_num-2][vsysname]
                if doDecorrelation:
                    bin1Syst*=math.sqrt(1.-deCorrFactor**2)
                if debug:
                    print 'low bin: ',bin1Syst,new_vals[bin_num-2],listV[bin_num-2][vsysname]

                if doDecorrelation:
                    bin1Syst+=math.sqrt(1.-deCorrFactor**2)*newSystmig23up
                else:
                    bin1Syst+=newSystmig23up
                # high dphijj
                bin1Systhigh=new_vals[bin_num_high-2]*listV[bin_num_high-2][vsysname]
                if doDecorrelation:
                    bin1Systhigh*=math.sqrt(1.-deCorrFactor**2)
                if debug:
                    print 'low bin: ',bin1Systhigh,new_vals[bin_num_high-2],listV[bin_num_high-2][vsysname]
                if doDecorrelation:
                    bin1Systhigh+=math.sqrt(1.-deCorrFactor**2)*newSystmig23uphigh
                else:
                    bin1Systhigh+=newSystmig23uphigh
                # combining for total unc
                linesys1+=('%0.4f,' %(check(1.-bin1Syst/listV[bin_num-2][vsysname])))
                for  a in range(2,(maxBin/2)): linesys1+='1.0,'
                linesys1+=('%0.4f,' %(check(1.-bin1Systhigh/listV[bin_num_high-2][vsysname])))                    
                for  a in range(2,(maxBin/2)): linesys1+='1.0,'                    
                tmp_line=sysname+'_uncbin1 '+linesys1.rstrip(',')
                print tmp_line+',1.0'
                line+=tmp_line+',1.0'+'\n'
                
    return line

def GetBins(fY, l, listV):
    addToList=False
    if len(listV)>0:
        addToList=True
    for bin_num in range(1,12):
        r1=l #'VBFjetSel_XNom_SRX_obs_cuts'
        r=r1.replace('X','%s' %bin_num)
        #print r
        zstrong=fY.Get('hZ_strong_'+r)
        zewk=fY.Get('hZ_EWK_'+r)
        wstrong=fY.Get('hW_strong_'+r)
        wewk=fY.Get('hW_EWK_'+r)
        #print bin_num,wewk.GetBinContent(1)
        #print zstrong,zewk,wstrong,wewk
        if addToList:
            listV[bin_num-1][0]+=zstrong.GetBinContent(1)
            listV[bin_num-1][1]+=zewk.GetBinContent(1)
            listV[bin_num-1][2]+=wstrong.GetBinContent(1)
            listV[bin_num-1][3]+=wewk.GetBinContent(1)
        else:
            listV+=[[zstrong.GetBinContent(1),zewk.GetBinContent(1),wstrong.GetBinContent(1),wewk.GetBinContent(1)]]

    
parser = argparse.ArgumentParser( description = "Changing to MG relative uncertainties", add_help=True , fromfile_prefix_chars='@')
parser.add_argument("--input",  dest='input', default='listTheorySystUpdatedv4', help="Input file with systematics")
parser.add_argument("--output", dest='output', default='listTheorySyst11STv4', help="Output file with ST approach")
parser.add_argument("--inputYields", dest='inputYields', default='/tmp/HF_jan7_mc16all_nom.root', help="Input file with yields")
parser.add_argument("--corrDPhi", dest='corrDPhi',action = "store_true",  default=True, help="Correlate dphijj bins")
parser.add_argument("--scaleUncor", dest='scaleUncor',action = "store_true",  default=False, help="Scale the uncertainties as if uncorrelated to match the correlated syst")
args, unknown = parser.parse_known_args()

fin = open(args.input,'r')
fout = open(args.output,'w')

fY = ROOT.TFile.Open(args.inputYields)
regionYields={}
regionYields['SR']=[]
regionYields['ZCR']=[]
regionYields['WCR']=[]
GetBins(fY, 'VBFjetSel_XNom_SRX_obs_cuts', regionYields['SR'])

for l in ['VBFjetSel_XNom_twoEleCRX_obs_cuts','VBFjetSel_XNom_twoMuCRX_obs_cuts',]:
    GetBins(fY, l, regionYields['ZCR'])

for l in ['VBFjetSel_XNom_oneElePosCRX_obs_cuts','VBFjetSel_XNom_oneEleNegCRX_obs_cuts','VBFjetSel_XNom_oneMuPosCRX_obs_cuts','VBFjetSel_XNom_oneMuNegCRX_obs_cuts']:
    GetBins(fY, l, regionYields['WCR'])

regions=['SRup','SRdown','ZCRup','ZCRdown','WCRup','WCRdown']
curr_region=''
last_region=''
systMap={}
tot_line=''
for i in fin:
    curr_line = i.rstrip('\n')
    regionLine=False
    for r in regions:
        if curr_line.count(r):
            curr_region=curr_line.strip()
            regionLine=True
    if regionLine:
        continue
    if last_region!=curr_region:
        # continue calculating
        print 'Done with region: ',last_region
        last_region=curr_region
        print curr_region
        tot_line+=curr_region+'\n'
    else:
        entries = (curr_line.strip()).split(' ')
        if len(entries)==2:
            yieldRegString=''
            if curr_region.count('SR'): yieldRegString='SR'
            elif curr_region.count('ZCR'): yieldRegString='ZCR'
            elif curr_region.count('WCR'): yieldRegString='WCR'
                
            if yieldRegString=='':
                print 'ERROR did not find string in ',curr_region
            systMap[entries[0]]=entries[1].split(',')
            print entries[0],systMap[entries[0]]
            if not args.scaleUncor:
                tot_line+=ReturnNewSyst(entries[0], systMap[entries[0]],regionYields[yieldRegString], EWKDecor=True)
            else:
                tot_line+=ReturnNewSystScaleUncor(entries[0], systMap[entries[0]],regionYields[yieldRegString])
        else:
            print 'ERROR could not parse:',entries
            print curr_line

fout.write(tot_line)
fout.close()
fin.close()
fY.Close()
print 'DONE'

