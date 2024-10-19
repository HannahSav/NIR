# Created by Hannah at 09.10.2024 12:43
import numpy as np
from matplotlib import pyplot as plt

# from Buhshtabera import pca_projection, sliding_window


from tkinter import filedialog, messagebox, ttk


# Функция для отображения графика
def show_plot_emg_for_view(columns_data, time, data_name):
    """
    Отображает графики ЭМГ с добавленной осью времени и возможностью отображения значений
    при наведении курсора на график.

    :param columns_data: dict{'data_name': 'List[float]}. Словарь с данными ЭМГ.
    :param time: List[float]. Список значений времени.
    :param data_name: str. Название для всего набора данных.
    :return: None.
    """
    if columns_data:
        num = len(columns_data)
        colors = plt.cm.viridis(np.linspace(0, 1, num))

        # Увеличение высоты подграфиков
        fig, axes = plt.subplots(num, 1, figsize=(10, 2.5 * num), sharex=True)

        # Уменьшенный заголовок
        fig.suptitle(data_name, fontsize=12)

        all_data = np.concatenate([np.array(data) for data in columns_data.values()])
        y_min, y_max = all_data.min(), all_data.max()

        for i, (key, data) in enumerate(columns_data.items()):
            axes[i].plot(time, data, color=colors[i], label=key)
            axes[i].tick_params(axis='both', which='major', labelsize=8)  # Уменьшенные подписи осей
            axes[i].set_ylim([y_min - 0.05 * y_min, y_max + 0.05 * y_max])
            axes[i].grid(True)

            # Добавление легенды сбоку
            axes[i].legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=10)

            # Установка минимального и максимального времени для графика
            time_min = min(time)
            time_max = max(time)
            axes[i].set_xlim([time_min, time_max])  # Обрезка графика по оси X

        # Уменьшенная подпись оси X
        axes[-1].set_xlabel('Time', fontsize=10)

        # Настройка частичной разметки оси X для отображения времени
        axes[-1].xaxis.set_major_locator(plt.MaxNLocator(10))  # Ограничение количества меток на оси X

        # Аннотация для отображения значений при наведении
        annotation = axes[-1].annotate(
            '', xy=(0, 0), xytext=(-40, 30),
            textcoords='offset points', bbox=dict(boxstyle="round", fc="w"),
            arrowprops=dict(arrowstyle="->")
        )
        annotation.set_visible(False)

        # Функция для обновления аннотации при наведении
        def update_annotation(event):
            if event.inaxes:  # Если курсор находится на графике
                for ax in axes:
                    if ax == event.inaxes:
                        xdata = event.xdata
                        # Нахождение ближайшего индекса времени
                        closest_index = np.searchsorted(time, xdata, side="left")
                        if 0 <= closest_index < len(time):
                            xdata = time[closest_index]
                            ydata = [columns_data[key][closest_index] for key in columns_data.keys()]

                            # Формирование строки для аннотации с названием каждого графика и его значением
                            annotation_text = f"Время: {xdata:.5f}\n" + "Значения:\n" + "\n".join(
                                [f"{key}: {y:.5f}" for key, y in zip(columns_data.keys(), ydata)]
                            )

                            annotation.xy = (xdata, ydata[0])  # Позиция аннотации
                            annotation.set_text(annotation_text)
                            annotation.set_visible(True)
                        fig.canvas.draw_idle()
            else:
                annotation.set_visible(False)

        fig.canvas.mpl_connect('motion_notify_event', update_annotation)

        # Опция для удаления пустых областей на краях
        plt.tight_layout(rect=[0, 0, 0.95, 0.96])  # Уменьшение правого отступа для легенды

        # Растягивание графиков по всему окну и удаление пустых частей
        fig.subplots_adjust(hspace=0.1)  # Сужение вертикальных отступов между графиками

        plt.show()

