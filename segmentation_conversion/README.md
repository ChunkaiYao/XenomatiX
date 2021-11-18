I recommend using python venv. There's no requirements.txt, so just install anything you need :p

The driver code is seg_conv.py. Run it as:
``python seg_conv.py /abs/path/to/images/ /abs/path/to/pointclouds /abs/path/to/output/``

Note:
- The images and pointclouds must be in .mat format (use Rodrigo's matlab script to convert)
- You must use absolute path and include the ending '/' in your paths for the arguments
- It takes 1-2 seconds to process each frame, so you could try with less frames first to see results faster

To verify the annotations, run:
``python viz_annotations.py </abs/path/to/folder/> <frame_0000xxxx>``

The expected result is a single frame in open3d viewer that has pointcloud of
pedestrians in red and boxed while the background points are blue. 
You want to orient the blue axis to point up, green to the left, and red into the screen.

TODO:
- [x] Visualiza the results, so we can verify the segmentation conversion is correct and good
