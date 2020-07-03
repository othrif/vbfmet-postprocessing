#!/usr/bin/env python
""" Utils for making plots out of numpy arrays """
import os
import shutil
import glob
import math

import numpy as np
import numpy.lib.recfunctions as recfn

# Matplotlib                                                                                  
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
###############################################################################  
def make1Dplot(arr1,arr2,xname,xmin,xmax,isLog,isNorm): 
    """Plot a histogram with error bars."""

    arr1Flat, arr2Flat = flatten_array(arr1, arr2)
    
    hist1, bin_edges1 = np.histogram(arr1Flat, bins=50,
                                     range=(xmin,xmax),
                                     density=isNorm)
    
    hist2, bin_edges2 = np.histogram(arr2Flat, bins=50, 
                                     range=(xmin,xmax),
                                     density=isNorm)
    
    bin_centers = (bin_edges2[:-1] + bin_edges2[1:]) / 2.
    fig, (ax1, ax2) = plt.subplots(nrows=2, 
                                   ncols=1, 
                                   sharex=True, 
                                   gridspec_kw={'height_ratios': [3,1]})
    
    err1 = np.sqrt(hist1)
    err2 = np.sqrt(hist2)
    
    if isNorm :
        nevents1 = float(sum(hist1))
        nevents2 = float(sum(hist2))
        binwidth = bin_edges1[1] - bin_edges1[0]
     #   hist1    = hist1/nevents1/binwidth
     #   hist2    = hist2/nevents2/binwidth
        err1     = err1/nevents1/binwidth
        err2     = err2/nevents2/binwidth

    ax1.step(bin_centers,
             hist1,
             where='mid',
             color='g',
             label='ODD')
    #ax1.errorbar(bin_centers, hist1, err1, fmt='g.')

    ax1.step(bin_centers,
             hist2,
             where='mid',
             color='b',
             label='generic')

    #ax1.errorbar(bin_centers, hist2, err2, fmt='b.')
    
    ax1.set_ylabel('A.U.')
    ax1.set_xlim(xmin,xmax)
    if isLog==False: ax1.set_ylim(ymin=0)
    ax1.legend()
    
    ratio = getRatio(hist1,hist2)
    
    ax2.step(bin_centers,
             ratio,
             where='mid',
             color='k')
    
    ax2.set_xlim(xmin,xmax)
    ax2.set_ylim(0.4,1.6)
    ax2.set_ylabel('ODD/Generic')
    ax2.set_xlabel(xname)    
    ax2.grid(True,'major','both')

    if isLog==True:
        ax1.set_yscale('log')
        pltname = '{}_log.png'.format(xname)
    else:
        ax1.set_yscale('linear')
        pltname = '{}.png'.format(xname)

    plt.show() 
    plt.savefig(pltname)       
    print('saved {}'.format(pltname))
    plt.clf()
#-----------------------------------------------------
def make2Dplot(arr1,arr2,xname,yname):
    arr1Flat, arr2Flat = flatten_array(arr1, arr2)
    plt.hist2d(arr1Flat,arr2Flat,100,norm=mcolors.LogNorm())
    plt.xlabel(xname)
    plt.ylabel(yname)
    plt.colorbar()
    plt.show()    
    pltname = '{}_vs_{}.png'.format(xname,yname)
    plt.savefig(pltname)
    print('saved {}'.format(pltname))
    plt.clf()
#-----------------------------------------------------
def getRatio(bin1, bin2):
    if len(bin1) != len(bin2):
        print ("Can't make a ratio! Unequal number of bins!")
    bins=[]
    for b1,b2 in zip(bin1,bin2):
        if b1==0 and b2==0:
            bins.append(1.)
        elif b2==0:
            bins.append(0.)
        else:
            bins.append(float(b1)/float(b2))
    return bins
#-----------------------------------------------------
def error(bins,edges):
    # Just estimate the error as the sqrt of the count
    err = [np.sqrt(x) for x in bins]
    errmin = []
    errmax = []
    for x,err in zip(bins,err):
        errmin.append(x-err/2)
        errmax.append(x+err/2)
    return errmin, errmax
#-----------------------------------------------------
def flatten_array(arr1,arr2):
    if arr1.dtype!=np.dtype('float32'):
        arr1Flat = np.hstack(arr1)
    else: 
        arr1Flat = arr1

    if arr2.dtype!=np.dtype('float32'):
        arr2Flat = np.hstack(arr2)
    else: 
        arr2Flat = arr2
    return arr1Flat, arr2Flat
#-----------------------------------------------------
def makeHTML(outFile,title):

    plots = glob.glob('*.pdf')
    f = open(outFile,"w+")
    f.write("<!DOCTYPE html\n")
    f.write(" PUBLIC \"-//W3C//DTD HTML 3.2//EN\">\n")
    f.write("<html>\n")
    f.write("<head><title>:"+ title +" </title></head>\n")
    f.write("<body bgcolor=\"EEEEEE\">\n")
    f.write("<table border=\"0\" cellspacing=\"5\" width=\"100%\">\n")
    for i in range(0,len(plots)):
        offset = 2
        if i==0 or i%3==0: f.write("<tr>\n")
        f.write("<td width=\"25%\"><a target=\"_blank\" href=\"" + plots[i] + "\"><img src=\"" + plots[i] + "\" alt=\"" + plots[i] + "\" width=\"100%\"></a></td>\n")
        if i==offset: 
            f.write("</tr>\n")
        elif (i>offset and (i-offset)%3==0) or i==len(plots): 
            f.write("</tr>\n")
            
    f.write("</table>\n")
    f.write("</body>\n")
    f.write("</html>")
    f.close()
