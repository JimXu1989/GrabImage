# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '2222.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


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
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 600, 480))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("black.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
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




        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # self.pushButton_test = QtWidgets.QPushButton(self.centralwidget)
        # self.pushButton_test.setGeometry(QtCore.QRect(690, 270, 31, 31))
        # self.pushButton_test.setObjectName("pushButton_test")

        self.led = LedIndicatorWidget.LedIndicator(self.centralwidget)
        self.led.setDisabled(True)
        self.led.setGeometry(QtCore.QRect(690, 270, 31, 31))

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setWindowFlags(Qt.FramelessWindowHint)
        self.exitButton.clicked.connect(MainWindow.close)
        self.manualButton.clicked.connect(self.showManualUI)
        self.settingButton.clicked.connect(self.showSettingUI)


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

    def showManualUI(self):
        self.ManualUIForm = QtWidgets.QWidget()
        self.manualui = manualui.Ui_Form()
        self.manualui.setupUi(self.ManualUIForm)
        self.manualui.sendButton.clicked.connect(self.sendManualResult)
        self.manualui.measureResultlineEdit.clicked.connect(self.showKeyboardUI)
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


    def showData(self):
        print('ok')




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
