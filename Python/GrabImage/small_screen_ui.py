# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fuck1.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets

import cv2
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
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
        self.communicationButton = QtWidgets.QPushButton(self.centralwidget)
        self.communicationButton.setGeometry(QtCore.QRect(0, 80, 100, 80))
        self.communicationButton.setObjectName("communicationButton")
        self.settingsButton = QtWidgets.QPushButton(self.centralwidget)
        self.settingsButton.setGeometry(QtCore.QRect(0, 640, 100, 80))
        self.settingsButton.setObjectName("settingsButton")
        self.manualSettingButton = QtWidgets.QPushButton(self.centralwidget)
        self.manualSettingButton.setGeometry(QtCore.QRect(700, 640, 100, 80))
        self.manualSettingButton.setObjectName("manualSettingButton")
        self.ReservedButton1 = QtWidgets.QPushButton(self.centralwidget)
        self.ReservedButton1.setGeometry(QtCore.QRect(40, 20, 111, 41))
        self.ReservedButton1.setObjectName("ReservedButton1")
        self.ReservedButton2 = QtWidgets.QPushButton(self.centralwidget)
        self.ReservedButton2.setGeometry(QtCore.QRect(180, 20, 91, 41))
        self.ReservedButton2.setObjectName("ReservedButton2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
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
        self.measurementStateButton.setText(_translate("MainWindow", "测量状态"))
        self.communicationButton.setText(_translate("MainWindow", "通讯"))
        self.settingsButton.setText(_translate("MainWindow", "拍照设置"))
        self.manualSettingButton.setText(_translate("MainWindow", "手动输入"))
        self.ReservedButton1.setText(_translate("MainWindow", "预留1"))
        self.ReservedButton2.setText(_translate("MainWindow", "预留2"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
