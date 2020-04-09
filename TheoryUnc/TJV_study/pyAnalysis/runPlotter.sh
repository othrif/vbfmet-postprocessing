# Usage: ./runPlotter.sh <path of parent folder>
#!/bin/bash

inputDir=${1:-"/Users/othmanerifki/vbf/myVBFAnalyzer/proc_160119"}

echo "################################################################################"
echo "Input Directory:  ${inputDir}"
echo "################################################################################"
rm -rf ${inputDir}/plots
root -l -q plotTJVCutMjj.C\(\"${inputDir}\"\);
root -l -q plotTJVCutTJV.C\(\"${inputDir}\"\);
root -l -q plotTJVRatio.C\(\"${inputDir}\"\);