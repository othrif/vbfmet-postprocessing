#!/bin/bash

set -e
set -u

mkdir A
touch A/file
ln -s A G
mkdir B
ln -s ../A B/C
mkdir D
touch D/file

result="`rc --internal rel_path A/file B`"
if test "$result" != "../A/file"
then
    echo wrong result for test 1: $result
    exit 1
fi

result="`rc --internal rel_path A/file G`"
if test "$result" != "file"
then
    echo wrong result for test 2: $result
    exit 1
fi

result="`rc --internal rel_path D/file B/C`"
if test "$result" != "../D/file"
then
    echo wrong result for test 3: $result
    exit 1
fi

true
