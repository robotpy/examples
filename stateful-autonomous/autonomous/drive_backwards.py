from robotpy_ext.autonomous import StatefulAutonomous, state, timed_state


class DriveBackwards(StatefulAutonomous):
    MODE_NAME = "Drive Backwards"

    def initialize(self):
        # This allows you to tune the variable via the SmartDashboard over
        # networktables
        self.register_sd_var("drive_speed", -1)

    @timed_state(duration=0.5, next_state="drive_backwards", first=True)
    def drive_wait(self):
        self.drive.tankDrive(0, 0)

    @timed_state(duration=5, next_state="stop")
    def drive_backwards(self):
        self.drive.tankDrive(self.drive_speed, -1 * (self.drive_speed))

    @state()  # Remove or modify this to add additional states to this class.
    def stop(self):
        self.drive.tankDrive(0, 0)
