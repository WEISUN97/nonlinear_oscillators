class LockinController:
    def __init__(self, daq, device):
        self.daq = daq
        self.device = device

    def configure_outputs(self):
        self.daq.setInt(f"/{self.device}/sigouts/0/on", 1)
        self.daq.setDouble(f"/{self.device}/sigouts/0/amplitudes/7", 0.5)

    def configure_modulation(self):
        self.daq.setInt(f"/{self.device}/mods/0/enable", 1)
        self.daq.setDouble(f"/{self.device}/oscs/1/freq", 59000.0)
