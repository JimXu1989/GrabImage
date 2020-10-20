# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '4.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
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

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
