import open3d as o3d
import numpy as np
import time
import csv
import os
from matplotlib import cm

# read csv files and store all frames
# play frame by frame after that

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
            # xyz = np.asarray([float(n) / 5000 for n in row[0:3]])
            xyz = np.asarray([float(row[0]), float(row[1]), float(row[2])])
            # print(xyz)

            # intensity compensated by range
            # refelctivity = float(row[3]) * float(row[6]) * float(row[6]) /200000^2

            # intensity = int(row[3])
            # rgb = cm.jet(intensity% 255)
            # print(intensity, rgb)

            pcd_single_frame.append(xyz)
            # pcd_sf_colors.append(rgb)
        # pcd = o3d.geometry.PointCloud()
        pcd_points = o3d.utility.Vector3dVector(pcd_single_frame)
        pcd_colors = o3d.utility.Vector3dVector(pcd_sf_colors)
        pcd_frames.append(pcd_points)


vis = o3d.visualization.Visualizer()
vis.create_window()
# o3d.utility.set_verbosity_level(o3d.utility.VerbosityLevel.Debug)



# show xyz axis, not showing bc in animation?
opt = vis.get_render_option()
opt.show_coordinate_frame = True
# opt.background_color = np.asarray([0.5, 0.5, 0.5])
opt.point_size = 3.5

# color_op = o3d.visualization.PointColorOption
# color_op.
# opt.point_color_option = color_op
# vis.run()


# xyz = np.random.rand(100, 3)
# pcd_perm.points = o3d.utility.Vector3dVector(xyz)

# open3d needs a permenent/same object, and just update it with new data
pcd_perm = o3d.geometry.PointCloud()
pcd_perm.points = pcd_frames[0]

# o3d.visualization.draw_geometries([pcd_perm])

# print("hi")
# print(pcd_frames[0])

# geometry is the point cloud used in your animaiton
# geometry = o3d.geometry.PointCloud()

vis.add_geometry(pcd_perm)
time.sleep(1)

# for x in range(100):
for pcd_points in pcd_frames:
# for i in range(0, 5):
    # print(i, pcd_list[i])
    # pcd = o3d.geometry.PointCloud()
    # xyz = np.random.rand(100, 3)
    # pcd_perm.points = o3d.utility.Vector3dVector(xyz)

    pcd_perm.points = pcd_points
    # now modify the points of your geometry
    # you can use whatever method suits you best, this is just an example
    # geometry.points = pcd_list[i].points
    vis.update_geometry(pcd_perm) # returns true/false
    time.sleep(0.2)
    vis.poll_events()
    vis.update_renderer()
    

# time.sleep(5)
# vis.destroy_window()