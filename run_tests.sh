#!/bin/bash -e

cd "$(dirname $0)"

BASE_TESTS="
  arcade-drive
  arm-simulation
  commands-v2/hatchbot
  commands-v2/ramsete
  commands-v2/romi
  cscore-intermediate-vision
  cscore-quick-vision
  elevator-simulation
  game-data
  getting-started
  gyro
  mecanum-drive
  mecanum-driveXbox
  motor-control
  physics/src
  physics-4wheel/src
  physics-camsim/src
  physics-mecanum/src
  physics-spi/src
  tank-drive
  timed/src
"

ROBOTPY_EXT_TESTS=""
  # magicbot-simple
# "

NAVX_TESTS="
  navx
  navx-rotate-to-angle
  navx-rotate-to-angle-arcade
"

IGNORED_TESTS="
  magicbot-simple
  stateful-autonomous
  shuffleboard
"

ALL_TESTS="${BASE_TESTS} ${ROBOTPY_EXT_TESTS}"
EVERY_TESTS="${ALL_TESTS} ${IGNORED_TESTS} ${NAVX_TESTS}"

if [ "$1" == "all" ]; then
  TESTS="$ALL_TESTS"
elif [ "$1" == "base" ]; then
  TESTS="$BASE_TESTS"
elif [ "$1" == "ext" ]; then
  TESTS="$ROBOTPY_EXT_TESTS"
elif [ "$1" == "navx" ]; then
  TESTS="$NAVX_TESTS"
else
  echo "Usage: run_tests.sh all|base|ext|navx"
  exit 1
fi

TMPD=$(mktemp -d)
trap 'rm -rf "$TMPD"' EXIT

# Ensure that when new samples are added, they are added to the list of things
# to test. Otherwise, exit.
for i in ${EVERY_TESTS}; do
  echo ./$i/robot.py
done | sort > $TMPD/a

find . -name robot.py | sort > $TMPD/b

if ! diff -u $TMPD/a $TMPD/b; then

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
