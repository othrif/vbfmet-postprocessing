#!/usr/bin/env python                                                                                                                                                                                             
import ROOT
import math
import subprocess
import argparse
import pickle

parser = argparse.ArgumentParser( description = "get total Nevent to weight samples", add_help=True , fromfile_prefix_chars='@')
parser.add_argument( "-l", "--list", type = str, dest = "filelist", default = "listslim", help = "list of files" )
parser.add_argument( "-g", "--grid", action = "store_true", dest = "grid", default = False, help = "-g if files are on grid site")
parser.add_argument( "-o", "--output", type = str, dest = "output", default = "f_out_total_v04.root", help = "output file name" )
parser.add_argument( "-p", "--pickle", type = str, dest = "pickle", default = None, help = "pickle file list" )
args, unknown = parser.parse_known_args()

Chain = ROOT.TChain("METTree")

fout = ROOT.TFile(args.output,"RECREATE")
h_total = ROOT.TH1F("h_total","",1,0,1)
if args.pickle==None:
    fdir_list = open(args.filelist,'r')
    for fdir in fdir_list:
        samplesplit = fdir.split(".")
        if "physics_Main" in fdir:
                continue
        for p,s in enumerate(samplesplit):
            if s[0]=="v":
                dsid_string = samplesplit[p+1]
    
        returnCode = -10
        while returnCode!=0:
            if args.grid:
                p = subprocess.Popen("rucio list-file-replicas --protocol root --pfns --rse MWT2_UC_LOCALGROUPDISK "+fdir, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            else:
                p = subprocess.Popen("ls "+fdir.replace("root","*/*"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            returnCode=p.returncode
        nevent = 0
        for line in p.stdout.readlines():
            filepath = line.strip()
            print filepath
            f = ROOT.TFile.Open(filepath)
            if not f:
                print 'bad file. continuing',filepath
                continue
            if f.IsZombie():
                print 'zombie file', filepath
                continue
            h = f.Get("NumberEvents")
            nevent += h.GetBinContent(2)
        h_total.Fill(dsid_string,nevent)
else:
    # run pickle file list
    list_file = pickle.load( open( args.pickle, "rb" ) )
    for container,contFileList in list_file.iteritems():
        samplesplit = container.split(".")
        if "physics_Main" in container:
            continue
        for p,s in enumerate(samplesplit):
            if s[0]=="v":
                    dsid_string = samplesplit[p+1]
        print 'dsid: ',dsid_string
        nevent = 0
        for line in contFileList:
            filepath = line.strip()
            print filepath
            f = ROOT.TFile.Open(filepath)
            if not f:
                print 'ERROR - bad file. continuing',filepath
                continue
            if f.IsZombie():
                print 'ERROR - zombie file', filepath
                continue
            h = f.Get("NumberEvents")
            nevent += h.GetBinContent(2)
            print 'total events: ',nevent
            f.Close()
        h_total.Fill(dsid_string,nevent)
        
    
h_total.Draw()
fout.Write()
