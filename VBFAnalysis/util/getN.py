#!/usr/bin/env python                                                                                                                                                                                             
import ROOT
import math
import subprocess

Chain = ROOT.TChain("METTree")

fdir_list = open('listslim','r')

fout = ROOT.TFile("f_out_total_v04.root","RECREATE")
#can = ROOT.TCanvas("can", "can")
h_total = ROOT.TH1F("h_total","",1,0,1)
for fdir in fdir_list:
    samplesplit = fdir.split(".")
    if "physics_Main" in fdir:
            continue
    for p,s in enumerate(samplesplit):
        if s[0]=="v":
            dsid_string = samplesplit[p+1]

    p = subprocess.Popen("ls "+fdir.replace("root","*/*"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    nevent = 0
    for line in p.stdout.readlines():
        filepath = line.strip()
        print filepath
        f = ROOT.TFile(filepath)
        h = f.Get("NumberEvents")
        nevent += h.GetBinContent(2)
    h_total.Fill(dsid_string,nevent)
    
h_total.Draw()
fout.Write()
