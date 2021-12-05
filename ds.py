
import os
import re
import sys
from shutil import copyfile

if len(sys.argv) != 3:
    print("Usage: python ds.py </path/to/Raw/> </path/to/output/>")
    print("Make sure to add the ending '/' in path")

data_folder = sys.argv[1]
out_folder = sys.argv[2]

xim_frame_ids = []
xpc_frame_ids = set()

for fn in sorted(os.listdir(data_folder)):
    frame_id = re.findall("\d+", fn)[0]
    if ".xim" in fn:
        xim_frame_ids.append(frame_id)
    elif ".xpc" in fn:
        xpc_frame_ids.add(frame_id)

print("number of xim:", len(xim_frame_ids))
print("number of xpc:", len(xpc_frame_ids))

# down-sample: sample 1 frame per 20 frames
sample_ratio = 20
samples = []

idx = 0
max_idx = len(xim_frame_ids)
while idx < max_idx:
    if xim_frame_ids[idx] in xpc_frame_ids:
        samples.append(xim_frame_ids[idx])
        # advance to next sampling once corresponding xpc frame exists
        idx += sample_ratio
    else:
        idx += 1

print("number of samples:", len(samples))
IM_PREFIX = "xl_visual"
PC_PREFIX = "xw_pointcloud"

for fid in samples:
    xim = IM_PREFIX + fid + ".xim"
    xpc = PC_PREFIX + fid + ".xpc"
    copyfile(data_folder + xim, out_folder + xim)
    copyfile(data_folder + xpc, out_folder + xpc)
