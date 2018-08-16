#!/bin/bash

set -e
set -u

if test -f $ROOTCOREBIN/lib/$ROOTCORECONFIG/libgc.dylib -a -f $ROOTCOREBIN/lib/$ROOTCORECONFIG/libgccpp.dylib
then
    export DYLD_INSERT_LIBRARIES=$ROOTCOREBIN/lib/$ROOTCORECONFIG/libgc.dylib:$ROOTCOREBIN/lib/$ROOTCORECONFIG/libgccpp.dylib
elif test -f $ROOTCOREBIN/lib/$ROOTCORECONFIG/libgc.so -a -f $ROOTCOREBIN/lib/$ROOTCORECONFIG/libgccpp.so
then
    export LD_PRELOAD=$ROOTCOREBIN/lib/$ROOTCORECONFIG/libgc.so:$ROOTCOREBIN/lib/$ROOTCORECONFIG/libgccpp.so
fi

exec root "$@"
