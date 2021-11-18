import open3d as o3d
import numpy as np

xyz = np.random.rand(100, 3) * 10000
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(xyz)

xyz2 = np.random.rand(100, 3) * 10000
pcd2 = o3d.geometry.PointCloud()
pcd2.points = o3d.utility.Vector3dVector(xyz2)

xyz3 = np.random.rand(100, 3) * 10000
pcd3 = o3d.geometry.PointCloud()
pcd3.points = o3d.utility.Vector3dVector(xyz3)
# print(xyz, xyz2, xyz3)
geometries = [pcd, pcd2, pcd3]

viewer = o3d.visualization.Visualizer()
viewer.create_window()
for geometry in geometries:
    viewer.add_geometry(geometry)
opt = viewer.get_render_option()
opt.show_coordinate_frame = True
opt.background_color = np.asarray([0.5, 0.5, 0.5])
print(opt.point_size)
# ctv = viewer.get_view_control()
# ctv.change_field_of_view(0)
# print(ctv.get_field_of_view())
# ctv.rotate(10, 0, 0)
viewer.run()
viewer.destroy_window()
