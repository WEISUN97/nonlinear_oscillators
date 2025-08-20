from module.tools import plot_from_csv
from datetime import datetime


pathbase = "./results/"
folder_name = [
    "2508201027_amp1_1_amp2_0.02",
    "2508201038_amp1_1_amp2_0.021",
    "2508201049_amp1_1_amp2_0.022",
    "2508201100_amp1_1_amp2_0.023",
    "2508201111_amp1_1_amp2_0.024",
    "2508201122_amp1_1_amp2_0.025",
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
