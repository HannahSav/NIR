from tkinter import messagebox

import numpy as np
import neurokit2 as nk

def process_data(columns_data, time_data):
    """
    Удаляет начальные и конечные нули, масштабирует данные ЭМГ (умножает на 1000) и вычитает среднее арифметическое по каждому времени.

    :param columns_data: dict{'data_name': 'List[float]}. Словарь с данными ЭМГ.
    :param time_data: List[float]. Список значений времени.
    :return: None.
    """
    # Преобразование данных ЭМГ в numpy массив для удобства работы
    emg_data = np.array([columns_data[key] for key in columns_data.keys()])

    # Нахождение индексов, где ЭМГ значения не равны 0
    non_zero_indices = np.where(np.any(emg_data != 0, axis=0))[0]

    if len(non_zero_indices) == 0:
        messagebox.showerror("Error", "Все данные равны нулю.")
        return

    # Определение первого и последнего индекса ненулевых значений
    first_non_zero_idx = non_zero_indices[0]
    last_non_zero_idx = non_zero_indices[-1] + 1  # +1 для правильного среза

    # Срез данных по найденным индексам
    emg_data = emg_data[:, first_non_zero_idx:last_non_zero_idx]
    time_data = time_data[first_non_zero_idx:last_non_zero_idx]

    # Масштабирование данных (умножение на 1000)
    emg_data_scaled = emg_data * 1000

    # Вычисление среднего значения по каждому времени
    mean_emg = np.mean(emg_data_scaled, axis=0)  # Среднее по всем графикам в каждом временном моменте

    # Нормализация данных: вычитание среднего
    emg_data_normalized = emg_data_scaled - mean_emg

    # Обновление данных в исходном словаре
    for i, key in enumerate(columns_data.keys()):
        columns_data[key] = emg_data_normalized[i].tolist()

    return columns_data, time_data


def smooth_emg(columns_data, time_data, smoothing_window=50):
    """
    Сглаживает данные ЭМГ с использованием библиотеки NeuroKit.

    :param columns_data: dict{'data_name': 'List[float]}. Словарь с данными ЭМГ.
    :param time_data: List[float]. Список значений времени.
    :param smoothing_window: int. Размер окна сглаживания (по умолчанию 50).
    :return: dict, List. Возвращает сглаженные данные ЭМГ и соответствующий массив времени.
    """
    smoothed_data = {}
    smoothed_time = []

    for key, emg_signal in columns_data.items():
        # Сглаживание сигнала ЭМГ
        #TODO: тут есть вопросики конечно
        emg_signal = list(abs(emg) for emg in emg_signal)
        smoothed_signal = nk.signal_smooth(emg_signal, method="rolling", size=smoothing_window)

        # Изменение массива времени в соответствии с точками сглаженного сигнала
        # Используем только те временные метки, которые соответствуют длине сглаженного сигнала
        smoothed_time = time_data[:len(smoothed_signal)]

        # Сохранение сглаженного сигнала
        smoothed_data[key] = smoothed_signal.tolist()

    return smoothed_data, smoothed_time
