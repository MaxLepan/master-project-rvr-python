from enum import Enum

class Action(Enum):
    WHEELS = "rotator"
    MOTOR = "motor"

class Data(Enum):
    TURNING = "turning"
    FORWARD = "forward"
    STOP = "stop"
    WING_MOTOR_ON = "wing_motor_on"
