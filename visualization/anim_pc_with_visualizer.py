# Play frames immediately after reading the csv
# use loading file as "real-time" processing and render each frame to see performance

import csv
import os

from visualizer import Visualizer

v = Visualizer(point_size=3, color_map_max=19000000)
v.create_window()

folder = "/home/mcity/Desktop/eastern_market_xpc/csvs/"

for fn in sorted(os.listdir(folder)):

    with open(folder + fn) as csvfile:
        pcd_single_frame = []
        data_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in data_reader:
            if 'NaN' in row[0:3]:
                continue
            pcd_single_frame.append([float(row[0]), float(row[1]), float(row[2]), float(row[3])])

        v.render(pcd_single_frame)


