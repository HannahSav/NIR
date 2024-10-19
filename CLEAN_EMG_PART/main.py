import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import json
import datetime
import os


from helper_viewer import show_plot_emg_for_view as show_plot_emg
from raw_data_processor import process_data, smooth_emg

# Функция для парсинга xlsx файла
def parse_xlsx(file_path):
    try:
        df = pd.read_excel(file_path)
        required_columns = ['X[s]', 'Avanti sensor 1 - brachioradialis: EMG 1',
                            'Avanti sensor 2: EMG 2', 'Avanti sensor 3 - palmaris longus: EMG 3',
                            'Avanti sensor 4: EMG 4', 'Avanti sensor 5: EMG 5',
                            'Avanti sensor 6: EMG 6', 'Avanti sensor 7: EMG 7',
                            'Avanti sensor 8: EMG 8']
        # Проверка на наличие колонок
        columns_data = {col: df[col].dropna().tolist() for col in required_columns if
                        col in df.columns and col != 'X[s]'}
        time_data = df['X[s]'].dropna().tolist()
        return time_data, columns_data, os.path.basename(file_path)
    except Exception as e:
        messagebox.showerror("Error", f"Ошибка при чтении файла: {e}")
        return None, None, None


# Функция для сохранения срезов данных в JSON с учетом временного интервала и названия файла
def save_intervals(columns_data, time_data, start, end, person_id, gesture_id, file_name):
    if not columns_data:
        messagebox.showerror("Error", "Данные отсутствуют для сохранения.")
        return

    # Выбор данных в пределах интервала
    indices = [i for i, t in enumerate(time_data) if start <= t <= end]
    if not indices:
        messagebox.showerror("Error", "Нет данных в заданном интервале.")
        return

    filtered_time = [time_data[i] for i in indices]
    filtered_columns_data = {key: [data[i] for i in indices] for key, data in columns_data.items()}

    data_to_save = {
        "file_name": file_name,
        "time_interval": {"start": start, "end": end},
        "save_time": str(datetime.datetime.now()),
        "time_data": filtered_time,
        "data": filtered_columns_data
    }

    save_dir = "cutted_data/raw2"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    file_path = os.path.join(save_dir, f"emg_data_person_{person_id}_gesture_{gesture_id}.json")

    # Проверка на существование файла
    if os.path.exists(file_path):
        # Если файл существует, загружаем его содержимое
        with open(file_path, "r") as json_file:
            try:
                existing_data = json.load(json_file)
                if not isinstance(existing_data, list):
                    # Если данные не в формате массива, преобразуем их в массив
                    existing_data = [existing_data]
            except json.JSONDecodeError:
                existing_data = []  # Если файл пуст или поврежден

        # Добавляем новые данные в существующий массив
        existing_data.append(data_to_save)

        # Сохраняем обновленные данные в файл
        with open(file_path, "w") as json_file:
            json.dump(existing_data, json_file, indent=4)

    else:
        # Если файл не существует, создаем новый файл с массивом
        with open(file_path, "w") as json_file:
            json.dump([data_to_save], json_file, indent=4)

    messagebox.showinfo("Success", f"Данные успешно сохранены в {file_path}!")


# Функция для выбора файла
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        entry_file_path.delete(0, tk.END)
        entry_file_path.insert(0, file_path)


# Функция для отображения графика по выбранному файлу
def plot_data():
    file_path = entry_file_path.get()
    if not file_path:
        messagebox.showerror("Error", "Не выбран файл!")
        return

    time_data, columns_data, file_name = parse_xlsx(file_path)
    if time_data and columns_data:
        columns_data, time_data = process_data(columns_data, time_data)

        # Получение значения ширины окна для сглаживания
        if entry_smoothing_window.get() == '':
            # Отображение графиков
            show_plot_emg(columns_data, time_data, f"EMG Data: {file_name}")
        else:
            try:
                smoothing_window = int(entry_smoothing_window.get())
            except ValueError:
                messagebox.showerror("Error", "Ширина окна должна быть числом!")
                return

            # Сглаживание данных
            smoothed_columns_data, smoothed_time_data = smooth_emg(columns_data, time_data, smoothing_window)
            # Отображение графиков
            show_plot_emg(smoothed_columns_data, smoothed_time_data, f"EMG Data: {file_name} \n SMOOTHED: {smoothing_window} ")




