import wpilib
import 
import subsystems.DriveSubsystem
import subsystems.ShooterSubsystem

#This class is where the bulk of the robot should be declared. Since Command-based is a
#"declarative" paradigm, very little robot logic should actually be handled in the {@link Robot}
#periodic methods (other than the scheduler calls). Instead, the structure of the robot (including
#subsystems, commands, and button mappings) should be declared here.


class RobotContainer():

    #The robots's subsystems

    robotDrive = subsystems.DriveSubsystem.DriveSubsystem.DriveSubsystem()
    shooter = subsystems.ShooterSubsystem.ShooterSubsystem.ShooterSubsystem()

    spinUpShooter = commands2.Subsystem.