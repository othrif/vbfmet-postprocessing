#!/usr/bin/env python

# Input dir of pickle files from YieldTables.py

import os
import sys
import ROOT
import math
import pickle


def LoadPickleFiles(dir_name):

    if not os.path.exists(dir_name):
        print 'Pickle directory does not exist'
        sys.exit(0)
    fnames=[]
    for f in os.listdir(dir_name):
        if f.count('pickle'):
            fnames+=[dir_name.rstrip('/')+'/'+f]
        
    print 'Loaded post fit files:',fnames

    fpickles = []
    for f in fnames:
        fpickles+=[pickle.load(open(f,'rb'))]
    return fpickles
   


def main():
    ROOT.gROOT.SetBatch(True)

    postFitPickles = LoadPickleFiles(sys.argv[1])
    chi2=[0.0]*len(postFitPickles)
    chi2_new=[0.0]*len(postFitPickles)
    chi2Poisson=[0.0]*len(postFitPickles)
    regionBin=-1
    for fpickle in postFitPickles: 
	regionBin+=1
        pickle_region_names = fpickle['names'] # these are the CR and SR names as entered. just a description of the entries
        for pickle_key in fpickle.keys():
	    if 'TOTAL_FITTED' in pickle_key:
		if 'err' in pickle_key:
		    err=fpickle[pickle_key]
		else:
		    bkg=fpickle[pickle_key]
	    elif 'nobs' in pickle_key:
		data=fpickle[pickle_key]
        index=0
	for i in range(len(data)):
	    if i>0:
	        chi2[regionBin]+=(data[i]-bkg[i])*(data[i]-bkg[i])/err[i]/err[i]
	        chi2_new[regionBin]+=(data[i]-bkg[i])*(data[i]-bkg[i])/(bkg[i]+(err[i]*err[i]))
	        chi2Poisson[regionBin]+=(data[i]-bkg[i])*(data[i]-bkg[i])/bkg[i]
	    index+=1 

    print "Chi2: "+str(chi2)
    print "Chi2 sum: "+str(sum(chi2))
    print "Chi2_new: "+str(chi2_new)
    print "Chi2_new sum: "+str(sum(chi2_new))
    print "Chi2Poisson: "+str(chi2Poisson)
    print "Chi2Poisson sum: "+str(sum(chi2Poisson))

if __name__=='__main__':
    main()
