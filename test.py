from zhinst.core import ziDAQServer
from module.scope import ScopeController
from module.sweeper import SweeperController
from module.lockin_config import LockinController
from module.tools import save_sweep_to_csv, create_new_folder, plot_sweep
import time

params = {
    "amp1": 1,  # Amplitude for modulation output
    "amp2": 0.001,
    # Amplitude for driven output
    "frerange": [56293, 56303],  # Frequency range for sweeper
    "bandwidth": 1,  # Bandwidth for sweeper
    "inaccuracy": 0.00001,  # Inaccuracy for sweeper
    "maxbandwidth": 0.5,  # Maximum bandwidth for sweeper
    "samplecount": 200,  # Number of samples for sweeper
    "settling_time": 0,  # Settling time for sweeper
    "bandwidthcontrol": 2,  # 0: manual, 1: fixed, 2: auto
    "demods": ["1", "2", "3"],  # Demodulator channels to use
    "avagering_sample": 10,
    "output_range1": 1,  # Output range for modulation output
    "output_range2": 1,  # Output range for driven output
}

device = "dev1657"
daq = ziDAQServer("127.0.0.1", 8005, 1)
daq.setInt("/dev1657/sigouts/0/on", 1)
daq.setInt("/dev1657/sigouts/1/on", 1)
# MOD
daq.set("/dev1657/mods/0/enable", 1)
lockin = LockinController(daq, device)
amp1 = params.get("amp1")
amp2 = params.get("amp2")
frerange = params.get("frerange")
bandwidth = params.get("bandwidth")
inaccuracy = params.get("inaccuracy")
maxbandwidth = params.get("maxbandwidth")
samplecount = params.get("samplecount")
settling_time = params.get("settling_time")
bandwidthcontrol = params.get("bandwidthcontrol")
demods = params.get("demods")
avagering_sample = params.get("avagering_sample")
output_range1 = params.get("output_range1")
output_range2 = params.get("output_range2")

start = frerange[0]
stop = frerange[1]
samplecount = samplecount
output_amplitude1 = amp1
output_amplitude2 = amp2
lockin.configure_modulation(
    filter_order=8,
    output_amplitude1=output_amplitude1,
    output_amplitude2=output_amplitude2,
    output_range1=output_range1,
    output_range2=output_range2,
)
samples = []
wait_time = 0.1  # seconds
for f in range(frerange[0], frerange[1]):
    daq.set("/dev1657/oscs/1/freq", f)
    sample = daq.getSample(f"/{device}/demods/1/sample")
    X = sample["x"][0]
    Y = sample["y"][0]
    print(X)
    samples.append(sample)
    time.sleep(wait_time)
