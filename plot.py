from module.tools import plot_from_csv
from datetime import datetime

folder = "251009_01"
pathbase = f"./results/{folder}/"
folder_name = [
    "2510091946_amp1_1_amp2_0.1",
    "2510092036_amp1_1_amp2_0.2",
    "2510092125_amp1_1_amp2_0.3",
    "2510092215_amp1_1_amp2_0.4",
    "2510092305_amp1_1_amp2_0.5",
    "2510092355_amp1_1_amp2_0.6",
    "2510100044_amp1_1_amp2_0.7",
    "2510100134_amp1_1_amp2_0.8",
    "2510100224_amp1_1_amp2_0.9",
    "2510100314_amp1_1_amp2_1",
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
