#from array import array
#import math
#from math import *


def BooleanInput(inStr):
    if inStr in ['T','t','True','true','TRUE','yes','Yes','YES','y','Y']:
        save=True
    elif inStr in ['F','f','False','false','FALSE','n','N','no','No','NO']:
        save=False
    else:
        print "Improper input"

    return save


def qgVariable(inStr):
    if inStr in ['1','NTracks','ntracks','ntrack','NTrack','n','N']:
        var="NTracks"
    elif inStr in ['2','Width','width','w','W']:
        var="TrackWidth"
    else:
        print "Improper input"

    return var
