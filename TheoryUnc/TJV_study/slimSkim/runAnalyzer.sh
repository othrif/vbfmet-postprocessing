#!/bin/bash

outputDir=${1:-"../processed"}
inputDir=${2:-"../input"}

mkdir -p ${outputDir}

echo "################################################################################"
echo "Input Directory:  ${inputDir}"
echo "Output Directory: ${outputDir}"
echo "################################################################################"

root -l -q runSkim.C\(\"${inputDir}\"\,\"${outputDir}\"\,\"W_strong\"\);
#root -l -q runSkim.C\(\"${inputDir}\"\,\"${outputDir}\"\,\"W_EWK\"\)
root -l -q runSkim.C\(\"${inputDir}\"\,\"${outputDir}\"\,\"Z_strong\"\);
#root -l -q runSkim.C\(\"${inputDir}\"\,\"${outputDir}\"\,\"Z_EWK\"\);
