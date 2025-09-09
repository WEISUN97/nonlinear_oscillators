from zhinst.core import ziDAQServer
from module.lockin_config import LockinController
import numpy as np
from module.setting_read import generate_setting, create_allsettings_json
from module.tools import (
    save_sweep_to_csv,
    create_new_folder,
    plot_sweep,
    create_data_json,
)
from module.json_merge import merge_demods_from_files
import time

setting = {
    "amp1": [1],  # Amplitude for modulation output
    "amp2": [0.002],
    # Amplitude for driven output
    "frerange": [[56200, 56250]],  # Frequency range for sweeper
    "bandwidth": 1,  # Bandwidth for sweeper
    "samplecount": 200,  # Number of result for sweeper
    "output_range1": 1,  # Output range for modulation output
    "output_range2": 1,  # Output range for driven output
    "demods": ["1", "2", "3"],  # Demodulator channels to use
    "wait_time": 0.2,  # Wait time after setting frequency
}
foldername = "250909_01"
list1 = []
timestamps = []


def main(params={}, basepath="./results"):
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
    samplecount = params.get("samplecount")
    output_range1 = params.get("output_range1")
    output_range2 = params.get("output_range2")
    demods = params.get("demods")
    wait_time = params.get("wait_time")

    start = frerange[0]
    stop = frerange[1]
    output_amplitude1 = amp1
    output_amplitude2 = amp2
    lockin.configure_modulation(
        filter_order=8,
        output_amplitude1=output_amplitude1,
        output_amplitude2=output_amplitude2,
        output_range1=output_range1,
        output_range2=output_range2,
    )
    result = {
        device: {
            "demods": {
                d: {"sample": [[{"frequency": [], "r": [], "phase": []}]]}
                for d in demods
            }
        }
    }
    counter = 1
    for f in np.linspace(start, stop, samplecount):
        daq.set("/dev1657/oscs/1/freq", f)
        for d in demods:
            sample = daq.getSample(f"/{device}/demods/{d}/sample")
            X = sample["x"][0]
            Y = sample["y"][0]
            R = np.abs(X + 1j * Y)
            Theta = np.arctan2(Y, X)
            demod_data = result[device]["demods"][d]["sample"][0][0]
            demod_data["frequency"].append(f)
            demod_data["r"].append(R)
            demod_data["phase"].append(Theta)
        print(f"Progress: {(counter / samplecount * 100):.2f}%")
        time.sleep(wait_time)
        counter += 1

    suffix = f"_amp1_{output_amplitude1}_amp2_{output_amplitude2}"
    path, timestamp = create_new_folder(base_path=basepath, suffix=suffix)
    create_data_json(result=result, path=path, timestamp="alldatas_" + timestamp)
    list1.append(f"{timestamp}{suffix}")
    timestamps.append(timestamp)
    create_allsettings_json(path=path, timestamp=timestamp)
    generate_setting(setting=params, filename=timestamp, folder=path)
    df = save_sweep_to_csv(
        result,
        device,
        demod=demods,
        suffix=suffix,
        path=path,
        timestamp=timestamp,
    )
    plot_sweep(df, path=path, timestamp=timestamp, demod=["1"])
    return daq


if __name__ == "__main__":
    basepath, t = create_new_folder(base_path="./results", suffix=foldername)
    setting_one = {}
    setting_one = setting.copy()
    for i in range(len(setting["amp1"])):
        setting_one["amp1"] = setting["amp1"][i]
        for j in range(len(setting["amp2"])):
            setting_one["amp2"] = setting["amp2"][j]
            # for k in range(len(setting["frerange"])):
            setting_one["frerange"] = setting["frerange"][i]
            print(f"Running with settings: {setting_one}")
            daq = main(params=setting_one, basepath=basepath)
    # Stop the lock-in outputs
    daq.setInt("/dev1657/sigouts/0/on", 0)
    daq.setInt("/dev1657/sigouts/1/on", 0)

    merged = merge_demods_from_files(
        timestamps,
        list1,
        device_id="dev1657",
        demod_ids=("1", "2", "3"),
        fields=("frequency", "x", "y", "r", "phase"),
        parent_folder=basepath,
        whole_name=list1,
    )
    # generate file name
    data = {"file_name": list1}
    create_data_json(
        result=data, path=basepath, timestamp=f"{foldername}_all_file_names"
    )
    print(list1)