def show_heatmap_emg(columns_data, time, data_name):
    '''
    Строит тепловую карту для данных ЭМГ
    :param columns_data: dict{'data_name':'List[float]}
    :param time: список значений времени
    :param data_name: название графа
    :return: None
    '''
    if columns_data:
        # Преобразование данных в двумерный массив для тепловой карты
        data_matrix = np.array([columns_data[key] for key in columns_data if columns_data[key] is not None])

        plt.figure(figsize=(12, 6))

        # Построение тепловой карты
        plt.imshow(data_matrix, aspect='equal', cmap='hot', extent=[time[0], time[-1], 0, len(columns_data)])

        plt.title('{}. Heatmap'.format(data_name))
        plt.xlabel('Time [s]')
        plt.ylabel('Channels')

        # Отображение цветовой шкалы
        plt.colorbar(label='Value')

        plt.grid(False)
        plt.show()

def view_buhshtaber(data_dict, plot_name, prog0, prog1):
    '''
    :param data: dict of dicts(emg) of the same gesture of different
    :param plot_name: plot name
    :return:
    '''
    num_plot_set = len(data_dict)
    num_lines = len(data_dict[list(data_dict.keys())[0]])
    colors = plt.cm.viridis(np.linspace(0, 1, num_lines))
    fig, axs = plt.subplots(num_plot_set, num_lines, figsize=(15, 5))
    plt.suptitle('{} on {} and {} projection'.format(plot_name, 'PC'+str(prog0+1), 'PC'+str(prog1+1)))
    for j, (gesture, g_data) in enumerate(data_dict.items()):
        for i, (emg, projections) in enumerate(g_data.items()):
            axs[j][i].scatter(projections[:, prog0], projections[:, prog1], color=colors[i], s=20, alpha=0.75)
            # Draw lines connecting points
            axs[j][i].plot(projections[:, prog0], projections[:, prog1], color='black', alpha=0.5)
            if j == 0:
                axs[j][i].set_title(emg)
            if j == num_plot_set-1:
                axs[j][i].set_xlabel('PC'+str(prog0+1))
            if i == 0:
                axs[j][i].set_ylabel(gesture+'\n'+'PC'+str(prog1+1))
            # else:
            #     axs[j][i].set_ylabel('PC'+str(prog1+1))
    plt.show()


if __name__ == "__main__":
    # data = {
    #     "g1":[1, 3, 5, 3, 1, 5, 4, 3, 2, 3, 2, 1, 2, 3, 4, -5],
    #     "g2":[-2, 3, 1, 3, 2, 5, 4, 3, 2, 3, 2, 1, 2, 3, 4, -5],
    #     "g3":[1,2, 3, 4, 1, 5, 4, 3, 2, 3, 2, 1, 2, 3, 4, -5],
    #     "g4":[0, 0, 1, 1,-1, 5, 4, 3, 2, 3, 2, 1, 2, 3, 4, -5],
    # }
    # time = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    # tit = "dghjk"
    # show_heatmap_emg(data, time, tit)

    print(pca_projection(sliding_window([1, 2, 3, 1, 2,1 ], 4), 3))
    data = {
        "m1": {
            'g1':pca_projection(sliding_window([1, 2, 3, 1, 2,1 ], 4), 3),
            'g2': pca_projection(sliding_window([1, 253, 1, 3, 1, 2, 1], 4), 3),
            'g3': pca_projection(sliding_window([1, 2, 3,32, 1, 2], 4), 3)
        },
        "m2": {
            'g1':pca_projection(sliding_window([4, 3, 2, 4, 1, 3], 4), 3),
            'g2': pca_projection(sliding_window([1, 25, 3, 4 ,3 , 2, 1], 4), 3),
            'g3': pca_projection(sliding_window([1, 2,6, 2, 4, 1, 2], 4), 3)
        },
    }
    # data = {
    #     "movie1":{
    #         "1":[[1,2, 3], [2, 1, 2], [2, 2, 2]],
    #         "2":[[2,4, 3], [2, 5, 4], [1, 1, 2]]
    #     },
    #     "movie2": {
    #         "1": [[2, 1, 1], [2, 4, 3], [2, 1, 2]],
    #         "2": [[2, 1, 1], [2, 4, 3], [1, 21, 2]]
    #     },
    #     "movie3": {
    #         "1": [[2, 1, 1], [2, 4, 3], [9, 1, 2]],
    #         "2": [[6, 1, 4], [2, 2, 3], [3, 1, 2]]
    #     }
    # }
    name = "buhshtaber_test"
    view_buhshtaber(data, name, 0, 1)
