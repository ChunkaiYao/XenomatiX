from numpy import genfromtxt
from PIL import Image
import matplotlib.pyplot as plt
from os import listdir

grey_scale_arr = genfromtxt('im_csv/xl_visual00005407.xim.csv', delimiter=',')
# print(grey_scale_arr)

# bounding boxes x1, y1, x2, y2
# 606, 77, 730, 421

box_width = 10

x1 = 606
y1 = 77
x2 = 730
y2 = 421

for r in range(y1, y2):
    for c in range(x1, x2):
        if (r < y1 + box_width or r > y2 - box_width) or (c < x1 + box_width or c > x2 - box_width):
            grey_scale_arr[r][c] = 0
            # print(r, c)

plt.imshow(grey_scale_arr, cmap='gray', vmin=0, vmax=255)
plt.show()