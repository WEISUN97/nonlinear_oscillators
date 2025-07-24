import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os


def save_sweep_to_csv(result, device, demod=["1"], ifplot=True, suffix=""):
    """
    Save sweep result of specified demodulator to CSV.

    Parameters:
        result (dict): Result from sweeper.read()
        device (str): e.g. 'dev1657'
        demod list(str): demodulator index, e.g. ['0', '1', ...]
        save_path (str): Output CSV file path
    """
    timestamp = datetime.now().strftime("%y%m%d%H%M")
    combined_df = None
    try:
        for d in demod:
            sample_data = result[device]["demods"][d]["sample"][0][0]
            freq = sample_data["grid"]
            amplitude = sample_data["r"]
            phase = sample_data["phase"]

            df = pd.DataFrame(
                {
                    "Frequency_Hz": freq,
                    f"Amplitude_d{d}": amplitude,
                    f"Phase_rad_d{d}": phase,
                }
            )

            if combined_df is None:
                combined_df = df
            else:
                # Merge on Frequency
                combined_df = pd.merge(combined_df, df, on="Frequency_Hz")

            print(f"Saved demod {d} data.")

        # If plotting is enabled, plot the sweep data
        if ifplot:
            save_path_plot = f"./results/figure/sweepplot_{timestamp}{suffix}.png"
            plot_sweep(combined_df, save_path=save_path_plot, demod=demod)
    except KeyError as e:
        print(f"Demodulator {demod} not found in result. Error: {e}")

    if combined_df is not None:
        file_name = f"sweep_all_{timestamp}{suffix}.csv"
        save_path = f"./results/data/{file_name}"
        combined_df.to_csv(save_path, index=False)
        print(f"All data saved to {save_path}")
        return combined_df
    else:
        print("No data saved.")
        return None


def plot_sweep(df, save_path="", demod=["1", "3"]):
    title = "Sweep Result"
    if not save_path:
        timestamp = datetime.now().strftime("%y%m%d%H%M")
        file_name = f"sweepplot_{timestamp}.png"
        save_path = f"./results/figure/{file_name}"
    amp_cols = [col for col in df.columns if "Amplitude" in col]
    # print(f"Plotting columns: {amp_cols}")
    # print(df)

    plt.figure(figsize=(10, 6))
    for col in amp_cols:
        plt.plot(df["Frequency_Hz"], df[col], label=col)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude (V)")
    plt.title(title)
    legend_labels = [f"Demod {int(d)+1}" for d in demod]
    plt.legend(legend_labels)
    plt.grid(True)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300)
        print(f"Plot saved to: {save_path}")
    else:
        plt.show()


def plot_from_csv(csv_path, column_indices=None, save_path=""):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    df = pd.read_csv(csv_path)

    if "Frequency_Hz" not in df.columns:
        raise ValueError("CSV must contain a 'Frequency_Hz' column.")

    # Get list of column names
    columns = df.columns.tolist()

    # Determine which columns to plot
    if column_indices is None:
        plot_columns = [col for col in columns if col != "Frequency_Hz"]
    else:
        plot_columns = []
        for idx in column_indices:
            if idx < 0 or idx >= len(columns):
                raise IndexError(f"Column index {idx} is out of range.")
            if columns[idx] != "Frequency_Hz":
                plot_columns.append(columns[idx])
    print(f"Plotting columns: {plot_columns}")

    # Plot
    plt.figure(figsize=(10, 6))
    for col in plot_columns:
        plt.plot(df["Frequency_Hz"], df[col], label=col)

    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Value")
    plt.title("Selected Columns vs Frequency")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300)
        print(f"Plot saved to: {save_path}")
    else:
        plt.show()
