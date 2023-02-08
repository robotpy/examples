# !/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#


class Units:
    def __init__(self) -> None:
        raise Exception("This is a utility class!")

    def rotationsPerMinuteToRadiansPerSecond(rpm: float) -> float:
        return rpm * 0.10472
