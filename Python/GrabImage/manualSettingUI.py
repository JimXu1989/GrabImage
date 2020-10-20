# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'shoudong.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import keyboard3
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

# 定义可以响应按键的LineEdit
class ResponseLineEdit(QLineEdit):
  clicked=pyqtSignal()  #定义clicked信号
  def mouseReleaseEvent(self, QMouseEvent):
    if QMouseEvent.button()==Qt.LeftButton:
      self.clicked.emit()   #发送clicked信号

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.mayorDiameterLineEdit = ResponseLineEdit(Form)
        self.mayorDiameterLineEdit.setGeometry(QtCore.QRect(180, 70, 113, 20))
        self.mayorDiameterLineEdit.setObjectName("mayorDiameterLineEdit")
        self.minorDiameterLineEdit = ResponseLineEdit(Form)
        self.minorDiameterLineEdit.setGeometry(QtCore.QRect(180, 180, 113, 20))
        self.minorDiameterLineEdit.setObjectName("minorDiameterLineEdit")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(40, 70, 101, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(30, 180, 101, 21))
        self.label_2.setObjectName("label_2")

        self.mayorDiameterLineEdit.clicked.connect(self.showKeyboardUIMayorDiameter)
        self.minorDiameterLineEdit.clicked.connect(self.showKeyboardUIMinorDiameter)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "手动输入"))
        self.label.setText(_translate("Form", "长径："))
        self.label_2.setText(_translate("Form", "短径："))

    def showKeyboardUIMayorDiameter(self):
        self.keyboardUIForm = QtWidgets.QWidget()
        self.keyboard = keyboard3.keyboard()
        self.keyboard.enterBtn.clicked.connect(self.keyboardSendTextMayorDiameter)
        # self.keyboard2.initUI()
        self.keyboard.show()

    def showKeyboardUIMinorDiameter(self):
        self.keyboardUIForm = QtWidgets.QWidget()
        self.keyboard = keyboard3.keyboard()
        self.keyboard.enterBtn.clicked.connect(self.keyboardSendTextMinorDiameter)
        # self.keyboard2.initUI()
        self.keyboard.show()

    def keyboardSendTextMayorDiameter(self):
        sender = self.keyboard.sender()
        if sender.text() == "Enter":
            temp = self.keyboard.display.text()
            self.mayorDiameterLineEdit.setText(temp)
        self.keyboard.close()

    def keyboardSendTextMinorDiameter(self):
        sender = self.keyboard.sender()
        if sender.text() == "Enter":
            temp = self.keyboard.display.text()
            self.minorDiameterLineEdit.setText(temp)
        self.keyboard.close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
