from zhinst.core import ziDAQServer
import os
import time

daq = ziDAQServer("127.0.0.1", 8005, 1)
device = "dev1657"
save_dir = (
    r"C:\Users\cnmuser\Desktop\nonlinear_oscillators\nonlinear_oscillators\results\data"
)
os.makedirs(save_dir, exist_ok=True)

sweeper = daq.sweep()
sweeper.set("device", device)
sweeper.set("start", 60000)
sweeper.set("stop", 70000)
sweeper.set("samplecount", 100)
sweeper.set("bandwidth", 1000)
sweeper.set("bandwidthcontrol", 1)
sweeper.set("xmapping", 0)
sweeper.set("gridnode", f"/{device}/oscs/0/freq")

sweeper.set("save/save", 1)
sweeper.set("save/saveonread", 1)
sweeper.set("save/directory", save_dir)
sweeper.set("save/filename", "test_sweep")
sweeper.set("save/fileformat", 1)
sweeper.set("save/csvseparator", ";")

sweeper.subscribe(f"/{device}/demods/0/sample")
sweeper.execute()

while not sweeper.finished():
    time.sleep(0.5)
    print(f"Progress: {sweeper.progress()[0] * 100:.1f}%")

result = sweeper.read()
sweeper.finish()
sweeper.unsubscribe("*")

full_path = os.path.join(save_dir, "test_sweep.csv")
if os.path.exists(full_path):
    print("✅ Saved file:", full_path)
else:
    print("❌ File not saved.")
