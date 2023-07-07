# =================== Manufacturing Test Program (COM Port) ====================
# Version: V1.0.21.1027    Date: 2021/10/27        Modify By: Max Chu
# Note: Manufacturing Test Program(COM Port)
# Need install packages, the follow command must be executed in administrator mode
# $ pip3 install pyserial
#
# Release Note:
# V1.0.21.1027 2021/10/27 Max Chu
# 1. First Release
#
# ==============================================================================
# -*- coding: UTF-8 -*-

import serial
import serial.tools.list_ports
import threading
import time

import ATE
# ==============================================================================


class comPort():
    def __init__(self):
        self.comPort = None
        self.debug = True
        self.isOpen = False
        self.receiveBuffer = ''
    # -------------------------------------------------------

    def printDebugMsg(self, msg):
        if self.debug == True:
            print(msg)
    # -------------------------------------------------------

    def list(self):
        portList = list(serial.tools.list_ports.comports())
        if len(portList) == 0:
            errorStr = '無可用串列埠(No serial port available!!)'
            self.printDebugMsg(errorStr)
        else:
            for i in range(0, len(portList)):
                self.printDebugMsg(portList[i])
    # -------------------------------------------------------

    def open(self, com, baudrate, timeout=0.1):
        try:
            self.comPort = serial.Serial(
                port=com, baudrate=baudrate, timeout=timeout)
            self.comPort.flushInput()   # flush input buffer
            self.comPort.flushOutput()  # flush output buffer
            self.receiveBuffer = ''
            self.recvThread = threading .Thread(target=self.receive,
                              args=(self.comPort,))
            self.recvThread.setName('recvThread')
            self.recvThread.start()
            self.isOpen = True
            return True
        except Exception as e:
            self.printDebugMsg('Exception: %s' % e)
            self.isOpen = False
            return False
    # -------------------------------------------------------

    def close(self):
        if self.comPort != None:
            self.comPort.close()
            self.comPort = None
            self.isOpen = False
    # -------------------------------------------------------

    def send(self, senddata):
        #if self.comPort.isOpen()==True:
        if self.isOpen==True:
            self.comPort.write(senddata)
    # -------------------------------------------------------

    def receive(self, comPort):
        while True:
            try:
                if comPort.in_waiting > 0:
                    received = self.comPort.read(comPort.in_waiting).decode()
                    self.receiveBuffer += received
                    #self.printDebugMsg(received)
            except Exception:
                break
            if ATE.TerminateProgram == True:
                break
            time.sleep(0.01)
# ==============================================================================
