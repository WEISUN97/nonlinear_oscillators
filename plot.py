from module.tools import plot_from_csv
from datetime import datetime

folder = "250821_02"
pathbase = f"./results/{folder}/"
folder_name = [
    "2508211136_amp1_1_amp2_0.04",
    "2508211144_amp1_1_amp2_0.041",
    "2508211152_amp1_1_amp2_0.042",
    "2508211200_amp1_1_amp2_0.043",
    "2508211208_amp1_1_amp2_0.044",
    "2508211215_amp1_1_amp2_0.045",
    "2508211223_amp1_1_amp2_0.046",
    "2508211231_amp1_1_amp2_0.047",
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
