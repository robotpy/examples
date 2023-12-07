#!/bin/bash -e

cd "$(dirname $0)"

# Keep this list alphabetically sorted
BASE_TESTS="
  addressableled
  arcade-drive
  arcade-drive-xbox-controller
  arm-simulation
  canpdp
  hatchbot
  hatchbot-inlined
  cscore-intermediate-vision
  cscore-quick-vision
  differential-drive-bot
  digital-communication
  elevator-profiled-pid
  elevator-simulation
  elevator-trapezoid-profile
  game-data
  getting-started
  gyro
  i2c-communication
  magicbot-simple
  mecanum-drive
  mecanum-driveXbox
  mechanism2d
  motor-control
  physics/src
  physics-4wheel/src
  physics-mecanum/src
  physics-spi/src
  potentiometer-pid
  relay
  shuffleboard
  solenoid
  stateful-autonomous
  state-space-flywheel
  tank-drive
  tank-drive-xbox-controller
  timed/src
  ultrasonic
"

IGNORED_TESTS="
  armbot
  armbotoffboard
  drive-distance-offboard
  frisbee-bot
  gyro-drive-commands
  ramsete
  scheduler-event-logging
  selectcommand
  romi
  physics-camsim/src
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
