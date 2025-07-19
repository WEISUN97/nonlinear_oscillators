import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


def save_sweep_to_csv(result, device, demod="0", ifplot=True, suffix=""):
    """
    Save sweep result of specified demodulator to CSV.

    Parameters:
        result (dict): Result from sweeper.read()
        device (str): e.g. 'dev1657'
        demod (str): demodulator index, e.g. '0', '1', ...
        save_path (str): Output CSV file path
    """

    try:
        sample_data = result[device]["demods"][demod]["sample"][0][0]

        freq = sample_data["grid"]
        amplitude = sample_data["r"]
        phase = sample_data["phase"]

        df = pd.DataFrame(
            {"Frequency_Hz": freq, "Amplitude": amplitude, "Phase_rad": phase}
        )
        timestamp = datetime.now().strftime("%y%m%d%H%M")
        file_name = f"sweep_{timestamp}{suffix}.csv"
        save_path = f"./results/data/{file_name}"
        df.to_csv(save_path)
        print(f"Saved demod {demod} data")

        # If plotting is enabled, plot the sweep data
        if ifplot:
            save_path_plot = f"./results/figure/sweepplot_{timestamp}{suffix}.png"
            plot_sweep(
                df, title=f"Sweep Result - Demod {demod}", save_path=save_path_plot
            )

        return df
    except KeyError as e:
        print(f"Demodulator {demod} not found in result. Error: {e}")


def plot_sweep(df, title="Sweep Result", save_path=""):
    if not save_path:
        timestamp = datetime.now().strftime("%y%m%d%H%M")
        file_name = f"sweepplot_{timestamp}.png"
        save_path = f"./results/figure/{file_name}"
    plt.figure(figsize=(8, 5))
    plt.plot(df["Frequency_Hz"], df["Amplitude"])
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude (V)")
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300)
        print(f"Plot saved to: {save_path}")
    else:
        plt.show()
