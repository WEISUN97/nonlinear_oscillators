class LockinController:
    def __init__(self, daq, device):
        self.daq = daq
        self.device = device

    def configure_outputs(self):
        pass
        # self.daq.setInt(f"/{self.device}/sigouts/0/on", 1)
        # self.daq.setDouble(f"/{self.device}/sigouts/0/amplitudes/7", 0.5)

    def configure_modulation(
        self, carrier=1000000, sideband_freqs=68000, filter_order=8
    ):
        # carrier frequency
        self.daq.setDouble("/dev1657/oscs/0/freq", carrier)
        # sideband frequencies
        self.daq.setDouble("/dev1657/oscs/1/freq", sideband_freqs)

        # low pass filter order
        self.daq.setInt("/dev1657/mods/0/carrier/order", filter_order)
        self.daq.setInt("/dev1657/mods/0/sidebands/0/order", filter_order)
        self.daq.setInt("/dev1657/mods/0/sidebands/1/order", filter_order)
