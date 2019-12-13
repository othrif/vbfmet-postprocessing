#!/usr/bin/env python
import os
import sys
import subprocess
import argparse
import ROOT
import math
import sys

parser = argparse.ArgumentParser( description = "Changing to MG relative uncertainties", add_help=True , fromfile_prefix_chars='@')
parser.add_argument("--mg", dest='mg_file', default='/tmp/HF_MG.root', help="Madgraph HF file")
parser.add_argument("--sh", dest='sh_file', default='/tmp/HF_SH.root', help="Sherpa HF file")
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
fsh=ROOT.TFile.Open(args.sh_file,'UPDATE')

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

#sys.exit(0)
for k in  region_nom_to_syst_map.keys():
    print 'Key: ',k
    khists = region_nom_to_syst_map[k]
    hmg_nom=fmg.Get(k)
    hsh_nom=fsh.Get(k)

    if not hmg_nom or not hsh_nom:
        print 'Could not load: ',k,hmg_nom,hsh_nom
        continue
    
    for iname in khists:
        hmg = fmg.Get(iname)
        hsh = fsh.Get(iname)

        if not hmg or not hsh:
            print 'ERROR loading syst: ',iname,hmg,hsh
            continue
        rel_err=0.0
        if hmg_nom.GetBinContent(1)>0.0:
            rel_err = hmg.GetBinContent(1)/hmg_nom.GetBinContent(1)
        sh_rel_err=0.0            
        if hsh_nom.GetBinContent(1)>0.0:
            sh_rel_err = hsh.GetBinContent(1)/hsh_nom.GetBinContent(1)

        #print rel_err,' sherpa: ',sh_rel_err
        hsh.SetBinError(1,hsh.GetBinContent(1)*rel_err)
        hsh.Write("",ROOT.TObject.kOverwrite)
#fsh.Write()
fsh.Close()
fmg.Close()
print 'DONE'
