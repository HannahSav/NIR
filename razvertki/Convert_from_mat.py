# Created by Hannah at 02.07.2024 1:05
from matplotlib import pyplot as plt
from scipy.io import loadmat
from Razvertka_Buhshtabera import sliding_window, pca_projection, plot_projection_diff_plots


file_path = 'resources/S1_E1_A1.mat'
file_path_2 = 'resources/S1_E2_A1.mat'
file_path_3 = 'resources/S1_E3_A1.mat'

# Загрузка данных из .mat файла
mat_data = loadmat(file_path)
mat_data_2 = loadmat(file_path_2)
mat_data_3 = loadmat(file_path_3)

print(mat_data.keys())
# Теперь из mat_data достаем данные ЭМГ

i = 6 # номер датчика 0-8
a = 30000 # начало среза эксперимента по времени
b = a+60000 # конец среза эксперимента по времени
# а+1000,a+10000 - сдвиг по времени, чтобы упражнения шли параллельно

emg_data = mat_data['emg'][:, i][a+10000:b+10000][7000:21000:100]
emg_data_2 = mat_data_2['emg'][:, i][a+5000:b+5000][7000:21000:100]
emg_data_3 = mat_data_3['emg'][:, i][a:b][7000:21000:100]


# Создание массива для временной оси (примерно так, как это может выглядеть)
time_axis = range(len(emg_data))
# Построение графика
plt.figure(figsize=(10, 6))


# Построение первого ряда данных
plt.plot(time_axis, emg_data, label='EMG Data (File 1)', color='blue', alpha = 0.5)
# Построение второго ряда данных
plt.plot(time_axis, emg_data_2, label='EMG Data (File 2)', color='red', alpha = 0.5)
# Построение первого ряда данных
plt.plot(time_axis, emg_data_3, label='EMG Data (File 3)', color='green', alpha = 0.5)


plt.title('EMG Data Comparison')
plt.xlabel('Timestamps')
plt.ylabel('Amplitude, mV')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()


n = 100
r = 2

# print('asdfghjkl;')
vector_columns = sliding_window(emg_data, n)
vector_columns_2 = sliding_window(emg_data_2, n)
vector_columns_3 = sliding_window(emg_data_3, n)

pca1 = pca_projection(vector_columns, r)
pca2 = pca_projection(vector_columns_2, r)
pca3 = pca_projection(vector_columns_3, r)

dict = {}
dict['exercise 1'] = pca1
dict['exercise 2'] = pca2
dict['exercise 3'] = pca3

plot_projection_diff_plots(dict, r, "")
