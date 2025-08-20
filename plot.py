from module.tools import plot_from_csv
from datetime import datetime


pathbase = "./results/"
folder_name = [
    "2508201533_amp1_1_amp2_0.023",
    "2508201541_amp1_1_amp2_0.024",
    "2508201549_amp1_1_amp2_0.025",
]
csv_paths = [_ for _ in range(len(folder_name))]
for i in range(len(folder_name)):
    csv_paths[i] = pathbase + folder_name[i] + "/sweep_" + folder_name[i] + ".csv"

timestamp = datetime.now().strftime("%y%m%d%H%M")
plot_from_csv(
    csv_paths,
    column_indices=[1],
    save_path=f"./results/figure/sweepplot_{timestamp}.png",
)
