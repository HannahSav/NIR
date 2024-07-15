# Created by Hannah at 15.07.2024 15:18
'''
Собственно сама развертка
PCA - Это??
TODO: проверить что PCA делает то же самое?
'''

import numpy as np
from sklearn.decomposition import PCA

'''
Заглучшка вместо данных (чтоб просто посмотреть на рандомный временной ряд)
'''
def create_time_series(N):
    t = np.linspace(0, 4 * np.pi, N)
    return np.sin(t) + 0.5 * np.random.randn(N)


'''
Формирование скользящих окон длины n из начального временного ряда
(2й пункт метода)
'''
def sliding_window(series, n):
    return np.array([series[i:i + n] for i in range(len(series) - n + 1)])


'''
Проекции при помощи PCA методов
'''
def pca_projection(vectors, r):
    pca = PCA(n_components=r)
    return pca.fit_transform(vectors)
