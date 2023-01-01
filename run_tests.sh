#!/bin/bash -e

cd "$(dirname $0)"

BASE_TESTS="
  addressableled
  arcade-drive
  arm-simulation
  commands-v2/armbotoffboard
  commands-v2/hatchbot
  commands-v2/frisbee-bot
  commands-v2/ramsete
  commands-v2/selectcommand
  cscore-intermediate-vision
  cscore-quick-vision
  elevator-simulation
  game-data
  getting-started
  gyro
  magicbot-simple
  mecanum-drive
  mecanum-driveXbox
  mechanism2d
  motor-control
  physics/src
  physics-4wheel/src
  physics-mecanum/src
  physics-spi/src
  tank-drive
  timed/src
  elevator-profiled-pid
  elevator-trapezoid-profile
  commands-v2/gyro-drive-commands
  commands-v2/drive-distance-offboard
"

IGNORED_TESTS="
  commands-v2/romi
  physics-camsim/src
  stateful-autonomous
  shuffleboard
"

ALL_TESTS="${BASE_TESTS}"
EVERY_TESTS="${ALL_TESTS} ${IGNORED_TESTS}"
TESTS="${ALL_TESTS}"

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
