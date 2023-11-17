import time
import atexit
from pumpCtrl import config

mh = []

# create a default object, no changes to I2C address or frequency
for i in range(0, config.PUMPS_NUMHATS):
    haddr = 0x60 + i
    newmh = MotorKit(addr=haddr, i2c_bus=config.I2C_BASEADDR) #busnum
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
    ndx = (pnum% 4)+1
    if (ndx == 1):
        myMotor = getHAT(pnum).motor1
    elif (ndx == 2):
        myMotor = getHAT(pnum).motor2
    elif (ndx == 3):
        myMotor = getHAT(pnum).motor3
    elif (ndx == 4):
        myMotor = getHAD(pnum).motor4
   
    myMotor.run(Adafruit_MotorHAT.RELEASE)

def runPump(pnum, volume):
    ndx = (pnum% 4)+1
    myMotor = getHAT(pnum).getMotor(ndx)

    rtime = calcRunTime(pnum, volume)
    myMotor.setSpeed(config.PUMP_CONFIG[pnum][config.PUMP_FLOW_RATE])
    myMotor.run(Adafruit_MotorHAT.FORWARD)
    time.sleep(rtime)

    # turn on motor
    myMotor.run(Adafruit_MotorHAT.RELEASE)
  
