import sounddevice as sd

devices = sd.query_devices()

print("SOUND DEVICEs\n===========")
print(devices)

inputdev = sd.query_devices(kind="input")
print("default input dev:", inputdev["name"])