# Функция для сохранения данных
def save_data():
    try:
        start = float(entry_interval_start.get())
        end = float(entry_interval_end.get())
    except ValueError:
        messagebox.showerror("Error", "Временные интервалы должны быть числами!")
        return

    person_id = person_menu.get().split(' - ')[0]
    gesture_id = gesture_menu.get().split(' - ')[0]

    file_path = entry_file_path.get()
    time_data, columns_data, file_name = parse_xlsx(file_path)
    if time_data and columns_data:
        save_intervals(columns_data, time_data, start, end, person_id, gesture_id, file_name)


# Создание основного окна
root = tk.Tk()
root.title("EMG Data Parser")

# Метка и поле для ввода пути к файлу
label_file_path = tk.Label(root, text="Выберите файл:")
label_file_path.grid(row=0, column=0, padx=5, pady=5)

entry_file_path = tk.Entry(root, width=50)
entry_file_path.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

button_browse = tk.Button(root, text="Обзор", command=select_file)
button_browse.grid(row=0, column=3, padx=5, pady=5)

# Новое поле для ввода ширины окна сглаживания
label_smoothing_window = tk.Label(root, text="Ширина окна сглаживания:\n(для графиков без сглаживания\n оставить пустым)")
label_smoothing_window.grid(row=1, column=0, padx=5, pady=5)

entry_smoothing_window = tk.Entry(root, width=10)
entry_smoothing_window.grid(row=1, column=1, padx=5, pady=5)

# Кнопка для построения графика
button_plot = tk.Button(root, text="Построить график", command=plot_data)
button_plot.grid(row=2, column=0, columnspan=4, padx=5, pady=5)

# Поля для указания интервалов
label_intervals = tk.Label(root, text="Интервал (начало-конец):")
label_intervals.grid(row=3, column=0, padx=5, pady=5)

entry_interval_start = tk.Entry(root, width=10)
entry_interval_start.grid(row=3, column=1, padx=5, pady=5)

entry_interval_end = tk.Entry(root, width=10)
entry_interval_end.grid(row=3, column=2, padx=5, pady=5)

# Словари для выбора человека и жеста
current_dir = os.path.dirname(os.path.abspath(__file__))
person_file_path = os.path.join(current_dir, 'like_static_db/persons.json')
gesture_file_path = os.path.join(current_dir, 'like_static_db/gestures.json')

with open(person_file_path, 'r', encoding='utf-8') as file:
    person_options = json.load(file)
# person_options = {"1": "dmitri", "2": "kate", "3": "kirill", "4": "maxim", "5": "nikita"}

with open(gesture_file_path, 'r', encoding='utf-8') as file:
    gesture_options = json.load(file)
# gesture_options = {"0": "rest", "1": "hold_fist", "2": "flexing_fist",
#                    "3": "extension_fist", "4": "flexing_big_finger"}

# Выпадающие меню для выбора человека и жеста
label_person = tk.Label(root, text="Выберите человека:")
label_person.grid(row=4, column=0, padx=5, pady=5)

person_menu = ttk.Combobox(root, values=[f"{k} - {v}" for k, v in person_options.items()])
person_menu.grid(row=4, column=1, padx=5, pady=5)

label_gesture = tk.Label(root, text="Выберите жест:")
label_gesture.grid(row=4, column=2, padx=5, pady=5)

gesture_menu = ttk.Combobox(root, values=[f"{k} - {v}" for k, v in gesture_options.items()])
gesture_menu.grid(row=4, column=3, padx=5, pady=5)

# Кнопка для сохранения данных
button_save = tk.Button(root, text="Сохранить данные", command=save_data)
button_save.grid(row=5, column=0, columnspan=4, padx=5, pady=5)

# Запуск GUI
root.mainloop()
