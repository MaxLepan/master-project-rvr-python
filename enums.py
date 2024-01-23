from enum import Enum

class Action(Enum):
    WHEELS = "rotator"
    PUMP = "pumping"

class Data(Enum):
    TURNING = "turning"
    FORWARD = "forward"
    STOP = "stop"
    PUMP_ON = "on"
