# pumpUtils
Library of routines for controlling liquid dispensing pumps

Calibration is controlled via settings in the config.py file

runPump arguments are pump number and volume in mL


## Installation

### Raspberry PI Prep
1. Enable i2C in raspi-config


### Install dependencies
`pip3 install adafruit-circuitpython-motor`

### Download pumpUtils
`git clone https://github.com/ionlabhouston/pumpUtils-Python.git`

### Install pumpUtils
`cd pumpUtils-Python`

`python3 setup.py`


## Basic use

1. Open a command prompt window

2. Type in the following:

`python3`

`from pumpCtrl import ccontrol`

`ccontrol.runPump(0, 100)`


## HTTP server

Start a lightweight server that the frontend can call:

`python3 -m pumpCtrl.server`

Endpoints:
- `GET /health` → returns `{ ok, controller }`
- `GET /run?p=<pumpIndex>&v=<ml>` → starts a dispense
- `GET /stop?p=<pumpIndex>` → stops a pump
- `POST /run` with JSON `{ "p": <pumpIndex>, "v": <ml> }`
- `POST /stop` with JSON `{ "p": <pumpIndex> }`

Default bind is `0.0.0.0:8080`. To customize, use:

```
python3 -c "from pumpCtrl.server import serve; serve(host='0.0.0.0', port=9090, auth_token='secret')"
```

Auth & CORS
- Optional bearer or `X-Auth-Token` required if `auth_token` is set.
- CORS enabled for `GET/POST` and preflight `OPTIONS`.
