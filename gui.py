"""
    Borehole echo gui

    This is the main GUI for the borehole echo depth sounder

    Aslak Grinsted 2023


"""
import sys

import numpy as np
import pyqtgraph as pg
from PyQt5.QtCore import QObject, Qt, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QFont, QIcon, QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPushButton
from PyQt5.QtWidgets import QSplitter, QTextEdit, QVBoxLayout, QWidget, QSizePolicy

import playrec_worker
import settings
from scipy.signal import find_peaks

import logging

logging.basicConfig(filename=r"boreholeechos.log", filemode="a", format="%(asctime)s %(levelname)s %(message)s", level=logging.INFO, force=True)


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
        self.line_data = self.graphWidget.plot(np.array([0, 0]), pen=(255, 230, 235), antialias=True)
        self.graphWidget.getAxis("left").setTickFont(font)
        self.graphWidget.invertY(True)
        self.graphWidget.setMouseEnabled(x=False)
        self.graphWidget.showGrid(y=True, alpha=0.5)
        # self.graphWidget.setLimits(xMin=0, xMax=1, minXRange=0, maxXRange=1)

        self.imageWidget = pg.PlotWidget()
        self.image = np.random.rand(200, 100)
        self.imageItem = pg.ImageItem(image=self.image)
        self.imageWidget.addItem(self.imageItem)
        self.imageWidget.showAxes(True)
        self.imageWidget.getAxis("left").setTickFont(font)
        self.imageWidget.invertY(True)
        self.imageWidget.setYLink(self.graphWidget)

        self.Hsplitter = QSplitter(Qt.Horizontal)
        # self.Hsplitter.addWidget(button)
        self.Hsplitter.addWidget(self.imageWidget)
        self.Hsplitter.addWidget(self.graphWidget)
        self.Hsplitter.setStretchFactor(0, 5)
        self.Hsplitter.setStretchFactor(1, 1)
        self.Hsplitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.button = QPushButton("Press to Pause.", self)  # make it start and stop.
        self.button.setCheckable(True)
        self.button.clicked.connect(self.on_click)
        self.button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        self.hbox = QHBoxLayout(self)
        self.label = QLabel()
        self.hbox.addWidget(self.button)  # bottom
        self.hbox.addWidget(self.label)  # bottom

        self.vbox = QVBoxLayout(self)
        self.vbox.addWidget(self.Hsplitter)  # top
        self.vbox.addLayout(self.hbox)  # bottom
        widget = QWidget()
        widget.setLayout(self.vbox)
        self.setCentralWidget(widget)

        # ------- setup play rec worker --------
        self.thread = QThread()
        self.audioworker = playrec_worker.PlayRecWorker(timewindow=settings.timewindow, fs=settings.fs)
        self.chirp = self.audioworker.chirp.copy()
        self.audioworker.moveToThread(self.thread)
        self.thread.started.connect(self.audioworker.start)
        self.audioworker.finished.connect(self.thread.quit)
        self.audioworker.finished.connect(self.audioworker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.audioworker.echoreceived.connect(self.echoreceived)
        self.thread.start()
        self.show()

    def echoreceived(self, recording):
        # c = np.abs(np.convolve(recording, np.flip(self.chirp), "valid"))  # use complex chirp to find phase of match.
        c = np.convolve(recording, np.flip(np.real(self.chirp)), "valid")  # insist on phase match
        # discard all data after the max displayed timewindow.
        max_ix = int(settings.display_timewindow * settings.fs)
        c = c[:max_ix]
        # Normalize returned echo with respect to highest peak
        c = c / np.max(c)
        # make a z-vector for each sample
        z = np.arange(0, max_ix) * settings.meters_per_second / settings.fs
        # try to find peaks. Require a peak separation distance of atleast 5meters.
        peaks, _ = find_peaks(c, distance=settings.fs * 5.0 / settings.meters_per_second, height=0.3)
        # require a min peak distance of 2m
        z = z - z[peaks[0]]
        if len(peaks) > 1:
            echodepth = z[peaks[1]]
            self.label.setText(f"{echodepth:.2f}m")
            logging.info(f"echodepth={echodepth:2f}")
        self.line_data.setData(c, z)
        if len(c) > self.image.shape[0]:
            self.image = np.zeros((len(c), 500))
        self.image = np.roll(self.image, -1, axis=1)
        self.image[:, -1] = c
        self.imageItem.setImage(self.image, autoLevels=False)
        self.imageItem.setRect(0, z[0], self.image.shape[1] * settings.timewindow, z[-1] - z[0])

    @pyqtSlot()
    def on_click(self):
        if self.button.isChecked():
            self.audioworker.stop()
            self.button.setText("Press to Start.")
        else:
            self.audioworker.start()
            self.button.setText("Press to Pause.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("QWidget{font-size: 18pt;}")
    mainwindow = App()
    sys.exit(app.exec_())
