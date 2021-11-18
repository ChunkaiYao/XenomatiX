from numpy import genfromtxt
from PIL import Image
import matplotlib.pyplot as plt
from os import listdir

# grey_scale_arr = genfromtxt('grey1314.csv', delimiter=',')

# print(len(grey_scale_arr), len(grey_scale_arr[0]))

# flat = grey_scale_arr.flatten()
# # for i, val in enumerate(flat):
# #     if val > 255:
# #         flat[i] = 255
# # norm = max(flat) / 255
# # for i in range(len(flat)):
# #     flat[i] /= norm
# print(max(flat), sum(flat) / len(flat))
# vmax_all = max(flat)
# # img = Image.fromarray(grey_scale_arr, 'L')
# # img.show()

# plt.imshow(grey_scale_arr, cmap='gray', vmin=0, vmax=vmax_all)
# plt.show()

folder = "im_csv/"

img = None

for fn in sorted(listdir(folder)):
    grayscale_arr = genfromtxt(folder + fn, delimiter=',')
    print(fn)
    if img is None:
        img = plt.imshow(grayscale_arr, cmap='gray', vmin=0, vmax=255)
    else:
        img.set_data(grayscale_arr)
    plt.pause(0.00001)
    plt.draw()


