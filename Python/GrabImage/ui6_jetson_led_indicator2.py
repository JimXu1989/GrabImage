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
import LedIndicatorWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # set IP
        addr = 'http://192.168.43.47:8888'
        self.test_url = addr + '/api/test'
        content_type = 'image/jpeg'
        self.headers = {'content-type': content_type}
        self.clientImID = int(round(time.time() * 1000))
        self.resDict = {}
        self.imgHeight = 1024
        self.imgWidth = 1280
        self.laserImg = np.zeros((self.imgHeight,self.imgWidth))
        self.inferredImg = np.zeros((self.imgHeight, self.imgWidth))
        self.nolightImg = np.zeros((self.imgHeight, self.imgWidth))
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1038, 740)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.cam_realtime_btn = QtWidgets.QPushButton(self.centralwidget)
        self.cam_realtime_btn.setGeometry(QtCore.QRect(90, 470, 201, 61))
        self.cam_realtime_btn.setObjectName("cam_realtime_btn")
        self.cam_laser_cap_btn = QtWidgets.QPushButton(self.centralwidget)
        self.cam_laser_cap_btn.setGeometry(QtCore.QRect(700, 440, 231, 31))
        self.cam_laser_cap_btn.setObjectName("cam_laser_cap_btn")
        self.real_time_img_win = QtWidgets.QLabel(self.centralwidget)
        self.real_time_img_win.setGeometry(QtCore.QRect(20, 50, 480, 360))
        self.real_time_img_win.setText("")
        self.real_time_img_win.setPixmap(QtGui.QPixmap("black.png"))
        self.real_time_img_win.setScaledContents(True)
        self.real_time_img_win.setObjectName("real_time_img_win")
        self.cap_img_win = QtWidgets.QLabel(self.centralwidget)
        self.cap_img_win.setGeometry(QtCore.QRect(530, 50, 480, 360))
        self.cap_img_win.setText("")
        self.cap_img_win.setPixmap(QtGui.QPixmap("black.png"))
        self.cap_img_win.setScaledContents(True)
        self.cap_img_win.setObjectName("cap_img_win")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 10, 111, 21))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(540, 10, 161, 21))
        self.label_4.setObjectName("label_4")
        self.stop_btn = QtWidgets.QPushButton(self.centralwidget)
        self.stop_btn.setGeometry(QtCore.QRect(90, 560, 201, 61))
        self.stop_btn.setObjectName("stop_btn")
        self.exposureLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.exposureLineEdit.setGeometry(QtCore.QRect(670, 590, 181, 31))
        self.exposureLineEdit.setObjectName("exposureLineEdit")
        self.setExposureButton = QtWidgets.QPushButton(self.centralwidget)
        self.setExposureButton.setGeometry(QtCore.QRect(870, 590, 91, 31))
        self.setExposureButton.setObjectName("setExposureButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(570, 600, 91, 20))
        self.label.setObjectName("label")
        self.cam_inferred_cap_btn_ = QtWidgets.QPushButton(self.centralwidget)
        self.cam_inferred_cap_btn_.setGeometry(QtCore.QRect(700, 480, 231, 31))
        self.cam_inferred_cap_btn_.setObjectName("cam_inferred_cap_btn_")
        self.cam_no_light_cap_btn_ = QtWidgets.QPushButton(self.centralwidget)
        self.cam_no_light_cap_btn_.setGeometry(QtCore.QRect(700, 520, 231, 31))
        self.cam_no_light_cap_btn_.setObjectName("cam_no_light_cap_btn_")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1038, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.sendImgButton = QtWidgets.QPushButton(self.centralwidget)
        self.sendImgButton.setGeometry(QtCore.QRect(944, 440, 81, 71))
        self.sendImgButton.setObjectName("sendImgButton")
        self.led = LedIndicatorWidget.LedIndicator(self.centralwidget)
        self.led.setDisabled(True)
        self.led.setGeometry(QtCore.QRect(544, 440, 20, 20))


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.cam_realtime_btn.clicked.connect(self.get_real_time_img)
        self.stop_btn.clicked.connect(self.stop_cam)
        self.cam_laser_cap_btn.clicked.connect(self.cap_cam_laser_img)
        self.cam_inferred_cap_btn_.clicked.connect(self.cap_cam_inferred_img)
        self.cam_no_light_cap_btn_.clicked.connect(self.cap_cam_no_light_img)
        self.sendImgButton.clicked.connect(self.send_conbine_img)
        self.setExposureButton.clicked.connect(self.set_exposure)


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

        self.setExposureButton.setDisabled(True)
        self.stop_btn.setDisabled(True)
        self.cam_laser_cap_btn.setDisabled(True)
        self.cam_inferred_cap_btn_.setDisabled(True)
        self.cam_no_light_cap_btn_.setDisabled(True)
        self.led.setChecked(False)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_realtime_label)
        self.timer.start(50)
        self.timer2 = QTimer()
        self.timer2.timeout.connect(self.test_connection)
        self.timer2.start(1)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.cam_realtime_btn.setText(_translate("MainWindow", "开始相机实时显示"))
        self.cam_laser_cap_btn.setText(_translate("MainWindow", "采集激光图片"))
        self.label_3.setText(_translate("MainWindow", "相机实时画面："))
        self.label_4.setText(_translate("MainWindow", "采集到的图片："))
        self.stop_btn.setText(_translate("MainWindow", "关闭相机"))
        self.exposureLineEdit.setText(_translate("MainWindow", "5000"))
        self.setExposureButton.setText(_translate("MainWindow", "设置曝光值"))
        self.label.setText(_translate("MainWindow", "相机曝光值(µs)："))
        self.cam_inferred_cap_btn_.setText(_translate("MainWindow", "采集红外光源图片"))
        self.cam_no_light_cap_btn_.setText(_translate("MainWindow", "采集没有光源图片"))
        self.sendImgButton.setText(_translate("MainWindow", "发送图片"))
        a = self.exposureLineEdit.text()
        b = float(a)
        c = str(b)


    def set_exposure(self):
        a = 111
        exposureVal = float(self.exposureLineEdit.text())
        ret = self.cam.MV_CC_SetFloatValue('ExposureTime',exposureVal)

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
        self.cam_realtime_btn.setDisabled(True)
        self.setExposureButton.setDisabled(False)
        self.stop_btn.setDisabled(False)
        self.cam_laser_cap_btn.setDisabled(False)
        self.cam_inferred_cap_btn_.setDisabled(False)
        self.cam_no_light_cap_btn_.setDisabled(False)
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
        self.cam_realtime_btn.setEnabled(True)
        self.stop_btn.setDisabled(True)
        self.setExposureButton.setDisabled(True)
        self.cam_no_light_cap_btn_.setDisabled(True)
        self.cam_inferred_cap_btn_.setDisabled(True)
        self.cam_laser_cap_btn.setDisabled(True)

    # 为线程定义一个函数
    def work_thread(self, cam=0, pData=0, nDataSize=0):
        self.stDeviceList = MV_FRAME_OUT_INFO_EX()
        memset(byref(self.stDeviceList), 0, sizeof(self.stDeviceList))
        self.flag = True
        while self.flag:
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
        self.real_time_img_win.setPixmap(self.pixmap)

    def send_conbine_img(self):
        self.sendImg = np.hstack((self.laserImg,self.inferredImg,self.nolightImg))
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
        if(not(os.path.exists(folderPath))):
            os.makedirs(folderPath)
        cv2.imwrite(folderPath + '/' +str(self.clientImID) + '.png', self.resized)
        self.laserImg = self.resized
        self.cap_img_win.setPixmap(self.pixmap)


    def cap_cam_inferred_img(self):
        folderPath = 'inferred'  
        if(not(os.path.exists(folderPath))):
            os.makedirs(folderPath)
        cv2.imwrite(folderPath + '/' +str(self.clientImID) + '.png', self.resized)
        self.inferredImg = self.resized
        self.cap_img_win.setPixmap(self.pixmap)

    
    def cap_cam_no_light_img(self):
        folderPath = 'nolight'  
        if(not(os.path.exists(folderPath))):
            os.makedirs(folderPath)
        cv2.imwrite(folderPath + '/' +str(self.clientImID) + '.png', self.resized)
        self.nolightImg = self.resized
        self.cap_img_win.setPixmap(self.pixmap)

    def test_connection(self):
        try:
            response = requests.post(self.test_url, data='1', headers=self.headers)
            self.connect_test_res = response.text
            self.led.setChecked(True)
        except:
            self.led.setChecked(False)







if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
