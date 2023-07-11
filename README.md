# pumpUtils
Library of routines for controlling liquid dispensing pumps

Calibration is controlled via settings in the config.py file

#basic use:

python3
import pumpCtrl

runPump arguments pump number, volume in mL

control.runPump(0, 100)
