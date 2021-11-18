import torch
TORCH_VERSION = ".".join(torch.__version__.split(".")[:2])
CUDA_VERSION = torch.__version__.split("+")[-1]
print("torch: ", TORCH_VERSION, "; cuda: ", CUDA_VERSION)

# Some basic setup:
# Setup detectron2 logger
# import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()

# import some common libraries
import numpy as np
import cv2
# import os, json, cv2, random

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog

class ObjectDetctor:
    """Wrapper class for running detectron2 model for object detection on images"""

    def __init__(self):
        """Load a default COCO model"""
        MODEL_CONFIG = "COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"
        print("Loading model:", MODEL_CONFIG)

        self.cfg = get_cfg()
        # add project-specific config (e.g., TensorMask) here if you're not running a model in detectron2's core library
        self.cfg.merge_from_file(model_zoo.get_config_file(MODEL_CONFIG))
        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # set threshold for this model
        # Find a model from detectron2's model zoo. You can use the https://dl.fbaipublicfiles... url as well
        self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(MODEL_CONFIG)
        self.cfg.MODEL.DEVICE = "cpu"

        self.predictor = DefaultPredictor(self.cfg)
        self.im = None
        self.results = None

    def inference(self, im_arr: np.ndarray):
        """Perform detection on given image and store output to internal state"""
        # input im_arr is of form (np.ndarray) – an image of shape (H, W, C) (in BGR order).
        self.im = im_arr
        self.results = self.predictor(im_arr)

        # Alternatively, load a png file to np array
        #im = cv2.imread("./xl_visual00005482.png")
        # cv2.imshow("test", im)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    def get_bbox(self, class_id: int) -> np.ndarray:
        """Get all class_id bounding boxes of the image in shape (N*4) and form (x1,y1,x2,y2)"""
        # look at the outputs. See https://detectron2.readthedocs.io/tutorials/models.html#model-output-format
        # for specification
        # print(self.results["instances"].pred_classes)
        # print(self.results["instances"].pred_boxes)

        if self.results is None:
            # TODO: or only expose this func and run inference within here?
            # if not, need to add this check to the vis funcs too
            print("Must run inference() before get_bbox()")
            return np.empty((0))

        target_class_bbox = []
        for i, instance_class in enumerate(self.results["instances"].pred_classes):
            if instance_class == class_id:
                bbox = self.results["instances"].pred_boxes[i]
                target_class_bbox.append(bbox.tensor.numpy()[0])
        # print(target_class_bbox)
        # converet the detectorn2 Boxes object to numpy array and return
        return np.array(target_class_bbox)

    def save_result_as_png(self, filename):
        """Save the result of image with bounding boxes and labels as .png"""
        v = Visualizer(self.im[:, :, ::-1], MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]), scale=1.2)
        out = v.draw_instance_predictions(self.results["instances"].to("cpu"))
        cv2.imwrite(filename + ".png", out.get_image()[:, :, ::-1])

    def visualize_result(self):
        """
        For testing only - Visualize the result of image with bounding boxes and labels 
        (press 0 to terminate)
        """
        v = Visualizer(self.im[:, :, ::-1], MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]), scale=1.2)
        out = v.draw_instance_predictions(self.results["instances"].to("cpu"))
        cv2.imshow("test", out.get_image()[:, :, ::-1])
        cv2.waitKey(0)
        cv2.destroyAllWindows()