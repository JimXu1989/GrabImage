# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'xiaoping.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!
import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
import measurementStateUI
import manualSettingUI
import settingsUI
import communicationUI
import keyboard3
import time
import numpy as np
import sys
import threading
import cv2
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
from PyQt5.QtGui import QImage, QPixmap





class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # set IP
        self.addr = '192.168.31.96'
        self.test_url = 'http://'+self.addr+':8888' + '/api/test'
        content_type = 'image/jpeg'
        self.headers = {'content-type': content_type}

        # 相机以及光源设置参数
        self.laser_exposure = 2000.0
        self.inferred_exposure = 500.0
        self.laser_brightness = 100.0
        self.inferred_brightness = 100.0

        # 测量状态
        self.measure_statement = ''
        # 时间戳，也是客户端图像编码
        self.clientImID = int(round(time.time() * 1000))
        # 返回的结果的字典
        self.resDict = {}
        self.imgHeight = 1024
        self.imgWidth = 1280

        # 初始化图像变量
        self.laserImg = np.zeros((self.imgHeight, self.imgWidth))
        self.inferredImg = np.zeros((self.imgHeight, self.imgWidth))

        # 拍照状态
        self.laser_trigger = 0
        self.inferred_trigger = 0

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.imgWin = QtWidgets.QLabel(self.centralwidget)
        self.imgWin.setGeometry(QtCore.QRect(0, 80, 800, 640))
        self.imgWin.setText("")
        self.imgWin.setPixmap(QtGui.QPixmap("black.png"))
        self.imgWin.setScaledContents(True)
        self.imgWin.setObjectName("imgWin")
        self.measurementStateButton = QtWidgets.QPushButton(self.centralwidget)
        self.measurementStateButton.setGeometry(QtCore.QRect(700, 80, 100, 80))
        self.measurementStateButton.setObjectName("measurementStateButton")
        # 测量状态按钮为绿色，表示测量成功
        self.measurementStateButton.setStyleSheet('''QPushButton{background:#8BDA67;border-radius:5px;}''')
        # 测量按钮状态为红色，表示测量失败
        # self.measurementStateButton.setStyleSheet('''QPushButton{background:#FF2A44;border-radius:5px;}''')
        # 测量按钮状态为黄色
        # self.measurementStateButton.setStyleSheet('''QPushButton{background:#FFE643;border-radius:5px;}''')

        self.communicationButton = QtWidgets.QPushButton(self.centralwidget)
        self.communicationButton.setGeometry(QtCore.QRect(0, 80, 100, 80))
        self.communicationButton.setObjectName("communicationButton")

        # 通讯按钮为绿色，代表通讯正常
        self.communicationButton.setStyleSheet('''QPushButton{background:#66FF67;border-radius:5px;}''')
        # 通讯按钮状态为红色，表示通讯异常
        # self.communicationButton.setStyleSheet('''QPushButton{background:#FF2A44;border-radius:5px;}''')


        self.settingsButton = QtWidgets.QPushButton(self.centralwidget)
        self.settingsButton.setGeometry(QtCore.QRect(0, 640, 100, 80))
        self.settingsButton.setObjectName("settingsButton")
        self.manualSettingButton = QtWidgets.QPushButton(self.centralwidget)
        self.manualSettingButton.setGeometry(QtCore.QRect(700, 640, 100, 80))
        self.manualSettingButton.setObjectName("manualSettingButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.ReservedButton1 = QtWidgets.QPushButton(self.centralwidget)
        self.ReservedButton1.setGeometry(QtCore.QRect(40, 20, 111, 41))
        self.ReservedButton1.setObjectName("ReservedButton1")
        self.ReservedButton2 = QtWidgets.QPushButton(self.centralwidget)
        self.ReservedButton2.setGeometry(QtCore.QRect(180, 20, 91, 41))
        self.ReservedButton2.setObjectName("ReservedButton2")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.measurementStateUI = measurementStateUI.Ui_Form
        self.measurementStateButton.clicked.connect(self.callMeasurementStateUI)
        self.manualSettingButton.clicked.connect(self.callManualSettingsUI)
        self.settingsButton.clicked.connect(self.callSettingsUI)
        self.communicationButton.clicked.connect(self.callCommunicationUI)

        self.ReservedButton1.clicked.connect(self.trigger_laser_img)
        self.ReservedButton2.clicked.connect(self.trigger_inferred_img)
        #
        self.start_cam()

        self.signal_update_imgwin = PyQt5.QtCore.pyqtSignal.pyqtSignal()
        self.signal_update_imgwin.connect(self.update_imgwin)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.measurementStateButton.setText(_translate("MainWindow", "测量状态"))
        self.communicationButton.setText(_translate("MainWindow", "通讯"))
        self.settingsButton.setText(_translate("MainWindow", "拍照设置"))
        self.manualSettingButton.setText(_translate("MainWindow", "手动输入"))
        self.ReservedButton1.setText(_translate("MainWindow", "预留1"))
        self.ReservedButton2.setText(_translate("MainWindow", "预留2"))

    def update_imgwin(self):
        self.imgWin.setPixmap(self.pixmap)

    # 测量状态窗口
    def callMeasurementStateUI(self):
        self.measurementStateForm = QtWidgets.QWidget()
        self.measurementStateUi = measurementStateUI.Ui_Form()
        self.measurementStateUi.setupUi(self.measurementStateForm)
        self.measurementStateForm.show()

    # 手动输入窗口
    def callManualSettingsUI(self):
        self.manualSettingForm = QtWidgets.QWidget()
        self.manualSettingUi = manualSettingUI.Ui_Form()
        self.manualSettingUi.setupUi(self.manualSettingForm)
        self.manualSettingForm.show()

    # 拍照设置窗口
    def callSettingsUI(self):
        self.SettingsForm = QtWidgets.QWidget()
        self.SettingsUi = settingsUI.Ui_Form()
        self.SettingsUi.setupUi(self.SettingsForm)

        self.SettingsUi.laserExposureLineEdit.setText(str(self.laser_exposure))
        self.SettingsUi.inferredExposureLineEdit.setText(str(self.inferred_exposure))
        self.SettingsUi.laserLightLineEdit.setText(str(self.laser_brightness))
        self.SettingsUi.inferredLightLineEdit.setText(str(self.inferred_brightness))

        self.SettingsUi.laserExposureLineEdit.clicked.connect(self.showKeyboardLaserExpoUI)
        self.SettingsUi.inferredExposureLineEdit.clicked.connect(self.showKeyboardInferredExpoUI)
        self.SettingsUi.laserLightLineEdit.clicked.connect(self.showKeyboardLaserLight)
        self.SettingsUi.inferredLightLineEdit.clicked.connect(self.showKeyboardInferredLight)

        self.SettingsForm.show()

    def showKeyboardLaserExpoUI(self):
        self.keyboardUIForm = QtWidgets.QWidget()
        self.keyboard = keyboard3.keyboard()
        self.keyboard.enterBtn.clicked.connect(self.keyboardSendTextLaserExpo)
        # self.keyboard2.initUI()
        self.keyboard.show()

    def showKeyboardInferredExpoUI(self):
        self.keyboardUIForm = QtWidgets.QWidget()
        self.keyboard = keyboard3.keyboard()
        self.keyboard.enterBtn.clicked.connect(self.keyboardSendTextInferredExpo)
        # self.keyboard2.initUI()
        self.keyboard.show()

    def showKeyboardLaserLight(self):
        self.keyboardUIForm = QtWidgets.QWidget()
        self.keyboard = keyboard3.keyboard()
        self.keyboard.enterBtn.clicked.connect(self.keyboardSendTextLaserLight)
        # self.keyboard2.initUI()
        self.keyboard.show()

    def showKeyboardInferredLight(self):
        self.keyboardUIForm = QtWidgets.QWidget()
        self.keyboard = keyboard3.keyboard()
        self.keyboard.enterBtn.clicked.connect(self.keyboardSendTextInferredLight)
        # self.keyboard2.initUI()
        self.keyboard.show()

    def keyboardSendTextLaserExpo(self):
        sender = self.keyboard.sender()
        if sender.text() == "Enter":
            temp = self.keyboard.display.text()
            self.SettingsUi.laserExposureLineEdit.setText(temp)
            self.laser_exposure = float(temp)
        self.keyboard.close()

    def keyboardSendTextInferredExpo(self):
        sender = self.keyboard.sender()
        if sender.text() == "Enter":
            temp = self.keyboard.display.text()
            self.SettingsUi.inferredExposureLineEdit.setText(temp)
            self.inferred_exposure = float(temp)
        self.keyboard.close()

    def keyboardSendTextLaserLight(self):
        sender = self.keyboard.sender()
        if sender.text() == "Enter":
            temp = self.keyboard.display.text()
            self.SettingsUi.laserLightLineEdit.setText(temp)
            self.laser_brightness = float(temp)
        self.keyboard.close()

    def keyboardSendTextInferredLight(self):
        sender = self.keyboard.sender()
        if sender.text() == "Enter":
            temp = self.keyboard.display.text()
            self.SettingsUi.inferredLightLineEdit.setText(temp)
            self.inferred_brightness = float(temp)
        self.keyboard.close()


    # 通讯设置窗口
    def callCommunicationUI(self):
        self.CommunicationForm = QtWidgets.QWidget()
        self.CommunicationUi = communicationUI.Ui_Form()
        self.CommunicationUi.setupUi(self.CommunicationForm)
        self.CommunicationUi.serverIPLineEdit.setText(self.addr)
        self.CommunicationUi.serverIPLineEdit.clicked.connect(self.showKeyboardUIServerIP)
        self.CommunicationForm.show()

    def showKeyboardUIServerIP(self):
        self.keyboardUIForm = QtWidgets.QWidget()
        self.keyboard = keyboard3.keyboard()
        self.keyboard.enterBtn.clicked.connect(self.keyboardSendTextServerIP)
        self.keyboard.show()

    def keyboardSendTextServerIP(self):
        sender = self.keyboard.sender()
        if sender.text() == "Enter":
            temp = self.keyboard.display.text()
            # set IP
            self.addr = temp
            self.test_url = 'http://' + self.addr + ':8888' + '/api/test'
            self.CommunicationUi.serverIPLineEdit.setText(self.addr)
        self.keyboard.close()

    def work_thread(self, cam=0, pData=0, nDataSize=0):
        self.stDeviceList = MV_FRAME_OUT_INFO_EX()
        memset(byref(self.stDeviceList), 0, sizeof(self.stDeviceList))
        self.flag = True
        while self.flag:
            # 首先设置曝光
            # if (self.laser_trigger):
            #     current_expo = c_float()
            #     # self.clientImID = int(round(time.time() * 1000))
            #     ret = self.cam.MV_CC_GetFloatValue('ExposureTime', current_expo)
            #     if (current_expo.value != self.laser_exposure):
            #         ret = self.cam.MV_CC_SetFloatValue('ExposureTime', self.laser_exposure)
            #
            # if (self.inferred_trigger):
            #     current_expo = c_float()
            #     ret = self.cam.MV_CC_GetFloatValue('ExposureTime', current_expo)
            #     if (current_expo.value != self.inferred_exposure):
            #         ret = self.cam.MV_CC_SetFloatValue('ExposureTime', self.inferred_exposure)

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

                    self.signal_update_imgwin.emit()
                    # self.imgWin.setPixmap(self.pixmap)

                except:
                    raise Exception("save file executed failed:%s" % e.message)


            else:
                print("get one frame fail, ret[0x%x]" % ret)

            # print("convert pixeltype succeed!")

    def start_cam(self):
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
        self.settingsButton.setDisabled(False)
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
            # aaa = 1
            self.hThreadHandle = threading.Thread(target=self.work_thread,
                                                  args=(self.cam, byref(self.data_buf), self.nPayloadSize))
            self.hThreadHandle.setDaemon(True)
            self.hThreadHandle.start()

            # self.gpioThreadHandle = threading.Thread(target=self.GPIO_main,
            #                                          )
            # self.gpioThreadHandle.setDaemon(True)
            # self.gpioThreadHandle.start()

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

    def trigger_laser_img(self):
        current_expo = c_float()
        self.clientImID = int(round(time.time() * 1000))
        ret = self.cam.MV_CC_GetFloatValue('ExposureTime', current_expo)
        if (current_expo.value != self.laser_exposure):
            ret = self.cam.MV_CC_SetFloatValue('ExposureTime', self.laser_exposure)
            time.sleep(0.1)
        self.laser_trigger = 1
        # self.clientImID = int(round(time.time() * 1000))
        self.inferred_trigger = 0
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
            time.sleep(0.1)
        self.laser_trigger = 0
        self.inferred_trigger = 1
        self.cam_get_one_frame()
        self.inferredImg = self.resized[:,:,0]
        folderPath = 'inferred'
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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
