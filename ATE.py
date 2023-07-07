# -*- coding: UTF-8 -*-
import os
import sys
# ----------------------------------- Define -----------------------------------
RPOGRAM_TITLE = 'LED Sensor Utility (ASC) '
PROGRAM_VERSION = '1.0.23.0707'
SENSOR_NO = 48
# ------------------------------ Global Variable  ------------------------------
Signals = None
sensorComPort = None
modbusClient = None
readThread = None
initialThread = None
sensorNo = 0
sensorType = 1
slaveAddr = 1
boardDelay = 0.1
interval = 0.5
continueRead = False
readOnce = False
Debug = True
TerminateProgram = False
comPortList = ['COM%d' % x for x in range(1, 21)]
slaveAddrList = ['%d' % x for x in range(1, 63)]
sensorList = ['%d' % x for x in range(0, 49)]
sensorTypeList = ['8', '48']
delayTimeList = ['%0.1f' % (x*0.1) for x in range(1, 11)]
intervalList = ['%0.1f' % (x*0.5) for x in range(1, 11)]
# ---------------------------- icon_resource_path() ----------------------------


def icon_resource_path(relative_path):
    # Get absolute path to resource, works for dev and for PyInstaller
    newPath = os.path.join(os.getcwd(), '..', 'Icon', 'Icons')
    if not hasattr(sys, '_MEIPASS'):
        base_path = os.environ.get('_MEIPASS2', newPath)
    else:
        base_path = getattr(sys, '_MEIPASS', newPath)
    return os.path.join(base_path, relative_path)
# ---------------------------- img_resource_path()  ----------------------------


def img_resource_path(relative_path):
    # Get absolute path to resource, works for dev and for PyInstaller
    newPath = os.path.join(os.getcwd(), '..', 'Icon', 'IMG')
    if not hasattr(sys, '_MEIPASS'):
        base_path = os.environ.get('_MEIPASS2', newPath)
    else:
        base_path = getattr(sys, '_MEIPASS', newPath)
    return os.path.join(base_path, relative_path)
# ===============================================================================
