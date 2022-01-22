import tkinter as tk
import logging
from afia import analyse
from afia import view
from afia import models
import logging

logger = logging.getLogger("analyse")

class MainApplication:
    def __init__(self, master=None):
        self.master = master
        self.foucault_test_model = models.foucault_test_model()
        callbacks = {
            "analyse": self.run_analysis,
            "apply_offset": self.apply_offset_config,
            "load_images": self.populate_images,
            "clear_images": self.clear_images,
        }
        self.control_view = view.ControlView(master=self.master, 
                                             button_callback_dict=callbacks, 
                                             foucault_test=self.foucault_test_model)
        self.control_view.grid(row=0, column=0)
        self.image_view_list = view.ImageList(self.master)
        self.image_view_list.grid(row=0, column=1)
        self.result_view = view.ResultView(self.master)
        self.result_view.grid(row=0, column=2)

    def _load_images(self, files):
        for file in files:
            image_model = models.image_model(file)
            self.foucault_test_model.add_image_model(image_model)
            self.image_view_list.add_image_model(image_model)
        self.image_view_list.update()


    def run_analysis(self):
        logger.debug("run_analysis")
        analyse.run_analysis(self.foucault_test_model)
        self.image_view_list.update()
        self.result_view.generate_result_plot(self.foucault_test_model)

    def apply_offset_config(self):
        logger.debug("apply_offset_config")
        offset = 0
        for image in self.foucault_test_model.image_list:
            image.position = offset
            offset += 0.1
        self.image_view_list.update()

    def populate_images(self):
        logger.debug("populate_images")
        files = tk.filedialog.askopenfilenames()
        self._load_images(files)

    def clear_images(self):
        logger.debug("clear_images")
        self.foucault_test_model.clear()
        self.image_view_list.clear()
        self.image_view_list.update()


  
def main():  
    logging.basicConfig(level=logging.DEBUG)
    root = tk.Tk()
    MainApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main()