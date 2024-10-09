# Created by Hannah at 09.10.2024 12:43
import numpy as np
from matplotlib import pyplot as plt


def show_plot_emg_one_plot(columns_data, time, data_name):
    '''
    Строит все линии ЭМГ
    :param columns_data: dict{'data_name':'List[float]}
    :param data_name: название графа
    :return: None
    '''
    if columns_data:
        x_values = time

        plt.figure(figsize=(12, 6))

        for column_name in columns_data.keys():
            if columns_data[column_name] is not None:
                plt.plot(x_values, columns_data[column_name], marker='o', markersize=3, linestyle='-',
                         label=column_name, alpha = 0.5)

        plt.title('{}. Data Plot'.format(data_name))
        plt.xlabel('X[s]')
        plt.ylabel('Value')
        plt.legend()
        plt.grid(True)
        plt.show()



def show_plot_emg(columns_data, time, data_name):
    '''
        Строит все линии ЭМГ
        :param columns_data: dict{'data_name':'List[float]}
        :param data_name: название графа
        :return: None
        '''
    if columns_data:
        num = len(columns_data)
        colors = plt.cm.viridis(np.linspace(0, 1, num))
        fig, axes = plt.subplots(num, 1, figsize=(8, 2*num), sharex=True)
        fig.suptitle(data_name)

        all_data = np.concatenate([np.array(data) for data in columns_data.values()])
        y_min, y_max = all_data.min(), all_data.max()

        for i, (key, data) in enumerate(columns_data.items()):
            axes[i].plot(time, data)
            axes[i].set_title(f"{key}")
            axes[i].set_label(key)
            axes[i].set_ylim([y_min - 0.05 * y_min, y_max + 0.05 * y_max])
            axes[i].grid(True)
        axes[-1].set_xlabel('Time')
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.show()


if __name__ == "__main__":
    data = {
        "g1":[1, 3, 5, 3, 1],
        "g2":[-2, 3, 1, 3, 2],
        "g3":[1,2, 3, 4, 1],
        "g4":[0, 0, 1, 1,-1],
    }
    time = [1, 2, 3, 4, 5]
    tit = "dghjk"
    show_plot_emg(data, time, tit)
