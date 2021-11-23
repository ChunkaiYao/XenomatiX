import os
from numpy.random.mtrand import f
import scipy.io as sio
import matplotlib.pyplot as plt
import numpy as np

def print_mat_file(dir='.'):
    files = [f for f in os.listdir(dir) if os.path.isfile(f)]
    for f in files[:]:
        if not f.endswith('.mat'):
            files.remove(f)
    # print(files)
    return files

def convert_mat_png(file_list):
    for mat_fname in file_list:
        mat_contents = sio.loadmat(mat_fname)
        img_content = mat_contents['ans'][0,0]['data']
        arr = np.asarray(img_content)
        plt.imshow(arr, cmap='gray', vmin=0, vmax=255)
        # plt.show()
        file_name = mat_fname.split('.')[0]
        # print(file_name)
        plt.imsave(file_name + '.png', arr, cmap='gray', vmin=0, vmax=255)
        print(file_name + '.png saved!')


if __name__ == "__main__":
    mat_files = print_mat_file()
    convert_mat_png(mat_files)