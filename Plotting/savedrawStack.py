import sys
import os
import re

inDir=sys.argv[1]
if inDir[-1]!='/':
	inDir+='/'
variables=sys.argv[2]

listfiles=os.listdir(inDir)
rootInputs=[]
elecVars=",j3metsig,j3metsig_eta28,met_significance"

if inDir.find("17")>0:
	lumi=str(44307.4)
else:
	lumi=str(59937)

for infile in listfiles:#infiles:

	filepath=inDir+infile
	print "In "+str(infile)
	anaName=re.sub('out34_','',infile)
	if inDir.find("17")>0:
		anaName2=re.sub('_17.root','',anaName)
	else:
		anaName2=re.sub('.root','',anaName)
	
	os.system("./savedrawStack_hadd.sh "+filepath +" wcr_"+anaName2+"_l "+variables+" "+lumi)
	os.system("./savedrawStack_hadd.sh "+filepath +" wcr_"+anaName2+"_e "+variables+elecVars+" "+lumi)
	os.system("./savedrawStack_hadd.sh "+filepath +" wcr_"+anaName2+"_u "+variables+" "+lumi)
	if anaName2!="allmjj" and anaName2!="njgt" and anaName2!="njgt4":
		os.system("./savedrawStack_hadd.sh "+filepath +" sr_"+anaName2+"_nn "+variables+" "+lumi)
	else:
		os.system("./savedrawStack_hadd_blind.sh "+filepath +" sr_"+anaName2+"_nn "+variables+" "+lumi)


	os.system("mkdir savedrawStackOutput_"+infile)
	os.system("mkdir savedrawStackOutput_"+infile+"/png")
	os.system("mkdir savedrawStackOutput_"+infile+"/pdf")
	os.system("mv *.pdf savedrawStackOutput_"+infile+"/pdf")
	os.system("mv *.png savedrawStackOutput_"+infile+"/png")
