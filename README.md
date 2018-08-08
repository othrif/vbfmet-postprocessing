## First time setup ##

```bash
cd $TestArea
git clone ssh://git@gitlab.cern.ch:7999/VBFInv/STPostProcessing.git source/
mkdir build;cd build
acmSetup AthAnalysis,21.2.35
acm compile
```

## Future setup ##

```bash
cd $TestArea/build
acmSetup
```

## Run VBFAnalysisAlg ##
This generates the micro ntuples.
```bash
cd run
athena VBFAnalysis/VBFAnalysisAlgJobOptions.py
```

## Run HF Input Maker ##

```bash
cd run
# run locally
athena VBFAnalysis/HFInputJobOptions.py --evtMax 10 --filesInput ~/eosvbfinv/FinalNtuplesJuly18/VBFHiggsInv_Ztot_bkg_fixednom.root - --currentSamples Z_EWK --currentVariation NONE
# submit to condor
python ../source/STPostProcessing/VBFAnalysis/scripts/submitHFInputCondor.py
```