#!/bin/bash -e

cd "$(dirname $0)"

BASE_TESTS="
  arcade-drive
  cscore-intermediate-vision
  cscore-quick-vision
  gearsbot
  getting-started
  gyro
  iterative/src
  mecanum-drive
  motor-control
  pacgoat
  physics/src
  physics-4wheel/src
  physics-camsim/src
  physics-mecanum/src
  physics-spi/src
  sample/src
  tank-drive
  timed/src
"

ROBOTPY_EXT_TESTS="
  command-based
  navx
  navx-rotate-to-angle
  navx-rotate-to-angle-arcade
  magicbot-simple
  stateful-autonomous
"

IGNORED_TESTS="
  physics-pathfinder
"

ALL_TESTS="${BASE_TESTS} ${ROBOTPY_EXT_TESTS}"
EVERY_TESTS="${ALL_TESTS} ${IGNORED_TESTS}"

if [ "$1" == "all" ]; then
  TESTS="$ALL_TESTS"
elif [ "$1" == "base" ]; then
  TESTS="$BASE_TESTS"
elif [ "$1" == "ext" ]; then
  TESTS="$ROBOTPY_EXT_TESTS"
else
  echo "Usage: run_tests.sh all|base|ext"
  exit 1
fi

# Ensure that when new samples are added, they are added to the list of things
# to test. Otherwise, exit.
EVERY_TESTS=$(for i in ${EVERY_TESTS}; do
  echo ./$i/robot.py
done | sort)

FOUND_TESTS=$(find . -name robot.py | sort)

if [ "$EVERY_TESTS" != "$FOUND_TESTS" ]; then
  echo "Specified:"
  echo "$EVERY_TESTS"
  echo
  echo "Found:"
  echo "$FOUND_TESTS"
  echo
  if [ -z "$FORCE_ANYWAYS" ]; then
    echo "ERROR: Not every robot.py file is in the list of tests!"
    exit 1
  fi
fi

for t in ${TESTS}; do
  pushd $t > /dev/null
  pwd
  if ! python3 robot.py test --builtin "${@:2}"; then
    EC=$?
    echo "Test in $(pwd) failed"
    exit 1
  fi
  popd > /dev/null
done

echo "All tests successful!"
