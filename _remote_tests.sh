#!/bin/bash -e
# Checks out repo 

if [ -d examples ]; then
    cd examples
    git fetch --depth=1
    git checkout origin/master
else
    git clone --depth=1 https://github.com/robotpy/examples
    cd examples
fi

git rev-parse HEAD

exec ./run_tests.sh "$@"
