#!/usr/bin/env python

import sys
import os

# usage: python runAllSystematics [REGION]

region = "SR"
if(len(sys.argv) > 1) :
    region = sys.argv[1]

channels = ["W_strong", "Z_strong"] #"W_EWK", "Z_EWK",
regions  = ["SR", "CRW", "CRZ"]
os.system("rm -f output.txt")
for channel in channels :
    for region in regions :
        if ("W_" in channel and "Z" in region) or ("Z_" in channel and "W" in region):
            continue
        print "\nRunning systs for channel:", channel, region
        os.system("python calculateOTFYields_allvars.py " + channel + " " + region + ">> output.txt")


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

