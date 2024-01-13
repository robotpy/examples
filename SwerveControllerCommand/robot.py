#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

from commands2 import TimedCommandRobot, CommandScheduler
from robotcontainer import RobotContainer


class Robot(TimedCommandRobot):
    def robotInit(self):
        """
        Instantiate our RobotContainer. This will perform all our button bindings, and put our
        autonomous chooser on the dashboard.
        """
        self.robotContainer = RobotContainer()

    def robotPeriodic(self):
        """
        Runs the Scheduler. This is responsible for polling buttons, adding newly-scheduled
        commands, running already-scheduled commands, removing finished or interrupted commands,
        and running subsystem periodic() methods. This must be called from the robot's periodic
        block in order for anything in the Command-based framework to work.
        """

    def disabledInit(self):
        pass

    def disabledPeriodic(self):
        pass

    def autonomousInit(self):
        self.autonomousCommand = self.robotContainer.getAutonomousCommand()

        """
        schedule the autonomous command (example)
        """
        if self.autonomousCommand is not None:
            self.autonomousCommand.schedule()

    def autonomousPeriodic(self):
        pass

    def autonomousCommand(self):
        pass

    def teleopInit(self):
        """
        This makes sure that the autonomous stops running when
        teleop starts running. If you want the autonomous to
        continue until interrupted by another command, remove
        this line or comment it out.
        """
        if self.autonomousCommand is not None:
            self.autonomousCommand.cancel()

    def teleopPeriodic(self):
        pass

    def testInit(self):
        """
        Cancels all running commands at the start of test mode.
        """
        CommandScheduler.getInstance().cancelAll()

    def testPeriodic(self):
        pass
