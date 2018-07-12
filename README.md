First time setup

```bash
cd $TestArea
git clone ssh://git@gitlab.cern.ch:7999/VBFInv/STPostProcessing.git source/
mkdir build;cd build
acmSetup AthAnalysis,21.2.35
acm compile
```

Future setup 

```bash
cd $TestArea/build
acmSetup
```

