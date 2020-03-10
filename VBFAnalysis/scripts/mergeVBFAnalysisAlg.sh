#!/bin/bash                                                                                                                                                                                                       
#OUTDIRM=/share/t3data2/schae/v32ETight
#OUTDIRM=${1:-v34mc16a}
OUTDIRM=v37Egam
mkdir $OUTDIRM
hadd $OUTDIRM/data.root data*root
#hadd $OUTDIRM/VVV.root VVV*root
#rm VVV*root
#hadd $OUTDIRM/Z_strong_VBFFilt.root Z_strong_VBFFilt*root
hadd $OUTDIRM/Z_strongPTVExt.root Z_strongPTVExt*root
hadd $OUTDIRM/Z_strongExt.root Z_strongExt*root
#hadd $OUTDIRM/Z_strongmVBFFilt.root Z_strongmVBFFilt*root
hadd $OUTDIRM/W_strongExt.root W_strongExt*root
#hadd $OUTDIRM/Z_strong_LowMass.root Z_strong_LowMass*root
rm Z_strong_VBFFilt*root
rm Z_strongPTVExt*root
rm Z_strong_LowMass*root
rm Z_strongExt*root
rm Z_strongmVBFFilt*root
rm W_strongExt*root

hadd $OUTDIRM/VBFH1000.root VBFH1000*root
rm VBFH1000*root
hadd $OUTDIRM/VBFH2000.root VBFH2000*root
rm VBFH2000*root
hadd $OUTDIRM/VBFH3000.root VBFH3000*root
rm VBFH3000*root
hadd $OUTDIRM/VBFH750.root VBFH750*root
rm VBFH750*root
hadd $OUTDIRM/VBFH300.root VBFH300*root
rm VBFH300*root
hadd $OUTDIRM/VBFH100.root VBFH100*root
rm VBFH100*root
hadd $OUTDIRM/VBFH75.root VBFH75*root
rm VBFH75*root
hadd $OUTDIRM/VBFH50.root VBFH50*root
rm VBFH50*root
# now hadd the standard samples
#hadd $OUTDIRM/VV.root VV*root
hadd $OUTDIRM/W_strong.root W_strong*root
hadd $OUTDIRM/Z_strong.root Z_strong*root
hadd $OUTDIRM/W_EWK.root W_EWK*root
hadd $OUTDIRM/Z_EWK.root Z_EWK*root
hadd $OUTDIRM/ttbar.root ttbar*root
#hadd $OUTDIRM/QCDw.root QCDw*root
#hadd $OUTDIRM/QCDunw.root QCDunw*root
#hadd signal.root *H125*root
#hadd $OUTDIRM/VBFH125Old.root  VBFH125Old*.root
rm VBFH125Old*.root
hadd $OUTDIRM/VBFH125.root  VBFH125*.root
#hadd $OUTDIRM/VBFHgam125.root  VBFHgam125*.root
hadd $OUTDIRM/VBFHOther.root  VBFHOther*.root
#hadd $OUTDIRM/ggFH125Old.root  ggFH125Old*.root
rm ggFH125Old*.root
hadd $OUTDIRM/ggFH125.root  ggFH125*.root
#hadd $OUTDIRM/VH125Old.root  VH125Old*.root
rm  VH125Old*.root
hadd $OUTDIRM/VH125.root  VH125*.root
hadd $OUTDIRM/TTH125.root  TTH125*.root

#hadd $OUTDIRM/Zg_EWK.root  Zg_EWK*.root
#hadd $OUTDIRM/Wg_EWK.root  Wg_EWK*.root
#hadd $OUTDIRM/Wg_strong.root Wg_strong*root
#hadd $OUTDIRM/Zg_strong.root Zg_strong*root
#hadd $OUTDIRM/ttg.root ttg*root
##hadd $OUTDIRM/SinglePhotonBCL.root SinglePhotonBCL*root
##rm SinglePhotonBCL*root
#hadd $OUTDIRM/SinglePhoton.root SinglePhoton*root
#hadd $OUTDIRM/VqqGam.root VqqGam*root
