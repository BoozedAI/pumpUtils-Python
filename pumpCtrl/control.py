#!/usr/bin/python
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

import time
import atexit
import config

mh[] = ?

# create a default object, no changes to I2C address or frequency
for i in range(config.I2C_BASEADDR, config.PUMPS_NUMHATS):
    mh[i] = Adafruit_MotorHAT(addr=0x60, i)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    for i in range(config.PUMPS_NUM):
        stopPump(i)

atexit.register(turnOffMotors)

def getHAT(pnum):
    shield = config.PUMP(pnum)
    return mh[shield]

def calcRunTime(pnum, volume):
    rtime = volume/config.PUMP[pnum].MLPS
    return rtime

def stopPump(pnum):
    getHAT(pnum).run(Adafruit_MotorHAT.RELEASE)

def runPump(pnum, volume):
    myMotor = getHAT(pnum).getMotor(pnum)

    rtime = calcRunTime(pnum, volume)
    myMotor.setSpeed(config.PUMP[pnum].FLOW_RATE)
    myMotor.run(Adafruit_MotorHAT.FORWARD)
    time.sleep(rtime)

    # turn on motor
    myMotor.run(Adafruit_MotorHAT.RELEASE)
