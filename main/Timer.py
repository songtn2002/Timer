from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QTimer
import time


class TimerWidget (QLabel):

    def __init__(self, parent=None):
        super(TimerWidget, self).__init__(parent)
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.updateTime())
        self.timerStarted = False
        self.updateTime()

    def startTimer(self):
        self.timer.start(50)
        self.startTime = time.time()
        self.timerStarted = True

    def updateTime(self):
        self.setText(self.getTimeString())

    def getTimeString(self):
        if (self.timerStarted):
            timeNow = time.time()
            gap = timeNow-self.startTime
            print("gap: {}".format(gap))
            fracSeconds = int(gap%1/0.01);
            minutes = int(gap/60);
            seconds = int(gap)%60;
            return "{}:{}:{}".format(minutes, seconds, fracSeconds)
        else:
            return "00:00:00"


app = QApplication([])
window = QWidget()
layout = QVBoxLayout()
timer = TimerWidget()
layout.addWidget(timer)
startButton = QPushButton("Start")
startButton.clicked.connect(lambda: timer.startTimer())
layout.addWidget(startButton)
window.setLayout(layout)
window.show()
app.exec_()