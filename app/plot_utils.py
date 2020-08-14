import os
from datetime import datetime
from math import floor, ceil

import matplotlib.pyplot as plt

from config import PLT_FIGSIZE, DPI

PLOT_PATH = 'app/static/plots'


def make_plot(dt_list, temp_list):
    min_temp, max_temp = floor(min(temp_list)), ceil(max(temp_list))
    y_range = range(min_temp - 2, max_temp + 2, 2)

    plt.figure(figsize=PLT_FIGSIZE)
    plt.xticks(rotation='vertical')
    plt.xlabel('Date & Time')
    plt.ylabel('Celsius degrees, °С')

    plt.plot(temp_list, zorder=5)
    plt.scatter(dt_list, temp_list, c='y', s=100, zorder=10)
    plt.yticks(y_range)

    fig_name = datetime.now().strftime('%d-%m-%y-%H-%M-%S') + '-plot.png'
    full_path = os.path.join(PLOT_PATH, fig_name)

    plt.savefig(full_path, dpi=DPI)

    return full_path
