"""

"""
import numpy as np


inputdevice = None
outputdevice = None
fs = 44100
timewindow = 0.5  # time between chirps


def soundspeed(T):
    Tref = 0
    return 331.4 * np.sqrt((273.15 + T) / (273.15 + Tref))


meters_per_second = soundspeed(T=-30)  # speed of sound

# -----
display_distance = 60.0  # meter
display_timewindow = display_distance / meters_per_second  # seconds.
