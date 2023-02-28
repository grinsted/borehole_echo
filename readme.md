
At EastGRIP we want to sense the liquid level in the borehole using sound. This project is intended as a GUI for a software that sends out a chirp every ~2secs and records the echo and visualizes it. 


## dependencies
* numpy
* pyqt (5?)
* pyqtgraph
* sounddevice, soundfile
* ????


# files

* gui.py: the main file with the GUI.
* playrec_worker.py: a worker that plays and records chirps. This will run it is own thread and trigger pyqtsignals to 
* settings.py: misc settings 
* find_sounddevices.py: used to find the first/best matching device from a prioritized list of device names. 




# TODO:

* record all inputs to a file. Ideally compressed in some way. I've not found nice simple libraries to deal with infinite streams. We could use subprocess to pipe into ffmpeg (like i use for dailyglacier videos)?
  - in the currently_unused_code/stream_encoder.py i have a little test showing how you can pipe data to ffmpeg and it will encode it as an ogg file. This functionality should probably be encapsulated in a separate worker thread so that it does not interfere with the GUI too much. 





Aslak Grinsted 2023
