# =================== LED Sensor Utility (ASC) (Read Thread) ===================
# Version: V1.0.23.0707    Date: 2023/07/07        Modify By: Max Chu
# Note: LED Sensor Utility (ASC)
#
# Release Note:
# V1.0.23.0707 2023/07/07 Max Chu
#   1. Change program title to 'LED Sensor Utility (ASC)'
#   2. Add save address combobox
# V1.0.23.0606 2023/06/06 Max Chu
#   1. Change the read command from 'get 01 all' to 'get 01 01 48'

# V1.0.23.0413 2023/04/13 Max Chu
#   1. First Release
# ==============================================================================
# -*- coding: UTF-8 -*-

import ATE
import datetime
import time
import threading

from dataclasses import asdict   # For dataclass
# =================================== Define ===================================
# ============================== Global  Variable ==============================
# ============================ ControlThread  Class ============================


class readThread(threading.Thread):
    def __init__(self) -> None:
        super(readThread, self).__init__()
        self.debug = True
        self.setName('ReadThread')
        self.start()
    # ------------------------ run -------------------------

    def run(self) -> None:
        while True:
            if ATE.sensorType == 0:
                endNo = 1
                ledNo = 8
            else:
                endNo = 1
                ledNo = 48
            if ATE.sensorComPort.isOpen == True:
                if ATE.continueRead == True or ATE.readOnce == True:
                    if ATE.sensorNo == 0:
                        # self.clear_sensor_table()
                        for i in range(endNo):
                            # cmd = 'get %02d all\r' % (i+1)
                            cmd = 'get %02d 01 %02d\r' % (ATE.slaveAddr, ledNo)
                            ATE.sensorComPort.send(cmd.encode())
                            if self.execute_command(ATE.sensorType, 3.0) == True:
                                for no, line in enumerate(self.readLines):
                                    if no == 0:
                                        continue
                                    if line == '':
                                        break
                                    values_str = line.split(' ')
                                    try:
                                        values = list(
                                            map(lambda x: int(x), values_str))
                                    except Exception:
                                        break
                                    for j in range(len(values)-1):
                                        self.display_sensor_table(
                                            ((no-1) % 4)*4+j+1, ((no-1)//4)+i*2, str(values[j+1]))
                                time.sleep(ATE.boardDelay)
                            else:
                                self.display_debug_message('Read Error!!', 2)
                                break
                    if ATE.readOnce == True:
                        ATE.readOnce = False
                    else:
                        time.sleep(ATE.interval)
            if ATE.TerminateProgram == True:
                break
            time.sleep(0.01)
    # -------------- display_debug_message()  --------------

    def execute_command(self, cmd: int, timeout: float = 2.0) -> bool:
        '''
        cmd: 0=read all(8), 1=read all(48)
        timeout: timeout
        '''
        last_check_time = time.time()
        while True:
            if time.time()-last_check_time > timeout:
                return False
            if ATE.sensorComPort.isOpen == True:
                self.readLines = ''
                if cmd == 1:
                    sensor_no = 48
                else:
                    sensor_no = 8
                index1 = ATE.sensorComPort.receiveBuffer.find(
                    '%03d ' % sensor_no)
                index2 = ATE.sensorComPort.receiveBuffer.find(
                    '\r\n', index1+1)
                if index1 != -1 and index2 != -1:
                    self.readLines = ATE.sensorComPort.receiveBuffer.split(
                        '\r\n')
                    self.display_debug_message(
                        ATE.sensorComPort.receiveBuffer, 0)
                    ATE.sensorComPort.receiveBuffer = ''
                    return True
            if ATE.TerminateProgram == True:
                return False
            time.sleep(0.01)

    # -------------- display_debug_message()  --------------

    def display_debug_message(self, msg: str, type: int = 0) -> None:
        '''
        type: 0=Normal Message, 1=Setup Message, 2=Error Message
        '''
        outMsg = datetime.datetime.now().strftime('%H:%M:%S ==> ')+msg
        if self.debug == True:
            if ATE is not None:
                ATE.Signals.display_sensor_message.emit(outMsg, type)
            print(outMsg)
    # --------------- display_sensor_table() ---------------

    def display_sensor_table(self, inputColumn: int, inputRow: int, data: str) -> None:
        ATE.Signals.display_sensor_table.emit(inputColumn, inputRow, data)

    # ---------------- clear_sensor_table() ----------------

    def clear_sensor_table(self) -> None:
        ATE.Signals.clear_sensor_table.emit()
     # ------------------------------------------------------

# ============================ initialThread Class  ============================


class initialThread(threading.Thread):
    def __init__(self) -> None:
        super(initialThread, self).__init__()
        self.setName('initialThread')
        self.start()
    # ------------------------ run -------------------------

    def run(self) -> None:
        time.sleep(2)
        self.changeToTestPage()
    # ----------------- changeToTestPage()  -----------------

    def changeToTestPage(self) -> None:
        if ATE is not None:
            ATE.Signals.change_to_test_page.emit()
# ==============================================================================
