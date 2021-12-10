This folder contains py scripts to visualize primarily point cloud (data format is csv, but can modify for any) and also grayscale images (`viz_im.py` and `anim_im.py`)

Most of these scripts are testing and experimenting with data and the open3d library, so they are not directly usable. 
Nevertheless, the most up-to-date and useful ones are
* `visualizer.py`: a wrapper class to easily animate point cloud frames
* `anim_pc_with_visualizer.py`: an example using the visualizer

In the basic_examples/ folder, there are simple examples of using the open3d API to visualize single point cloud frame. 
The animation is simply building off of that by rendering at each frame.

Tips to orient the 3d space in visualization - use ctrl and shift to rotate or shift the view, and scroll to zoom in/out.
