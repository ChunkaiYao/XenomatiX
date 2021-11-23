from typing import List, Tuple
import scipy.io as sio
import numpy as np

def mat_to_im(mat_filename) -> np.ndarray:
    """Convert grayscale image as .mat data to npdarry of (H, W, 3)"""
    mat_contents = sio.loadmat(mat_filename)
    img_content = mat_contents['ans'][0,0]['data']

    # Convert pixel values to uint8 (min: 0, max: 255) 
    # and fill RGB with same values to create grayscale image ((512, 1536) --> (512, 1536, 3))
    arr2d = np.asarray([[np.uint8(min(255, pix_val)) for pix_val in row] for row in img_content])
    arr3d = np.repeat(arr2d[:, :, None], repeats=3, axis=2)
    return arr3d

def mat_to_pc(mat_filename) -> List[Tuple[np.float64]]:
    """Convert pointcloud data from .mat data to List while filtering out NaN rows"""
    mat_contents = sio.loadmat(mat_filename)
    pcs_content = mat_contents['ans'][0,0]['data']

    # list of tuple (filter out rows that have NaN)
    pc_list = [(row[0], row[1], row[2], row[3], row[4], row[5]) for row in pcs_content if not np.isnan(row).any()]
    # return pcs_content[:,:3]
    return pc_list

# pcs = mat_to_pc("/home/mcity/Desktop/eastern_market_xpc/pc_mat/xw_pointcloud00005391.mat")
# print(pcs[0])
# print(np.isnan(pcs[0]).any())