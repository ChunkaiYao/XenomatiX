# Tool to visualize 3d bbox in pointcloud (along with 2d image?) for verification and sanity check
import open3d as o3d
import numpy as np
import os
import sys

# Example arguments:
# out_fd = "/home/mcity/xenomatix/bbox_conversion/out2/"
# frame_id = "frame_00005404"

if len(sys.argv) != 3:
    print("usage: python viz_annotations.py <path/to/folder/> <frame_0000xxxx>")
    exit(0)
 
out_fd = sys.argv[1]
frame_id = sys.argv[2]

ann_path = out_fd + frame_id + "/Annotations/"

viewer = o3d.visualization.Visualizer()
viewer.create_window()

for ann_file in os.listdir(ann_path):
    fp = ann_path + ann_file
    data_rows = np.genfromtxt(fp, delimiter=' ')
    pcd_points = o3d.utility.Vector3dVector(data_rows[:,:3])
    
    if "pedestrian" in ann_file:
        # Make all ped points red, and add a bbox around to indicate/distinguish the annotation
        pcd_colors = o3d.utility.Vector3dVector([(1, 0, 0) for _ in range(len(data_rows))])
        bbox = o3d.geometry.AxisAlignedBoundingBox.create_from_points(pcd_points)
        lines = o3d.geometry.LineSet.create_from_axis_aligned_bounding_box(bbox)
        viewer.add_geometry(lines)
    elif "background" in ann_file:
        # Make all points for background blue
        pcd_colors = o3d.utility.Vector3dVector([(0, 0, 1) for _ in range(len(data_rows))])

    pcd = o3d.geometry.PointCloud()
    pcd.points = pcd_points
    pcd.colors = pcd_colors

    viewer.add_geometry(pcd)

opt = viewer.get_render_option()
opt.show_coordinate_frame = True
opt.background_color = np.asarray([0.5, 0.5, 0.5])
opt.point_size = 4

viewer.run()
viewer.destroy_window()
