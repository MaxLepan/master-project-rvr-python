import os
import sys
import json
import time
from wss_connection_rover import WebSocketServer 
from commands_rover import rover_init, rover_drive_forward, rover_rotator_turn, rover_stop, wing_motor_activate
from enums import Action, Data
sys.path.append(os.path.abspath(os.path.join( '/home/pi/Documents/sphero-sdk-raspberrypi-python/')))

from sphero_sdk import SpheroRvrObserver
from sphero_sdk import *

rvr = SpheroRvrObserver()
dir(SpheroRvrObserver)

max_wing_motor_repeat = 15
turning_received = 0

def wss_WHEELS(action = "",data = ""):
    
    action = str(action)
    data = str(data)

    
    if(action == Action.WHEELS.value):
        if(data == Data.STOP.value):
            print("in stop")
            rover_stop()
        if(data == Data.TURNING.value):
            print("in turning")
            global turning_received
            turning_received = turning_received + 1

            if turning_received > 5:
                rover_rotator_turn(90,-90)
                turning_received = 0
            rover_rotator_turn(90,-90)
        if(data == Data.FORWARD.value):
            print("in forward")
            rover_drive_forward(90, 2.0)

 
def wss_WING_MOTOR (action = "", data = ""):

    action = str(action)
    data = str(data)

    if (action == Action.PUMP.value):
        if (data == Data.PUMP_ON.value):
            global max_wing_motor_repeat
            if max_wing_motor_repeat > 10:
                wing_motor_activate(0.1)
            elif 5 < max_wing_motor_repeat <= 10:
                wing_motor_activate(0.3)
            elif 0 < max_wing_motor_repeat <= 5:
                wing_motor_activate(0.5)
            else:
                return
            max_wing_motor_repeat = max_wing_motor_repeat - 1
            print("in motor, remaining: " + str(max_wing_motor_repeat))


messages = [
    wss_WHEELS,
    wss_WING_MOTOR
]


def commandInterpretor(message):
    global messages
    data = json.loads(message)
    action = data.get("action", 0)
    result = data.get("message", 0)

    for message in messages:
        message(action,result)
    


def main():
    
    #Init
    rover_init()
    time.sleep(2)
    #Server
    server = WebSocketServer(cmdCallback=commandInterpretor, port=8080)
    server.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
