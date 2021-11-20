# Tool to visualize 3d bbox in pointcloud (along with 2d image?) for verification and sanity check
from dt2_model import ObjectDetctor
from utils import mat_to_im
import scipy.io as sio
import sys
import os
import numpy as np
import matplotlib.pyplot as plt


HUMAN_CLASS_ID = 0

if len(sys.argv) != 3:
    print("Usage: python viz__bbox.py <path to mat folder> <0000xxxx>")
    exit(0)

mat_folder, file_name = sys.argv[1:]
mat_file = os.path.join(mat_folder, 'xl_visual' + file_name + '.mat')

# visualize the raw grayscale data
mat_contents = sio.loadmat(mat_file)
img_content = mat_contents['ans'][0,0]['data']
arr = np.asarray(img_content)
plt.imshow(arr, cmap='gray', vmin=0, vmax=40)
plt.show()

# visualize the detection results
image = mat_to_im(mat_file)
model = ObjectDetctor()
model.inference(image)
model.visualize_result()
