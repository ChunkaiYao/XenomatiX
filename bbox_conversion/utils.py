import scipy.io as sio
import numpy as np

def mat_to_im(mat_filename):
    """Convert grayscale image as .mat data to npdarry of (H, W, 3)"""
    mat_contents = sio.loadmat(mat_filename)
    img_content = mat_contents['ans'][0,0]['data']

    # Convert pixel values to uint8 (min: 0, max: 255) 
    # and fill RGB with same values to create grayscale image ((512, 1536) --> (512, 1536, 3))
    arr2d = np.asarray([[np.uint8(min(255, pix_val)) for pix_val in row] for row in img_content])
    arr3d = np.repeat(arr2d[:, :, None], repeats=3, axis=2)
    return arr3d

def mat_to_pc(mat_filename):
    """Convert pointcloud data as .mat data to npdarry of (R, 3)"""
    mat_contents = sio.loadmat(mat_filename)
    pcs_content = mat_contents['ans'][0,0]['data']

    # return pcs_content[:,:3]
    return pcs_content

# pcs = mat_to_pc("/home/mcity/Desktop/eastern_market_xpc/pc_mat/xw_pointcloud00005391.mat")
# print(pcs[0])
# print(np.isnan(pcs[0]).any())