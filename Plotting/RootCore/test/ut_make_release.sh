#!/bin/bash

if test "$ROOTCORE_AUTO_UT" == "1" -a "$ROOTCORE_SLOW_UT" != "1"
then
    exit 0
fi

set -e
set -u

pwd

rc checkout_pkg RootCore

source $ROOTCOREDIR/scripts/unsetup.sh
source RootCore/scripts/setup.sh

rc checkout_pkg atlasoff/PhysicsAnalysis/D3PDTools/RootCoreUtils/tags
if test \! -z "${NKLOCATION:+x}"
then
    echo WARNING: found NKLOCATION, assuming this is Nils Krumnack running it
    export CERN_USER=krumnack
fi
rc checkout_pkg atlasoff/PhysicsAnalysis/D3PDTools/SampleHandler/tags
rc checkout_pkg atlasoff/PhysicsAnalysis/D3PDTools/EventLoop/tags/

mkdir MyPackage
rc make_skeleton MyPackage

rc find_packages
source RootCore/scripts/setup_external.sh
rc compile 
rc compile --log-files
rc test_ut --fast

test -f PhysicsAnalysis_D3PDTools_RootCore.loglog
test -f MyPackage.loglog

rc --internal manage_pkg update atlasoff/PhysicsAnalysis/D3PDTools/EventLoop/tags/EventLoop-00-00-01
if test \! -z "${NKLOCATION:+x}"
then
    echo WARNING: found NKLOCATION, assuming this is Nils Krumnack running it
    unset CERN_USER
fi
test "`rc version | grep EventLoop-00-00-01`" != ""
rc --internal manage_pkg update atlasoff/PhysicsAnalysis/D3PDTools/EventLoop/tags
rc --internal manage_pkg update svn+ssh://nonexistantuser@svn.cern.ch/reps/atlasoff/PhysicsAnalysis/D3PDTools/EventLoop/tags
rc status
rc update

mkdir tmp1
rc version | grep -v MyPackage >tmp1/packages.txt
cd tmp1
rc checkout packages.txt
