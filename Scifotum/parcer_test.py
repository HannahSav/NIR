# Created by Hannah at 16.07.2024 20:13
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy import interpolate
import math
import neurokit2 as nk


def plot_columns_data_one_plot(columns_data, time, data_name):
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



'''
Creating start graphics
'''

def create_old_graphics(data_file, data_name, column_names):
    data = pd.read_excel(data_file)
    columns_data = {}
    time = data['X[s]'].tolist()
    for column_name in column_names:
        if column_name != 'X[s]':
            columns_data[column_name] = data[column_name].tolist()#[1700:2800:5]
    plot_columns_data_one_plot(columns_data, time, data_name)
    return columns_data


'''
After Maxim smalltalk
'''
def take_data(data_file, data_name, column_names):
    '''
    :param data_file: str путь до файла
    :param data_name: str название графика
    :param column_names: List[str] названия колонок
    :return: List[float] Данные после чтения
    '''
    def move_to_isoline(data_column):
        '''
        Функция для сдвига к изолинии
        :param data_column: List[float] изначальные данные ЭМГ
        :return: сдвинутые данные ЭМГ
        '''
        mean = np.mean(data_column)
        for i in range(len(data_column)):
            data_column[i] -= mean
        return data_column

    def choose_best_line():
        num = input("Which line was more important (0-7) :").split()[0]
        while num not in ['0', '1', '2', '3', '4', '5', '6', '7']:
            num = input('Try again: ').split()
            print(num)
        return int(num)

    # def creating_emg_amplitude_abs(data_column):
    #     '''
    #     просто модуль
    #
    #     Функция для выделения амплитуды.Пока неправильная
    #     :param data_column: List[float] изначальные данные
    #     :return: List[float] данные после выделения амплитуды
    #     '''
    #     new_data_column = []
    #     for i in range(len(data_column) - 1):
    #         # new_data_column.append(abs(data_column[i] - data_column[i + 1]))
    #         new_data_column.append(abs(data_column[i]))
    #     return new_data_column
    def creating_emg_amplitude_pos_neg(data_column):
        '''
        Искать минимум в отрицательном и максимум в положительном

        Функция для выделения амплитуды. Через соседей меньше больше
        :param data_column: List[float] изначальные данные
        :param time: List[float] моменты времени
        :return: List[float] data данные после выделения амплитуды
        :return: List[float] time временные точки, после нарезки

        '''
        new_data_column = []
        if_positive = data_column[0]
        i = 0
        prev_best = 0
        best_i = 0
        best = 0
        while i < len(data_column):
            new_data_column.append(abs(data_column[i]))
            if abs(data_column[i]) >= best:
                best = abs(data_column[i])
                best_i = i
            elif data_column[i] * if_positive < 0:
                if_positive *= -1
                print(best_i, prev_best, (best_i - prev_best))
                step = (new_data_column[best_i] - new_data_column[prev_best]) / (best_i - prev_best)
                for j in range(prev_best + 1, best_i):
                    new_data_column[j] = new_data_column[j - 1] + step
                prev_best = best_i
                best = 0
            i += 1
        print("like made")
        return new_data_column


    # def creating_emg_amplitude_with_diff(data_column):
    #     '''
    #     Разница между макс минами(как creating_emg_amplitude_pos_neg но с разницей)
    #
    #     Функция для выделения амплитуды. Через соседей меньше больше
    #     :param data_column: List[float] изначальные данные
    #     :return: List[float] данные после выделения амплитуды
    #
    #     '''
    #     new_data_column = []
    #     new_data_column.append(data_column[0])
    #     # for i in range(1, len(data_column) - 1):
    #         # if data[i] > data[]
    #     # return new_data_column


    #take data


    data = pd.read_excel(data_file)

    # нули в начале и в конце записи (не изолиния, а именно нули!!!!)
    START_NO_ZEROS = 120
    STOP_NO_ZEROS = -140

    #for start data, for prepared data
    columns_data = {}
    columns_data_new = {}
    time = data['X[s]'].tolist()[START_NO_ZEROS:STOP_NO_ZEROS]

    #painting start (before find isolines)
    for column_name in column_names:
        if column_name != 'X[s]':
            columns_data[column_name] = data[column_name].tolist()[START_NO_ZEROS:STOP_NO_ZEROS]
    plot_columns_data_one_plot(columns_data, time, "START DATA.\n" + data_name)

    #after found isolines
    for column_name, data in columns_data.items():
        if column_name !=  'Avanti sensor 1 - brachioradialis: EMG 1':
            columns_data_new[column_name] = np.zeros(len(time))
        else:
            columns_data_new[column_name] = move_to_isoline(data)

        # columns_data_new[column_name] = interpolate.interp1d(columns_data_new[column_name], time[:1500], kind="linear")
    # print(columns_data_new)
    plot_columns_data_one_plot(columns_data_new, time, "AFTER MOVING ISOLINE.\n" + data_name)

    # Наиболее значимый датчик (на что ориенируемся?)
    best_line = choose_best_line()

    for column_name, data in columns_data_new.items():
        if column_name ==  'Avanti sensor 1 - brachioradialis: EMG 1':
            columns_data_new[column_name] = creating_emg_amplitude_pos_neg(data)
    plot_columns_data_one_plot(columns_data_new, time, "AFTER CREATING EMG AMPLITUDE.\n"+data_file)


if __name__ == '__main__':
    # столбцы из xslx, которые нам надо
    column_names = ['X[s]', 'Avanti sensor 1 - brachioradialis: EMG 1', 'Avanti sensor 2: EMG 2',
                    'Avanti sensor 3 - palmaris longus: EMG 3', 'Avanti sensor 4: EMG 4', 'Avanti sensor 5: EMG 5',
                    'Avanti sensor 6: EMG 6', 'Avanti sensor 7: EMG 7', 'Avanti sensor 8: EMG 8']
    # Путь до файла
    data_file = "resources/1_gesture_nikita_Plot_and_Store_Rep_1.2.xlsx"
    # Для названия графиков
    data_name = 'Pron'
    # # Которая раньше чето строила
    # create_old_graphics(data_file=data_file, data_name="Pron'", columns_names)
    # главная преобразующая и получающая данные функция
    take_data(data_file=data_file, data_name=data_name, column_names = column_names)

