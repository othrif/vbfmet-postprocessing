#!/bin/bash                                                                                                                                                                                                       
OUTDIRM=v13
mkdir $OUTDIRM
hadd $OUTDIRM/data.root data*root
#hadd VV_VVV.root VV*root
hadd $OUTDIRM/VV.root VV*root
hadd $OUTDIRM/VVV.root VVV*root
hadd $OUTDIRM/W_strong.root W_strong*root
hadd $OUTDIRM/Z_strong.root Z_strong*root
hadd $OUTDIRM/Z_strong_VBFFilt.root Z_strong_VBFFilt*root
hadd $OUTDIRM/Z_strong_LowMass.root Z_strong_LowMass*root
hadd $OUTDIRM/W_EWK.root W_EWK*root
hadd $OUTDIRM/Z_EWK.root Z_EWK*root
hadd $OUTDIRM/ttbar.root ttbar*root
hadd $OUTDIRM/QCDw.root QCDw*root
hadd $OUTDIRM/QCDunw.root QCDunw*root
#hadd signal.root *H125*root
hadd $OUTDIRM/VBFH125.root  VBFH125*.root
hadd $OUTDIRM/ggFH125.root  ggFH125*.root
hadd $OUTDIRM/VH125.root  VH125*.root
