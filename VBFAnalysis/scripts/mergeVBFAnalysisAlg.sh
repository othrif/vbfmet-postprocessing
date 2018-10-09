#!/bin/bash                                                                                                                                                                                                       

hadd data.root data*root
#hadd VV_VVV.root VV*root
hadd VV.root VV*root
hadd VVV.root VVV*root
hadd W_strong.root W_strong*root
hadd Z_strong.root Z_strong*root
hadd Z_strong_VBFFilt.root Z_strong_VBFFilt*root
hadd Z_strong_LowMass.root Z_strong_LowMass*root
hadd W_EWK.root W_EWK*root
hadd Z_EWK.root Z_EWK*root
hadd ttbar.root ttbar*root
hadd QCDw.root QCDw*root
hadd QCDunw.root QCDunw*root
#hadd signal.root *H125*root
hadd VBFH125.root  VBFH125*.root
hadd ggFH125.root  ggFH125*.root
hadd VH125.root  VH125*.root
