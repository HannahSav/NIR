# Created by Hannah at 19.10.2024 10:09
import json
import os

import numpy as np
from helper_viewer import view_buhshtaber

from sklearn.decomposition import PCA

avanty_dict = {
    'Avanti sensor 1 - brachioradialis: EMG 1' : 'emg 1',
    'Avanti sensor 2: EMG 2':'emg 2',
    'Avanti sensor 3 - palmaris longus: EMG 3': 'emg 3',
    'Avanti sensor 4: EMG 4':'emg 4',
    'Avanti sensor 5: EMG 5': 'emg 5',
    'Avanti sensor 6: EMG 6': 'emg 6',
    'Avanti sensor 7: EMG 7': 'emg 7',
    'Avanti sensor 8: EMG 8': 'emg 8'

}
def sliding_window(series, n):
    return np.array([series[i:i + n] for i in range(len(series) - n + 1)])


def pca_projection(vectors, r=3):
    pca = PCA(n_components=r)
    return pca.fit_transform(vectors)

# snaps = 100 # сколько точек отстроить
skip = 2 # сколько пропускать
N_slises = 150
r = 4
prog0 = 0
prog1 = 1
# prog2 = 3

def same_from_one_file(file):
    full_dict = {}
    plot_name = file
    with open(file, 'r') as f:
        data = json.load(f)
    for d in data:
        # print(file, d['save_time'])
        my_dict = d['data']
        for k, k_new in avanty_dict.items():
            my_dict[k_new] = my_dict[k]
            my_dict.pop(k)

        for k, v in my_dict.items():
            # 100 1-4
            # my_dict[k] = pca_projection(sliding_window(v[::len(v)//snaps], N_slises), r)
            my_dict[k] = pca_projection(sliding_window(v[::skip], N_slises), r)
        set_name = d['file_name'][: 2]+d['file_name'][-13: -5]
        full_dict[set_name] = my_dict
        # print(d['data'].keys())
    view_buhshtaber(full_dict, plot_name+'\n N={} r={} projections: pc{},pc{}'.format(N_slises, r, prog0, prog1), prog0, prog1, 2, 2)

def diff_files(files):
    full_dict = {}
    plot_name = "diff_gestures"
    for file in files:
        with open(file, 'r') as f:
            d = json.load(f)[0]
        my_dict = d['data']
        for k, k_new in avanty_dict.items():
            my_dict[k_new] = my_dict[k]
            my_dict.pop(k)

        for k, v in my_dict.items():
            # 100 1-4
            # my_dict[k] = pca_projection(sliding_window(v[::len(v)//snaps], N_slises), r)
            my_dict[k] = pca_projection(sliding_window(v[::skip], N_slises), r)
        set_name = d['file_name'][: 2]+d['file_name'][-13: -5]
        full_dict[set_name] = my_dict
    view_buhshtaber(full_dict, plot_name+'\n N={} r={} projections: pc{},pc{}'.format(N_slises, r, prog0, prog1), prog0, prog1, 2, 2)


def buhshtabera():
    print("SAME")
    data_to_plot = {}
    pth = 'cutted_data/raw2'
    files = os.listdir('cutted_data/raw2')
    files_all = []
    for file in files:
        same_from_one_file(pth+'/'+file)
        files_all.append(pth+'/'+file)
    diff_files(files_all)


if __name__ == '__main__':
    buhshtabera()