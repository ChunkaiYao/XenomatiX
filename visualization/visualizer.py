import open3d as o3d
from matplotlib import cm
import time

class Visualizer:
    def __init__(self, point_size, color_map_max):
        self.vis = o3d.visualization.Visualizer()
        self.first_frame = True
        self.point_size = point_size
        self.color_map_max = color_map_max
        self.color_range = self.color_map_max / 255

        # o3d requires a permenatn pointCloud object
        self.pcd_perm = o3d.geometry.PointCloud()

    def create_window(self):
        self.vis.create_window()
        opt = self.vis.get_render_option()
        opt.point_size = self.point_size

    def get_rgb(self, val):
        """Maps val to rgb ([0,255], [0,255], [0,255]) given the max bound provided in ctor"""
        normalized_val = int(min(val, self.color_map_max) / self.color_range)
        return cm.jet(normalized_val)[:-1]

    def render(self, pc_frame_data):
        """Render and updates the visualization window for pc_frame, which is a list of xyz points"""
        pcd_single_frame = []
        color_single_frame = []
        for row in pc_frame_data:
            pcd_single_frame.append(row[0:3])
            color_single_frame.append(self.get_rgb(row[3]))
        self.pcd_perm.points = o3d.utility.Vector3dVector(pcd_single_frame)
        self.pcd_perm.colors = o3d.utility.Vector3dVector(color_single_frame)

        if self.first_frame:
            self.vis.add_geometry(self.pcd_perm)
            self.first_frame = False
        else:
            self.vis.update_geometry(self.pcd_perm)
            time.sleep(0.01)  # required for rendering updates
            self.vis.poll_events()
            self.vis.update_renderer()
        
        
