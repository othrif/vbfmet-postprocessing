#!/usr/bin/env python
import os
import sys
import subprocess
import argparse
import ROOT
import math

parser = argparse.ArgumentParser( description = "Changing to MG relative uncertainties", add_help=True , fromfile_prefix_chars='@')
parser.add_argument("--mg", dest='mg_file', default='/tmp/HF_MG.root', help="Madgraph HF file")
parser.add_argument("--sh", dest='sh_file', default='/tmp/HF_SH.root', help="Sherpa HF file")
parser.add_argument("--mergeSyst", action='store_true',  dest='mergeSyst', default=False, help="Merge the systematics by weight")
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

# if there are systematics like the theory corrections that shouldn't be swapped for MG, then add them here
ignore_syst=[]
    
samples =['hZ_strong_',
          'hW_strong_',
]
bins=[1,2,3,4,5,6,7,8,9,10,11]

fmg=ROOT.TFile.Open(args.mg_file)
fsh=ROOT.TFile.Open(args.sh_file,"UPDATE")

# create a region map
region_nom_to_syst_map={}
for bin_num in bins:
    for r1 in regions:
        r=r1.replace('X','%s' %bin_num)
        for s in samples:
            region_nom_to_syst_map[s+r]=[]
# List Histograms
hList=[]
for i in fmg.GetListOfKeys():
    skipHist=True
    iname=i.GetName()
    for j in samples:
        if iname.count(j):
            skipHist=False
    if skipHist:
        continue    
    #print i.GetName()
    hList+=[iname]

# Loading the map
for i in hList:
    for k in region_nom_to_syst_map.keys():
        bin_name = k[:k.find('Nom')]
        remain_name = k[k.find('Nom_')+4: ]
        #print bin_name,' ',remain_name
        if i.count(bin_name) and i.count(remain_name) and not i.count('Nom_'):
            skipSyst=False
            # make sure we want to swap this systematic
            for sys in ignore_syst:
                if i.count(sys):
                    skipSyst=True
                    break
            if not skipSyst:
                region_nom_to_syst_map[k]+=[i]

# Checking it is filled correctly
for k in  region_nom_to_syst_map.keys():
    print k,len(region_nom_to_syst_map[k])

nj=0
#sys.exit(0)
for k in  region_nom_to_syst_map.keys():
    print 'Key: ',k
    khists = region_nom_to_syst_map[k]
    hmg_nom=fmg.Get(k)
    hsh_nom=fsh.Get(k)
    if hsh_nom.GetBinContent(1)<0.0:
        # removing a negative yeild
        print 'Removing a negative nominal yield: ',hsh_nom.GetBinContent(1)
        hsh_nom.SetBinContent(1,0.001)
        fsh.cd()
        hsh_nom.Write(hsh_nom.GetName(),ROOT.TObject.kOverwrite)
        
    if not hmg_nom or not hsh_nom:
        print 'Could not load: ',k,hmg_nom,hsh_nom
        continue
    
    for iname in khists:
        hmg = fmg.Get(iname)
        hsh = fsh.Get(iname)

        if not hmg or not hsh:
            print 'ERROR loading syst: ',iname,hmg,hsh
            continue
        rel_err=1.0
        if hmg_nom.GetBinContent(1)>0.0:
            rel_err = hmg.GetBinContent(1)/hmg_nom.GetBinContent(1)
        sh_rel_err=1.0            
        if hsh_nom.GetBinContent(1)>0.0:
            sh_rel_err = hsh.GetBinContent(1)/hsh_nom.GetBinContent(1)

        print iname,rel_err,' sherpa: ',sh_rel_err
        nj+=1
        # use the average
        if args.mergeSyst:
            if hmg_nom.GetBinContent(1)>0.0 and hsh_nom.GetBinContent(1)>0.0:
                stat_sh = hsh_nom.GetBinError(1)/hsh_nom.GetBinContent(1)
                stat_mg = hmg_nom.GetBinError(1)/hmg_nom.GetBinContent(1)
                if (stat_sh+stat_mg)>0.0:
                    rel_err = (stat_sh*rel_err+stat_mg*sh_rel_err)/(stat_sh+stat_mg)
            print 'avg - ',iname,rel_err,' sherpa: ',sh_rel_err
        if hsh.GetBinContent(1)<0.0:
            # removing a negative yeild
            print 'Removing a negative yield: ',hsh.GetBinContent(1)
            hsh.SetBinContent(1,0.001)
        DoReset=True
        if abs(1.-rel_err)>abs(1.-sh_rel_err):            
            if stat_mg>0.4 or hmg_nom.GetBinContent(1)<5.0:
                print 'Stats are too small to reset anything: ',stat_mg
                DoReset=False
            print 'Larger relative ERROR: ',rel_err,sh_rel_err,' MG: ',hmg_nom.GetBinContent(1),'+/-',hmg_nom.GetBinError(1),' SH: ',hsh_nom.GetBinContent(1),' +/- ',hsh_nom.GetBinError(1)
        else:
            print 'Smaller relative ERROR: ',rel_err,sh_rel_err,' MG: ',hmg_nom.GetBinContent(1),'+/-',hmg_nom.GetBinError(1),' SH: ',hsh_nom.GetBinContent(1),' +/- ',hsh_nom.GetBinError(1)
        if DoReset:
            hsh.SetBinContent(1,hsh.GetBinContent(1)*rel_err)
        fsh.cd()
        #hsh.Write("",ROOT.TObject.kOverwrite)
        hsh.Write(hsh.GetName(),ROOT.TObject.kOverwrite)
        #hsh.Write(0,2,0)
    #if nj>100:
    #    break
#fsh.Write()
fsh.Close()
fmg.Close()
print 'DONE'
