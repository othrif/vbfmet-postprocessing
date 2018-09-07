#grep "connect_wrapper  | User job exit with code 2" testSystV3/output2484* | awk -F':' '{print $1}' | awk -F'/' '{print $1" "$2}'  &> failConnectv4.txt &

MYDIR=""
JOB=""
LIST=""
PRINT=1
while read i ; do
    PRINT=1
    com=`echo $i | awk -F'.' '{print $1" "$2}'`
    arraycom=($com)
    MYDIR=${arraycom[0]}
    #echo ${arraycom[1]}
    if [[ $JOB = ${arraycom[1]} ]]; then
	LIST="$LIST ${arraycom[2]}"
    else
	if [[ $JOB != "" ]]; then
	    echo "$MYDIR $JOB $LIST"
	    PRINT=0
	fi
	LIST=${arraycom[2]}
	JOB=${arraycom[1]}
    fi

done < failConnectv4.txt

if [[ $PRINT -eq 1 ]]; then
    echo "$MYDIR $JOB $LIST"
fi