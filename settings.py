import numpy as np
from find_sounddevice import choose_device

# prioritized lists of preferred devices...
inputdevice = ["focusrite", "default"]
outputdevice = ["focusrite", "default"]

# select the first matching device
inputdevice = choose_device(inputdevice, kind="input")["fullname"]

outputdevice = choose_device(outputdevice, kind="output")["fullname"]
print(inputdevice)
print(outputdevice)
fs = 44100  # sample rate...
timewindow = 0.5  # time between chirps (SHOULD be ~2secs )


def soundspeed(T):
    Tref = 0
    return 331.4 * np.sqrt((273.15 + T) / (273.15 + Tref))


meters_per_second = 0.5 * soundspeed(T=-30)  # speed of sound halved because we deal with two-way-travel-time.


display_distance = 60.0  # meter
display_timewindow = display_distance / meters_per_second  # seconds.

# you are not allowed to display more than the time between chirps:
display_timewindow = np.min((display_timewindow, timewindow))
