import sounddevice as sd


def choose_device(device_priority_list=["default"], kind="output"):
    """
    Give this function a prioritized list of device names.

    It will also accept partial matches.
    - the key "default" will select the default output device on the first hostapi.

    """
    # 1) Construct a list of devices.
    # 2) add a fullname that contains both the "[device name], [hostapi-name]"
    # 3) filter on input/output
    hostapis = sd.query_hostapis()
    devs = list(sd.query_devices())  # full list of devices
    for ix, dev in enumerate(devs):
        dev["fullname"] = f"{dev['name']}, {hostapis[dev['hostapi']]['name']}"
        dev["device_index"] = ix  # not used?

    devs = list(filter(lambda d: d[f"max_{kind}_channels"] > 0, devs))  # only input or output devices.

    selected = ""
    for q in device_priority_list:
        if q == "default":
            default_ix = hostapis[0][f"default_{kind}_device"]
            candidates = list(filter(lambda d: d[f"device_index"] == default_ix, devs))
        else:
            candidates = list(filter(lambda d: d[f"fullname"].lower().startswith(q.lower()), devs))
        if len(candidates) > 0:
            # if there is more than one candidate, then pick the low-latency one
            candidates = sorted(candidates, key=lambda d: d[f"default_low_{kind}_latency"])
            selected = candidates[0]
            break
    if not selected:
        # No matches!
        # print a list and raise an error
        print(f"\n   valid {kind}-devices:".upper())
        print("=" * 50)
        for dev in devs:
            print(f"- {dev['fullname']}")

        raise Exception(f"No {kind}-devices match {repr(device_priority_list)}!")

    return selected


if __name__ == "__main__":

    1 / 0
    try:
        choose_device(device_priority_list=[], kind="output")
    except:
        pass
    print("---")
    try:
        choose_device(device_priority_list=[], kind="input")
    except:
        pass
