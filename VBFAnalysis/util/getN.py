#!/usr/bin/env python                                                                                                                                                                                             
import ROOT
import math
import subprocess
import argparse

parser = argparse.ArgumentParser( description = "get total Nevent to weight samples", add_help=True , fromfile_prefix_chars='@')
parser.add_argument( "-l", "--list", type = str, dest = "filelist", default = "listslim", help = "list of files" )
parser.add_argument( "-g", "--grid", action = "store_true", dest = "grid", default = False, help = "-g if files are on grid site")
parser.add_argument( "-o", "--output", type = str, dest = "output", default = "f_out_total_v04.root", help = "output file name" )
args, unknown = parser.parse_known_args()

Chain = ROOT.TChain("METTree")

fdir_list = open(args.filelist,'r')

fout = ROOT.TFile(args.output,"RECREATE")
#can = ROOT.TCanvas("can", "can")
h_total = ROOT.TH1F("h_total","",1,0,1)
for fdir in fdir_list:
    samplesplit = fdir.split(".")
    if "physics_Main" in fdir:
            continue
    for p,s in enumerate(samplesplit):
        if s[0]=="v":
            dsid_string = samplesplit[p+1]

    if args.grid:
        p = subprocess.Popen("rucio list-file-replicas --protocol root --pfns --rse MWT2_UC_LOCALGROUPDISK "+fdir, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    else:
        p = subprocess.Popen("ls "+fdir.replace("root","*/*"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    nevent = 0
    for line in p.stdout.readlines():
        filepath = line.strip()
        print filepath
        f = ROOT.TFile(filepath)
        if not f:
            print 'bad file. continuing',filepath
            continue
        if f.IsZombie():
            print 'zombie file', filepath
            continue
        h = f.Get("NumberEvents")
        nevent += h.GetBinContent(2)
    h_total.Fill(dsid_string,nevent)
    
h_total.Draw()
fout.Write()
