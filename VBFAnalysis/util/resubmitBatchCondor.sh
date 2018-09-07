
SYSTDIR=$1
rm $SYSTDIR/filelistRESUB*
grep ERROR $SYSTDIR/* | grep root &> fail.txt
#grep "User job exit with code 2" $SYSTDIR/* &> fail_other.txt
for i in `cat fail.txt`; do echo  "$i" | awk -F':' '{print $1}' ; done | grep output &> failoutput.txt
while read i; do echo  "$i" | awk -F'[' '{print $2}' | awk -F']' '{print $1}' ; done < fail.txt | grep root  &> failFiles.txt
for i in `cat failoutput.txt`; do cat  $i | grep THistSvc | awk -F'[' '{print $2}' | awk -F']' '{print $1}'  ; done  &> failSyst.txt
for i in `cat failFiles.txt `; do grep $i $SYSTDIR/filelist ; done &> lauchList.txt
python resubmit.py

while read i; do s=($i)  ; 
    for b in `ls $SYSTDIR/submit*${s[0]}*.sh`; do 
	cp $b ${b}.resubmit; 
	c=$b".resubmit"; 
	rep="filelistRESUB"${s[0]}; 
	#echo $rep; 
	perl -pi -e 's/filelist/'${rep}'/g' $c ; 

	line=`cat $c | grep filelist`
	inputFile=""
	for w in $line; do
	    `echo $w | grep "filelist" > inputFile`
	    
	    for n in `cat inputFile`; do 
		echo "${s[1]} ${s[2]}" >> $n
	    done
	done
	echo "condor_submit $c"
    done ; 
done < writeOut.txt

#for i in `ls $SYSTDIR/*.resubmit`; do  perl -pi -e 's/filelist/filelistRESUB/g' $i; done
#while read i; do echo $i ; done < writeOut.txt