"""

"""

inputdevice = None
outputdevice = None
fs = 44100
timewindow = 2.0


import numpy as np
Tref = 0
Tegrip = -30
speed_of_sound = 331.4 * np.sqrt((273.15 + Tegrip) / (273.15 + Tref))

meters_per_second = speed_of_sound  # speed of sound / 2 (note temperature dependence)
