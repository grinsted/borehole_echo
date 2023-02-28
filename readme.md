
At EastGRIP we want to sense the liquid level in the borehole using sound. This project is intended as a GUI for a software that sends out a chirp every ~2secs and records the echo and visualizes it. 


## dependencies
* numpy
* pyqt (5?)
* pyqtgraph
* sounddevice, soundfile
* ????


# files

* gui.py: the main file with the GUI.
* playrec_worker.py: a worker that plays and records chirps.
* settings.py: misc settings 
* find_sounddevices.py: used to find the first/best matching device from a prioritized list of device names. 


# TODO:

* record all inputs to a file. 
    - Ideally compressed in some way. I've not found nice simple libraries to deal with infinite streams. We could use subprocess to pipe into ffmpeg (like i use for dailyglacier videos)?





Aslak Grinsted 2022
