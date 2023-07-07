# ========================== LED Sensor Calibartion Program ===========================
# Version: V1.0.23.0707    Date: 2023/07/07        Modify By: Max Chu
# Note: LED Sensor Calibartion Program
#
# Need install following packages:
#   1. PySide6-Essentials 6.4.1
# Install command:
#   # pip install pyside6            (For GUI, use Pyside6, when execute failed, please uninstall pyside6 and install pyside6-essentials)
#   $ pip install pyside6-essentials

# Convert .ui to .py:
#   $ uic -g python Main_GUI.ui -o Main_GUI.py
# Release Note:
# V1.0.23.0707 2023/07/07 Max Chu
#   1. Change program title to 'LED Sensor Utility (ASC)'
#   2. Add save address combobox

# V1.0.23.0606 2023/06/06 Max Chu
# 1. Change the read command from 'get 01 all' to 'get 01 01 48'

# V1.0.23.0421 2023/05/05 Max Chu
#   1. First Release
# ==============================================================================
# -*- coding: UTF-8 -*-
import sys
import ATE
import Main_GUI
from readThread import readThread, initialThread
from comPort import comPort
from PySide6.QtCore import (Qt, QObject, Slot, Signal)
from PySide6.QtGui import (
    QFont, QColor, QIcon, QTextCursor, QStandardItemModel, QStandardItem, QCursor, QPixmap)
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenu)
# =================================== Define ===================================
TITLE = ATE.RPOGRAM_TITLE+' Version '+ATE.PROGRAM_VERSION
ICON_FILENAME = 'LED.ico'
LOGO_FILENAME = 'accton_logo.png'
# ============================== Global Variable  ==============================
global MainWindowUI

MainWindowUI = None
# =================================== Class  ===================================
# ================================ Communicate  ================================
# Signals must inherit QObject


class Communicate(QObject):
    clear_message = Signal()
    clear_sensor_message = Signal()
    clear_sensor_table = Signal()
    display_message = Signal(str, int)
    display_sensor_message = Signal(str, int)
    display_sensor_table = Signal(int, int, str)
    change_to_test_page = Signal()
# ============================ Setup Signal & Slot  ============================
# ------------------------------ clear_message()  ------------------------------


@ Slot()
def clear_message():
    MainWindowUI.messageTextEdit1.clear()
# --------------------------- clear_sensor_message() ---------------------------


@ Slot()
def clear_sensor_message():
    MainWindowUI.messageTextEdit2.clear()

# ---------------------------- clear_sensor_table() ----------------------------


@ Slot()
def clear_sensor_table():
    for i in range(1, 17):
        for j in range(12):
            display_sensor_table(i, j, '')
# ----------------------------- display_message()  -----------------------------


@ Slot(str, int)
def display_message(data: str, type: int = 0) -> None:
    '''
    data: message
    type: 0=Normal Message, 1=Setup Message, 2=Error Message
    '''
    if type == 0:
        MainWindowUI.messageTextEdit1.setTextColor(QColor('black'))
    elif type == 1:
        MainWindowUI.messageTextEdit1.setTextColor(QColor('blue'))
    elif type == 2:
        MainWindowUI.messageTextEdit1.setTextColor(QColor('red'))
    MainWindowUI.messageTextEdit1.append(data)
    MainWindowUI.messageTextEdit1.moveCursor(QTextCursor.End)
# -------------------------- display_sensor_message() --------------------------


@ Slot(str, int)
def display_sensor_message(data: str, type: int = 0) -> None:
    '''
    data: message
    type: 0=Normal Message, 1=Setup Message, 2=Error Message
    '''
    if type == 0:
        MainWindowUI.messageTextEdit2.setTextColor(QColor('black'))
    elif type == 1:
        MainWindowUI.messageTextEdit2.setTextColor(QColor('blue'))
    elif type == 2:
        MainWindowUI.messageTextEdit2.setTextColor(QColor('red'))
    MainWindowUI.messageTextEdit2.append(data)
    MainWindowUI.messageTextEdit2.moveCursor(QTextCursor.End)
