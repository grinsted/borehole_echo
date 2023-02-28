import subprocess as sp
import numpy as np

"""
an experiment in how to pipe into an ogg file. 

"""


def chirp(tmax=0.035, f1=22000, f2=1000, fs=44100):
    """
    generates a chirp waveform. (it is time reversed because that sounds better.)

    Currently it generates a complex numbered waveform.
    - The real part should be played.
    - The echo can be correlated with the either the real part or the full complex waveform.
      (If the complex waveform is used then we can measure the phase shift of the returned echo.
      But we dont expect a phase shift, and in that case maybe only the real part is needed.)

    """
    f = np.exp(np.linspace(np.log(2 * np.pi * f1 / fs), np.log(2 * np.pi * f2 / fs), int(tmax * fs)))
    phase = np.cumsum(f)
    amp = np.tanh(np.sin(np.linspace(0, np.pi, len(f))) * 10)
    c = np.cos(phase) * amp
    s = np.sin(phase) * amp
    return s + 1j * c


testsound = np.real(chirp())
outputfname = "test.ogg"

p = sp.Popen(
    [
        "ffmpeg",
        # "-hide_banner",
        # "-loglevel",
        # "warning",
        "-nostats",
        "-y",
        "-f",
        "f32le",  # FORMAT: just assume that we have little endian,
        "-ar",
        "44100",
        "-ac",
        "1",  # MONO
        "-channel_layout",
        "mono",
        "-i",
        "-",  # use pipe
        "-acodec",
        "libvorbis",
        outputfname,
    ],
    stdin=sp.PIPE,
    bufsize=int(1e6),
)
p.stdin.write(np.float32(testsound))
p.stdin.flush()

p.stdin.close()
p.wait()
