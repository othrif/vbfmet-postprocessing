#!/bin/bash

root -q -l plot_7point_pdf.cxx'("allregions_final","PhiLow")'
root -q -l plot_7point_pdf.cxx'("allregions_final","PhiHigh")'
root -q -l plot_7point_pdf.cxx'("allregions_final","Njet")'
root -q -l plot_7point_pdf.cxx'("allregions_final","METlow")'
root -q -l plot_7point_pdf.cxx'("allregions_final","VRPhiHigh")'

root -q -l plot_TF_unc.cxx'("allregions_final","PhiLow")'
root -q -l plot_TF_unc.cxx'("allregions_final","PhiHigh")'
root -q -l plot_TF_unc.cxx'("allregions_final","Njet")'
root -q -l plot_TF_unc.cxx'("allregions_final","METlow")'
root -q -l plot_TF_unc.cxx'("allregions_final","VRPhiHigh")'