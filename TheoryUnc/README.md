# Theory Uncertainties for V+jets #


## Renormalization/Factorization scale uncertainties using on-the-fly weights ##
- Code directory:

The following is needed to calculate truth variations from on-the-fly sherpa samples:
- Run `VBFInvTruth` algorithm from `STAnalysisCode` on input `DAOD_TRUTH3`
- Run `VBFAnalysisAlg` algorithm from `STPostProcessing` on input `MiniNtuple` from the previous step, then merge outputs
``` bash
submitVBFTruthCondor.py -l input.list -n -p /nfs/dust/atlas/user/othrif/vbf/myPP/run_condor_300919/x509up_u29949
mergeVBFTruthAlg.sh
```
- The latest version of the variations is located in `/eos/atlas/atlascerngroupdisk/phys-exotics/jdm/vbfinv/truthNtuples/final_scaleOTF_260620`
- Add the variations to the `input` directory in `Scale_OTF`
- Run the following for single tests:
``` bash
python computeOTFUnc.py Z_strong SR # as an example to run variations for all 16 bins + 1 VR bin with 0 lepton SR selection for QCD Z+jets
root plot_7point_pdf.cxx'("input directory","PhiLow")' # visualize the 7 point scale and pdf variations for SR/CRZ/CRW PhiLow region
root plot_TF_binom.cxx'("input directory","PhiLow")' # visualize the transfer factor uncertainty for SR/CRZ/CRW PhiLow region
```
- Run the following to reproduce all plots and results:
``` bash
python runAllSystematics.py # runs all regions in one go and produce the final theory systematics input for Z and W in all SRs, CRs, and VRs for up and down variations
./plotAll.sh # make plots for all SR/CRZ/CRW/VR regions
python plotVar.py listTheorySyst_CONF listTheorySyst_NEW  outputname # compare the transfer factor uncertainty between the old and new setup
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
