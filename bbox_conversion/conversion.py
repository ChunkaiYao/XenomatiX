from dt2_model import ObjectDetctor
from utils import mat_to_im, mat_to_pc

import re
import sys
import os
from typing import List
import numpy as np

HUMAN_CLASS_ID = 0

# for each image frame
#   get bbox (x,y 2d box), find corresponding pc frame
#   scan thru all pc points
#       if points is within ith bbox, put in to ith bucket
#   for each bucket
#       find median of depth to create 3d box (x, y, median_z)
#       output the result (box coord or label points in box)

# future problem: if output must be all original pc with labeled (in box ith), we need code changes

IM_PREFIX = "xl_visual"
PC_PREFIX = "xw_pointcloud" 

def get_frame_ids(im_fd: str, pc_fd: str) -> List[str]:
    """Return a list a frame ids that present in both im and pc folders"""
    im_ids = [re.findall("\d+", fn)[0] for fn in os.listdir(im_fd)]
    pc_ids = [re.findall("\d+", fn)[0] for fn in os.listdir(pc_fd)]

    return list(set(im_ids).intersection(set(pc_ids)))

def convert(im_fd: str, pc_fd: str, out_fd: str):
    """Converts 2D bbox in image to 3D bbox in pointcloud"""
    model = ObjectDetctor()
    im_fd_prefix = im_fd + IM_PREFIX
    pc_fd_prefix = pc_fd + PC_PREFIX

    for frame_id in sorted(get_frame_ids(im_fd, pc_fd)):
        # Run 2D detection model to obtain all bbox in current frame
        im_arr = mat_to_im(im_fd_prefix + frame_id + ".mat")
        model.inference(im_arr)
        bbox_list = model.get_bbox(HUMAN_CLASS_ID)

        # Each bbox will have a list of pointclouds that are enclosed by it
        enclosed_pc_data = [[] for _ in range(len(bbox_list))]

        # Load corresponding frame of pc data to capture points that fall in the 2D bbox
        pcs = mat_to_pc(pc_fd_prefix + frame_id + ".mat")
        for row in pcs:
            if np.isnan(row).any():
                # skip rows with NaN values
                continue

            # (u, v) are the 1:1 mapping from pc to pixel
            pc_u, pc_v = row[5], row[4]
            pc_x, pc_y, pc_z = row[0], row[1], row[2]

            for i, (x1, y1, x2, y2) in enumerate(bbox_list):
                if (pc_u > y1 and pc_u < y2) and (pc_v > x1 and pc_v < x2):
                    # TODO: include other pc data if needed (for final output format)
                    enclosed_pc_data[i].append((pc_x, pc_y, pc_z))

        for pc_list in enclosed_pc_data:
            # find the depth median of all points, and set that as center depth of box
            # then we extend 1 meter on both sides to form a more accurate 3d bbox
            all_depth = [pc[0] for pc in pc_list]
            depth_median = np.median(all_depth)

            # Capture all pcs in the 3d bbox
            enc_pcs = []
            for pc in pc_list:
                # Only needs to check depth because hese pc
                # already fall within width and height range of box (x1, y1, x2, y2)
                if pc[0] > depth_median - 1000 and pc[0] < depth_median + 1000:
                    enc_pcs.append(pc)
            
            # output the result (box coord or label points in box)
            print("num pc in box", len(enc_pcs))
            print("depth median", depth_median)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python conversion.py <path to dir of img> <path to dir of pc> <output path>")
        exit(0)
    
    im_folder, pc_folder, output_folder = sys.argv[1:]
    convert(im_folder, pc_folder, output_folder)
