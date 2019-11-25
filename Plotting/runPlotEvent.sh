#declare -a analysisArray=("allmjj" "mjjLow200" "mjjLowNjetFJVT" "njgt" "mjjLowNjet" "njgt4")
declare -a analysisArray=("njgt" "mjjLowNjet" "njgt4")

path='out34_'
path1='_puDown.root'
path2='_puUp.root'
path3='.root'

for i in "${analysisArray[@]}"; do
	#python HInvPlot/macros/plotEvent.py -i inputs/input34LoosePF18OTM_NoPUCorr_mj.txt -r $path$i$path3 --analysis ${i}  --year 2018 --int-lumi 59937
	python HInvPlot/macros/plotEvent.py -i inputs/input34LoosePF18OTM_NoPUCorr_mj.txt -r $path$i$path1 --analysis ${i}  --year 2018 --int-lumi 59937 --syst PRW_DATASF__1down
	python HInvPlot/macros/plotEvent.py -i inputs/input34LoosePF18OTM_NoPUCorr_mj.txt -r $path$i$path2 --analysis ${i}  --year 2018 --int-lumi 59937 --syst PRW_DATASF__1up
done
