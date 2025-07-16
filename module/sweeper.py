import time


class SweeperController:
    def __init__(self, daq, device):
        self.device = device
        self.sweeper = daq.sweep()

    def configure(
        self,
        gridnode,
        start,
        stop,
        samplecount,
        bandwidth,
        xmapping,
        filtermode=1,
        save_dir=None,
    ):
        self.sweeper.set("device", self.device)
        self.sweeper.set("start", start)
        self.sweeper.set("stop", stop)
        self.sweeper.set("samplecount", samplecount)
        self.sweeper.set("gridnode", gridnode)
        self.sweeper.set("bandwidth", bandwidth)
        self.sweeper.set("bandwidthcontrol", filtermode)
        self.sweeper.set("xmapping", xmapping)
        self.sweeper.set("settling/inaccuracy", 1e-4)
        self.sweeper.set("order", 4)
        self.sweeper.set("omegasuppression", 40)
        if save_dir:
            self.sweeper.set("save/directory", save_dir)

    def run(self, demods=["0", "1"], timeout=30):
        for d in demods:
            self.sweeper.subscribe(f"/{self.device}/demods/{d}/sample")
        self.sweeper.execute()
        start_time = time.time()
        while not self.sweeper.finished():
            time.sleep(0.5)
            progress = self.sweeper.progress()[0]
            print(f"Sweeper progress: {progress * 100:.2f}%")
            if time.time() - start_time > timeout:
                print("Timeout while waiting for sweep to complete.")
                break
        result = self.sweeper.read()
        self.sweeper.finish()
        self.sweeper.unsubscribe("*")
        return result

    def stop(self):
        self.sweeper.finish()
        self.sweeper.unsubscribe("*")
