# pumpUtils
Library of routines for controlling liquid dispensing pumps

Calibration is controlled via settings in the config.py file

runPump arguments are pump number and volume in mL


## Installation

### Raspberry PI Prep
1. Enable i2C in raspi-config



### Download pumpUtils
`git clone https://github.com/ionlabhouston/pumpUtils-Python.git`

`cd pumpUtils-Python`
`python3 -m venv env`

`source pumpUtils-Python/env/bin/activate.sh`

### Install dependencies
`pip3 install adafruit-motor-hat`

## Install pumpUtils
`cd pumpUtils-Python`

`python3 setup.py`


## Basic use

1. Open a command prompt window

2. Type in the following:

`python3`

`from pumpCtrl import control`

`control.runPump(0, 100)`