# --------------------------- display_sensor_table() ---------------------------


@ Slot(int, int, str)
def display_sensor_table(inputColumn: int, inputRow: int, data: str) -> None:
    font1 = QFont('Arial')
    font1.setBold(True)
    font1.setPointSize(10)
    item = QStandardItem()
    item.setData(data, Qt.DisplayRole)
    item.setTextAlignment(Qt.AlignCenter)
    item.setFont(font1)
    MainWindowUI.testItemModel.setItem(inputRow, inputColumn, item)

    if inputColumn == 0:
        item.setForeground(QColor('Black'))
        item.setBackground(QColor('#DCDCDC'))
    else:
        col = inputColumn-1

        if ((col//4) % 2) == 0:
            item.setBackground(QColor('#FFFFFF'))
        else:
            item.setBackground(QColor('#E0FFF4'))

        if (col % 4) == 0:
            item.setForeground(QColor('Red'))
        elif (col % 4) == 1:
            item.setForeground(QColor('Green'))
        elif (col % 4) == 2:
            item.setForeground(QColor('Blue'))
        else:
            item.setForeground(QColor('Black'))
# --------------------------- change_to_test_page()  ---------------------------


@ Slot()
def change_to_test_page():
    MainWindowUI.mainTabWidget.setCurrentIndex(0)
# ================================== Function ==================================
# --------------------------- sensorButtonOnClicked() ---------------------------


def sensorButtonOnClicked(self):
    result = False
    sensorComPort = ATE.comPortList[self.sensorComboBox1.currentIndex()]
    if self.sensorButton.text() == 'Open':
        clear_message()
        clear_sensor_message()
        clear_sensor_table()
        if ATE.sensorComPort.open(sensorComPort, 38400) == True:
            self.sensorButton.setText('Close')
            display_message('Open Sensor COM Port Success!!', 1)
        else:
            display_message('Open Sensor COM Port Fail!!', 2)
    else:
        if ATE.sensorComPort.isOpen == True:
            ATE.sensorComPort.close()
            self.sensorButton.setText('Open')
            display_message('Sensor Port Closed!!', 2)
# ------------------- readRGBButtonOnClicked() -------------------


def readRGBButtonOnClicked(self):
    ATE.readOnce = True
# --------------------- continuousCheckBoxOnStateChanged() ---------------------


def continuousCheckBoxOnStateChanged(self):
    ATE.continueRead = self.continuousCheckBox.isChecked()

# ------------------- controlComboBox1OncurrentTextChanged() -------------------


def controlComboBox1OnCurrentTextChanged(self):
    ATE.sensorNo = self.controlComboBox1.currentIndex()
# ------------------- sensorComboBox2OnCurrentTextChanged() -------------------


def sensorComboBox2OnCurrentTextChanged(self):
    ATE.sensorType = self.sensorComboBox2.currentIndex()
# ------------------- sensorComboBox2OnCurrentTextChanged() -------------------


def sensorComboBox3OnCurrentTextChanged(self):
    ATE.slaveAddr = self.sensorComboBox3.currentIndex()+1
# ------------------- controlComboBox2OnCurrentTextChanged() -------------------


def controlComboBox2OnCurrentTextChanged(self):
    ATE.boardDelay = (self.controlComboBox2.currentIndex()+1)*0.1
# ------------------- controlComboBox3OnCurrentTextChanged() -------------------


def controlComboBox3OnCurrentTextChanged(self):
    ATE.interval = (self.controlComboBox3.currentIndex()+1)*0.5

# ------------------------------ copyTableView()  ------------------------------


def copyTableView(self):
    try:
        indexes = self.selectedIndexes()  # 获取表格对象中被选中的数据索引列表
        indexes_dict = {}
        for index in indexes:  # 遍历每个单元格
            row, column = index.row(), index.column()  # 获取单元格的行号，列号
            if row in indexes_dict.keys():
                indexes_dict[row].append(column)
            else:
                indexes_dict[row] = [column]

        # 将数据表数据用制表符(\t)和换行符(\n)连接，使其可以复制到excel文件中
        text = ''
        for row, columns in indexes_dict.items():
            row_data = ''
            for column in columns:
                data = self.model().item(row, column).text()
                if row_data:
                    row_data = row_data + '\t' + data
                else:
                    row_data = data

            if text:
                text = text + '\n' + row_data
            else:
                text = row_data
    except BaseException as e:
        print(e)
        text = ''
    clipboard = QApplication.clipboard()
    clipboard.setText(text)
# ------------------------------ cTableView() ------------------------------


def pasteTableView(self):
    try:
        indexes = self.selectedIndexes()
        for index in indexes:
            index = index
            break
        r, c = index.row(), index.column()
        text = QApplication.clipboard().text()
        ls = text.split('\n')
        ls1 = []
        for row in ls:
            ls1.append(row.split('\t'))
        model = self.model()
        rows = len(ls)
        columns = len(ls1[0])
        for row in range(rows):
            for column in range(columns):
                item = QStandardItem()
                item.setText((str(ls1[row][column])))
                model.setItem(row + r, column + c, item)
    except Exception as e:
        print(e)
# ---------------------------- setup_main_window()  ----------------------------


def setup_main_window(self, window):
    self.aboutLabel1.setText(TITLE)
    logo_pixmap = QPixmap(ATE.img_resource_path(LOGO_FILENAME))
    self.logoLabel.setPixmap(logo_pixmap)
    self.mainTabWidget.setCurrentIndex(1)

    self.sensorComboBox1.addItems(ATE.comPortList)
    self.sensorComboBox2.addItems(ATE.sensorTypeList)
    self.sensorComboBox3.addItems(ATE.slaveAddrList)
    self.controlComboBox1.addItems(ATE.sensorList)
    self.controlComboBox2.addItems(ATE.delayTimeList)
    self.controlComboBox3.addItems(ATE.intervalList)

    self.controlComboBox1.setCurrentIndex(0)
    self.controlComboBox2.setCurrentIndex(0)
    self.controlComboBox3.setCurrentIndex(0)
    self.sensorComboBox1.setCurrentIndex(12)
    self.sensorComboBox2.setCurrentIndex(1)
    self.sensorComboBox3.setCurrentIndex(0)

    headerList = ['LED No']+[x for x in 'RGBIRGBIRGBIRGBI']
    font1 = QFont()
    font1.setFamily('Arial')
    font1.setBold(True)
    # font1.setPointSize(10)
    # font4.setWeight(50)
    self.testItemModel = QStandardItemModel(0, 16)
    self.testItemModel.setColumnCount(17)
    self.testItemModel.setRowCount(12)
    self.testItemModel.setHorizontalHeaderLabels(headerList)
    self.sensorTableView.setModel(self.testItemModel)
    self.sensorTableView.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
    self.sensorTableView.horizontalHeader().setStyleSheet(
        '::section {color: black; background-color: lightGray;}')
    self.sensorTableView.horizontalHeader().setFont(font1)
    for i in range(17):
        self.sensorTableView.setColumnWidth(i, 60)

    # 在TableView中增加Copy選單及功能
    self.sensorTableView.setContextMenuPolicy(Qt.CustomContextMenu)
    self.sensorTableView.customContextMenuRequested.connect(
        lambda: self.sensorTableView.contextMenu.exec(QCursor.pos()))
    self.sensorTableView.contextMenu = QMenu(self.sensorTableView)
    self.sensorTableView.COPY = self.sensorTableView.contextMenu.addAction(
        'Copy')
    self.sensorTableView.PASTE = self.sensorTableView.contextMenu.addAction(
        'Paste')
    self.sensorTableView.COPY.triggered.connect(
        lambda: copyTableView(self.sensorTableView))
    self.sensorTableView.PASTE.triggered.connect(
        lambda: pasteTableView(self.sensorTableView))

    # Initail table view
    for i in range(0, 17):
        for j in range(12):
            if i == 0:
                display_sensor_table(0, j, '%02d ~ %02d' %
                                     ((j*4+1), (j+1)*4))
            else:
                display_sensor_table(i, j, '')
    # --------------------- Set  Event ---------------------
    self.readRGBButton.clicked.connect(lambda: readRGBButtonOnClicked(self))
    self.sensorButton.clicked.connect(lambda: sensorButtonOnClicked(self))
    self.continuousCheckBox.stateChanged.connect(
        lambda: continuousCheckBoxOnStateChanged(self))
    self.controlComboBox1.currentTextChanged.connect(
        lambda: controlComboBox1OnCurrentTextChanged(self))
    self.sensorComboBox2.currentTextChanged.connect(
        lambda: sensorComboBox2OnCurrentTextChanged(self))
    self.sensorComboBox3.currentTextChanged.connect(
        lambda: sensorComboBox3OnCurrentTextChanged(self))
    self.controlComboBox2.currentTextChanged.connect(
        lambda: controlComboBox2OnCurrentTextChanged(self))
    self.controlComboBox3.currentTextChanged.connect(
        lambda: controlComboBox3OnCurrentTextChanged(self))

    ATE.sensorComPort = comPort()
    ATE.readThread = readThread()

    ATE.Signals = Communicate()
    ATE.Signals.clear_sensor_table.connect(clear_sensor_table)
    ATE.Signals.display_message.connect(display_message)
    ATE.Signals.display_sensor_message.connect(display_sensor_message)
    ATE.Signals.display_sensor_table.connect(display_sensor_table)
    ATE.Signals.change_to_test_page.connect(change_to_test_page)

    releaseNote = "LED Sensor Utility Version 1.0.23.0707\n"\
        "Copyright (C) 2023 Accton Technology Corporation.\n"\
        "http://www.accton.com.tw\n"\
        "All Rights Reserved.\n\n"\
        "Release Note:\n"\
        "V1.0.23.0707 2023/07/07 Max Chu\n"\
        "   1. Change program title to 'LED Sensor Utility (ASC)'\n"\
        "   2. Add save address combobox\n"\
        "   3. Add tabwidget\n\n"\
        "V1.0.23.0606 2023/06/06 Max Chu\n"\
        "   1. Change the read command from 'get 01 all' to 'get 01 01 48'\n\n"\
        "V1.0.23.0413 2023/04/13\n"\
        "   1. First Release\n\n"
    self.releasenoteTextEdit.setText(releaseNote)
    ATE.initialThread = initialThread()
# -------------------------------- closeWindow() --------------------------------


def closeWindow(self):
    ATE.TerminateProgram = True
# ==================================== Main ====================================


def Main():
    global MainWindowUI

    title = ATE.RPOGRAM_TITLE+' Version '+ATE.PROGRAM_VERSION
    app = QApplication(sys.argv)
    MainWindowGUI = QMainWindow()

    MainWindowUI = Main_GUI.Ui_MainWindow()
    MainWindowUI.setupUi(MainWindowGUI)
    MainWindowGUI.setWindowIcon(QIcon(ATE.icon_resource_path(ICON_FILENAME)))
    MainWindowGUI.setWindowTitle(title)
    setup_main_window(MainWindowUI, MainWindowGUI)
    app.aboutToQuit.connect(lambda: closeWindow(MainWindowUI))
    MainWindowGUI.show()

    sys.exit(app.exec())


# ================================== __name__ ==================================
if __name__ == "__main__":
    Main()
# ==============================================================================
