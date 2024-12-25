# Created by Hannah at 20.10.2024 17:07
import json
import os

from helper_viewer import show_heatmap_emg, plot_heatmap

# , , , , , m. extensor digitorum, m. extensor carpi radialis brevis, m. extensor carpi radialis longus

avanty_dict = {
    'Avanti sensor 1 - brachioradialis: EMG 1' : 'm. brachioradialis',
    'Avanti sensor 2: EMG 2':'m. flexor carpi radialis',
    'Avanti sensor 3 - palmaris longus: EMG 3': 'm. palmaris longus',
    'Avanti sensor 4: EMG 4':'m. flexor carpi ulnaris',
    'Avanti sensor 5: EMG 5': 'm. extensor carpi ulnaris',
    'Avanti sensor 6: EMG 6': 'm. extensor digitorum',
    'Avanti sensor 7: EMG 7': 'm. extensor carpi radialis brevis',
    'Avanti sensor 8: EMG 8': 'm. extensor carpi radialis longus'
}

def heat_map_many_from_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    for i, d in enumerate(data):
        columns_data = d['data']
        time = d['time_data']
        plot_heatmap(columns_data, time, "fist clenching"+str(i+1))

def heat_map_from_one_file(file_path, name):
    with open(file_path, 'r') as f:
        data = json.load(f)
    data = data[-1]
    print(file_path, data.keys())
    columns_data = data['data']
    time = data['time_data']
    plot_heatmap(columns_data, time, name)


if __name__ == '__main__':
    pth = 'cutted_data/smooth'
    files = os.listdir(pth)
    files_all = []
    names=["fist clenching", "finger extension", "thumb elevation"]
    # heat_map_many_from_file(pth+'/'+files[7])
    # for i, file in enumerate(files[7:]):
    heat_map_from_one_file(pth + '/' + files[8], "thumb elevation")
