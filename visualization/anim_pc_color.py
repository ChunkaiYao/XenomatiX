import open3d as o3d
import numpy as np
import time
import csv
import os
from matplotlib import cm

folder = "/home/mcity/xenomatix/visualization/pc_csv/"
# folder = "/home/mcity/Desktop/eastern_market_xpc/csvs/"

pcd_frames = []

for fn in os.listdir(folder):
    with open(folder + fn) as csvfile:
        pcd_single_frame = []
        pcd_sf_colors = []
        data_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in data_reader:
            if 'NaN' in row[0:3]:
                continue
            xyz = np.asarray([float(row[0]), float(row[1]), float(row[2])])

            # intensity compensated by range
            # refelctivity = float(row[3]) * float(row[6]) * float(row[6]) /200000^2

            # intensity = int(float(row[3]))
            # range_int = int(float(row[6]))
            max_bound = 3300000 # 500000 ref, 32000 range, 3300000
            refelctivity = float(row[3]) * float(row[6]) * float(row[6]) / 200000 / 200000
            refelctivity = min(refelctivity, max_bound)

            ref_val = int(refelctivity / (max_bound / 255))

            range_val = int(min(float(row[6]), max_bound) / (max_bound / 255))

            intensity_val = int(min(float(row[3]), max_bound) / (max_bound / 255))

            # print(ref_val)
            rgb = cm.jet(intensity_val)[:-1]
            # print(intensity_val)
            # print(intensity, rgb)

            pcd_single_frame.append(xyz)
            pcd_sf_colors.append(rgb)
        # pcd = o3d.geometry.PointCloud()
        pcd_points = o3d.utility.Vector3dVector(pcd_single_frame)
        pcd_colors = o3d.utility.Vector3dVector(pcd_sf_colors)
        pcd_frames.append((pcd_points, pcd_colors))

vis = o3d.visualization.Visualizer()
vis.create_window()
# o3d.utility.set_verbosity_level(o3d.utility.VerbosityLevel.Debug)



# show xyz axis, not showing bc in animation?
opt = vis.get_render_option()
opt.show_coordinate_frame = True
# opt.background_color = np.asarray([0.5, 0.5, 0.5])
opt.point_size = 3

# open3d needs a permenent/same object, and just update it with new data
pcd_perm = o3d.geometry.PointCloud()
pcd_perm.points = pcd_frames[0][0]
pcd_perm.colors = pcd_frames[0][1]
vis.add_geometry(pcd_perm)
time.sleep(1)

for x in range(100):
    for pcd_points, pcd_colors in pcd_frames:

        pcd_perm.points = pcd_points
        pcd_perm.colors = pcd_colors
        # now modify the points of your geometry
        # you can use whatever method suits you best, this is just an example
        # geometry.points = pcd_list[i].points
        vis.update_geometry(pcd_perm) # returns true/false
        time.sleep(0.2)
        vis.poll_events()
        vis.update_renderer()
