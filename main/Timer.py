from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QTimer, Qt, QSize, QStringListModel
from PyQt5.QtGui import QFont
import time

def fontSize (size):
    font = QFont()
    font.setPointSize(size)
    return font

class TimerWidget (QLabel):

    accMin = 0
    accSec = 0
    accFracSec = 0

    timeList = []

    def __init__(self, parent=None):
        super(TimerWidget, self).__init__(parent)
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.updateTime())
        self.timerOn = False
        self.updateTime()
        self.setFont(fontSize(60))


    def startTimer(self):
        self.timer.start(50)
        self.startTime = time.time()
        self.timerOn = True

    def stopTimer(self):
        self.timer.stop()
        self.timerOn = False
        self.updateTime()

    def reset(self):
        self.timerOn = False
        self.accSec = 0
        self.accFracSec = 0
        self.accMin = 0
        self.updateTime()
        self.timeList.clear()
        updateView()


    def lap(self):
        timeNow = time.time()
        gap = timeNow - self.startTime
        # print("gap: {}".format(gap))
        fracSeconds = int(gap % 1 / 0.01)
        minutes = int(gap / 60)
        seconds = int(gap) % 60
        # print("minutes: "+str(minutes)+" seconds: "+str(seconds)+" fracSeconds: "+str(fracSeconds))
        self.accFracSec += fracSeconds
        self.accSec += seconds
        self.accMin += minutes
        # print("{}:{}:{}".format(self.accMin, self.accSec, self.accFracSec))
        self.accSec += int(self.accFracSec / 100)
        self.accFracSec = int(self.accFracSec % 100)
        self.accMin += int(self.accSec / 60)
        self.accSec = int(self.accSec % 60)
        self.startTime = timeNow
        lapStr = "Lap {}".format(len(self.timeList)+1)
        timeStr = self.getTimeString()
        strAppended = lapStr + " "*(40-len(lapStr)) + timeStr
        self.timeList.append(strAppended)
        updateView()

    def updateTime(self):
        if (self.timerOn):
            timeNow = time.time()
            gap = timeNow - self.startTime
            # print("gap: {}".format(gap))
            fracSeconds = int(gap % 1 / 0.01)
            minutes = int(gap / 60)
            seconds = int(gap) % 60
            #print("minutes: "+str(minutes)+" seconds: "+str(seconds)+" fracSeconds: "+str(fracSeconds))
            self.accFracSec += fracSeconds
            self.accSec += seconds
            self.accMin += minutes
            #print("{}:{}:{}".format(self.accMin, self.accSec, self.accFracSec))
            self.accSec += int(self.accFracSec/100)
            self.accFracSec = int(self.accFracSec%100)
            self.accMin += int(self.accSec/60)
            self.accSec = int(self.accSec%60)
            self.startTime = timeNow
        self.setText(self.getTimeString())

    def getTimeString(self):
        minStr = ("0"+str(self.accMin))[-2:]
        secStr = ("0"+str(self.accSec))[-2:]
        fracSecStr = ("0"+str(self.accFracSec))[-2:]
        return "{}:{}:{}".format(minStr, secStr, fracSecStr)

def buttonGroup():
    layout = QHBoxLayout()
    global leftButton
    leftButton = QPushButton("Reset")
    leftButton.clicked.connect(LBttnSignal)
    leftButton.setFont(fontSize(15))
    global rightButton
    rightButton = QPushButton("Start")
    rightButton.clicked.connect(RBttnSignal)
    rightButton.setFont(fontSize(15))
    layout.addWidget (leftButton)
    layout.addWidget (rightButton)
    return layout

def updateView():
    model = QStringListModel(timer.timeList)
    lapView.setModel(model)

def listView():
    global lapView
    lapView = QListView()
    lapView.setEditTriggers(QAbstractItemView.NoEditTriggers)
    lapView.setFont(fontSize(15))
    return lapView

def LBttnSignal():
    if (timer.timerOn):
        timer.lap()
    else:
        timer.reset()

def RBttnSignal():
    if (timer.timerOn):
        rightButton.setText("Start")
        leftButton.setText("Reset")
        timer.stopTimer()
    else:
        rightButton.setText("Stop")
        leftButton.setText("Lap")
        timer.startTimer()

def exportSignal():
    pass

def exportButton():
    export = QPushButton("Export")
    export.setFont(fontSize(15))
    export.clicked.connect(exportSignal)
    return export

app = QApplication([])
app.setApplicationName("Timer")
window = QWidget()
window.setFixedWidth(550)
mainLayout = QVBoxLayout()
timer = TimerWidget()
mainLayout.addWidget(timer, alignment=Qt.AlignCenter)
mainLayout.addLayout(buttonGroup())
mainLayout.addWidget(listView())
mainLayout.addWidget(exportButton())
window.setLayout(mainLayout)
window.show()
app.exec_()