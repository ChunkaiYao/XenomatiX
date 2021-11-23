** Pointcloud
- Animation approaches
  1. load all frames in memory, then play all frames after
  2. play a frame immediately after loading the data file
- Challenge
  - control the fps


** 2D Images
- Animation
  - Challenge
    - file size ~10MB (512 * 1536), loading time too loading
    - fps becomes very low: ~ 1


** Preparing bbox for training
- convert 2d bounding box (obtained from 2d image) to 3d bbox within the pointcloud
- Challenge
  - 2d box to 3d box (dimension difference)
  - now, we simply map the (x, y) and just use the default z
  - 