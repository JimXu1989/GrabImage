# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '2222.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate, QTime, QTimer
import sys
import threading
import cv2
import numpy as np
from PyQt5.QtGui import QImage, QPixmap
import os,os.path
from ctypes import *
sys.path.append("../MvImport")
from MvCameraControl_class import *
import json
import time
import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import manualui
import settingui
import keyboard2
import LedIndicatorWidget

class mylineedit(QLineEdit):
  clicked=pyqtSignal()  #定义clicked信号
  def mouseReleaseEvent(self, QMouseEvent):
    if QMouseEvent.button()==Qt.LeftButton:
      self.clicked.emit()   #发送clicked信号

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.laser_trigger = 0
        self.inferred_trigger = 0
        self.nolight_trigger = 0
        self.laser_exposure = 4000
        self.inferred_exposure = 3000
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
        self.label_3.setGeometry(QtCore.QRect(160, 520, 261, 31))
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
        self.cancelButton = QtWidgets.QPushButton(self.centralwidget)
        self.cancelButton.setGeometry(QtCore.QRect(720, 120, 61, 61))
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
        self.stopCamButton = QtWidgets.QPushButton(self.centralwidget)
        self.stopCamButton.setGeometry(QtCore.QRect(410, 510, 121, 41))
        self.stopCamButton.setObjectName("stopCamButton")
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

        self.capButton.clicked.connect(self.simulate_cap_images)

        self.settingButton.setDisabled(True)
        self.stopCamButton.setDisabled(True)

        self.resized = cv2.imread('black.png')
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

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_realtime_label)
        self.timer.start(50)



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.settingButton.setText(_translate("MainWindow", "设置"))
        self.label_2.setText(_translate("MainWindow", "设备状态:"))
        self.label_3.setText(_translate("MainWindow", "距离太远"))
        self.label_4.setText(_translate("MainWindow", "检尺径："))
        self.label_5.setText(_translate("MainWindow", "88.88"))
        self.manualButton.setText(_translate("MainWindow", "人工"))
        self.confirmButton.setText(_translate("MainWindow", "确认"))
        self.cancelButton.setText(_translate("MainWindow", "取消"))
        self.label_6.setText(_translate("MainWindow", "连接状态："))
        # self.pushButton_test.setText(_translate("MainWindow", "PushButton"))
        self.exitButton.setText(_translate("MainWindow", "退出"))

        #测试用####################################################
        self.capButton.setText(_translate("MainWindow", "拍照（测试）"))
        self.initCamButton.setText(_translate("MainWindow", "打开相机（测试）"))
        self.stopCamButton.setText(_translate("MainWindow", "关闭相机（测试）"))

    def showManualUI(self):
        self.ManualUIForm = QtWidgets.QWidget()
        self.manualui = manualui.Ui_Form()
        self.manualui.setupUi(self.ManualUIForm)
        self.manualui.sendButton.clicked.connect(self.sendManualResult)
        # self.manualui.measureResultlineEdit.clicked.connect(self.showKeyboardUI)
        self.showKeyboardUI()
        # self.manualui.measureResultlineEdit.clicked.connect(MainWindow.close)
        self.ManualUIForm.show()

    def sendManualResult(self):
        self.aa = self.manualui.measureResultlineEdit.text()
        print(self.aa)
        return self.aa

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
        # tmpExposure = c_float(0.0)
        # rr = self.cam.MV_CC_GetFloatValue('ExposureTime', tmpExposure)
        # exposureVal = float(self.exposureLineEdit.text())
        # qq = c_float(3000.0)
        # ret = self.cam.MV_CC_SetFloatValue('ExposureTime', qq)
        # ret = self.cam.MV_CC_SetFloatValue('ExposureTime', tmpExposure)
        # aaa = 111

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
                if(current_expo.value != self.inferred_exposure):
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

                    # 进行图像的保存
                    if (self.laser_trigger):
                        self.clientImID = int(round(time.time() * 1000))
                        folderPath = 'laser'
                        if (not (os.path.exists(folderPath))):
                            os.makedirs(folderPath)
                        cv2.imwrite(folderPath + '/' + str(self.clientImID) + '.png', self.resized)
                        self.laserImg = self.resized
                        self.laser_trigger = 0
                    if (self.inferred_trigger):
                        folderPath = 'inferred'
                        if (not (os.path.exists(folderPath))):
                            os.makedirs(folderPath)
                        cv2.imwrite(folderPath + '/' + str(self.clientImID) + '.png', self.resized)
                        self.inferredImg = self.resized
                        self.img_win.setPixmap(self.pixmap)
                        self.inferred_trigger = 0
                        # 停止实时显示
                        self.timer.stop()
                    if (self.nolight_trigger):
                        current_expo = c_float()
                        ret = self.cam.MV_CC_GetFloatValue('ExposureTime', current_expo)
                        if (current_expo.value != self.inferred_exposure):
                            ret = self.cam.MV_CC_SetFloatValue('ExposureTime', self.inferred_exposure)
                        folderPath = 'nolight'
                        if (not (os.path.exists(folderPath))):
                            os.makedirs(folderPath)
                        cv2.imwrite(folderPath + '/' + str(self.clientImID) + '.png', self.resized)
                        self.inferredImg = self.resized
                        self.img_win.setPixmap(self.pixmap)

                        self.nolight_trigger

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
        self.sendImg = np.hstack((self.laserImg, self.inferredImg, self.nolightImg))
        # prepare headers for http request
        content_type = 'image/jpeg'
        headers = {'content-type': content_type}
        # capture = cv2.VideoCapture(0)
        # ret, frame = capture.read()
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

        # encode image as jpeg
        _, img_encoded = cv2.imencode('.jpg', self.sendImg, encode_param)
        # send http request with image and receive response
        response = requests.post(self.test_url, data=img_encoded.tostring() + str(self.clientImID).encode('utf-8'),
                                 headers=self.headers)
        self.resDict = eval(response.text)
        ContourPointX = list(map(int, self.resDict['ContourPointX'].split(',')))
        ContourPointY = list(map(int, self.resDict['ContourPointY'].split(',')))
        cr = np.vstack((ContourPointX, ContourPointY))
        crt = (cr.T).astype(np.int32)
        crt = np.expand_dims(crt, axis=1)
        height, width, bytesPerComponent = self.inferredImg.shape
        if (bytesPerComponent == 1):
            clone = cv2.cvtColor(self.inferredImg, cv2.COLOR_GRAY2RGB)
        else:
            clone = self.inferredImg.copy()
        bytesPerLine = bytesPerComponent * width
        cv2.drawContours(clone, [crt], -1, (0, 255, 0), 2)
        if (bytesPerComponent == 3):
            self.QImg2 = QImage(clone.data, width, height, bytesPerLine,
                                QImage.Format_RGB888).rgbSwapped()
        else:
            self.QImg2 = QImage(clone.data, width, height, bytesPerLine,
                                QImage.Format_Grayscale8)

        self.pixmap = QtGui.QPixmap.fromImage(self.QImg2)
        self.cap_img_win.setPixmap(self.pixmap)

        folderPath = 'result'
        if (not (os.path.exists(folderPath))):
            os.makedirs(folderPath)
        cv2.imwrite(folderPath + '/' + str(self.clientImID) + '.png', clone)

        print(json.loads(response.text))

    def cap_cam_laser_img(self):
        self.clientImID = int(round(time.time() * 1000))
        folderPath = 'laser'
        if (not (os.path.exists(folderPath))):
            os.makedirs(folderPath)
        cv2.imwrite(folderPath + '/' + str(self.clientImID) + '.png', self.resized)
        self.laserImg = self.resized
        # self.cap_img_win.setPixmap(self.pixmap)

    def cap_cam_inferred_img(self):
        folderPath = 'inferred'
        if (not (os.path.exists(folderPath))):
            os.makedirs(folderPath)
        cv2.imwrite(folderPath + '/' + str(self.clientImID) + '.png', self.resized)
        self.inferredImg = self.resized
        self.img_win.setPixmap(self.pixmap)

    def cap_cam_no_light_img(self):
        folderPath = 'nolight'
        if (not (os.path.exists(folderPath))):
            os.makedirs(folderPath)
        cv2.imwrite(folderPath + '/' + str(self.clientImID) + '.png', self.resized)
        self.nolightImg = self.resized
        # self.cap_img_win.setPixmap(self.pixmap)

    def simulate_cap_images(self):
        self.laser_trigger = 1
        self.inferred_trigger = 0
        self.nolight_trigger = 0

        time.sleep(0.1)
        self.laser_trigger = 0
        self.inferred_trigger = 0
        self.nolight_trigger = 1

        time.sleep(0.1)
        self.laser_trigger = 0
        self.inferred_trigger = 1
        self.nolight_trigger = 0

    def cap_images(self):
        self.cap_cam_laser_img()
        if(self.laser_exposure==self.inferred_exposure):
            self.cap_cam_inferred_img()
            self.cap_cam_no_light_img()
        else:
            ret = self.cam.MV_CC_SetFloatValue('ExposureTime', self.inferred_exposure)
            self.cap_cam_inferred_img()
            self.cap_cam_no_light_img()

    def test_connection(self):
        response = requests.post(self.test_url, data='1', headers=self.headers)
        self.connect_test_res = response.text
        if (self.connect_test_res == 'ok'):
            self.led.setChecked(True)
        else:
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


    def showData(self):
        print('ok')

    def trigger_laser_img(self):
        self.laser_trigger = 1
        self.inferred_trigger = 0
        self.nolight_trigger = 0

    def trigger_inferred_img(self):
        self.laser_trigger = 0
        self.inferred_trigger = 1
        self.nolight_trigger = 0

    def trigger_nolight_img(self):
        self.laser_trigger = 0
        self.inferred_trigger = 0
        self.nolight_trigger = 1






if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
