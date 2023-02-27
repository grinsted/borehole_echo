"""\

This script is currently unused! 


The intent of it was to make a settings window where you could select the sound device you want to use. 

"""

import sys

import numpy as np
import sounddevice as sd
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class DevicePicker(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        layout = QVBoxLayout(self)

        # nice widget for editing the date
        textLabel = QLabel(self)
        textLabel.setText("Input device:")
        layout.addWidget(textLabel)
        self.inputdevicecombo = QComboBox()
        for ix, dev in enumerate(sd.query_devices()):
            if dev["max_input_channels"] > 0:
                self.inputdevicecombo.addItem(f"#{ix}: {dev['name']}")
        layout.addWidget(self.inputdevicecombo)

        textLabel = QLabel(self)
        textLabel.setText("Output device:")
        layout.addWidget(textLabel)
        self.outputdevicecombo = QComboBox()
        for ix, dev in enumerate(sd.query_devices()):
            if dev["max_output_channels"] > 0:
                self.outputdevicecombo.addItem(f"#{ix}: {dev['name']}")
        layout.addWidget(self.outputdevicecombo)

        # OK and Cancel buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    # get current date and time from the dialog
    def input_device(self):
        return self.inputdevicecombo.currentText()

    # static method to create the dialog and return (date, time, accepted)
    @staticmethod
    def getDevices(parent=None):
        dialog = DevicePicker(parent)
        result = dialog.exec_()
        inputdevice = dialog.input_device()
        return inputdevice


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("QWidget{font-size: 18pt;}")
    val = DevicePicker.getDevices()
    print(val)
