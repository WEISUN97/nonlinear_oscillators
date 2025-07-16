from zhinst.core import ziDAQServer
from module.scope import ScopeController
from module.sweeper import SweeperController
from module.lockin_config import LockinController


def main():
    device = "dev1657"
    daq = ziDAQServer("127.0.0.1", 8005, 1)

    # Lock-in configuration
    lockin = LockinController(daq, device)
    lockin.configure_outputs()
    lockin.configure_modulation(filter_order=8)

    # Sweeper
    sweeper = SweeperController(daq, device)
    sweeper.configure(
        gridnode=f"/{device}/oscs/1/freq",
        start=55000,
        stop=63000,
        samplecount=1000,
        bandwidth=1000,
        xmapping=0,
        save_dir=r"C:\your\save\path",
    )

    result = sweeper.run()

    # scope.stop()
    # sweeper.stop()

    # print("Scan complete.")

    # # Scope
    # scope = ScopeController(daq, device, save_dir=r"C:\your\save\path")
    # scope.configure()


if __name__ == "__main__":
    main()
