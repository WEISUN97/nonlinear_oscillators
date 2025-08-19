from module.tools import plot_from_csv
from datetime import datetime


pathbase = "./results/"
folder_name = [
    "2508181824_amp1_1_amp2_0.023",
    "2508181914_amp1_1_amp2_0.024",
    "2508182004_amp1_1_amp2_0.0241",
    "2508182054_amp1_1_amp2_0.0242",
    "2508182144_amp1_1_amp2_0.0243",
    "2508182233_amp1_1_amp2_0.0244",
    "2508182323_amp1_1_amp2_0.0245",
    "2508190013_amp1_1_amp2_0.0246",
    "2508190103_amp1_1_amp2_0.0247",
    "2508190153_amp1_1_amp2_0.0248",
    "2508190243_amp1_1_amp2_0.0249",
    "2508190332_amp1_1_amp2_0.025",
    "2508190422_amp1_1_amp2_0.026",
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
