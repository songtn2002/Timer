from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QTimer, Qt, QSize, QStringListModel
from PyQt5.QtGui import QFont
import numpy as np
import pandas as pd
import time

export_data = None # in general not a good idea to use global within methods but I don't know where export signal's return goes so I'm just having it set a global variable right now

def fontSize (size):
    font = QFont()
    font.setPointSize(size)
    return font

class TimerWidget (QLabel):

    accMin = 0
    accSec = 0
    accFracSec = 0

    run_id = 1 #id for the run, not reset at all for a given app session. We might consider using seeded hash or something so that we will never get the same values. I'll handle this part later

    timeList = []
    current_run_lap_times = [] #the times for the current run at the times the lap button is pressed
    export_ls = []  # list of all the data ready to be put into an excel file. Stores pd.DataFrame objects

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

        run_data = pd.DataFrame(columns=["RunId", "SegmentId", "Time"],
                                data=np.column_stack(
                                    [np.full(shape=(len(self.current_run_lap_times),), fill_value=self.run_id),
                                     np.arange(1, len(self.current_run_lap_times) + 1),
                                     self.current_run_lap_times]))
        self.export_ls.append(run_data)

        self.timerOn = False
        self.accSec = 0
        self.accFracSec = 0
        self.accMin = 0
        self.updateTime()
        self.timeList.clear()
        self.current_run_lap_times.clear()
        self.run_id += 1
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
        timeStr, timeSecStr = self.getTimeString(return_sec=True)
        self.timeList.append(timeStr)
        self.current_run_lap_times.append(timeSecStr)
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

    def getTimeString(self, return_sec=False):
        minStr = ("0"+str(self.accMin))[-2:]
        secStr = ("0"+str(self.accSec))[-2:]
        fracSecStr = ("0"+str(self.accFracSec))[-2:]
        if return_sec:
            return "{}:{}:{}".format(minStr, secStr, fracSecStr), (self.accMin * 60 + self.accSec + self.accFracSec/100.0)
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
    global export_data
    try:
        export_data = pd.concat(timer.export_ls, axis=0)
    except:
        print("Concat error. Likely forgot to press button to track the run")

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

# output to csv
print(export_data)
# export_data.to_csv("data.csv") # this part is just a placeholder, the name should be dynamic (current timestamp) etc. I'll handle it later