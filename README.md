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
For running locally with athena:
```bash
cd run
# run locally on 10 events over a file
athena VBFAnalysis/VBFAnalysisAlgJobOptions.py --evtMax 10 --filesInput /eos/user/r/rzou/v04/user.othrif.v04.364162.Sherpa_221_NNPDF30NNLO_Wmunu_MAXHTPTV140_280_CVetoBVeto.e5340_s3126_r9364_r9315_p3575_MiniNtuple.root/user.othrif.14790250._000001.MiniNtuple.root - --currentVariation Nominal
# run locally over a dir
athena VBFAnalysis/VBFAnalysisAlgJobOptions.py --evtMax 10 --filesInput /eos/user/r/rzou/v04/user.othrif.v04.364106.Sherpa_221_NNPDF30NNLO_Zmumu_MAXHTPTV140_280_CVetoBVeto.e5271_s3126_r9364_r9315_p3575_MiniNtuple.root/* - --currentVariation Nominal
```
For running on condor:
```bash
# run on condor over a list of files for nominal
submitVBFAnalysisCondor.py -l list -n
# run on condor over a list of files for all sys
submitVBFAnalysisCondor.py -l list
# run on condor over a list of files for all sys with log files saved to a specific dir
submitVBFAnalysisCondor.py -l list -d dir
```
You can change the list of systematics in VBFAnalysis/scripts/submitVBFAnalysisCondor.py.


## Run HF Input Maker ##
This generates histograms for HistFitter to read from. It currently reads from Merged Ntuples for 2nd circulation of 36.1 fb-1 paper.
```bash
cd run
# run locally over 10 events for Z_EWK contribution nominal
athena VBFAnalysis/HFInputJobOptions.py --evtMax 10 --filesInput /eos/atlas/atlascerngroupdisk/phys-exotics/jdm/vbfinv/FinalNtuplesJuly18/VBFHiggsInv_Ztot_bkg_fixednom.root - --currentSamples Z_EWK --currentVariation NONE
```
For running on condor:
```bash
# run on condor over all the contributions and nominal only
submitHFInputCondor.py -n 
# run on condor over all the contributions and systematics 
submitHFInputCondor.py
```
You can change the list of systematics in VBFAnalysis/scripts/submitHFInputCondor.py and list of contributions in VBFAnalysis/scripts/LoopOverHF.py (this can be improved).