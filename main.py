from zhinst.core import ziDAQServer
from module.scope import ScopeController
from module.sweeper import SweeperController
from module.lockin_config import LockinController
from module.setting_read import generate_setting, create_json_file
from module.tools import save_sweep_to_csv, create_new_folder, plot_sweep


setting = {
    "amp1": [0.5],  # Amplitude for drive output
    "amp2": [0.4],  # Amplitude for modulation output
    "frerange": [[60000, 63000]],  # Frequency range for sweeper
    "bandwidth": 1,  # Bandwidth for sweeper
    "inaccuracy": 0.00001,  # Inaccuracy for sweeper
    "maxbandwidth": 100,  # Maximum bandwidth for sweeper
    "samplecount": 10,  # Number of samples for sweeper
}


def main(params={}):
    device = "dev1657"
    daq = ziDAQServer("127.0.0.1", 8005, 1)
    daq.setInt("/dev1657/sigouts/0/on", 1)
    daq.setInt("/dev1657/sigouts/1/on", 1)
    # MOD
    daq.set("/dev1657/mods/0/enable", 1)

    # Lock-in configuration
    lockin = LockinController(daq, device)
    amp1 = params.get("amp1")
    amp2 = params.get("amp2")
    frerange = params.get("frerange")
    bandwidth = params.get("bandwidth")
    inaccuracy = params.get("inaccuracy")
    maxbandwidth = params.get("maxbandwidth")
    samplecount = params.get("samplecount")

    for i in range(len(amp1)):
        for j in range(len(amp2)):
            for k in range(len(frerange)):
                start = frerange[k][0]
                stop = frerange[k][1]
                samplecount = samplecount
                output_amplitude1 = amp1[i]
                output_amplitude2 = amp2[j]
                lockin.configure_modulation(
                    filter_order=8,
                    output_amplitude1=output_amplitude1,
                    output_amplitude2=output_amplitude2,
                )

                # Sweeper
                sweeper = SweeperController(
                    daq,
                    device,
                    gridnode=f"/{device}/oscs/1/freq",
                )
                sweeper.configure(
                    start=start,
                    stop=stop,
                    samplecount=samplecount,
                    maxbandwidth=maxbandwidth,
                    xmapping=0,  # 0: linear, 1: logarithmic
                    settling_time=0,  # seconds
                    inaccuracy=inaccuracy,
                    bandwidthcontrol=2,  # 0: manual, 1: fixed, 2: auto
                    bandwidth=bandwidth,  # Hz
                )

                result = sweeper.run()
                sweeper.stop()
                suffix = f"amp{output_amplitude1}V"
                generate_setting
                path, timestamp = create_new_folder()
                create_json_file(path=path, timestamp=timestamp)
                generate_setting(setting=setting, filename=timestamp, folder=path)
                df = save_sweep_to_csv(
                    result,
                    device,
                    demod=["1"],
                    suffix=suffix,
                    path=path,
                    timestamp=timestamp,
                )
                plot_sweep(df, path=path, timestamp=timestamp, demod=["1"])

    # Stop the lock-in outputs
    daq.setInt("/dev1657/sigouts/0/on", 0)
    daq.setInt("/dev1657/sigouts/1/on", 0)


if __name__ == "__main__":
    main(params=setting)
