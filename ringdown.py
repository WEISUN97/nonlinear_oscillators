import time
import numpy as np
import zhinst.core
from zhinst.core import ziDAQServer

# === 1. 连接设备 ===
device_id = "dev1657"
daq = ziDAQServer("127.0.0.1", 8005, 1)

# === 2. 设置输出通道 ===
daq.setInt(f"/{device_id}/sigouts/1/on", 1)  # 开启 Output 2
daq.setDouble(f"/{device_id}/sigouts/1/amplitudes/7", 0.01)  # 设置幅值（如 0.2 V）
daq.setDouble(f"/{device_id}/sigouts/1/enables/on", 1)  # Enable

# === 3. 设置频率和 demod ===
daq.setDouble(f"/{device_id}/oscs/1/freq", 60e3)  # 60 kHz 激励

# === 4. 配置数据记录器（记录 demod R or X/Y） ===
daq_module = daq.dataAcquisitionModule()
daq_module.set("device", device_id)
daq_module.set("grid/mode", 4)  # Linear
daq_module.set("grid/cols", 10000)  # 10 秒内采样 10k 点
daq_module.set("duration", 10.0)  # 10 秒总时长
daq_module.set("type", 0)  # Instant start
daq_module.subscribe(f"/{device_id}/demods/1/sample")  # 或 sample.x/y

# === 5. 启动采集 ===
daq_module.execute()
print("Recording started...")
time.sleep(2.0)

# === 6. 2 秒时关闭 Output2 ===
daq.setInt(f"/{device_id}/sigouts/1/on", 0)
print("Drive OFF at 2s")

# === 7. 等待采集完成 ===
time.sleep(8.5)
data = daq_module.read(True)
daq_module.finish()
print(data)
# === 8. 获取数据 ===
signal = data[f"/{device_id}/demods/0/sample"][0]["value"]
timestamps = data[f"/{device_id}/demods/0/sample"][0]["timestamp"]
t = (timestamps - timestamps[0]) / daq.getDouble(f"/{device_id}/clockbase")  # 转换为秒

# === 9. 可视化 ===
import matplotlib.pyplot as plt

plt.plot(t, signal)
plt.axvline(2, color="r", linestyle="--", label="Drive OFF")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude (V)")
plt.title("Ringdown Measurement")
plt.legend()
plt.grid()
plt.show()
