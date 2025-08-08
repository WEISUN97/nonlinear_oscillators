from zhinst.core import ziDAQServer


def get_lockin_settings(
    host="127.0.0.1",
    port=8005,
    api_level=1,
    device="dev1657",
    path="",
) -> dict:
    """
    Read Zurich Instruments Lock-in Amplifier settings.

    Parameters:
        host     : LabOne Data Server host
        port     : LabOne Data Server port
        api_level: API version
        device   : Device ID, e.g. 'dev1657'

    Return:
        settings: dict of settings
    """
    daq = ziDAQServer(host, port, api_level)
    daq.connect()

    nodes_to_read = [
        f"/{device}/oscs/*",  # Oscillator
        f"/{device}/demods/*",  # Demodulator
        f"/{device}/sigouts/*",  # output settings
        f"/{device}/sigins/*",  # input settings
        f"/{device}/mods/*",  # modulation settings (if needed)
    ]

    settings = {}
    for node in nodes_to_read:
        try:
            data = daq.get(node)
            settings[node] = data
        except Exception as e:
            settings[node] = f"Error reading {node}: {e}"

    return settings


if __name__ == "__main__":
    DEVICE = "dev1657"
    cfg = get_lockin_settings()

    osc_data = cfg[f"/{DEVICE}/oscs/*"]
    print("OSC settings:", osc_data)
