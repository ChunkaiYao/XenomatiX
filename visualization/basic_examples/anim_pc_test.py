import open3d as o3d
import numpy as np
import time

vis = o3d.visualization.Visualizer()
vis.create_window()
o3d.utility.set_verbosity_level(o3d.utility.VerbosityLevel.Debug)

opt = vis.get_render_option()
opt.show_coordinate_frame = True
opt.background_color = np.asarray([0.5, 0.5, 0.5])
# vis.run()

xyz = np.random.rand(100, 3)
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(xyz)

xyz2 = np.random.rand(100, 3)
pcd2 = o3d.geometry.PointCloud()
pcd2.points = o3d.utility.Vector3dVector(xyz2)

xyz3 = np.random.rand(100, 3)
pcd3 = o3d.geometry.PointCloud()
pcd3.points = o3d.utility.Vector3dVector(xyz3)

# o3d.visualization.draw_geometries([pcd])

# pcd_list = [pcd, pcd2, pcd3]

# # geometry is the point cloud used in your animaiton
geometry = o3d.geometry.PointCloud()
vis.add_geometry(pcd)

for i in range(1, 5):
    # print(i, pcd_list[i])
    # pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(np.random.rand(100, 3))
    # now modify the points of your geometry
    # you can use whatever method suits you best, this is just an example
    # geometry.points = pcd_list[i].points
    time.sleep(0.5)
    print(vis.update_geometry(pcd))
    # time.sleep(1)
    vis.poll_events()
    vis.update_renderer()
    

# # time.sleep(5)
vis.destroy_window()