from adafruit_motorkit import MotorKit

import time
import atexit
from pumpCtrl import config

mh = []

# create a default object, no changes to I2C address or frequency
for i in range(0, config.PUMPS_NUMHATS):
    haddr = 0x60 + i
    newmh = MotorKit(address=haddr)
    mh.append(newmh)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    for i in range(config.PUMPS_NUM):
        stopPump(i)

atexit.register(turnOffMotors)

def getHAT(pnum):
    shield = config.PUMP_CONFIG[pnum][config.PUMP_HAT]
    return mh[shield]

def calcRunTime(pnum, volume):
    rtime = volume/config.PUMP_CONFIG[pnum][config.PUMP_MLPS]
    return rtime

def getMotor(pnum):
    ndx = (pnum% 4)+1
    if (ndx == 1):
        mtr = getHAT(pnum).motor1
    elif (ndx == 2):
        mtr = getHAT(pnum).motor2
    elif (ndx == 3):
        mtr = getHAT(pnum).motor3
    else:
        mtr = getHAT(pnum).motor4

    return mtr

def getDir(pnum):
    ndx = (pnum% 4)+1
    if (ndx == 1):
        dir = -1.0
    elif (ndx == 2):
        dir = 1.0
    elif (ndx == 3):
        dir = -1.0
    else:
        dir = 1.0

    return dir


def stopPump(pnum):
    myMotor = getMotor(pnum)
    # myMotor.run(Adafruit_MotorHAT.RELEASE)
    myMotor.throttle = 0.0

def runPump(pnum, volume):
    myMotor = getMotor(pnum)

    rtime = calcRunTime(pnum, volume)
    # myMotor.throttle(config.PUMP_CONFIG[pnum][config.PUMP_FLOW_RATE])
    # myMotor.run(Adafruit_MotorHAT.FORWARD)
    myMotor.throttle = getDir(pnum)
    time.sleep(rtime)

    # turn off motor
    # myMotor.run(Adafruit_MotorHAT.RELEASE)
    myMotor.throttle = 0.0
