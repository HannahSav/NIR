# Created by Hannah at 16.07.2024 20:13

import pandas as pd
from matplotlib import pyplot as plt
import neurokit2 as nk


def plot_columns_data_one_plot(columns_data, data_name):
    '''
    Строит все линии ЭМГ
    :param columns_data: dict{'data_name':'List[float]}
    :param data_name: название графа
    :return: None
    '''
    if columns_data and 'X[s]' in columns_data:
        x_values = columns_data['X[s]']

        plt.figure(figsize=(12, 6))

        for column_name in columns_data.keys():
            if column_name != 'X[s]' and columns_data[column_name] is not None:
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
    for column_name in column_names:
        columns_data[column_name] = data[column_name].tolist()[1700:2800:5]
    plot_columns_data_one_plot(columns_data, data_name)
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
    def creating_emg_amplitude(data_column):
        '''
        Функция для выделения амплитуды.Пока неправильная
        :param data_column: List[float] изначальные данные
        :return: List[float] данные после выделения амплитуды
        '''
        new_data_column = []
        for i in range(len(data_column) - 1):
            # new_data_column.append(abs(data_column[i] - data_column[i + 1]))
            new_data_column.append(abs(data_column[i]))
        return new_data_column

    data = pd.read_excel(data_file)
    columns_data = {}
    columns_data_new = {}
    for column_name in column_names:
        columns_data[column_name] = data[column_name].tolist()[1500:2550]
        if column_name != 'X[s]':
            columns_data_new[column_name] = creating_emg_amplitude(data[column_name].tolist())[1500:1550]
        else:
            columns_data_new[column_name] = columns_data[column_name]
        print(columns_data[column_name])
        print(columns_data_new[column_name])
    plot_columns_data_one_plot(columns_data, data_name)
    plot_columns_data_one_plot(columns_data_new, data_name)
    return columns_data

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

