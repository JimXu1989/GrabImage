# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'celiangzhuangtai.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import keyboard3

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(40, 60, 191, 31))
        self.label.setObjectName("label")
        self.stateLabel = QtWidgets.QLabel(Form)
        self.stateLabel.setGeometry(QtCore.QRect(40, 110, 331, 31))
        self.stateLabel.setObjectName("stateLabel")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "测量状态"))
        self.label.setText(_translate("Form", "当前测量状态："))
        self.stateLabel.setText(_translate("Form", "TextLabel"))

    def runUi(self):
        # import sys
        # app = QtWidgets.QApplication(sys.argv)
        Form = QtWidgets.QWidget()
        ui = Ui_Form()
        ui.setupUi(Form)
        Form.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
