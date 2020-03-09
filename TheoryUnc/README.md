# Theory Uncertainties for V+jets #


## Renormalization/Factorization scale uncertainties using on-the-fly weights ##
- Code directory:

The following is needed to calculate truth variations from on-the-fly sherpa samples:
- Run `VBFInvTruth` algorithm from `STAnalysisCode` on input `DAOD_TRUTH3`
- Run `VBFAnalysisAlg` algorithm from `STPostProcessing` on input `MiniNtuple` from the previous step, then merge outputs
``` bash
submitVBFTruthCondor.py -l input.list -n -p /nfs/dust/atlas/user/othrif/vbf/myPP/run_condor_300919/x509up_u29949 --noSubmit
mergeVBFTruthAlg.sh
```
- Add the variations to the `input` directory in `Scale_OTF`
- Run the following:
``` bash
python calculateOTFYields.py Z_strong SR # as an example
python runAllSystematics.py # runs all regions in one go
root plot_7point_pdf.cxx # visualize the 7 point and pdf variations
root plot_7point.cxx # visualize the 7 point  variations
root plot_TF_unc.cxx # visualize the transfer factor uncertainty
```

## ckkw/qsf uncertainties using varied samples ##
- Code directory: `CKKW_QSF_Varied`

To get started, copy the inputs from eos `/eos/atlas/atlascerngroupdisk/phys-exotics/jdm/vbfinv/theoryUnc/theoVariation_met200` to the `./input` directory and change the path in the code.

Run the following:
``` bash
python calculateOTFYields.py Z_strong SR # as an example
python runAllSystematics.py # runs all regions in one go
root interpolate.cxx # example on how to perform a linear fit
root plot_ckkw_resum.cxx # visualize the ckkw/resummation variations
```

## ckkw/qsf uncertainties using SUSY parametrization##
- Code directory: `CKKW_QSF_SUSYparam`

Using the MicroNtuples produced with `VBFAnalysisAlg`, the variations weights will be added as branches using the truth number of jets and truth boson pT with the following:

``` bash
lsetup "root 6.14.04-x86_64-slc6-gcc62-opt"
python VBFAnalysis/scripts/AddVjetsSUSYParam.py Z_strong.root Z_strongNominal
python VBFAnalysis/scripts/AddVjetsSUSYParam.py W_strong.root W_strongNominal
```
Once the `ckkw` and `qsf` variations branches are added to MicroNtuples, they can be processed and analuysis regions defined using:
``` bash
lsetup "root 6.14.04-x86_64-slc6-gcc62-opt"
root start_SherpaVjetsUncert.C'("suffix",entries)'
python computeSherpaVjetsUncert.py suffix
```
