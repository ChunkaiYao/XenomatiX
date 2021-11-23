# Play frames immediately after reading the csv
# use loading file as "real-time" processing and render each frame to see performance

import open3d as o3d
import numpy as np
import time
import csv
import os

vis = o3d.visualization.Visualizer()
vis.create_window()
# o3d.utility.set_verbosity_level(o3d.utility.VerbosityLevel.Debug)

opt = vis.get_render_option()
opt.point_size = 3.5

# IMPORTNAT: open3d needs a permenent/same object, and just update it with new data
pcd_perm = o3d.geometry.PointCloud()

folder = "/home/mcity/Desktop/eastern_market_xpc/csvs/"

flag = False
for fn in os.listdir(folder):

    with open(folder + fn) as csvfile:
        pcd_single_frame = []
        data_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in data_reader:
            if 'NaN' in row[0:3]:
                continue

            xyz = np.asarray([float(row[0]), float(row[1]), float(row[2])])
            pcd_single_frame.append(xyz)

        # For better coloring (e.g. using reflectivity or range)
        # refer to anim_pc_color to incorporate colors here too

        pcd_points = o3d.utility.Vector3dVector(pcd_single_frame)
        pcd_perm.points = pcd_points
        if not flag:
            vis.add_geometry(pcd_perm)
            flag = True

        time.sleep(0.1) # optional, to tune fps
        vis.update_geometry(pcd_perm) # returns true/false
        vis.poll_events()
        vis.update_renderer()
        # print(fn)


