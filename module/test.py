from zhinst.core import ziDAQServer

daq = ziDAQServer("127.0.0.1", 8005, 1)
daq.connect()

sweeper = daq.sweep()
sweeper.set("device", "dev1657")
sweeper.set("start", 2e3)  # 起始频率
sweeper.set("stop", 1e6)  # 结束频率
# 读取当前 sweeper 节点树
print(daq.get("/dev1657/sweep/*"))
