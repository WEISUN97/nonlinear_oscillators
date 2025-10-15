from module.tools import plot_from_csv
from datetime import datetime

folder = "251014_01"
pathbase = f"./results/{folder}/"
folder_name = [
    "2510141739_amp1_1_amp2_0.005",
    "2510141815_amp1_1_amp2_0.01",
    "2510141850_amp1_1_amp2_0.015",
    "2510141925_amp1_1_amp2_0.02",
    "2510142001_amp1_1_amp2_0.025",
    "2510142036_amp1_1_amp2_0.03",
]
csv_paths = [_ for _ in range(len(folder_name))]
for i in range(len(folder_name)):
    csv_paths[i] = pathbase + folder_name[i] + "/sweep_" + folder_name[i] + ".csv"

timestamp = datetime.now().strftime("%y%m%d%H%M")
plot_from_csv(
    csv_paths,
    column_indices=[1],
    save_path=f"./results/figure/open_loop_sweep_{folder}.png",
    title=f"Open Loop Sweep {folder}",
)
plot_from_csv(
    csv_paths,
    column_indices=[1],
    save_path=f"./results/{folder}/open_loop_sweep_{folder}.png",
    show_plot=False,
    title=f"Open Loop Sweep {folder}",
)
