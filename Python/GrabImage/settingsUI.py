# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'shezhi.ui'
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
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(30, 30, 91, 31))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(30, 100, 91, 31))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(30, 170, 101, 31))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(30, 240, 121, 31))
        self.label_4.setObjectName("label_4")
        self.laserExposureLineEdit = ResponseLineEdit(Form)
        self.laserExposureLineEdit.setGeometry(QtCore.QRect(120, 40, 113, 20))
        self.laserExposureLineEdit.setObjectName("laserExposureLineEdit")
        self.inferredExposureLineEdit = ResponseLineEdit(Form)
        self.inferredExposureLineEdit.setGeometry(QtCore.QRect(120, 110, 113, 20))
        self.inferredExposureLineEdit.setObjectName("inferredExposureLineEdit")
        self.laserLightLineEdit = ResponseLineEdit(Form)
        self.laserLightLineEdit.setGeometry(QtCore.QRect(120, 180, 113, 20))
        self.laserLightLineEdit.setObjectName("laserLightLineEdit")
        self.inferredLightLineEdit = ResponseLineEdit(Form)
        self.inferredLightLineEdit.setGeometry(QtCore.QRect(120, 250, 113, 20))
        self.inferredLightLineEdit.setObjectName("inferredLightLineEdit")



        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "拍照参数设置"))
        self.label.setText(_translate("Form", "激光曝光："))
        self.label_2.setText(_translate("Form", "红外曝光："))
        self.label_3.setText(_translate("Form", "激光亮度："))
        self.label_4.setText(_translate("Form", "红外亮度："))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
