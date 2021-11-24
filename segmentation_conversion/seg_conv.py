from dt2_model import ObjectDetctor
from utils import mat_to_im, mat_to_pc

import re
import sys
import os
import csv
from pathlib import Path
from typing import List
import numpy as np

HUMAN_CLASS_ID = 0

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
    frame_list = get_frame_ids(im_fd, pc_fd)
    i = 0
    total_frames = len(frame_list)

    # down sample
    sample_ratio = 20

    for frame_id in sorted(frame_list):
        if i % sample_ratio != 5:
            i += 1
            continue

        print(i, " / ", total_frames)
        i += 1

        # Run 2D detection model to obtain all bbox in current frame
        im_arr = mat_to_im(im_fd_prefix + frame_id + ".mat")
        model.inference(im_arr)
        # bbox_list = model.get_bbox(HUMAN_CLASS_ID)

        # Load corresponding frame of pc data
        pcs = mat_to_pc(pc_fd_prefix + frame_id + ".mat")
        pcs = np.array(pcs)
        pcs[:,0:3] /= 1000
        pcs[:,3] = (pcs[:,4] - np.min(pcs[:,4])) / (np.max(pcs[:,4]) - np.min(pcs[:,4]))
        pcs = np.round(pcs, 3)
        pcs = pcs.tolist()
        pcs_background_set = set([(round(row[0], 3), round(row[1], 3), round(row[2], 3), round(row[3], 3)) for row in pcs])

        # pcs_background_set = set([row[0:4] for row in pcs])
        # print(pcs_background_set)

        # Create frame dir structure: out_fd/frame_i/Annotations, frame_i.txt
        frame_name = "/frame_" + frame_id
        Path(out_fd + frame_name + "/Annotations").mkdir(parents=True, exist_ok=True)
        with open(out_fd + frame_name + frame_name + ".txt" , "w") as f:
            # write all rows of x,y,z,i
            writer = csv.writer(f, delimiter=" ")
            writer.writerows([row[0:4] for row in pcs])

        seg_counter = 1
        for ped_seg in model.get_segmentation(HUMAN_CLASS_ID):
            # Scan through all pc for each pedestrian segmentation result
            matched_pcs = []
            for row in pcs:

                # (u, v) are the 1:1-ish mapping from pc to pixel
                # so need to adjust to integers to exact match pixel
                pc_u, pc_v = round(row[5]), round(row[4])
                # u1, v1 = math.floor(pc_u), math.floor(pc_v)
                # u2, v2 = math.ceil(pc_u), math.ceil(pc_v)
                # u3, v3 = math.floor(pc_u), math.ceil(pc_v)
                # u4, v4 = math.ceil(pc_u), math.floor(pc_v)

                if (pc_u, pc_v) in ped_seg:
                    matched_pcs.append(row[0:4])

            # estimate depth for 3d
            all_depth = [pc[0] for pc in matched_pcs]
            depth_median = np.median(all_depth)
            
            # filter out of range pcs
            ped_seg_pcs = []
            for pc in matched_pcs:
                pc = tuple(pc)
                if pc[0] > depth_median - 1000 and pc[0] < depth_median + 1000:
                    ped_seg_pcs.append(pc)
                    # remove ped pc from background pc set
                    if pc in pcs_background_set:
                        pcs_background_set.remove(pc)

            # print(len(ped_seg_pcs))
            # output ped pc to annotation file
            anno_path = out_fd + frame_name + "/Annotations"
            if len(ped_seg_pcs) > 100:
                with open(anno_path + "/pedestrian_" + str(seg_counter) + ".txt", "w") as f:
                    writer = csv.writer(f, delimiter=" ")
                    writer.writerows(ped_seg_pcs)
                seg_counter += 1
        
        # output bacground pc to annotation file
        anno_path = out_fd + frame_name + "/Annotations"
        if len(pcs_background_set) > 0:
            with open(anno_path + "/background_1.txt", "w") as f:
                writer = csv.writer(f, delimiter=" ")
                writer.writerows(pcs_background_set)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python conversion.py <path to dir of img> <path to dir of pc> <output path>")
        exit(0)
    
    im_folder, pc_folder, output_folder = sys.argv[1:]
    convert(im_folder, pc_folder, output_folder)
