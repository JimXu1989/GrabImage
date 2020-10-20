# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '2222.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate, QTime, QTimer, QThread, pyqtSignal, QObject
import sys
import threading
import cv2
import numpy as np
from PyQt5.QtGui import QImage, QPixmap
import os,os.path
from ctypes import *
sys.path.append("/opt/MVS/Samples/aarch64/Python/MvImport")
from MvCameraControl_class import *
import json
import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import manualui
import settingui
import keyboard2
import LedIndicatorWidget
import judge_result_txt0812
from os import listdir
import Jetson.GPIO as GPIO
import time
import RPi.GPIO as GPIO
from PCA9685 import PCA9685




# Pin Definitions:
#output pins
gpo1 = 37
gpo2 = 35
gpo3 = 33
gpo4 = 31
gpo5 = 29
gpo6 = 15
gpo7 = 13


#input pins
gpi_left_page = 32
gpi_grabimage = 36
gpi_right_page = 22


#reserved input pins
gpi_reserved_1 = 40
gpi_reserved_2 = 38



#reserved output pins
gpo_reserved_1 = 12
gpo_reserved_2 = 16
gpo_reserved_3 = 18


print_once_flag = 0
clickState = 0
firstTime = 0
secondTime = 0
program_step = 0
time_long_set = 0.5
time_long_long_set = 2
time_short_set = 0
timeEclipse = 0
clickFlag = 0
click_once =  0
falling_edge_flag = 0
rising_edge_flag = 0
cansel_flag = 0
ok_flag = 0


class mylineedit(QLineEdit):
  clicked=pyqtSignal()  #定义clicked信号
  def mouseReleaseEvent(self, QMouseEvent):
    if QMouseEvent.button()==Qt.LeftButton:
      self.clicked.emit()   #发送clicked信号

