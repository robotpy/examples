#!/bin/bash -e

cd "$(dirname $0)"

# Keep this list alphabetically sorted
BASE_TESTS="
  AddressableLED
  ArcadeDrive
  ArcadeDriveXboxController
  ArmSimulation
  CANPDP
  DifferentialDriveBot
  DigitalCommunication
  DutyCycleEncoder
  DutyCycleInput
  ElevatorProfiledPID
  ElevatorSimulation
  ElevatorTrapezoidProfile
  Encoder
  FlywheelBangBangController
  GameData
  GettingStarted
  Gyro
  GyroMecanum
  HatchbotInlined
  HatchbotTraditional
  HidRumble
  I2CCommunication
  IntermediateVision
  MagicbotSimple
  MecanumBot
  MecanumDrive
  MecanumDriveXbox
  Mechanism2d
  MotorControl
  Physics/src
  Physics4Wheel/src
  PhysicsMecanum/src
  PhysicsSPI/src
  PotentiometerPID
  QuickVision
  RamseteController
  Relay
  ShuffleBoard
  Solenoid
  StatefulAutonomous
  StateSpaceElevator
  StateSpaceFlywheel
  StateSpaceFlywheelSysId
  SwerveBot
  TankDrive
  TankDriveXboxController
  Timed/src
  Ultrasonic
  UltrasonicPID
"

IGNORED_TESTS="
  ArmBot
  ArmBotOffboard
  DriveDistanceOffboard
  FrisbeeBot
  GyroDriveCommands
  RamseteCommand
  SchedulerEventLogging
  SelectCommand
  RomiReference
  PhysicsCamSim/src
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
