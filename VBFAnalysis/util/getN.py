#!/usr/bin/env python                                                                                                                                                                                             
import ROOT
import math
import subprocess
import argparse
import pickle
import sys

parser = argparse.ArgumentParser( description = "get total Nevent to weight samples", add_help=True , fromfile_prefix_chars='@')
parser.add_argument( "-l", "--list", type = str, dest = "filelist", default = "listslim", help = "list of files" )
parser.add_argument( "-r", "--event-count", type = int, dest = "event_count", default = 2, help = "event count. 1= raw, 2= sum of event weights" )
parser.add_argument( "-g", "--grid", action = "store_true", dest = "grid", default = False, help = "-g if files are on grid site")
parser.add_argument( "-o", "--output", type = str, dest = "output", default = "f_out_total_v04.root", help = "output file name" )
parser.add_argument( "-p", "--pickle", type = str, dest = "pickle", default = None, help = "pickle file list" )
args, unknown = parser.parse_known_args()

print 'Collecting your files!'
sys.stdout.flush()

fout = ROOT.TFile(args.output,"RECREATE")
h_total = ROOT.TH1D("h_total","",1,0,1)
if args.pickle==None:
    print 'not a pickle'
    fdir_list = open(args.filelist,'r')
    print 'fdir_list: ',fdir_list
    sys.stdout.flush()
    for fdir in fdir_list:
        print 'Directory:',fdir
        sys.stdout.flush()
        samplesplit = fdir.split(".")
        if "physics_Main" in fdir and args.event_count!=1:
                continue
        for p,s in enumerate(samplesplit):
            if s[0]=="v":
                dsid_string = samplesplit[p+1]
    
        returnCode = -10
        if args.grid:
            while returnCode!=0:
                p = subprocess.Popen("rucio list-file-replicas --protocol root --pfns --rse MWT2_UC_LOCALGROUPDISK "+fdir, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                returnCode=p.returncode
        else:
            p = subprocess.Popen("ls "+fdir.replace("root","*/*"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            
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
            nevent += h.GetBinContent(args.event_count)
        h_total.Fill(dsid_string,nevent)
else:
    # run pickle file list
    list_file = pickle.load( open( args.pickle, "rb" ) )
    for container,contFileList in list_file.iteritems():
        samplesplit = container.split(".")
        if "physics_Main" in container and (args.event_count!=4):
            continue
	#if not "physics_Main" in container:
	#    continue
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
            if not h:
		print 'ERROR - histogram invalid',filepath
		continue
	    nevent += h.GetBinContent(args.event_count)
            print 'total events: ',nevent
            f.Close()
        h_total.Fill(dsid_string,nevent)
        
    
h_total.Draw()
fout.Write()
