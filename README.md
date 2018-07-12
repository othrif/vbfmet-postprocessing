First time setup
`cd $TestArea
git clone ssh://git@gitlab.cern.ch:7999/VBFInv/STPostProcessing.git source/
mkdir build;cd build
acmSetup AthAnalysis,21.2.35
acmCompile `

Future setup 
`cd $TestArea/build
acmSetup`

