import itertools
def grouper(n, iterable):
    it = iter(iterable)
    while True:
       chunk = tuple(itertools.islice(it, n))
       if not chunk:
           return
       yield chunk

import os
import ROOT
import numpy as np

import argparse

parser = argparse.ArgumentParser(description='Author: O. Rifki')
parser.add_argument('files', type=str, nargs='+', metavar='<file.root>', help='ROOT files containing the jigsaw information. Histograms will be drawn and saved in the file.')
args = parser.parse_args()

branches=['runNumber', 'eventNumber']
processes = {"Zvv_QCD": "(364142 <= runNumber && runNumber <= 364155)",
             "Zll_QCD": "(364114 <= runNumber && runNumber <= 364127)",
             "Wlv_QCD": "(364170 <= runNumber && runNumber <= 364183)"
             }
common = " && jet_pt[0]>60e3 && jet_pt[1]>40e3 && n_jet>=2 && jet_eta[0]*jet_eta[1]<0 && jj_deta>2.5 && jj_dphi<2.4  && jj_mass>200e3"
SR     = " && met_et>100e3       && (n_el+n_mu==0)"
CRW    = " && met_nolep_et>100e3 && ( (n_el==1 && n_mu==0 ) )"
CRZ    = " && met_nolep_et>100e3 && ( (n_el==2 && n_mu==0 && el_charge[0]*el_charge[1]<0 && abs(mll-91.2e3)<25e3) )"
selection = {
             "Zvv_QCD_SR"  : processes["Zvv_QCD"] + common + SR,
             "Zll_QCD_SR"  : processes["Zll_QCD"] + common + SR,
             "Wlv_QCD_SR"  : processes["Wlv_QCD"] + common + SR,
             "Zll_QCD_CR"  : processes["Zll_QCD"] + common + CRZ,
             "Wlv_QCD_CR"  : processes["Wlv_QCD"] + common + CRW,
             }

for f in args.files:
  print "\nopening {0}".format(f)
  for key, sel in selection.iteritems():
    print "Processing ", key, "..."
    treelist_r21 = ROOT.TList()
    in_f_r21 = ROOT.TFile.Open(f, "READ")
    keyList = in_f_r21.GetListOfKeys()
    for keyName in keyList:
      inputTreeName=keyName.GetName()
    in_t_r21 = in_f_r21.Get(inputTreeName)
    print "Old tree: ", in_t_r21.GetEntries()
    outfilename = os.path.join(os.path.dirname(f), "extract_{0:s}.root".format(key))
    out_f_r21 = ROOT.TFile.Open("tmp.root", "RECREATE")
    new_t_r21 = in_t_r21.CopyTree(sel)
    print "New tree: ", new_t_r21.GetEntries()
    new_t_r21.SetName("nominal")
    new_t_r21.SetTitle("nominal")
    #print new_t_r21.GetEntries()
    if new_t_r21.GetEntries()==0:
      #print "Skipping... "
      os.remove("tmp.root")
      continue
    else:
      os.rename("tmp.root",outfilename)
    print "Keeping ", outfilename
    treelist_r21.Add(new_t_r21)
    out_f_r21.cd()
    out_t_r21 = ROOT.TTree.MergeTrees(treelist_r21)
    out_t_r21.SetName("nominal")
    out_t_r21.SetTitle("nominal")
    out_f_r21.Write("",ROOT.TObject.kOverwrite)
    out_f_r21.Close()
    in_f_r21.Close()