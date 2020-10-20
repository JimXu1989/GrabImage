

class Example(QWidget):
    signal = pyqtSignal()    # 括号里填写信号传递的参数
    # 发射信号
    def func(self):
        self.signal.emit()

# 使用信号
a = Example()
a.signal.connect(callback)

# 槽函数
def callback():
    pass