from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys

#方法1
class mylineedit(QLineEdit):
  clicked=pyqtSignal()  #定义clicked信号
  def mouseReleaseEvent(self, QMouseEvent):
    if QMouseEvent.button()==Qt.LeftButton:
      self.clicked.emit()   #发送clicked信号

class Wind(QDialog):
  clicked=pyqtSignal()
  def __init__(self):
    super().__init__()
    self.lnd=mylineedit()
    self.edit=mylineedit()
    # self.edit.installEventFilter(self)  #方法2(1)

    vb=QVBoxLayout()
    vb.addWidget(self.lnd)
    vb.addWidget(self.edit)
    self.setLayout(vb)

    self.lnd.clicked.connect(self.showData)
    self.edit.clicked.connect(self.showData)
    # self.clicked.connect(self.showData)   #该clicked信号是W1的信号而非edit的信号，但可以实现焦点落到edit时触发信号

  # 方法2(2)

  def showData(self):
    print('ok')

if __name__=="__main__":
  app=QApplication(sys.argv)
  w=Wind()
  w.show()
  sys.exit(app.exec_())

