# Created by Hannah at 05.06.2024 14:14


# метод разверток (пришлет ВЮ)
# поиграть с параметрами (скользящие окна)

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt



# Функция для отображения изначальных данных на разных графиках
# def plot_columns_data_diff_plots(columns_data):
#     if columns_data and 'X[s]' in columns_data:
#         x_values = columns_data['X[s]']
#
#         plt.figure(figsize=(15, 10))
#         plt.title('{}. Data Plot'.format(data_name))
#
#         for i, column_name in enumerate(columns_data.keys()):
#             if column_name != 'X[s]' and columns_data[column_name] is not None:
#                 plt.subplot(3, 2, i + 1)
#                 plt.plot(x_values, columns_data[column_name], marker='o', markersize = 3, linestyle='-', label=column_name)
#                 plt.title(column_name)
#                 plt.xlabel('X[s]')
#                 plt.ylabel('Value')
#                 plt.legend()
#                 plt.grid(True)
#
#         plt.tight_layout()
#         plt.show()


# Функция для отображения изначальных данных на одном графике
def plot_columns_data_one_plot(columns_data, data_name):
    if columns_data and 'X[s]' in columns_data:
        x_values = columns_data['X[s]']

        plt.figure(figsize=(12, 6))

        for column_name in columns_data.keys():
            if column_name != 'X[s]' and columns_data[column_name] is not None:
                plt.plot(x_values, columns_data[column_name], marker='o', markersize=3, linestyle='-',
                         label=column_name)

        plt.title('{}. Data Plot'.format(data_name))
        plt.xlabel('X[s]')
        plt.ylabel('Value')
        plt.legend()
        plt.grid(True)
        plt.show()

def take_data(data_file, data_name):
    column_names = ['X[s]', 'FDS galileo: dEMG.A 1', 'FDS galileo: dEMG.B 1', 'FDS galileo: dEMG.C 1', 'FDS galileo: dEMG.D 1', 'FDS avanti: EMG 2']
    start = 0
    # stop = 9000 # почему при 10-15к соединяются?? разное количество измерений....
    stop = 15550
    step = 50
    data = pd.read_excel(data_file)
    columns_data = {}
    print(f"{finger} : {data.size} lines in file")
    for column_name in column_names:
        columns_data[column_name] = data[column_name].tolist()[start:stop:step]
    plot_columns_data_one_plot(columns_data, data_name)
    return columns_data


# Заглучшка вместо данных
def create_time_series(N):
    t = np.linspace(0, 4 * np.pi, N)
    return np.sin(t) + 0.5 * np.random.randn(N)


# Формирование векторов размерности n
def sliding_window(series, n):
    return np.array([series[i:i + n] for i in range(len(series) - n + 1)])


# Проекция на пространство меньшей размерности с помощью PCA
def pca_projection(vectors, r):
    pca = PCA(n_components=r)
    return pca.fit_transform(vectors)

# Визуализация проекций для r=2 или r=3
def plot_projection_diff_plots(projections_dict, r, data_name):
    num_fingers = len(projections_dict)
    if r == 2:
        fig, axs = plt.subplots(1, num_fingers, figsize=(15, 5))
        plt.suptitle('{} on {} projections'.format(data_name, r))
        for i, (finger, projections) in enumerate(projections_dict.items()):
            axs[i].scatter(projections[:, 0], projections[:, 1], color='green', s=20, alpha=0.75)
            # Draw lines connecting points
            axs[i].plot(projections[:, 0], projections[:, 1], color='red', alpha=0.5)
            axs[i].set_title(finger)
            axs[i].set_xlabel('PC1')
            axs[i].set_ylabel('PC2')
        plt.show()
    elif r == 3:
        fig = plt.figure(figsize=(15, 10))
        plt.suptitle('{} on {} projections'.format(data_name, r))
        for i, (finger, projections) in enumerate(projections_dict.items()):
            ax = fig.add_subplot(2, 3, i + 1, projection='3d')
            ax.scatter(projections[:, 0], projections[:, 1], projections[:, 2], color='green', s=20, alpha=0.75)
            # Draw lines connecting points
            for j in range(len(projections) - 1):
                ax.plot([projections[j, 0], projections[j + 1, 0]],
                        [projections[j, 1], projections[j + 1, 1]],
                        [projections[j, 2], projections[j + 1, 2]], color='red', alpha=0.5)
            ax.set_title(finger)
            ax.set_xlabel('PC1')
            ax.set_ylabel('PC2')
            ax.set_zlabel('PC3')
        plt.show()
    else:
        print("r слишком велик для визуализации. Посмотреть не получится. Придумай как оценить...")

# def plot_projection_one_plot(projections_dict, r, data_name):
#     if r == 2:
#         plt.figure(figsize=(8, 6))
#         plt.suptitle('{} on {} projections'.format(data_name, r))
#         for finger, projections in projections_dict.items():
#             plt.scatter(projections[:, 0], projections[:, 1], label=finger)
#         plt.xlabel('PC1')
#         plt.ylabel('PC2')
#         plt.legend()
#         plt.show()
#     elif r == 3:
#         fig = plt.figure(figsize=(10, 8))
#         plt.suptitle('{} on {} projections'.format(data_name, r))
#         ax = fig.add_subplot(111, projection='3d')
#         for finger, projections in projections_dict.items():
#             ax.scatter(projections[:, 0], projections[:, 1], projections[:, 2], label=finger)
#         ax.set_xlabel('PC1')
#         ax.set_ylabel('PC2')
#         ax.set_zlabel('PC3')
#         ax.legend()
#         plt.show()
#     else:
#         print("r слишком велик для визуализации. Посмотреть не получится. Придумай как оценить...")

if __name__ == '__main__':

    N = 200
    n = 100
    r = 3


    # # Создание временного ряда
    # time_series = create_time_series(N)

    # пальчики
    # Primus - 1
    # Secundus - 2
    # Medius - 3
    # Anularis - 4
    # Minimi - 5

    add_path = 'resources/'

    fingers_file_names = {
        "Primus" : "Primus_flex_Rep_10.62.xlsx",
        "Secundus" : "secundus_flex_Rep_2.33.xlsx",
        "Medius" : "medius_flex_Rep_1.22.xlsx",
        "Anularis" : "anularis_flex_Rep_1.12.xlsx",
        "Minimi" : "minimi_flex_Rep_2.2.xlsx"
    }

    projections_columns = {}

    for finger, file in fingers_file_names.items():
        # Чтение временного ряда
        time_series_columns = take_data(data_file=add_path + file, data_name=finger)

        # Формирование векторов
        vector_columns = {}
        for key, value in time_series_columns.items():
            if key != 'X[s]':
                vector_columns[key] = sliding_window(value, n)

        # Проекция на r-мерное пространство
        for key, value in vector_columns.items():
            if key not in projections_columns.keys():
                projections_columns[key] = {}
            projections_columns[key][finger] = pca_projection(value, r)

    # Визуализация проекций
    for key, fingers in projections_columns.items():
        print(key)
        plot_projection_diff_plots(fingers, r, key)

