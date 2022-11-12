"""
    Borehole echo gui
    Aslak Grinsted 2022
"""
import sys

import numpy as np
import sounddevice as sd
import soundfile as sf
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIcon, QImage, QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QWidget, QMainWindow
import playrec_worker
import pyqtgraph as pg
import settings


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Borehole echo GUI")
        self.setGeometry(64, 64, 700, 700)
        self.setWindowIcon(QIcon("assets/icon.png"))

        self.textLabel = QLabel(self)
        self.textLabel.setText("Hello World!")
        self.textLabel.move(10, 10)

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)
        self.line_data = self.graphWidget.plot(np.array([0, 0]))
        font = QFont()
        font.setPixelSize(24)
        font.setBold(True)
        self.graphWidget.getAxis("bottom").setTickFont(font)

        button = QPushButton("Start button", self)
        button.move(2, 2)
        button.clicked.connect(self.on_click)

        self.thread = QThread()
        self.worker = playrec_worker.PlayRecWorker(timewindow=settings.timewindow, fs=settings.fs)
        self.chirp = self.worker.chirp.copy()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.start)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.echoreceived.connect(self.echoreceived)

        self.show()

    def echoreceived(self, recording):
        c = np.abs(np.convolve(recording, self.chirp))
        max_ix = int(settings.display_timewindow * settings.fs)
        c = c[:max_ix]
        x = np.arange(0, max_ix) * settings.meters_per_second / settings.fs
        ix = np.argmax(c)
        print(f"{ix}frames\t{x[ix]}m")
        self.line_data.setData(x, c)

    @pyqtSlot()
    def on_click(self):
        self.thread.start()
        print("PyQt5 button click")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("QWidget{font-size: 18pt;}")
    mainwindow = App()
    sys.exit(app.exec_())