class Ui_MainWindow(QObject):
    def setupUi(self, MainWindow):
        # set IP
        addr = 'http://192.168.31.96:8888'
        # addr = 'http://192.168.43.47:8888'
        self.test_url = addr + '/api/test'
        content_type = 'image/jpeg'
        self.headers = {'content-type': content_type}
        self.imgNum = 0
        self.statement = ''
        # self.imgNames = listdir('image/laserImage')
        self.clientImID = int(round(time.time() * 1000))
        self.resDict = {}
        self.imgHeight = 1024
        self.imgWidth = 1280
        self.laserImg = np.zeros((self.imgHeight, self.imgWidth))
        self.inferredImg = np.zeros((self.imgHeight, self.imgWidth))
        self.nolightImg = np.zeros((self.imgHeight, self.imgWidth))

        #查看图片是否正常采集
        self.laser_img_got = 0
        self.inferred_img_got = 0
        self.nolight_img_got = 0

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.laser_trigger = 0
        self.inferred_trigger = 0
        self.nolight_trigger = 0
        self.laser_exposure = 2000.0
        self.inferred_exposure = 500.0
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.img_win = QtWidgets.QLabel(self.centralwidget)
        self.img_win.setGeometry(QtCore.QRect(10, 10, 600, 480))
        self.img_win.setText("")
        self.img_win.setPixmap(QtGui.QPixmap("black.png"))
        self.img_win.setScaledContents(True)
        self.img_win.setObjectName("label")
        self.settingButton = QtWidgets.QPushButton(self.centralwidget)
        self.settingButton.setGeometry(QtCore.QRect(660, 410, 111, 61))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.settingButton.setFont(font)
        self.settingButton.setObjectName("settingButton")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(23, 520, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(160, 520, 500, 31))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(640, 20, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(660, 60, 91, 21))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.manualButton = QtWidgets.QPushButton(self.centralwidget)
        self.manualButton.setGeometry(QtCore.QRect(660, 330, 111, 71))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.manualButton.setFont(font)
        self.manualButton.setObjectName("manualButton")
        self.confirmButton = QtWidgets.QPushButton(self.centralwidget)
        self.confirmButton.setGeometry(QtCore.QRect(630, 120, 61, 61))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.confirmButton.setFont(font)
        self.confirmButton.setObjectName("confirmButton")
        self.confirmButton.setVisible(False)
        self.cancelButton = QtWidgets.QPushButton(self.centralwidget)
        self.cancelButton.setGeometry(QtCore.QRect(720, 120, 61, 61))
        self.cancelButton.setVisible(False)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.cancelButton.setFont(font)
        self.cancelButton.setObjectName("cancelButton")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(650, 220, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")

        self.exitButton = QtWidgets.QPushButton(self.centralwidget)
        self.exitButton.setGeometry(QtCore.QRect(660, 480, 111, 61))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.exitButton.setFont(font)
        self.exitButton.setObjectName("exitButton")

        # 测试用##############################
        self.capButton = QtWidgets.QPushButton(self.centralwidget)
        self.capButton.setGeometry(QtCore.QRect(550, 510, 91, 41))
        self.capButton.setObjectName("capButton")
        self.initCamButton = QtWidgets.QPushButton(self.centralwidget)
        self.initCamButton.setGeometry(QtCore.QRect(280, 510, 121, 41))
        self.initCamButton.setObjectName("initCamButton")
        self.initCamButton.setVisible(False)
        self.stopCamButton = QtWidgets.QPushButton(self.centralwidget)
        self.stopCamButton.setGeometry(QtCore.QRect(410, 510, 121, 41))
        self.stopCamButton.setObjectName("stopCamButton")
        self.stopCamButton.setVisible(False)
        #####################################


        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.led = LedIndicatorWidget.LedIndicator(self.centralwidget)
        self.led.setDisabled(True)
        self.led.setGeometry(QtCore.QRect(690, 270, 31, 31))

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setWindowFlags(Qt.FramelessWindowHint)
        self.exitButton.clicked.connect(MainWindow.close)
        self.manualButton.clicked.connect(self.showManualUI)
        self.settingButton.clicked.connect(self.showSettingUI)
        #打开/关闭相机
        self.initCamButton.clicked.connect(self.get_real_time_img)
        self.stopCamButton.clicked.connect(self.stop_cam)

       

        self.settingButton.setDisabled(True)
        self.stopCamButton.setDisabled(True)

        self.resized = cv2.imread('/opt/MVS/Samples/aarch64/Python/GrabImage/black.png')
        height, width, bytesPerComponent = self.resized.shape
        bytesPerLine = bytesPerComponent * width

        if (bytesPerComponent == 3):
            self.QImg2 = QImage(self.resized.data, width, height, bytesPerLine,
                                QImage.Format_RGB888)
        else:
            self.QImg2 = QImage(self.resized.data, width, height, bytesPerLine,
                                QImage.Format_Grayscale8)

        if (bytesPerComponent == 3):
            self.QImg2 = QImage(self.resized.data, width, height, bytesPerLine,
                                QImage.Format_RGB888).rgbSwapped()
        self.pixmap = QtGui.QPixmap.fromImage(self.QImg2)

        self.confirmButton.clicked.connect(self.confirm_result)
        self.cancelButton.clicked.connect(self.cancel_result)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_realtime_label)
        self.timer.start(50)

        self.timer2 = QTimer()
        self.timer2.timeout.connect(self.test_connection)
        self.timer2.start(50)
        
        self.signal_send_imgs.connect(self.send_conbine_img)
        self.signal_cancel_result.connect(self.cancel_result)
        self.signal_confirm_result.connect(self.confirm_result)
        self.signal_cap_laserimg.connect(self.trigger_laser_img)
        self.signal_cap_nolightimg.connect(self.trigger_nolight_img)
        self.signal_cap_inferredimg.connect(self.trigger_inferred_img)
        self.get_real_time_img()
        # self.img_win.setVisible(False)

        # self.GPIOThreadHandle = threading.Thread(target=self.GPIO_main)
        # self.GPIOThreadHandle.setDaemon(True)
        # self.GPIOThreadHandle.start()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.settingButton.setText(_translate("MainWindow", "设置"))
        self.label_2.setText(_translate("MainWindow", "设备状态:"))
        self.label_3.setText(_translate("MainWindow", " "))
        self.label_4.setText(_translate("MainWindow", "检尺径："))
        self.label_5.setText(_translate("MainWindow", "00.00"))
        self.manualButton.setText(_translate("MainWindow", "人工"))
        self.confirmButton.setText(_translate("MainWindow", "确认"))
        self.cancelButton.setText(_translate("MainWindow", "取消"))
        self.label_6.setText(_translate("MainWindow", "连接状态："))
        # self.pushButton_test.setText(_translate("MainWindow", "PushButton"))
        self.exitButton.setText(_translate("MainWindow", "退出"))

        #测试用####################################################
        self.capButton.setText(_translate("MainWindow", "拍照（测试）"))
        self.capButton.setVisible(False)
        self.initCamButton.setText(_translate("MainWindow", "打开相机（测试）"))
        self.stopCamButton.setText(_translate("MainWindow", "关闭相机（测试）"))

    def showManualUI(self):
        self.ManualUIForm = QtWidgets.QWidget()
        self.manualui = manualui.Ui_Form()
        self.manualui.setupUi(self.ManualUIForm)
        self.manualui.sendButton.clicked.connect(self.sendManualResult)
        self.manualui.measureResultlineEdit.clicked.connect(self.showKeyboardUI)
        self.showKeyboardUI()
        # self.manualui.measureResultlineEdit.clicked.connect(MainWindow.close)
        self.ManualUIForm.show()

    def sendManualResult(self):
        self.ManualUIForm.close()
        self.resDictBack = {}
        self.resDictBack['GaugeMode'] = 2
        self.resDictBack['ImageID'] = self.clientImID
        self.resDictBack['Diameter'] = self.manualui.measureResultlineEdit.text()
        self.resDictBack['LongDiameter'] = 0
        self.resDictBack['SlopeAngle'] = 0
        self.resDictBack['SensorDist'] = 0
        self.timer.start(50)
        self.sendback_result()
        if (self.feedbackResponse.text == '"feed back result got"'):
            self.label_3.setText("手动输入成功")
        else:
            a = 777

    def showSettingUI(self):
        self.SettingUIForm = QtWidgets.QWidget()
        self.settingui = settingui.Ui_Form()
        self.settingui.setupUi(self.SettingUIForm)
        self.settingui.laserExposurelineEdit.setText(str(self.laser_exposure))
        self.settingui.inferredExposurelineEdit.setText(str(self.inferred_exposure))
        self.settingui.confirmButton.clicked.connect(self.confirm_setting)
        self.settingui.laserExposurelineEdit.clicked.connect(self.showKeyboardUI2)
        self.settingui.inferredExposurelineEdit.clicked.connect(self.showKeyboardUI3)
        self.SettingUIForm.show()

    def showKeyboardUI(self):
        self.keyboardUIForm = QtWidgets.QWidget()
        self.keyboard2 = keyboard2.Example()
        self.keyboard2.enterBtn.clicked.connect(self.keyboardSendText)
        # self.keyboard2.initUI()
        self.keyboard2.show()

    def keyboardSendText(self):
        sender = self.keyboard2.sender()
        if sender.text() == "Enter":
            temp = self.keyboard2.display.text()
            self.manualui.measureResultlineEdit.setText(temp)
        self.keyboard2.close()

    def showKeyboardUI2(self):
        self.keyboardUIForm = QtWidgets.QWidget()
        self.keyboard2 = keyboard2.Example()
        self.keyboard2.enterBtn.clicked.connect(self.keyboardSendText2)
        # self.keyboard2.initUI()
        self.keyboard2.show()

    def keyboardSendText2(self):
        sender = self.keyboard2.sender()
        if sender.text() == "Enter":
            temp = self.keyboard2.display.text()
            self.settingui.laserExposurelineEdit.setText(temp)
        self.keyboard2.close()

    def showKeyboardUI3(self):
        self.keyboardUIForm = QtWidgets.QWidget()
        self.keyboard2 = keyboard2.Example()
        self.keyboard2.enterBtn.clicked.connect(self.keyboardSendText3)
        # self.keyboard2.initUI()
        self.keyboard2.show()

    def keyboardSendText3(self):
        sender = self.keyboard2.sender()
        if sender.text() == "Enter":
            temp = self.keyboard2.display.text()
            self.settingui.inferredExposurelineEdit.setText(temp)
        self.keyboard2.close()

    def set_exposure(self):
        exposureVal = float(self.exposureLineEdit.text())
        ret = self.cam.MV_CC_SetFloatValue('ExposureTime', exposureVal)

    def set_laser_exposure(self):
        exposureVal = float(self.exposureLineEdit.text())
        ret = self.cam.MV_CC_SetFloatValue('ExposureTime', exposureVal)

    def get_real_time_img(self):
        self.deviceList = MV_CC_DEVICE_INFO_LIST()
        self.tlayerType = MV_GIGE_DEVICE | MV_USB_DEVICE

        # ch:枚举设备 | en:Enum device
        ret = MvCamera.MV_CC_EnumDevices(self.tlayerType, self.deviceList)
        if ret != 0:
            print("enum devices fail! ret[0x%x]" % ret)
            sys.exit()

        if self.deviceList.nDeviceNum == 0:
            print("find no device!")
            sys.exit()
        self.initCamButton.setDisabled(True)
        self.settingButton.setDisabled(False)
        self.stopCamButton.setDisabled(False)
        print("Find %d devices!" % self.deviceList.nDeviceNum)

        for i in range(0, self.deviceList.nDeviceNum):
            mvcc_dev_info = cast(self.deviceList.pDeviceInfo[i], POINTER(MV_CC_DEVICE_INFO)).contents
            if mvcc_dev_info.nTLayerType == MV_GIGE_DEVICE:
                print("\ngige device: [%d]" % i)
                strModeName = ""
                for per in mvcc_dev_info.SpecialInfo.stGigEInfo.chModelName:
                    strModeName = strModeName + chr(per)
                print("device model name: %s" % strModeName)

                nip1 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0xff000000) >> 24)
                nip2 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x00ff0000) >> 16)
                nip3 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x0000ff00) >> 8)
                nip4 = (mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x000000ff)
                print("current ip: %d.%d.%d.%d\n" % (nip1, nip2, nip3, nip4))
            elif mvcc_dev_info.nTLayerType == MV_USB_DEVICE:
                print("\nu3v device: [%d]" % i)
                strModeName = ""
                for per in mvcc_dev_info.SpecialInfo.stUsb3VInfo.chModelName:
                    if per == 0:
                        break
                    strModeName = strModeName + chr(per)
                print("device model name: %s" % strModeName)

                strSerialNumber = ""
                for per in mvcc_dev_info.SpecialInfo.stUsb3VInfo.chSerialNumber:
                    if per == 0:
                        break
                    strSerialNumber = strSerialNumber + chr(per)
                    self.cameraID = strSerialNumber
                print("user serial number: %s" % strSerialNumber)

        # nConnectionNum = input("please input the number of the device to connect:")
        nConnectionNum = 0
        if int(nConnectionNum) >= self.deviceList.nDeviceNum:
            print("intput error!")
            sys.exit()

        # ch:创建相机实例 | en:Creat Camera Object
        self.cam = MvCamera()

        # ch:选择设备并创建句柄 | en:Select device and create handle
        self.stDeviceList = cast(self.deviceList.pDeviceInfo[int(nConnectionNum)], POINTER(MV_CC_DEVICE_INFO)).contents

        ret = self.cam.MV_CC_CreateHandle(self.stDeviceList)
        if ret != 0:
            print("create handle fail! ret[0x%x]" % ret)
            sys.exit()

        # ch:打开设备 | en:Open device
        ret = self.cam.MV_CC_OpenDevice(MV_ACCESS_Exclusive, 0)
        if ret != 0:
            print("open device fail! ret[0x%x]" % ret)
            sys.exit()

        # ch:探测网络最佳包大小(只对GigE相机有效) | en:Detection network optimal package size(It only works for the GigE camera)
        if self.stDeviceList.nTLayerType == MV_GIGE_DEVICE:
            nPacketSize = self.cam.MV_CC_GetOptimalPacketSize()
            if int(nPacketSize) > 0:
                ret = self.cam.MV_CC_SetIntValue("GevSCPSPacketSize", nPacketSize)
                if ret != 0:
                    print("Warning: Set Packet Size fail! ret[0x%x]" % ret)
            else:
                print("Warning: Get Packet Size fail! ret[0x%x]" % nPacketSize)

        # ch:设置触发模式为off | en:Set trigger mode as off
        ret = self.cam.MV_CC_SetEnumValue("TriggerMode", MV_TRIGGER_MODE_OFF)
        if ret != 0:
            print("set trigger mode fail! ret[0x%x]" % ret)
            sys.exit()

        # ch:获取数据包大小 | en:Get payload size
        stParam = MVCC_INTVALUE()
        memset(byref(stParam), 0, sizeof(MVCC_INTVALUE))

        ret = self.cam.MV_CC_GetIntValue("PayloadSize", stParam)
        # 设置曝光测试
        rrr = self.cam.MV_CC_SetEnumValue('ExposureAuto', MV_EXPOSURE_AUTO_MODE_OFF)
       

        if ret != 0:
            print("get payload size fail! ret[0x%x]" % ret)
            sys.exit()
        self.nPayloadSize = stParam.nCurValue

        # ch:开始取流 | en:Start grab image
        ret = self.cam.MV_CC_StartGrabbing()
        if ret != 0:
            print("start grabbing fail! ret[0x%x]" % ret)
            sys.exit()

        self.data_buf = (c_ubyte * self.nPayloadSize)()

        try:
            self.hThreadHandle = threading.Thread(target=self.work_thread,
                                                  args=(self.cam, byref(self.data_buf), self.nPayloadSize))
            self.hThreadHandle.setDaemon(True)
            self.hThreadHandle.start()

            self.gpioThreadHandle = threading.Thread(target=self.GPIO_main,
                                                  )
            self.gpioThreadHandle.setDaemon(True)
            self.gpioThreadHandle.start()

        except:
            print("error: unable to start thread")

    # 关闭相机
    def stop_cam(self):
        self.flag = False
        print("press a key to stop grabbing.")
        # msvcrt.getch()

        g_bExit = True
        self.hThreadHandle.join()

        # ch:停止取流 | en:Stop grab image
        ret = self.cam.MV_CC_StopGrabbing()
        if ret != 0:
            print("stop grabbing fail! ret[0x%x]" % ret)
            del self.data_buf
            sys.exit()

        # ch:关闭设备 | Close device
        ret = self.cam.MV_CC_CloseDevice()
        if ret != 0:
            print("close deivce fail! ret[0x%x]" % ret)
            del self.data_buf
            sys.exit()

        # ch:销毁句柄 | Destroy handle
        ret = self.cam.MV_CC_DestroyHandle()
        if ret != 0:
            print("destroy handle fail! ret[0x%x]" % ret)
            del self.data_buf
            sys.exit()

        del self.data_buf
        self.initCamButton.setEnabled(True)
        self.stopCamButton.setDisabled(True)
        self.settingButton.setDisabled(True)


    # 为线程定义一个函数
    def work_thread(self, cam=0, pData=0, nDataSize=0):
        self.stDeviceList = MV_FRAME_OUT_INFO_EX()
        memset(byref(self.stDeviceList), 0, sizeof(self.stDeviceList))
        self.flag = True
        while self.flag:
            # 首先设置曝光
            if (self.laser_trigger):
                current_expo = c_float()
                # self.clientImID = int(round(time.time() * 1000))
                ret = self.cam.MV_CC_GetFloatValue('ExposureTime', current_expo)
                if(current_expo.value != self.laser_exposure):
                    ret = self.cam.MV_CC_SetFloatValue('ExposureTime', self.laser_exposure)

            if (self.inferred_trigger):
                current_expo = c_float()
                ret = self.cam.MV_CC_GetFloatValue('ExposureTime', current_expo)
                if(current_expo.value != self.inferred_exposure):
                    ret = self.cam.MV_CC_SetFloatValue('ExposureTime', self.inferred_exposure)

            if (self.nolight_trigger):
                current_expo = c_float()
                ret = self.cam.MV_CC_GetFloatValue('ExposureTime', current_expo)
                if(current_expo.value != self.laser_exposure):
                    ret = self.cam.MV_CC_SetFloatValue('ExposureTime', self.inferred_exposure)

            aa = self.cam
            ret = cam.MV_CC_GetOneFrameTimeout(byref(self.data_buf), self.nPayloadSize, self.stDeviceList, 1000)
            if ret == 0:
                #
                # print("get one frame: Width[%d], Height[%d], nFrameNum[%d]" % (
                #     self.stDeviceList.nWidth, self.stDeviceList.nHeight, self.stDeviceList.nFrameNum))

                nRGBSize = self.stDeviceList.nWidth * self.stDeviceList.nHeight * 3
                stConvertParam = MV_CC_PIXEL_CONVERT_PARAM()
                memset(byref(stConvertParam), 0, sizeof(stConvertParam))
                stConvertParam.nWidth = self.stDeviceList.nWidth
                stConvertParam.nHeight = self.stDeviceList.nHeight
                stConvertParam.pSrcData = self.data_buf
                stConvertParam.nSrcDataLen = self.stDeviceList.nFrameLen
                stConvertParam.enSrcPixelType = self.stDeviceList.enPixelType
                stConvertParam.enDstPixelType = PixelType_Gvsp_RGB8_Packed
                stConvertParam.pDstBuffer = (c_ubyte * nRGBSize)()
                stConvertParam.nDstBufferSize = nRGBSize

                ret = self.cam.MV_CC_ConvertPixelType(stConvertParam)
                if ret != 0:
                    print("convert pixel fail! ret[0x%x]" % ret)
                    del self.data_buf
                    sys.exit()
                

                try:
                    self.img_buff = (c_ubyte * stConvertParam.nDstLen)()
                    memmove(byref(self.img_buff), stConvertParam.pDstBuffer, stConvertParam.nDstLen)
                    aa = np.frombuffer(self.img_buff, dtype=np.uint8, count=-1, offset=0)
                    b = np.max(aa)
                    c = np.min(aa)
                    self.resized = aa.reshape((stConvertParam.nHeight, stConvertParam.nWidth, 3))
                    height, width, bytesPerComponent = self.resized.shape
                    bytesPerLine = bytesPerComponent * width

                                       
                    
                    if (bytesPerComponent == 3):
                        self.QImg2 = QImage(self.resized.data, width, height, bytesPerLine,
                                            QImage.Format_RGB888).rgbSwapped()
                    else:
                        self.QImg2 = QImage(self.resized.data, width, height, bytesPerLine,
                                            QImage.Format_Grayscale8)

                    self.pixmap = QtGui.QPixmap.fromImage(self.QImg2)

                    # self.real_time_img_win.setPixmap(self.pixmap)

                except:
                    raise Exception("save file executed failed:%s" % e.message)


            else:
                print("get one frame fail, ret[0x%x]" % ret)

            # print("convert pixeltype succeed!")

    def update_realtime_label(self):
        self.img_win.setPixmap(self.pixmap)


    def send_conbine_img(self):
        self.capButton.setDisabled(True)
        # self.laserImg = cv2.imread('image/laserImage/' + self.imgNames[(self.imgNum % len(self.imgNames))])
        # self.inferredImg = cv2.imread('image/grayImage/' + self.imgNames[(self.imgNum % len(self.imgNames))])
        # self.nolightImg = cv2.imread('image/backImage/' + self.imgNames[(self.imgNum % len(self.imgNames))])
        self.sendImg = np.hstack((self.laserImg,self.inferredImg,self.nolightImg))
        self.imgNum += 1
        # prepare headers for http request
        content_type = 'image/jpeg'
        headers = {'content-type': content_type}
        # capture = cv2.VideoCapture(0)
        # ret, frame = capture.read()
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

        # encode image as jpeg
        _, img_encoded = cv2.imencode('.jpg', self.sendImg, encode_param)
        # send http request with image and receive response
        response = requests.post(self.test_url, data=img_encoded.tostring()+str(self.clientImID).encode('utf-8'), headers=self.headers)
        self.resDict = eval(response.text)
        ContourPointX = list(map(int, self.resDict['ContourPointX'].split(',')))
        ContourPointY = list(map(int, self.resDict['ContourPointY'].split(',')))
        cr = np.vstack((ContourPointX, ContourPointY))
        crt = (cr.T).astype(np.int32)
        crt = np.expand_dims(crt, axis=1)
        height, width  = self.inferredImg.shape
        self.timer.stop()
        clone = cv2.cvtColor(self.inferredImg, cv2.COLOR_GRAY2RGB)
               
        bytesPerLine = width
        cv2.drawContours(clone, [crt], -1, (0, 255, 0), 2)

        TarBoxPts = list(map(int, self.resDict['TarBoxPts'].split(',')))
        clone = cv2.rectangle(clone, (TarBoxPts[0],TarBoxPts[1]), (TarBoxPts[2],TarBoxPts[3]), [0,0,255], 2)

        AimBoxXcnt = list(map(int, self.resDict['AimBoxXcnt'].split(',')))
        AimBoxYcnt = list(map(int, self.resDict['AimBoxYcnt'].split(',')))
        AimBoxPts = np.array([AimBoxXcnt,AimBoxYcnt],dtype=np.int32).T
        clone = cv2.polylines(clone, pts=[AimBoxPts], isClosed=True, color=[255,0,0], thickness=2)
        self.img_win.setVisible(True)

        
        # self.timer.start(50)
        self.QImg2 = QImage(clone.data, width, height, 1280*3,
                            QImage.Format_RGB888).rgbSwapped()
        
        self.pixmap = QtGui.QPixmap.fromImage(self.QImg2)
        self.img_win.setPixmap(self.pixmap)
        self.label_5.setText(self.resDict['Diameter'])
        aaa = judge_result_txt0812.check_resDict(self.clientImID, self.resDict)
        self.statement = aaa[0]
        self.label_3.setText(aaa[0])
        folderPath = 'result'
        if (not (os.path.exists(folderPath))):
            os.makedirs(folderPath)
        cv2.imwrite(folderPath + '/' + str(self.clientImID) + '.png', clone)
        
        print(json.loads(response.text))


    def test_connection(self):
        try:
            senddata = {}
            senddata['TimeID'] = int(round(time.time() * 1000))
            senddata['cameraID'] = self.cameraID
            response = requests.post(self.test_url, data=str(senddata).encode('utf-8'), headers=self.headers)
            self.connect_test_res = response.text
            self.led.setChecked(True)
        except:
            self.led.setChecked(False)


    def confirm_setting(self):
        self.laser_exposure = float(self.settingui.laserExposurelineEdit.text())
        self.inferred_exposure = float(self.settingui.inferredExposurelineEdit.text())
        ret = self.cam.MV_CC_SetFloatValue('ExposureTime', self.laser_exposure)

        # 得到相机的曝光###############################
        # fuck = c_float()
        # s = time.time()
        # ret = self.cam.MV_CC_GetFloatValue('ExposureTime', fuck)
        # ffuck = fuck.value
        # s2 = time.time()
        # s3 = s2-s
        # print('get expo time:'+str(s3*1000))
        # a = 1
        # bb = time.time()
        # ret = self.cam.MV_CC_SetFloatValue('ExposureTime', self.laser_exposure)
        # cc = time.time()
        # s6 = cc-bb
        # print('set expo time:' + str(s6 * 1000))
        ############################################################
        self.SettingUIForm.close()

    def sendback_result(self):
        self.feedbackResponse = ""
        try:
            response = requests.post(self.test_url, data=str(self.resDictBack).encode('utf-8'), headers=self.headers)
            self.feedbackResponse = response
        except:
            self.led.setDisabled(True)

    def confirm_result(self):
        self.capButton.setDisabled(False)
        self.resDictBack = {}
        # self.resDictBack['cameraID'] = self.cameraID
        self.resDictBack['GaugeMode'] = 1
        self.resDictBack['ImageID'] = self.clientImID
        self.resDictBack['Diameter'] = self.resDict['Diameter']
        self.resDictBack['LongDiameter'] = self.resDict['LongDiameter']
        self.resDictBack['SlopeAngle'] = self.resDict['SlopeAngle']
        self.resDictBack['SensorDist'] = self.resDict['SensorDist']
        self.resDictBack['Statement'] = self.statement
        self.timer.start(50)
        # realtime_update_flag = True
        self.sendback_result()
        if (self.feedbackResponse.text == '"feed back result got"'):
            self.label_3.setText('确认成功')

    def cancel_result(self):
        self.capButton.setDisabled(False)
        self.resDictBack = {}
        self.resDictBack['GaugeMode'] = 0
        self.resDictBack['ImageID'] = self.clientImID
        self.resDictBack['Diameter'] = 0
        self.resDictBack['LongDiameter'] = 0
        self.resDictBack['SlopeAngle'] = 0
        self.resDictBack['SensorDist'] = 0
        # realtime_update_flag = True
        self.timer.start(50)
        self.sendback_result()
        if (self.feedbackResponse.text == '"feed back result got"'):
            self.label_3.setText('取消成功')

    def showData(self):
        print('ok')




    def trigger_laser_img(self):
        current_expo = c_float()
        self.clientImID = int(round(time.time() * 1000))
        ret = self.cam.MV_CC_GetFloatValue('ExposureTime', current_expo)
        if (current_expo.value != self.laser_exposure):
            ret = self.cam.MV_CC_SetFloatValue('ExposureTime', self.laser_exposure)
        self.laser_trigger = 1
        # self.clientImID = int(round(time.time() * 1000))
        self.inferred_trigger = 0
        self.nolight_trigger = 0
        self.cam_get_one_frame()
        self.laserImg = self.resized[:,:,0]
        folderPath = 'laser'
        if (not (os.path.exists(folderPath))):
            os.makedirs(folderPath)
        cv2.imwrite(folderPath + '/' + str(self.clientImID) + '.png', self.resized)

    def trigger_inferred_img(self):
        current_expo = c_float()
        ret = self.cam.MV_CC_GetFloatValue('ExposureTime', current_expo)
        if (current_expo.value != self.inferred_exposure):
            ret = self.cam.MV_CC_SetFloatValue('ExposureTime', self.inferred_exposure)
        self.laser_trigger = 0
        self.inferred_trigger = 1
        self.nolight_trigger = 0
        self.cam_get_one_frame()
        self.inferredImg = self.resized[:,:,0]
        folderPath = 'inferred'
        if (not (os.path.exists(folderPath))):
            os.makedirs(folderPath)
        cv2.imwrite(folderPath + '/' + str(self.clientImID) + '.png', self.resized)

    def trigger_nolight_img(self):
        current_expo = c_float()
        # self.clientImID = int(round(time.time() * 1000))
        ret = self.cam.MV_CC_GetFloatValue('ExposureTime', current_expo)
        if (current_expo.value != self.laser_exposure):
            ret = self.cam.MV_CC_SetFloatValue('ExposureTime', self.laser_exposure)
        self.laser_trigger = 0
        self.inferred_trigger = 0
        self.nolight_trigger = 1
        self.cam_get_one_frame()
        self.nolightImg = self.resized[:,:,0]
        folderPath = 'nolight'
        if (not (os.path.exists(folderPath))):
            os.makedirs(folderPath)
        cv2.imwrite(folderPath + '/' + str(self.clientImID) + '.png', self.resized)

    def cam_get_one_frame(self,cam=0):
        ret = self.cam.MV_CC_GetOneFrameTimeout(byref(self.data_buf), self.nPayloadSize, self.stDeviceList, 1000)
        if ret == 0:
            #
            # print("get one frame: Width[%d], Height[%d], nFrameNum[%d]" % (
            #     self.stDeviceList.nWidth, self.stDeviceList.nHeight, self.stDeviceList.nFrameNum))

            nRGBSize = self.stDeviceList.nWidth * self.stDeviceList.nHeight * 3
            stConvertParam = MV_CC_PIXEL_CONVERT_PARAM()
            memset(byref(stConvertParam), 0, sizeof(stConvertParam))
            stConvertParam.nWidth = self.stDeviceList.nWidth
            stConvertParam.nHeight = self.stDeviceList.nHeight
            stConvertParam.pSrcData = self.data_buf
            stConvertParam.nSrcDataLen = self.stDeviceList.nFrameLen
            stConvertParam.enSrcPixelType = self.stDeviceList.enPixelType
            stConvertParam.enDstPixelType = PixelType_Gvsp_RGB8_Packed
            stConvertParam.pDstBuffer = (c_ubyte * nRGBSize)()
            stConvertParam.nDstBufferSize = nRGBSize

            ret = self.cam.MV_CC_ConvertPixelType(stConvertParam)
            if ret != 0:
                print("convert pixel fail! ret[0x%x]" % ret)
                del self.data_buf
                sys.exit()

            try:
                self.img_buff = (c_ubyte * stConvertParam.nDstLen)()
                memmove(byref(self.img_buff), stConvertParam.pDstBuffer, stConvertParam.nDstLen)
                aa = np.frombuffer(self.img_buff, dtype=np.uint8, count=-1, offset=0)
                b = np.max(aa)
                c = np.min(aa)
                self.resized = aa.reshape((stConvertParam.nHeight, stConvertParam.nWidth, 3))
                height, width, bytesPerComponent = self.resized.shape
            except:
                raise Exception("save file executed failed:%s" % e.message)

    signal_send_imgs = pyqtSignal()
    signal_confirm_result = pyqtSignal()
    signal_cancel_result = pyqtSignal()
    signal_cap_laserimg = pyqtSignal()
    signal_cap_inferredimg = pyqtSignal()
    signal_cap_nolightimg = pyqtSignal()

    def blink(self, channel):

        global clickState
        global firstTime
        global secondTime
        global program_step
        global print_once_flag
        global rising_edge_flag
        global falling_edge_flag
        global click_once

        # print("Blink LED 2, %s"%num)

        if (GPIO.input(channel) == GPIO.LOW):
            if (program_step == 0):
                falling_edge_flag = 1
                program_step = 1

            if (clickState == 0 and program_step == 2):
                firstTime = time.time()
                clickState = 1
                click_once = 1
                # print("state 1")

            if (clickState == 1 and click_once == 0 and program_step == 2):
                secondTime = time.time()
                clickState = 2
                # print("state 2")

        elif (GPIO.input(channel) == GPIO.HIGH):
            if (program_step == 1):
                rising_edge_flag = 1
                program_step = 2

        GPIO.remove_event_detect(channel)
        GPIO.add_event_detect(gpi_grabimage, GPIO.BOTH, callback=self.blink, bouncetime=200)

    def GPIO_main(self):
        # self.timer.moveToThread(self.GPIOThreadHandle)
        global clickState
        global firstTime
        global secondTime
        global program_step
        global print_once_flag
        global timeEclipse
        global clickFlag
        global click_once
        global time_long_set
        global time_long_long_set
        global falling_edge_flag
        global rising_edge_flag
        global cansel_flag
        global ok_flag

        # Pin Setup:
        GPIO.setmode(GPIO.BOARD)  # BOARD pin-numbering scheme
        # GPIO.setup([led_pin_1, led_pin_2], GPIO.OUT)  # LED pins set as output
        GPIO.setup(gpi_grabimage, GPIO.IN)  # button pin set as input


        GPIO.add_event_detect(gpi_grabimage, GPIO.BOTH, callback=self.blink, bouncetime=200)

        # print("Starting demo now! Press CTRL+C to exit")
        pwm = PCA9685()
        pwm.setPWMFreq(50)
        pwm.setPWM(3, 0, 0)  # 关闭可见激光
        pwm.setPWM(4, 0, 0)  # 关闭红外光源
        pwm.setPWM(5, 0, 0)  # 关闭红外激光

        try:
            while True:

                if (clickState == 1):
                    timeEclipse = time.time() - firstTime
                    if (timeEclipse > time_long_set):
                        ok_flag = 1
                        clickFlag = 1
                        clickState = 0
                        firstTime = 0
                        # print("state 3")

                    else:
                        # time.sleep(0.01)
                        click_once = 0

                if (clickState == 2):
                    timeEclipse = secondTime - firstTime
                    if (timeEclipse < time_long_set):
                        cansel_flag = 1
                        clickFlag = 2
                        secondTime = 0
                        firstTime = 0
                        clickState = 0

                if (clickFlag == 1):
                    # print("this is single click")
                    clickState = 0
                    clickFlag = 0
                elif (clickFlag == 2):
                    # print("this is double click")
                    clickState = 0
                    clickFlag = 0
                if (clickFlag == 3):
                    clickState = 0
                    clickFlag = 0
                    # print("this is changan")

                if (program_step == 1 and print_once_flag == 0):
                    # print("点亮可见激光")
                    # print("点亮不可见激光")
                    # print("点亮光源")
                    pwm.setPWM(3, 0, 4095)  # 点亮可见激光
                    pwm.setPWM(4, 0, 4095)  # 点亮红外光源
                    pwm.setPWM(5, 0, 4095)  # 点亮红外激光
                    print("======================================================================")
                    print_once_flag = 1
                if (program_step == 2 and print_once_flag == 1):
                    # print("熄灭光源")
                    pwm.setPWM(4, 0, 0)  # 熄灭红外光源
                    print("抓拍一张激光图像")  # 将此句话替换成拍照激光图片的函数即可
                    # set laser exposure
                    current_expo = c_float()
                    self.clientImID = int(round(time.time() * 1000))
                    ret = self.cam.MV_CC_GetFloatValue('ExposureTime', current_expo)
                    if (current_expo.value != self.laser_exposure):
                        ret = self.cam.MV_CC_SetFloatValue('ExposureTime', self.laser_exposure)
                    time.sleep(0.5)
                    self.trigger_laser_img()

                    pwm.setPWM(3, 0, 0)  # 熄灭可见激光
                    pwm.setPWM(5, 0, 0)  # 熄灭红外激光
                    time.sleep(0.5)
                    print("抓拍一张heise图像")  # 将此句话替换成拍照heise图片的函数即可
                    self.trigger_nolight_img()
                    # time.sleep(0.5)

                    # print("打开光源")
                    # print("熄灭可见激光")
                    # print("熄灭不可见激光")
                    pwm.setPWM(4, 0, 4095)  # 打开红外光源
                    pwm.setPWM(3, 0, 0)  # 熄灭可见激光
                    pwm.setPWM(5, 0, 0)  # 熄灭红外激光
                    current_expo = c_float()
                    ret = self.cam.MV_CC_GetFloatValue('ExposureTime', current_expo)
                    if (current_expo.value != self.inferred_exposure):
                        ret = self.cam.MV_CC_SetFloatValue('ExposureTime', self.inferred_exposure)
                    time.sleep(0.5)
                    print("抓拍一张灰度图像")  # 将此句话替换成拍照灰度图片的函数即可
                    self.trigger_inferred_img()
                    pwm.setPWM(4, 0, 0)  # 熄灭红外光源
                    print("开始上传激光图像")  # 将此句话替换成上传激光图片的函数即可
                    print("开始上传灰度图像")  # 将此句话替换成上传灰度图片的函数即可
                    self.signal_send_imgs.emit()
                    print("显示轮廓图像")  # 将此句话替换成显示轮廓图片的函数即可
                    print("等待确认回复")
                    print("======================================================================")
                    print_once_flag = 2

                if (program_step == 2 and cansel_flag == 1 and print_once_flag == 2):
                    cansel_flag = 0
                    print("取消重新开始")
                    self.signal_cancel_result.emit()
                    # self.cancel_result()
                    print("======================================================================")
                    print_once_flag = 0
                    program_step = 0

                if (program_step == 2 and ok_flag == 1 and print_once_flag == 2):
                    ok_flag = 0
                    print("确认重新开始")
                    self.signal_confirm_result.emit()
                    # self.confirm_result()
                    print("======================================================================")
                    print_once_flag = 0
                    program_step = 0

        finally:
            GPIO.cleanup()  # cleanup all GPIOs















if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
