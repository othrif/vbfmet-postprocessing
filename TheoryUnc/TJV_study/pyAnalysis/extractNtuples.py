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

processes = {"Zvv_QCD": "((312484 <= runNumber && runNumber <= 312495) || (364222 <= runNumber && runNumber <= 364223))", #
             "Zll_QCD": "((312448 <= runNumber && runNumber <= 312483) || (364216 <= runNumber && runNumber <= 364221))", #
             "Zee_QCD": "((312448 <= runNumber && runNumber <= 312459) || (364218 <= runNumber && runNumber <= 364219))", #
             "Zmm_QCD": "((312460 <= runNumber && runNumber <= 312471) || (364216 <= runNumber && runNumber <= 364217))", #
             "Wlv_QCD": "((312496 <= runNumber && runNumber <= 312531) || (364224 <= runNumber && runNumber <= 364229))", #
             "Wev_QCD": "((312496 <= runNumber && runNumber <= 312507) || (364226 <= runNumber && runNumber <= 364227))", #
             "Wmv_QCD": "((312508 <= runNumber && runNumber <= 312519) || (364224 <= runNumber && runNumber <= 364225))", #
             }
#common = "   && met_nolep_et > 200e3 && jet_pt[0]>80e3 && jet_pt[1]>50e3 && jj_deta>3.8 && jj_dphi<2  && jj_mass>800e3 &&  n_jet25>=2"
common = "   && jet_pt[0]>80e3 && jet_pt[1]>50e3 && jj_deta>3.8 && jj_dphi<2  && jj_mass>800e3 &&  n_jet25>=2" #
selection = {
             "Zvv_QCD"  : processes["Zvv_QCD"] + common,
             "Wlv_QCD"  : processes["Wlv_QCD"] + common,
             "Zll_QCD"  : processes["Zll_QCD"] + common,
             "Zee_QCD"  : processes["Zee_QCD"] + common,
             "Zmm_QCD"  : processes["Zmm_QCD"] + common,
             "Wev_QCD"  : processes["Wev_QCD"] + common,
             "Wmv_QCD"  : processes["Wmv_QCD"] + common,
             }

for f in args.files:
  print "\nopening {0}".format(f)
  for key, sel in selection.iteritems():
    print "Processing ", key, "..."
    if "Z" in key and "W" in f or  "W" in key and "Z" in f:
      print "Skipping... "
      continue
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