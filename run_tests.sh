#!/bin/bash -e

cd "$(dirname $0)"

# Keep this list alphabetically sorted
BASE_TESTS="
  addressableled
  arcadedrive
  arcadedrivexboxcontroller
  armsimulation
  canpdp
  differentialdrivebot
  digitalcommunication
  dutycycleencoder
  dutycycleinput
  elevatorprofiledpid
  elevatorsimulation
  elevatortrapezoidprofile
  encoder
  flywheelbangbangcontroller
  gamedata
  gettingstarted
  gyro
  gyromecanum
  hatchbot
  hatchbotinlined
  hidrumble
  i2ccommunication
  intermediatevision
  magicbotsimple
  mecanumbot
  mecanumdrive
  mecanumdriveXbox
  mechanism2d
  motorcontrol
  physics/src
  physics4wheel/src
  physicsmecanum/src
  physicsspi/src
  potentiometerpid
  quickvision
  ramsetecontroller
  relay
  shuffleboard
  solenoid
  statefulautonomous
  statespaceflywheel
  tankdrive
  tankdrivexboxcontroller
  timed/src
  ultrasonic
  ultrasonicpid
"

IGNORED_TESTS="
  armbot
  armbotoffboard
  drivedistanceoffboard
  frisbeebot
  gyrodrivecommands
  ramsetecommand
  schedulereventlogging
  selectcommand
  romi
  physicscamsim/src
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
