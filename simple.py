import os
import sys
import json
import time
import threading
from wss_connection_rover import WebSocketServer 
from commands_rover import rover_init, rover_drive_forward, rover_rotator_turn, rover_stop, wing_motor_activate
from enums import Action, Data
sys.path.append(os.path.abspath(os.path.join( '/home/pi/Documents/sphero-sdk-raspberrypi-python/')))

from sphero_sdk import SpheroRvrObserver
from sphero_sdk import *

rvr = SpheroRvrObserver()
dir(SpheroRvrObserver)

max_wing_motor_repeat = 1000
turning_received = 0
breakLoop = False
is_thread_already_started = False

def rvr_drive_threaded():
    global breakLoop
    breakLoop = False
    print("in thread")
    print("breakLoop before: " + str(breakLoop))
    while not breakLoop:
        rover_rotator_turn(110, -110)
        time.sleep(2.3)
    print("breakLoop after: " + str(breakLoop))

def wss_WHEELS(action = "",data = ""):
    global breakLoop, is_thread_already_started

    action = str(action)
    data = str(data)

    if(action == Action.ROTATOR.value):
        if(data == Data.STOP.value):
            print("in stop")
            breakLoop = True
            rover_stop()
        if(data == Data.TURNING.value):
            print("in turning")
            global turning_received

            if turning_received < 5:
                rover_rotator_turn(90,-90)
                time.sleep(2.3)
                print("manual turning")
            else:
                if is_thread_already_started == False:
                    print("before thread start")
                    threading.Thread(target=rvr_drive_threaded, daemon=True).start()
                    is_thread_already_started = True
                else:
                    print("thread already started")
            
            # rover_rotator_turn(90,-90)
            turning_received = turning_received + 1
        if(data == Data.FORWARD.value):
            print("in forward")
            rover_drive_forward(90, 2.0) 
        if(data == Data.RESET.value):
            global max_wing_motor_repeat

            max_wing_motor_repeat = 1000
            turning_received = 0
            breakLoop = True
            is_thread_already_started = False
            rover_stop()
            print("in reset")

 
def wss_WING_MOTOR (action = "", data = ""):

    action = str(action)
    data = str(data)

    if (action == Action.PUMP.value):
        if (data == Data.PUMP_ON.value):
            global max_wing_motor_repeat
            if max_wing_motor_repeat > 10:
                # wing_motor_activate(0.1)
                wing_motor_activate(0.5)
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
