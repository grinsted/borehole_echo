"""
    Borehole echo gui
    Aslak Grinsted 2022
"""
import sys

import numpy as np
import sounddevice as sd
import soundfile as sf
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot, Qt
from PyQt5.QtGui import QIcon, QImage, QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QWidget, QMainWindow
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QSplitter, QTextEdit, QLineEdit

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
        self.showMaximized()
        self.setWindowIcon(QIcon("assets/icon.png"))
        pg.setConfigOption("imageAxisOrder", "row-major")  # best performance

        font = QFont()
        font.setPixelSize(20)
        self.graphWidget = pg.PlotWidget()
        self.line_data = self.graphWidget.plot(np.array([0, 0]))
        self.graphWidget.getAxis("left").setTickFont(font)
        self.graphWidget.invertY(True)
        self.graphWidget.setLimits(minXRange=1)
        self.graphWidget.showGrid(y=True, alpha=0.3)

        self.imageWidget = pg.PlotWidget()
        self.image = np.random.rand(200, 100)
        self.imageItem = pg.ImageItem(image=self.image)
        self.imageWidget.addItem(self.imageItem)
        self.imageWidget.showAxes(True)
        self.imageWidget.getAxis("left").setTickFont(font)
        self.imageWidget.invertY(True)
        self.imageWidget.setYLink(self.graphWidget)

        button = QPushButton("Start button", self)
        button.move(2, 2)
        button.clicked.connect(self.on_click)

        self.Hsplitter = QSplitter(Qt.Horizontal)
        # self.Hsplitter.addWidget(button)
        self.Hsplitter.addWidget(self.imageWidget)
        self.Hsplitter.addWidget(self.graphWidget)

        self.vbox = QVBoxLayout(self)
        self.vbox.addWidget(self.Hsplitter)  # top
        self.vbox.addWidget(button)  # bottom
        widget = QWidget()
        widget.setLayout(self.vbox)
        self.setCentralWidget(widget)

        # ------- setup play rec worker --------
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
        c = c / np.max(c)
        z = np.arange(0, max_ix) * settings.meters_per_second / settings.fs
        ix = np.argmax(c)
        print(f"{ix}frames\t{z[ix]}m")
        self.line_data.setData(c, z)
        if len(c) > self.image.shape[0]:
            self.image = np.zeros((len(c), 500))
        self.image = np.roll(self.image, -1, axis=1)
        self.image[:, -1] = c
        self.imageItem.setImage(self.image, autoLevels=False)
        self.imageItem.setRect(0, z[0], self.image.shape[1] * settings.timewindow, z[-1] - z[0])
        print(len(c))

    @pyqtSlot()
    def on_click(self):
        self.thread.start()
        print("PyQt5 button click")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("QWidget{font-size: 18pt;}")
    mainwindow = App()
    sys.exit(app.exec_())
