import cv2
import logging

logger = logging.getLogger("models")

class foucault_test_model:
    def __init__(self):
        self.image_list = list()
        self.mirror_diameter = 200
        self.mirror_roc = 1000
        self.conic_constant = 0
        self.zone_count = 10
        self.mirror_pixel_radius = 1500
        self.greyscale_bar_width_percent = 1
        self.reduce_image_size_factor = 4
        self.center_obstruction = 0
        self.image_smooth_factor = 10

    def add_image_model(self, image_model):
        logger.debug("add_image_model")
        self.image_list.append(image_model)

    def generate_config_dict(self):
        return {
            "mirror_diameter": self.mirror_diameter,
            "mirror_roc": self.mirror_roc,
            "zone_count": self.zone_count,
            "greyscale_bar_width_percent": self.greyscale_bar_width_percent,
            "conic_constant": self.conic_constant,
            "mirror_pixel_radius": self.mirror_pixel_radius,
            "image_smooth_factor": self.image_smooth_factor,
        }

    def clear(self):
        logger.debug("clear")
        self.image_list = list()

    def change(self, key, value):
        logger.debug("change key %s to %s"%(key, value))
        setattr(self, key, int(value))


class image_model:
    def __init__(self, filepath, image=None, position=0):
        self.position = position
        self.filepath = filepath
        self.filename = filepath.split("/")[-1]
        if image == None:
            self.image = cv2.imread(self.filepath, flags=cv2.IMREAD_REDUCED_GRAYSCALE_4 )
        else:
            self.image = image
        self.crop_image = None
        self.g1 = None
        self.g2 = None
        self.zones = list()


