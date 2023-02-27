
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
* settings.py: settings 
* list_sounddevices.py: prints out the names and details of all the sounddevices connected to the system. 


# TODO:

* record all inputs to a file. 
* respect input/output device names when starting playrec_worker. Should it fallback to default devices (?), should it allow regexps?



Aslak Grinsted 2022
