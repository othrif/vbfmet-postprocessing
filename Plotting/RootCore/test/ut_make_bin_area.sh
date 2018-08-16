#!/bin/bash

if test "$ROOTCORE_AUTO_UT" == "1" -a "$ROOTCORE_SLOW_UT" != "1"
then
    exit 0
fi

set -e
set -u

rc make_bin_area RootCoreBin
source $ROOTCOREDIR/scripts/unsetup.sh
source RootCoreBin/local_setup.sh
rc find_packages
rc compile
rc test_ut
