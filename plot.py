from module.tools import plot_from_csv
from datetime import datetime


pathbase = "./results/data/"
csv_file = [
    "sweep_all_2507281046amp1.25V",
]
csv_paths = [_ for _ in range(len(csv_file))]
for i in range(len(csv_file)):
    csv_paths[i] = pathbase + csv_file[i] + ".csv"
if len(csv_file) == 1:
    save_path_plot = f"./results/figure/{csv_file}.png"
else:
    save_path_plot = f"./results/figure/sweep_overlay.png"

timestamp = datetime.now().strftime("%y%m%d%H%M")
plot_from_csv(
    csv_paths,
    column_indices=[1],
    # save_path=f"./results/figure/sweepplot_{timestamp}.png",
    save_path="",
)
