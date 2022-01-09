import cv2

class foucault_test_model:
    def __init__(self):
        self.image_list = list()
        self.mirror_diameter = 200
        self.mirror_roc = 1000
        self.conic_constant = 0
        self.zone_count = 10
        self.greyscale_bar_width_percent = 0.01

    def add_image_model(self, image_model):
        self.image_list.append(image_model)

    def generate_config_dict(self):
        return {
            "mirror_diameter": self.mirror_diameter,
            "mirror_roc": self.mirror_roc,
            "zone_count": self.zone_count,
            "bar_width": self.greyscale_bar_width_percent,
            "conic_constant": self.conic_constant,
        }


class image_model:
    def __init__(self, filepath, image=None, position=0):
        self.position = position
        self.filepath = filepath
        self.filename = filepath.split("/")[-1]
        if image == None:
            self.image = cv2.imread(self.filepath)
        else:
            self.image = image
        self.crop_image = None
        self.g1 = None
        self.g2 = None
        self.zones = list()


