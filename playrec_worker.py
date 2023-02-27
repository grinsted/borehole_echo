"""
    A QT worker that plays a chirp and records the echo.

    It works by having a fixed circular play and record buffer.

    When the recording buffer loops then it triggers a callback.
    (takes into account the latency reported by the system.).

    The two buffers have equal length. The play-buffer is mostly 
    silent except for a short chirp in the beginning. 

    Aslak Grinsted 2022
"""

import atexit

import numpy as np
import sounddevice as sd
import soundfile as sf
from PyQt5.QtCore import QObject, pyqtSignal
import settings


def chirp(tmax=0.035, f1=22000, f2=1000, fs=44100):
    f = np.exp(np.linspace(np.log(2 * np.pi * f1 / fs), np.log(2 * np.pi * f2 / fs), int(tmax * fs)))
    phase = np.cumsum(f)
    amp = np.tanh(np.sin(np.linspace(0, np.pi, len(f))) * 10)
    c = np.cos(phase) * amp
    s = np.sin(phase) * amp
    return s + 1j * c


class PlayRecWorker(QObject):

    finished = pyqtSignal()
    echoreceived = pyqtSignal(np.ndarray)

    def __init__(self, chirp_waveform=None, fs=44100, timewindow=2.0):
        super().__init__()
        if not chirp_waveform:
            chirp_waveform = chirp()
        self.chirp = chirp_waveform
        data = np.append(np.real(chirp_waveform), np.zeros(int(fs * timewindow) - len(chirp_waveform)))
        self.soundloop = data
        self.fs = fs
        # have a recording buffer exactly as long as the soundloop.
        self.recordbuffer = np.zeros(len(data))
        self.stream = None
        self.play_position = 0
        self.rec_position = 0
        atexit.register(self.stop)

    def start(self):
        self.stop()
        self.stream = sd.Stream(samplerate=self.fs, channels=1, callback=self.stream_callback, latency="low")  # , device=("FocusRite", "Speaker/HP"))
        total_latency = np.sum(np.array(self.stream.latency))
        self.play_position = 0
        self.rec_position = -int(total_latency * self.fs) % len(self.recordbuffer)
        self.stream.start()

    def stop(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None

    def stream_callback(self, indata, outdata, frames, time, status):
        indata = indata.ravel()
        out = outdata.ravel()
        if status:
            print(status)
        next_playpos = self.play_position + frames
        next_recpos = self.rec_position + frames
        # output buffer
        if next_playpos <= len(self.soundloop):
            out[:] = self.soundloop[self.play_position : next_playpos]
        else:
            # we've reached the end
            wrap_at = len(self.soundloop) - self.play_position
            out[:wrap_at] = self.soundloop[self.play_position :]
            next_playpos = frames - wrap_at
            out[wrap_at:] = self.soundloop[:next_playpos]
        # -rec buffer-
        if next_recpos <= len(self.recordbuffer):
            self.recordbuffer[self.rec_position : next_recpos] = indata
        else:
            # we've reached the end and must fire an event with the recorded echo and loop
            wrap_at = len(self.recordbuffer) - self.rec_position
            self.recordbuffer[self.rec_position :] = indata[:wrap_at]
            # EMIT...
            self.echoreceived.emit(self.recordbuffer)
            # fill rest....
            next_recpos = frames - wrap_at
            self.recordbuffer[:next_recpos] = indata[wrap_at:]

        self.play_position = next_playpos
        self.rec_position = next_recpos


if __name__ == "__main__":
    # test code
    print(sd.query_devices())
    worker = PlayRecWorker()
    worker.start()
    import time

    time.sleep(4)
    worker.stop()
    print("done")
