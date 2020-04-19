#!/bin/bash

OUTDIRVAR=theoryVariation
mkdir $OUTDIRVAR

if [ $(ls | grep theoVariation_W_strong | wc -l) == 0 ] ;then echo "WARNING: (W_strongNominal*root) No Files found" ;else hadd ${OUTDIRVAR}/theoVariation_W_strong.root theoVariation_W_strongNominal*root; fi
if [ $(ls | grep theoVariation_Z_strong | wc -l) == 0 ] ;then echo "WARNING: (Z_strongNominal*root) No Files found" ;else hadd ${OUTDIRVAR}/theoVariation_Z_strong.root theoVariation_Z_strongNominal*root; fi
if [ $(ls | grep theoVariation_W_EWK | wc -l) == 0 ] ;then echo "WARNING: (W_EWKNominal*.root) No Files found" ;else hadd ${OUTDIRVAR}/theoVariation_W_EWK.root theoVariation_W_EWKNominal*.root; fi
if [ $(ls | grep theoVariation_Z_EWK | wc -l) == 0 ] ;then echo "WARNING: (Z_EWKNominal*root) No Files found" ;else hadd ${OUTDIRVAR}/theoVariation_Z_EWK.root theoVariation_Z_EWKNominal*root; fi

if [ $(ls | grep theoVariation_W_strong_ckkw15 | wc -l) == 0 ] ;then echo "WARNING: (W_strong_ckkw15*root) No Files found" ;else hadd ${OUTDIRVAR}/theoVariation_W_strong_ckkw15.root theoVariation_W_strong_ckkw15*root; fi
if [ $(ls | grep theoVariation_Z_strong_ckkw15 | wc -l) == 0 ] ;then echo "WARNING: (Z_strong_ckkw15*root) No Files found" ;else hadd ${OUTDIRVAR}/theoVariation_Z_strong_ckkw15.root theoVariation_Z_strong_ckkw15*root; fi
if [ $(ls | grep theoVariation_W_EWK_ckkw15 | wc -l) == 0 ] ;then echo "WARNING: (W_EWK_ckkw15*root) No Files found" ;else hadd ${OUTDIRVAR}/theoVariation_W_EWK_ckkw15.root theoVariation_W_EWK_ckkw15*.root; fi
if [ $(ls | grep theoVariation_Z_EWK_ckkw15 | wc -l) == 0 ] ;then echo "WARNING: (Z_EWK_ckkw15*root) No Files found" ;else hadd ${OUTDIRVAR}/theoVariation_Z_EWK_ckkw15.root theoVariation_Z_EWK_ckkw15*root; fi

if [ $(ls | grep theoVariation_W_strong_ckkw30 | wc -l) == 0 ] ;then echo "WARNING: (W_strong_ckkw30*root) No Files found" ;else hadd ${OUTDIRVAR}/theoVariation_W_strong_ckkw30.root theoVariation_W_strong_ckkw30*root; fi
if [ $(ls | grep theoVariation_Z_strong_ckkw30 | wc -l) == 0 ] ;then echo "WARNING: (Z_strong_ckkw30*root) No Files found" ;else hadd ${OUTDIRVAR}/theoVariation_Z_strong_ckkw30.root theoVariation_Z_strong_ckkw30*root; fi
if [ $(ls | grep theoVariation_W_EWK_ckkw30 | wc -l) == 0 ] ;then echo "WARNING: (W_EWK_ckkw30*root) No Files found" ;else hadd ${OUTDIRVAR}/theoVariation_W_EWK_ckkw30.root theoVariation_W_EWK_ckkw30*.root; fi
if [ $(ls | grep theoVariation_Z_EWK_ckkw30 | wc -l) == 0 ] ;then echo "WARNING: (Z_EWK_ckkw30*root) No Files found" ;else hadd ${OUTDIRVAR}/theoVariation_Z_EWK_ckkw30.root theoVariation_Z_EWK_ckkw30*root; fi

if [ $(ls | grep theoVariation_W_strong_qsf025 | wc -l) == 0 ] ;then echo "WARNING: (W_strong_qsf025*root) No Files found" ;else hadd ${OUTDIRVAR}/theoVariation_W_strong_qsf025.root theoVariation_W_strong_qsf025*root; fi
if [ $(ls | grep theoVariation_Z_strong_qsf025 | wc -l) == 0 ] ;then echo "WARNING: (Z_strong_qsf025*root) No Files found" ;else hadd ${OUTDIRVAR}/theoVariation_Z_strong_qsf025.root theoVariation_Z_strong_qsf025*root; fi
if [ $(ls | grep theoVariation_W_EWK_qsf025 | wc -l) == 0 ] ;then echo "WARNING: (W_EWK_qsf025*root) No Files found" ;else hadd ${OUTDIRVAR}/theoVariation_W_EWK_qsf025.root theoVariation_W_EWK_qsf025*.root; fi
if [ $(ls | grep theoVariation_Z_EWK_qsf025 | wc -l) == 0 ] ;then echo "WARNING: (Z_EWK_qsf025*root) No Files found" ;else hadd ${OUTDIRVAR}/theoVariation_Z_EWK_qsf025.root theoVariation_Z_EWK_qsf025*root; fi

if [ $(ls | grep theoVariation_W_strong_qsf4 | wc -l) == 0 ] ;then echo "WARNING: (W_strong_qsf4*root) No Files found" ;else hadd ${OUTDIRVAR}/theoVariation_W_strong_qsf4.root theoVariation_W_strong_qsf4*root; fi
if [ $(ls | grep theoVariation_Z_strong_qsf4 | wc -l) == 0 ] ;then echo "WARNING: (Z_strong_qsf4*root) No Files found" ;else hadd ${OUTDIRVAR}/theoVariation_Z_strong_qsf4.root theoVariation_Z_strong_qsf4*root; fi
if [ $(ls | grep theoVariation_W_EWK_qsf4 | wc -l) == 0 ] ;then echo "WARNING: (W_EWK_qsf4*root) No Files found" ;else hadd ${OUTDIRVAR}/theoVariation_W_EWK_qsf4.root theoVariation_W_EWK_qsf4*.root; fi
if [ $(ls | grep theoVariation_Z_EWK_qsf4 | wc -l) == 0 ] ;then echo "WARNING: (Z_EWK_qsf4*root) No Files found" ;else hadd ${OUTDIRVAR}/theoVariation_Z_EWK_qsf4.root theoVariation_Z_EWK_qsf4*root; fi


hadd ${OUTDIRVAR}/Z_strong.root Z_strongNominal*root
hadd ${OUTDIRVAR}/Z_strong_ckkw15.root Z_strong_ckkw15*root
hadd ${OUTDIRVAR}/Z_strong_ckkw30.root Z_strong_ckkw30*root
hadd ${OUTDIRVAR}/Z_strong_qsf025.root Z_strong_qsf025*root
hadd ${OUTDIRVAR}/Z_strong_qsf4.root Z_strong_qsf4*root
hadd ${OUTDIRVAR}/W_strong.root W_strongNominal*root
hadd ${OUTDIRVAR}/W_strong_ckkw15.root W_strong_ckkw15*root
hadd ${OUTDIRVAR}/W_strong_ckkw30.root W_strong_ckkw30*root
hadd ${OUTDIRVAR}/W_strong_qsf025.root W_strong_qsf025*root
hadd ${OUTDIRVAR}/W_strong_qsf4.root W_strong_qsf4*root
