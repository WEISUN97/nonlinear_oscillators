from zhinst.core import ziDAQServer
from module.scope import ScopeController
from module.sweeper import SweeperController
from module.lockin_config import LockinController
from module.tools import save_sweep_to_csv


amp2 = [0.4]  # Amplitude for modulation output
amp1 = [1.25, 1, 0.75, 0.5]  # Amplitude for drive output
frerange = [[61500, 63000]]


def main():
    device = "dev1657"
    daq = ziDAQServer("127.0.0.1", 8005, 1)
    daq.setInt("/dev1657/sigouts/0/on", 1)
    daq.setInt("/dev1657/sigouts/1/on", 1)
    # Lock-in configuration
    lockin = LockinController(daq, device)

    for i in range(len(amp1)):
        for j in range(len(amp2)):
            for k in range(len(frerange)):
                start = frerange[k][0]
                stop = frerange[k][1]
                samplecount = 1500
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
                    maxbandwidth=1,
                    xmapping=0,  # 0: linear, 1: logarithmic
                    settling_time=0,  # seconds
                    inaccuracy=0.00001,
                    bandwidthcontrol=2,  # 0: manual, 1: fixed, 2: auto
                    bandwidth=1,  # Hz
                )

                result = sweeper.run()
                sweeper.stop()
                suffix = f"amp{output_amplitude1}V"
                demod = save_sweep_to_csv(
                    result, device, demod=["1"], ifplot=True, suffix=suffix
                )

    # Stop the lock-in outputs
    daq.setInt("/dev1657/sigouts/0/on", 0)
    daq.setInt("/dev1657/sigouts/1/on", 0)


if __name__ == "__main__":
    main()
