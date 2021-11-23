import open3d as o3d
import numpy as np
import csv
import math
from matplotlib import cm

# convert 2d bounding box (obtained from 2d image) to 3d bbox within the pointcloud
# optional: visualize both bbox in viz

# img is 512 * 1536
# every pointcloud has a (u, v) that maps to the img pixel (1 to 1 mapping)
# pc: (u, v) (data[4], data[5)]

# reveresd mapping from pixel to pc to find (x, y, z) for 3d bounding boxes
# challenges
# - no perfect mapping from (x, y) -> (u, v) bc of floating point and rounding
# sol 1: make (u, v) to (ceil(u), ceil(v)) and (floor(u), floor(v))
# Also, two choices - replace the xyz with bbox, or make new pc with slight offset of original xyz

fnum = 5407

x1 = 606
y1 = 77
x2 = 730
y2 = 421

bbox_coords = []

box_width = 15

for r in range(y1, y2):
    for c in range(x1, x2):
        if (r < y1 + box_width or r > y2 - box_width) or (c < x1 + box_width or c > x2 - box_width):
            bbox_coords.append((r,c))
            # print(r, c)


# print(bbox_coords)

# add all bbox coords to pc, what for z?

pcd_frames = []
pcd_sf_colors = []

pc_file = "pc_csv/xw_pointcloud00005407.mat.csv"
with open(pc_file) as csvfile:
    pcd_single_frame = []
    data_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in data_reader:
        if 'NaN' in row[0:3]:
            continue

        # max_bound = 32000
        # range_val = int(min(float(row[6]), max_bound) / (max_bound / 255))
        # rgb = cm.jet(range_val)[:-1]

        max_bound = 400000
        refelctivity = float(row[3]) * float(row[6]) * float(row[6]) / 200000 / 200000
        refelctivity = min(refelctivity, max_bound)

        ref_val = int(refelctivity / (max_bound / 255))
        rgb = cm.jet(ref_val)[:-1]

        # max_bound = 3300000
        # intensity_val = int(min(float(row[3]), max_bound) / (max_bound / 255))
        # rgb = cm.jet(intensity_val)[:-1]

        xyz = np.asarray([float(row[0]), float(row[1]), float(row[2])])
        # print(rgb)
        
        # try to match r, c
        u, v = float(row[5]), float(row[4])
        # print(u, v)
        u1, v1 = math.ceil(u), math.ceil(v)
        u2, v2 = math.floor(u), math.floor(v)
        if (u1, v1) in bbox_coords:
            pcd_single_frame.append(xyz)
            pcd_sf_colors.append((0.1, 0.1, 0.1))
            # print(u1, v1)
        elif (u2, v2) in bbox_coords:
            pcd_single_frame.append(xyz)
            pcd_sf_colors.append((0.1, 0.1, 0.1))
            # print(u2, v2)
        else:
            pcd_single_frame.append(xyz)
            pcd_sf_colors.append(rgb)
        
        # print(xyz)
        
    # pcd = o3d.geometry.PointCloud()
    pcd_points = o3d.utility.Vector3dVector(pcd_single_frame)
    pcd_colors = o3d.utility.Vector3dVector(pcd_sf_colors)
    pcd_frames.append((pcd_points, pcd_colors))


pcd = o3d.geometry.PointCloud()
pcd.points = pcd_frames[0][0]
pcd.colors = pcd_frames[0][1]
geometries = [pcd]

viewer = o3d.visualization.Visualizer()
viewer.create_window()
for geometry in geometries:
    viewer.add_geometry(geometry)
opt = viewer.get_render_option()
opt.show_coordinate_frame = True
opt.background_color = np.asarray([0.5, 0.5, 0.5])
opt.point_size = 3

viewer.run()
viewer.destroy_window()