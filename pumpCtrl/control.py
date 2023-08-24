#!/usr/bin/python
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

import time
import atexit
from pumpCtrl import config

mh = []

# create a default object, no changes to I2C address or frequency
for i in range(0, config.PUMPS_NUMHATS):
    haddr = 0x60 + i
    newmh = Adafruit_MotorHAT(addr=haddr, i2c_bus=config.I2C_BASEADDR) #busnum
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

def stopPump(pnum):
    getHAT(pnum).run(Adafruit_MotorHAT.RELEASE)

def runPump(pnum, volume):
    ndx = (pnum% 4)+1
    myMotor = getHAT(pnum).getMotor(ndx)

    rtime = calcRunTime(pnum, volume)
    myMotor.setSpeed(config.PUMP_CONFIG[pnum][config.PUMP_FLOW_RATE])
    myMotor.run(Adafruit_MotorHAT.FORWARD)
    time.sleep(rtime)

    # turn on motor
    myMotor.run(Adafruit_MotorHAT.RELEASE)
