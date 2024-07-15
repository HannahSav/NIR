# Created by Hannah at 15.07.2024 15:26
'''
Доп функции для развертки:
1) графики исходных данных
2) графики проекций
TODO: 3) парсеры данных
TODO: UI (чтобы выбирать что отобразить)
TODO: правильные описания функций по красоте чтоб высвечивались
'''



from matplotlib import pyplot as plt


'''
Функция для отображения графиков исходных данных (на одном графике)

На вход передаем 

columns_name: словарь
Название для легенды: список данных

data_name: название самого графика

ДОБАВИТЬ: ЕДИНИЦЫ ИЗМЕРЕНИЯ ПО ОСЯМ 
'''
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


'''
Построение проекций на r = 2 и  r = 3

на вход: 

projection_dict: словарь с данными
r : размерность
data_name : название графа
'''
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

