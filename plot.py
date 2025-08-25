from module.tools import plot_from_csv
from datetime import datetime

folder = "250825_01"
pathbase = f"./results/{folder}/"
folder_name = [
    "2508221818_amp1_1_amp2_0.0005",
    "2508221839_amp1_1_amp2_0.0004",
    "2508221901_amp1_1_amp2_0.0003",
    "2508221923_amp1_1_amp2_0.0002",
    "2508221944_amp1_1_amp2_0.0001",
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
