# Othmane Rifki
# usage: python runAllSysteamtics.py
# Runs all systematics for the W and Z backgrounds in all analysis regions - the output is the 11 bins variations for ckkw/qsf

#!/usr/bin/env python

import sys
import os

# usage: python runAllSystematics [REGION]

region = "SR"
if(len(sys.argv) > 1) :
    region = sys.argv[1]

channels = ["W_strong", "Z_strong"]
regions  = ["SR", "CRW", "CRZ"]
os.system("rm -f output.txt")
for channel in channels :
    for region in regions :
        if ("W_" in channel and "Z" in region) or ("Z_" in channel and "W" in region):
            continue
        print "\nRunning systs for channel:", channel, region
        os.system("python calculateOTFYields.py " + channel + " " + region + ">> output.txt")


with open("output.txt") as f:
    content = f.readlines()
    content=sorted(content, key=lambda x:x.split(' ')[0], reverse=True)
content = [x.strip() for x in content]
content = list(filter(None, content))

f = open("listTheorySyst", "w")
varOLD = "old"
for x in content:
    if "=" not in x:
        continue
    var = x.split("=")[0]
    if varOLD != var:
        f.write(var+"\n")
    varOLD = var
    f.write(x.split("=")[1]+"\n")

os.system("rm -f output.txt")
