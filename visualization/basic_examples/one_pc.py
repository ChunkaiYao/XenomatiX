import open3d as o3d
import numpy as np
import csv
import os

folder = "/home/mcity/xenomatix/visualization/pc_csv/"

pcd_frames = []

for fn in os.listdir(folder):
    with open(folder + fn) as csvfile:
        pcd_single_frame = []
        data_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in data_reader:
            if 'NaN' in row[0:3]:
                continue
            # xyz = np.asarray([float(n) / 5000 for n in row[0:3]])
            # xyz = np.asarray(row[0:3])
            xyz = np.asarray([float(row[0]), float(row[1]), float(row[2])])
            # print(xyz)
            pcd_single_frame.append(xyz)
        # pcd = o3d.geometry.PointCloud()
        pcd_points = o3d.utility.Vector3dVector(pcd_single_frame)
        pcd_frames.append(pcd_points)



pcd = o3d.geometry.PointCloud()
pcd.points = pcd_frames[len(pcd_frames) // 2]
geometries = [pcd]

viewer = o3d.visualization.Visualizer()
viewer.create_window()
for geometry in geometries:
    viewer.add_geometry(geometry)
opt = viewer.get_render_option()
opt.show_coordinate_frame = True
opt.background_color = np.asarray([0.5, 0.5, 0.5])
opt.point_size = 3.5

viewer.run()
viewer.destroy_window()
