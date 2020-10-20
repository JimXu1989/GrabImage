from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
class Example(QWidget):
    _startPos = None
    _endPos = None
    _isTracking = False

    def __init__(self):
        super().__init__()
        self._initUI()
        self.Use_Qss()
        self.show()

    def _initUI(self):
        self.resize(350, 350)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 无边框
    def Use_Qss(self):
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("./p1.jpg")))
        self.setPalette(palette)
        #self.setObjectName("MainWindow")
        # #todo 1 设置窗口背景图片
        #self.setStyleSheet("#MainWindow{border-image:url(.\p1.jpg);}")
        # todo 2 设置窗口背景色
        #self.setStyleSheet("#MainWindow{background-color: gray}")
        #self.show()
    def mouseMoveEvent(self, e: QMouseEvent):  # 重写移动事件
        self._endPos = e.pos() - self._startPos
        self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = True
            self._startPos = QPoint(e.x(), e.y())

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())