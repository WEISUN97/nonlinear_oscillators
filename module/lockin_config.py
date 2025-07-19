class LockinController:
    def __init__(self, daq, device):
        self.daq = daq
        self.device = device

    def configure_modulation(
        self,
        carrier=1000000,
        sideband_freqs=68000,
        filter_order=8,
        output_range=1,
        output_amplitude1=0.2,
        output_amplitude2=0.5,
    ):
        # carrier frequency
        self.daq.setDouble("/dev1657/oscs/0/freq", carrier)
        # sideband frequencies
        self.daq.setDouble("/dev1657/oscs/1/freq", sideband_freqs)

        # low pass filter order
        self.daq.setInt("/dev1657/mods/0/carrier/order", filter_order)
        self.daq.setInt("/dev1657/mods/0/sidebands/0/order", filter_order)
        self.daq.setInt("/dev1657/mods/0/sidebands/1/order", filter_order)

        self.daq.setDouble("/dev1657/demods/0/rate", 1000.00000000)
        # drive output
        self.daq.setDouble("/dev1657/sigouts/0/range", output_range)
        self.daq.setDouble("/dev1657/sigouts/0/amplitudes/7", output_amplitude1)
        # # modulation output
        self.daq.setDouble("/dev1657/sigouts/1/range", output_range)
        self.daq.setDouble("/dev1657/sigouts/1/amplitudes/6", output_amplitude2)
