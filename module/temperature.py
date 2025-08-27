import os
import serial
import time
from datetime import datetime
from tools import save_data_to_csv
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


class MK2000:
    def __init__(self, serial_port="COM4", baud_rate=115200, timeout=10):
        # Initialize serial connection
        self.mk2000 = serial.Serial(
            port=serial_port,
            baudrate=baud_rate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=timeout,
            xonxoff=False,  # No flow control
            rtscts=False,  # No RTS/CTS flow control
            dsrdtr=True,  # Data Terminal Ready on
        )
        # Check connection status
        print(f"Using port: {self.mk2000.port}")
        print(f"mk2000 Status: {'Open' if self.mk2000.is_open else 'Closed'}")

    def read_temperature_once(self, temperatures, start_time):
        if not self.mk2000.is_open:
            self.mk2000.open()
        # Send the identification command
        self.mk2000.write(b"*IDN?\n")
        idn_response = self.mk2000.readline().decode().strip()
        # print(f"Device ID: {idn_response}")

        # Send the command to read the current temperature
        self.mk2000.write(b"temp:ctemperature?\n")
        temp_response = self.mk2000.readline().decode().strip()
        # print(f"Temperature Response: {temp_response}")
        mk2000_record_time = time.perf_counter() - start_time
        try:
            temperature = float(temp_response)
            temperatures[1] += [temperature]
            # temperatures[0] += [mk2000_record_time]
            temperatures[0] += [datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")]
        except ValueError as ve:
            # close the connection
            self.close_connection()
            print(f"Error converting response to float: {temp_response} - {ve}")
        return temperatures

    def mk2000_read_temperature(
        self,
        duration=5,
        sample_rate=10,
        temperatures=[[], []],
        start_time=0,
        formatted_time="None",
    ):
        try:
            start_time2 = time.perf_counter() - start_time
            print(f"MK2000 start:{start_time2}")
            interval = 1 / sample_rate
            for _ in range(int(duration)):
                for _ in range(sample_rate):
                    start_time_temp = time.perf_counter()  # Start high-resolution timer

                    # Call the temperature recording function
                    self.read_temperature_once(temperatures, start_time)

                    # Calculate elapsed time
                    elapsed_time = time.perf_counter() - start_time_temp

                    # Sleep for the remaining time of the interval if needed
                    sleep_time = interval - elapsed_time
                    if sleep_time > 0:
                        time.sleep(
                            sleep_time
                        )  # Adjust sleep to maintain precise timing
                    else:
                        raise Exception(
                            "Function execution took longer than the interval."
                        )

        except Exception as e:
            # close the connection
            self.mk2000.close()
            print(f"Exception occurred: {e}")
        end_time2 = time.perf_counter() - start_time
        print(f"MK2000 end:{end_time2}")
        print(f"MK2000 worked: {end_time2-start_time2}s")
        current_date = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_path = f"./temperature/{formatted_time}/temperature_data{current_date}.csv"
        save_data_to_csv(
            csv_path,
            temperatures,
            titles=["Time", "Temperature"],
        )
        return temperatures, csv_path

    def close_mk2000(self):
        self.mk2000.close()
        print(f"MK2000 Status: {'Open' if self.mk2000.is_open else 'Closed'}")


def plot_temperature_from_csv(file_path=""):
    df = pd.read_csv(file_path, parse_dates=["Time"])
    plt.figure(figsize=(10, 5))
    plt.plot(df["Time"], df["Temperature"], marker="", linestyle="-")
    plt.title("Temperature over Time")
    plt.xlabel("Time")
    plt.ylabel("Temperature (°C)")
    plt.grid(True)

    time_values = df["Time"]
    num_ticks = 5
    tick_indices = list(
        range(0, len(time_values), max(1, len(time_values) // num_ticks))
    )
    tick_indices = tick_indices[:num_ticks]
    tick_labels = time_values.iloc[tick_indices]

    plt.xticks(tick_labels)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
    plt.xticks(rotation=45)

    plt.tight_layout()
    save_path = file_path.replace(".csv", ".png")
    plt.savefig(save_path)


# Example usage
if __name__ == "__main__":
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y_%m_%d_%H_%M")
    os.makedirs(f"./temperature/{formatted_time}", exist_ok=True)
    # Adjust the COM port as needed
    mk2000 = MK2000(serial_port="COM4")
    data, csv_path = mk2000.mk2000_read_temperature(
        sample_rate=1, duration=43200, formatted_time=formatted_time
    )
    # Close the connection
    mk2000.close_mk2000()
    # Plot the temperature data from the saved CSV file
    plot_temperature_from_csv(csv_path)
