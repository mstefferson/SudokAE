import numpy as np
from glob import glob


def read_data(dir2read):
    all_files = glob(dir2read + '*')
    data = []
    for f in all_files:
        data.append(np.loadtxt(f))
    data = np.array(data)
    data = data.reshape(data.shape[0], data.shape[1] * data.shape[2])
    return data


if __name__ == '__main__':
    dir2read = 'data/easy/x/'
    x = read_data(dir2read)
    dir2read = 'data/easy/y/'
    y = read_data(dir2read)
    print(x[0])
    print(y[0])
