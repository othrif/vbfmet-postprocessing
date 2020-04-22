#!/bin/bash
export xsec_Path=/cvmfs/atlas.cern.ch/repo/sw/database/GroupData/dev/PMGTools/PMGxsecDB_mc15.txt
#export xsec_Path=../VBFAnalysis/data/PMGxsecDB_mc16.txt

echo " All samples:"
for i in Zee
do
    cat ${xsec_Path} | grep $i | grep ckkw15 | grep -v 2JetsEW1 | sort
done

for i in Zee
do
    cat ${xsec_Path} | grep Sherpa_221_NNPDF30NNLO_${i}_MAXHTPTV | grep -v Hinv  | grep -v e5340_e4083 | grep -v e5679 | grep -v e5750 | grep -v e5750 | grep -v e6405 | grep -v e6779 | grep -v e5585 | grep -v VBFfilt | grep -v Mll | grep -v noHadMPI | grep -v hpsmode0  | grep -v _l | grep -v _h | sort
done


#echo "      ckkw15"
for i in Zee
do
    ckkw15=`cat ${xsec_Path} | grep $i | grep ckkw15  | grep -v 2JetsEW1  | awk '{sum += $5*$4*$3} END {print sum}'`
    cvbv_ckkw15=`cat ${xsec_Path} | grep $i | grep ckkw15  | grep -v 2JetsEW1  | grep CVetoBVeto | awk '{sum += $5*$4*$3} END {print sum}'`
    cfbv_ckkw15=`cat ${xsec_Path} | grep $i | grep ckkw15  | grep -v 2JetsEW1  | grep CFilterBVeto | awk '{sum += $5*$4*$3} END {print sum}'`
    bf_ckkw15=`cat ${xsec_Path} | grep $i | grep ckkw15  | grep -v 2JetsEW1  | grep BFilter | awk '{sum += $5*$4*$3} END {print sum}'`
    echo "$i ckkw15 inclusive $ckkw15"
    echo "$i ckkw15 CVetoBVeto $cvbv_ckkw15"
    echo "$i ckkw15 CFilterBVeto $cfbv_ckkw15"
    echo "$i ckkw15 BFilter $bf_ckkw15"
done



for i in Zee
do
    count=`cat ${xsec_Path} | grep Sherpa_221_NNPDF30NNLO_${i}_MAXHTPTV | grep -v Hinv  | grep -v e5340_e4083 | grep -v e5679 | grep -v e5750 | grep -v e5750 | grep -v e6405 | grep -v e6779 | grep -v e5585 | grep -v VBFfilt | grep -v Mll | grep -v noHadMPI | grep -v hpsmode0  | grep -v _l | grep -v _h | sort | wc -l`
    proc=`cat ${xsec_Path} | grep Sherpa_221_NNPDF30NNLO_${i}_MAXHTPTV | grep -v Hinv  | grep -v e5340_e4083 | grep -v e5679 | grep -v e5750 | grep -v e5750 | grep -v e6405 | grep -v e6779 | grep -v e5585 | grep -v VBFfilt | grep -v Mll | grep -v noHadMPI | grep -v hpsmode0 | grep -v _l | grep -v _h | sort | awk '{sum += $5*$4*$3} END {print sum}'`
    cvbv=`cat ${xsec_Path} | grep Sherpa_221_NNPDF30NNLO_${i}_MAXHTPTV | grep CVetoBVeto  | grep -v Hinv  | grep -v e5340_e4083 | grep -v e5679 | grep -v e5750 | grep -v e5750 | grep -v e6405 | grep -v e6779 | grep -v e5585 | grep -v VBFfilt | grep -v Mll | grep -v noHadMPI | grep -v hpsmode0 | grep -v _l | grep -v _h | sort | awk '{sum += $5*$4*$3} END {print sum}'`
    cfbv=`cat ${xsec_Path} | grep Sherpa_221_NNPDF30NNLO_${i}_MAXHTPTV | grep CFilterBVeto  | grep -v Hinv  | grep -v e5340_e4083 | grep -v e5679 | grep -v e5750 | grep -v e5750 | grep -v e6405 | grep -v e6779 | grep -v e5585 | grep -v VBFfilt | grep -v Mll | grep -v noHadMPI | grep -v hpsmode0 | grep -v _l | grep -v _h | sort | awk '{sum += $5*$4*$3} END {print sum}'`
    bf=`cat ${xsec_Path} | grep Sherpa_221_NNPDF30NNLO_${i}_MAXHTPTV | grep BFilter  | grep -v Hinv  | grep -v e5340_e4083 | grep -v e5679 | grep -v e5750 | grep -v e5750 | grep -v e6405 | grep -v e6779 | grep -v e5585 | grep -v VBFfilt | grep -v Mll | grep -v noHadMPI | grep -v hpsmode0 | grep -v _l | grep -v _h | sort | awk '{sum += $5*$4*$3} END {print sum}'`

    echo "$i inclusive: nominal=$proc / ckkw15=$ckkw15  => ratio=`bc -l <<<"scale=2;$proc/$ckkw15"`"
    echo "$i CVetoBVeto: nominal=$cvbv / ckkw15=$cvbv_ckkw15  => ratio=`bc -l <<<"scale=2;$proc/$cvbv_ckkw15"`"
    echo "$i CFilterBVeto: nominal=$cfbv / ckkw15=$cfbv_ckkw15  => ratio=`bc -l <<<"scale=2;$proc/$cfbv_ckkw15"`"
    echo "$i BFilter: nominal=$bf / ckkw15=$bf_ckkw15  => ratio=`bc -l <<<"scale=2;$proc/$bf_ckkw15"`"
done


# Zee ckkw15 24 lines
# Zee nominal 14 lines
