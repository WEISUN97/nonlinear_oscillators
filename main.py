from zhinst.core import ziDAQServer
from module.scope import ScopeController
from module.sweeper import SweeperController
from module.lockin_config import LockinController
from module.tools import save_sweep_to_csv, plot_sweep


amp2 = [0.1, 0.5]  # Amplitude for modulation output
amp1 = [0.02, 0.05, 0.1, 0.2, 0.5]  # Amplitude for drive output
frerange = [[60000, 90000], [63500, 64500], [70000, 80000], [71500, 72500]]


def main():
    device = "dev1657"
    daq = ziDAQServer("127.0.0.1", 8005, 1)

    # Lock-in configuration
    lockin = LockinController(daq, device)

    for i in range(len(amp1)):
        for j in range(len(amp2)):
            for k in range(len(frerange)):
                start = frerange[k][0]
                stop = frerange[k][1]
                samplecount = stop - start
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
                    xmapping=1,  # 0: linear, 1: logarithmic
                )

                result = sweeper.run()
                sweeper.stop()
                suffix = f"amp{output_amplitude1}V"
                data = save_sweep_to_csv(
                    result, device, demod="1", ifplot=True, suffix=suffix
                )

    # Stop the lock-in outputs
    daq.setInt("/dev1657/sigouts/0/on", 0)
    daq.setInt("/dev1657/sigouts/1/on", 0)


if __name__ == "__main__":
    main()
