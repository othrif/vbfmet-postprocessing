truth study for TJV and Mjj variation:
``` bash
./runAnalyzer.sh test
python extract_CRSR.py test/*
python ntuplesToHists.py test/extract_* --config hists_config_MjjTJV.json --treename nominal --eventWeight "1" --newOutputs
./runPlotter.sh test
```