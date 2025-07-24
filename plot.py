from module.tools import plot_from_csv


pathbase = "./results/data/"
csv_file = f"sweep_2507211322amp0.1V"
csv_path = pathbase + csv_file + ".csv"
save_path_plot = f"./results/figure/{csv_file}.png"
plot_from_csv(csv_path, column_indices=[2], save_path="")
