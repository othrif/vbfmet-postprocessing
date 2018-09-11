
iPATH=$1
grep "connect_wrapper  | User job exit with code 2" $iPATH/output* | awk -F':' '{print $1}' | awk -F'/' '{print $1" "$2}'  &> failConnectv4.txt 
#grep "connect_wrapper  | User job exit with code 2" testSystV3/output24847* testSystV3/output24848* | awk -F':' '{print $1}' | awk -F'/' '{print $1" "$2}'  &> failConnectv4.txt 
#grep "connect_wrapper  | User job exit with code 2"  testSystV3/output248484* testSystV3/output248485*  | awk -F':' '{print $1}' | awk -F'/' '{print $1" "$2}'  &> failConnectv4.txt 
source org.sh &> org_fail.txt

while read inputs ; do
    #inputs="testSystV3 output2484555 0 1 170 171 172 173 174 175 176 177 178 179 180 181 182 183 258 259 260 261 262 263 265 267"

    inputsarray=($inputs)
    n_inputsarray=${#inputsarray[@]}
    
    SubDir=${inputsarray[0]}
    
# write the file
    LOGFILE="${inputsarray[1]}.${inputsarray[2]}"
    mySample=`cat ${SubDir}/${LOGFILE} | grep INPUT`
    mySample=${mySample:6}
    myVariation=`cat ${SubDir}/${LOGFILE} | grep athena | awk -F' ' '{print $7}'`
    VARFILELIST="fileslistRESUB${myVariation}"
# create file
    echo "$mySample" &> $SubDir/$VARFILELIST
    
#loop over the remaining inputs
    for (( i=3; i<${n_inputsarray}; i++ ));
    do
	LOGFILE="${inputsarray[1]}.${inputsarray[$i]}"
	mySample=`cat ${SubDir}/${LOGFILE} | grep INPUT`
	mySample=${mySample:6}
	#echo $mySample
	
	myVariation=`cat ${SubDir}/${LOGFILE} | grep athena | awk -F' ' '{print $7}'`
	
	echo "$mySample" >> $SubDir/$VARFILELIST
	
    done
    
#output2484555.0
#myVariation=`cat ${SubDir}/${LOGFILE} | grep athena | awk -F' ' '{print $7}'`

#testSystV3/submit_this_pythonMUON_TTVA_STAT__1down.sh
    cp $SubDir/submit_this_python${myVariation}.sh $SubDir/submit_this_python${myVariation}.sh.resubmit
    
    if [[ $myVariation != "Nominal" ]]
    then
	perl -pi -e 's/filelistMC/'${VARFILELIST}'/g' $SubDir/submit_this_python${myVariation}.sh.resubmit ;
	#echo "NOT NOM"
    else
	perl -pi -e 's/filelist/'${VARFILELIST}'/g' $SubDir/submit_this_python${myVariation}.sh.resubmit ;
    fi
    
    echo condor_submit $SubDir/submit_this_python${myVariation}.sh.resubmit
done < org_fail.txt