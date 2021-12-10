# Tool to visualize 3d bbox in pointcloud (could potentially display it along with corresponding 2d image for sanity check)
import open3d as o3d
from matplotlib import cm
import numpy as np

import argparse
import os

# README.md:
# Valid examplex: 
# ``python viz_annotations.py </abs/path/to/folder/frame_0000xxxx/> -b``
# ``python viz_annotations.py </abs/path/to/folder/frame_0000xxxx/>``

# ** The expected result is a single frame in open3d viewer that has pointcloud of annotated/segmented pedestrians. 
# ** The -b flag is optional, which draws a bounding box around the pedestrians
# ** To view at right orientation, orient the blue axis to point up, green to the left, and red into the screen.
# (pressing down ctrl or shift will help rotate or lateral move, scroll to zoom in/out)

INTENSITY_MAX = 17000000
COLOR_RANGE = INTENSITY_MAX / 255


def viz_helper(frame_fd, draw_bbox):

    ann_path = frame_fd + "Annotations/"

    viewer = o3d.visualization.Visualizer()
    viewer.create_window()

    for ann_file in os.listdir(ann_path):
        fp = ann_path + ann_file
        data_rows = np.genfromtxt(fp, delimiter=' ')

        # Commented out is code that colors with original intensity
        # pcd_colors_arr = []
        # for v in data_rows[:,3]:
        #     intensity_val = int(min(v, INTENSITY_MAX) / COLOR_RANGE)
        #     rgb = cm.jet(intensity_val)[:-1]
        #     pcd_colors_arr.append(rgb)
        # pcd_colors = o3d.utility.Vector3dVector(pcd_colors_arr)

        pcd_points = o3d.utility.Vector3dVector(data_rows[:,:3])
        pcd_colors = None
        if "pedestrian" in ann_file:
            # Make all ped points red, and add a bbox around to indicate/distinguish the annotation
            pcd_colors = o3d.utility.Vector3dVector([(1, 0, 0) for _ in range(len(data_rows))])

            if draw_bbox:
                bbox = o3d.geometry.AxisAlignedBoundingBox.create_from_points(pcd_points)
                lines = o3d.geometry.LineSet.create_from_axis_aligned_bounding_box(bbox)
                viewer.add_geometry(lines)
        elif "background" in ann_file:
            # Make all points for background blue
            pcd_colors = o3d.utility.Vector3dVector([(0, 0, 1) for _ in range(len(data_rows))])

        else:
            print("Skipping invalid annotation file name:", ann_file)
            continue

        pcd = o3d.geometry.PointCloud()
        pcd.points = pcd_points
        pcd.colors = pcd_colors

        viewer.add_geometry(pcd)

    opt = viewer.get_render_option()
    opt.show_coordinate_frame = True
    opt.background_color = np.asarray([0.5, 0.5, 0.5])
    opt.point_size = 3

    viewer.run()
    viewer.destroy_window()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='visualize annotations')
    parser.add_argument('path', help='/abs/path/to/folder/frame_0000xxxx/', type=str)
    parser.add_argument('-b','--bbox', help='Add bounding boxes on top of segmentation', action='store_true')

    args = parser.parse_args()
    frame_fd = args.path

    viz_helper(frame_fd, args.bbox)
