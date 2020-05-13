#!/bin/bash
#export xsec_Path=/cvmfs/atlas.cern.ch/repo/sw/database/GroupData/dev/PMGTools/PMGxsecDB_mc15.txt
export xsec_Path=../VBFAnalysis/data/PMGxsecDB_mc16.txt

echo " All samples:"
for i in Znunu Zee Wenu_
do
    cat ${xsec_Path} | grep $i | grep ckkw15
    cat ${xsec_Path} | grep $i | grep ckkw30
    cat ${xsec_Path} | grep $i | grep qsf025
    cat ${xsec_Path} | grep $i | grep qsf4
done

for i in Znunu Zee Zmumu Ztautau Wenu Wmunu Wtaunu
do
    cat ${xsec_Path} | grep Sherpa_221_NNPDF30NNLO_${i}_MAXHTPTV | grep -v Hinv  | grep -v e5340_e4083 | grep -v e5679 | grep -v e5750 | grep -v e5750 | grep -v e6405 | grep -v e6779 | grep -v e5585 | grep -v VBFfilt | grep -v Mll | grep -v noHadMPI | grep -v hpsmode0  | grep -v _l | grep -v _h | sort
done


echo "      ckkw15 ckkw30 qsf025 qsf4"
for i in Znunu Zee Wenu_
do
    ckkw15=`cat ${xsec_Path} | grep $i | grep ckkw15 | awk '{sum += $5*$4*$3} END {print sum}'`
    ckkw30=`cat ${xsec_Path} | grep $i | grep ckkw30 | awk '{sum += $5*$4*$3} END {print sum}'`
    qsf025=`cat ${xsec_Path} | grep $i | grep qsf025 | awk '{sum += $5*$4*$3} END {print sum}'`
    qsf4=`cat ${xsec_Path}   | grep $i | grep qsf4   | awk '{sum +=   $5*$4*$3} END {print sum}'`
    echo "$i $ckkw15 $ckkw30 $qsf025 $qsf4"
done




for i in Znunu Zee Zmumu Ztautau Wenu Wmunu Wtaunu
do
    count=`cat ${xsec_Path} | grep Sherpa_221_NNPDF30NNLO_${i}_MAXHTPTV | grep -v Hinv  | grep -v e5340_e4083 | grep -v e5679 | grep -v e5750 | grep -v e5750 | grep -v e6405 | grep -v e6779 | grep -v e5585 | grep -v VBFfilt | grep -v Mll | grep -v noHadMPI | grep -v hpsmode0  | grep -v _l | grep -v _h | sort | wc -l`
    proc=`cat ${xsec_Path} | grep Sherpa_221_NNPDF30NNLO_${i}_MAXHTPTV | grep -v Hinv  | grep -v e5340_e4083 | grep -v e5679 | grep -v e5750 | grep -v e5750 | grep -v e6405 | grep -v e6779 | grep -v e5585 | grep -v VBFfilt | grep -v Mll | grep -v noHadMPI | grep -v hpsmode0 | grep -v _l | grep -v _h | sort | awk '{sum += $5*$4*$3} END {print sum}'`
    echo "$i $proc"
done

