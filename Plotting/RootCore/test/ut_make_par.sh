#!/bin/bash

if test "$ROOTCORE_AUTO_UT" == "1" -a "$ROOTCORE_SLOW_UT" != "1"
then
    exit 0
fi

set -e
set -u

rc make_par RootCore.par
source $ROOTCOREDIR/scripts/unsetup.sh
tar xfz RootCore.par
cd RootCore
PROOF-INF/BUILD.sh
root -l -b -q PROOF-INF/SETUP.C
