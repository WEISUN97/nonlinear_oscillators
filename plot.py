from module.tools import plot_from_csv
from datetime import datetime

folder = "250821_01"
pathbase = f"./results/{folder}/"
folder_name = [
    "2508210948_amp1_1_amp2_0.025",
    "2508210956_amp1_1_amp2_0.03",
    "2508211004_amp1_1_amp2_0.035",
    "2508211012_amp1_1_amp2_0.04",
    "2508211020_amp1_1_amp2_0.045",
    "2508211027_amp1_1_amp2_0.05",
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
