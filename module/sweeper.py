import time


class SweeperController:
    def __init__(self, daq, device, gridnode="/dev1657/oscs/1/freq"):
        self.device = device
        self.sweeper = daq.sweep()
        self.gridnode = gridnode
        sweeper = daq.sweep()
        sweeper.set("device", device)
        sweeper.set("xmapping", 1)
        sweeper.set("historylength", 100)
        sweeper.set("settling/inaccuracy", 0.00010000)
        sweeper.set("averaging/sample", 1)
        sweeper.set("bandwidth", 1000.00000000)
        sweeper.set("maxbandwidth", 1250000.00000000)
        sweeper.set("omegasuppression", 40.00000000)
        sweeper.set("order", 4)
        sweeper.set(
            "save/directory",
            r"C:\Users\cnmuser\Documents\Zurich Instruments\LabOne\WebServer",
        )
        sweeper.set("averaging/tc", 0.00000000)
        sweeper.set("averaging/time", 0.00000000)
        sweeper.set("bandwidth", 1000.00000000)
        sweeper.set("start", 1000.00000000)
        sweeper.set("stop", 1000000.00000000)
        sweeper.set("omegasuppression", 40.00000000)
        sweeper.set("order", 4)
        sweeper.set("settling/inaccuracy", 0.00010000)

    def configure(
        self,
        start,
        stop,
        samplecount,
        maxbandwidth=100,
        xmapping=0,  # 0: linear, 1: logarithmic
        # filtermode=2,
    ):
        self.sweeper.set("device", self.device)
        self.sweeper.set("start", start)
        self.sweeper.set("stop", stop)
        self.sweeper.set("samplecount", samplecount)
        # self.sweeper.set("bandwidth", bandwidth)
        # self.sweeper.set("bandwidthcontrol", filtermode)    # 0:manual, 1:fixed, 2: auto
        self.sweeper.set("maxbandwidth", maxbandwidth)
        self.sweeper.set("xmapping", xmapping)

        # self.sweeper.set("save/save", 1)
        # self.sweeper.set("save/saveonread", 1)
        # self.sweeper.set("save/directory", save_dir)
        # self.sweeper.set("save/filename", "sweep")
        # self.sweeper.set("save/fileformat", 1)  # 0=matlab,  1 = CSV
        # self.sweeper.set("save/csvseparator", ";")

    def run(self, demods=["0", "1"], timeout=5000000):
        self.sweeper.set("gridnode", self.gridnode)
        for d in demods:
            self.sweeper.subscribe(f"/{self.device}/demods/{d}/sample")
        self.sweeper.execute()
        start_time = time.time()
        while not self.sweeper.finished():
            time.sleep(0.5)
            progress = self.sweeper.progress()[0]
            print(f"Sweeper progress: {progress * 100:.2f}%")
            if time.time() - start_time > timeout:
                print("Timeout reached before sweep finished.")
                break
        result = self.sweeper.read()
        self.sweeper.finish()
        self.sweeper.unsubscribe("*")

        return result

    def stop(self):
        self.sweeper.finish()
        self.sweeper.unsubscribe("*")
