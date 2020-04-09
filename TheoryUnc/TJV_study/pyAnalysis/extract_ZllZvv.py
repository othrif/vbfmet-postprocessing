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
import root_numpy as rnp

import argparse

parser = argparse.ArgumentParser(description='Author: O. Rifki')
parser.add_argument('files', type=str, nargs='+', metavar='<file.root>', help='ROOT files containing the jigsaw information. Histograms will be drawn and saved in the file.')
args = parser.parse_args()

branches=['runNumber', 'eventNumber']
processes = {"VBF":     "(runNumber == 308276 || runNumber == 308567)",
             "ggF":     "(runNumber == 308284)",
             "Zvv_QCD": "(364142 <= runNumber && runNumber <= 364155)",
             "Zvv_EWK": "(308095 <= runNumber && runNumber <= 308095)",
             "Zll_QCD": "(364100 <= runNumber && runNumber <= 364141)",
             "Zll_EWK": "(308092 <= runNumber && runNumber <= 308094)",
             "Wlv_QCD": "(364156 <= runNumber && runNumber <= 364197)",
             "Wlv_EWK": "(308096 <= runNumber && runNumber <= 308098)"
             }
common = " && n_jet>=2 " # " && jet_pt[0]>60e3 && jet_pt[1]>40e3 && n_jet>=2 && jet_eta[0]*jet_eta[1]<0 && jj_deta>2.5 && jj_dphi<2.4  && jj_mass>200e3 "
SR     = " && (n_nu==2  )" # && met_et>100e3 && abs(mll-91.2e3)<25e3
CRZ    = " && (n_el==2 )" #  && met_nolep_et>100e3 && el_charge[0]*el_charge[1]<0 && abs(mll-91.2e3)<25e3
#CRW    = " && met_nolep_et>100e3 && ( (n_el==1 && n_mu==0 ) || (n_el==0 && n_mu==1 ) )"
#CRZ    = " && met_nolep_et>100e3 && ( (n_el==2 && n_mu==0 && el_charge[0]*el_charge[1]<0 && abs(mll-91.2e3)<25e3) || (n_el==0 && n_mu==2 && mu_charge[0]*mu_charge[1]<0 && abs(mll-91.2e3)<25e3) )"
selection = {
             #"VBF_SR"      : processes["VBF"]     + common + SR,
             #"ggF_SR"      : processes["ggF"]     + common + SR,
             "Zvv_QCD_SR"  : processes["Zvv_QCD"] + common + SR,
             #"Zvv_EWK_SR"  : processes["Zvv_EWK"] + common + SR,
             #"Zll_QCD_SR"  : processes["Zll_QCD"] + common + SR,
            # "Zll_EWK_SR"  : processes["Zll_EWK"] + common + SR,
             #"Wlv_QCD_SR"  : processes["Wlv_QCD"] + common + SR,
    #         "Wlv_EWK_SR"  : processes["Wlv_EWK"] + common + SR,
             "Zll_QCD_CR"  : processes["Zll_QCD"] + common + CRZ,
             #"Zll_EWK_CR"  : processes["Zll_EWK"] + common + CRZ,
             #"Wlv_QCD_CR"  : processes["Wlv_QCD"] + common + CRW,
    #"Wlv_EWK_CR"  : processes["Wlv_EWK"] + common + CRW
             }

for f in args.files:
  print "\nopening {0}".format(f)
  for key, sel in selection.iteritems():
    print "Processing ", key, "..."
    treelist_r21 = ROOT.TList()
    in_f_r21 = ROOT.TFile.Open(f, "READ")
    in_t_r21 = in_f_r21.Get("nominal")
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
