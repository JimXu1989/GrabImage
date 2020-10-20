# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tongxun.ui'
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
        Form.setObjectName("通讯设置")
        Form.resize(400, 300)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(20, 40, 111, 16))
        self.label.setObjectName("label")
        self.serverIPLineEdit = ResponseLineEdit(Form)
        self.serverIPLineEdit.setGeometry(QtCore.QRect(20, 70, 271, 31))
        self.serverIPLineEdit.setObjectName("serverIPLineEdit")
        self.ClientIPLineEdit = ResponseLineEdit(Form)
        self.ClientIPLineEdit.setGeometry(QtCore.QRect(20, 200, 271, 31))
        self.ClientIPLineEdit.setObjectName("ClientIPLineEdit")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(20, 160, 131, 21))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "通讯设置"))
        self.label.setText(_translate("Form", "ServerIP地址："))
        self.label_2.setText(_translate("Form", "本机IP地址："))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
