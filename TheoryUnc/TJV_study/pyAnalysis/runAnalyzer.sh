#!/bin/bash

outputDir=${1:-"/nfs/dust/atlas/user/othrif/scratch/myPP/latest/processed"}
inputDir=${2:-"/nfs/dust/atlas/user/othrif/samples/MicroNtuples/v35Truth/"}

mkdir -p ${outputDir}

echo "################################################################################"
echo "Input Directory:  ${inputDir}"
echo "Output Directory: ${outputDir}"
echo "################################################################################"

#root -l -q procAnalyzer.C\(\"${inputDir}\"\,\"${outputDir}\"\,\"VBFH125\"\);
#root -l -q procAnalyzer.C\(\"${inputDir}\"\,\"${outputDir}\"\,\"ggFH125\"\);
#root -l -q procAnalyzer.C\(\"${inputDir}\"\,\"${outputDir}\"\,\"VH125\"\);
root -l -q procAnalyzer.C\(\"${inputDir}\"\,\"${outputDir}\"\,\"W_strong\"\);
root -l -q procAnalyzer.C\(\"${inputDir}\"\,\"${outputDir}\"\,\"W_EWK\"\)
root -l -q procAnalyzer.C\(\"${inputDir}\"\,\"${outputDir}\"\,\"Z_strong\"\);
root -l -q procAnalyzer.C\(\"${inputDir}\"\,\"${outputDir}\"\,\"Z_EWK\"\);