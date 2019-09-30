#!/bin/bash                                                                                                                                                                                                       
#OUTDIRM=v31TightEM2018
OUTDIRM=/share/t3data2/schae/v32ETight
mkdir $OUTDIRM
hadd $OUTDIRM/data.root data*root
#hadd $OUTDIRM/VVV.root VVV*root
#rm VVV*root
hadd $OUTDIRM/Z_strong_VBFFilt.root Z_strong_VBFFilt*root
hadd $OUTDIRM/Z_strongPTVExt.root Z_strongPTVExt*root
hadd $OUTDIRM/Z_strongExt.root Z_strongExt*root
hadd $OUTDIRM/Z_strongmVBFFilt.root Z_strongmVBFFilt*root
#hadd $OUTDIRM/Z_strong_LowMass.root Z_strong_LowMass*root
rm Z_strong_VBFFilt*root
rm Z_strongPTVExt*root
rm Z_strong_LowMass*root
rm Z_strongExt*root
rm Z_strongmVBFFilt*root

# now hadd the standard samples
#hadd $OUTDIRM/VV.root VV*root
hadd $OUTDIRM/W_strong.root W_strong*root
hadd $OUTDIRM/Z_strong.root Z_strong*root
hadd $OUTDIRM/W_EWK.root W_EWK*root
hadd $OUTDIRM/Z_EWK.root Z_EWK*root
hadd $OUTDIRM/ttbar.root ttbar*root
hadd $OUTDIRM/QCDw.root QCDw*root
#hadd $OUTDIRM/QCDunw.root QCDunw*root
#hadd signal.root *H125*root
hadd $OUTDIRM/VBFH125Old.root  VBFH125Old*.root
rm VBFH125Old*.root
hadd $OUTDIRM/VBFH125.root  VBFH125*.root
hadd $OUTDIRM/VBFHgam125.root  VBFHgam125*.root
hadd $OUTDIRM/VBFHOther.root  VBFHOther*.root
hadd $OUTDIRM/ggFH125Old.root  ggFH125Old*.root
rm ggFH125Old*.root
hadd $OUTDIRM/ggFH125.root  ggFH125*.root
hadd $OUTDIRM/VH125Old.root  VH125Old*.root
rm  VH125Old*.root
hadd $OUTDIRM/VH125.root  VH125*.root
hadd $OUTDIRM/Zg_EWK.root  Zg_EWK*.root
hadd $OUTDIRM/Wg_EWK.root  Wg_EWK*.root
hadd $OUTDIRM/TTH125.root  TTH125*.root

#hadd $OUTDIRM/Wg_strong.root Wg_strong*root
#hadd $OUTDIRM/Zg_strong.root Zg_strong*root
#hadd $OUTDIRM/ttg.root ttg*root
#hadd $OUTDIRM/SinglePhotonBCL.root SinglePhotonBCL*root
#rm SinglePhotonBCL*root
#hadd $OUTDIRM/SinglePhoton.root SinglePhoton*root
#hadd $OUTDIRM/VqqGam.root VqqGam*root
