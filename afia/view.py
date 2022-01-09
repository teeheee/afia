import tkinter as tk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ImageView:
    def __init__(self, master=None, row=0):
        self.master = master
        self.image_model = None
        self.row = row

    def set_image_model(self, image_model):
        self.image_model = image_model
        self.update()

    def generate_input_image_widget(self):
        self.figure = Figure(figsize=(1, 1), dpi=100)
        axis = self.figure.add_subplot(111)
        axis.imshow(self.image_model.image)
        axis.axis('off')
        canvas = FigureCanvasTkAgg(self.figure, master=self.master)  # A tk.DrawingArea.
        canvas.draw()
        return canvas.get_tk_widget()

    def generate_crop_image_widget(self):
        self.figure = Figure(figsize=(1, 1), dpi=100)
        if self.image_model.crop_image is not None:
            axis = self.figure.add_subplot(111)
            axis.imshow(self.image_model.crop_image)
            offset = len(self.image_model.crop_image)/2
            axis.plot(self.image_model.g1*offset+offset)
            axis.plot(self.image_model.g2*offset/5+offset)
            axis.axis('off')
        canvas = FigureCanvasTkAgg(self.figure, master=self.master)  # A tk.DrawingArea.
        canvas.draw()
        return canvas.get_tk_widget()

    def generate_label_text(self):
        return tk.Label(self.master, text=self.image_model.filename)

    def generate_position_text(self):
        return tk.Label(self.master, text="%02f"%self.image_model.position)

    def generate_zone_text(self):
        return tk.Label(self.master, text=str(self.image_model.zones))

    def update(self):
        self.label_text = self.generate_label_text()
        self.label_text.grid(row=self.row, column=0)
        self.tk_widget = self.generate_input_image_widget()
        self.tk_widget.grid(row=self.row, column=1)
        self.position_text = self.generate_position_text()
        self.position_text.grid(row=self.row, column=2)
        self.crop_image_widget = self.generate_crop_image_widget()
        self.crop_image_widget.grid(row=self.row, column=3)
        self.crop_image_widget = self.generate_zone_text()
        self.crop_image_widget.grid(row=self.row, column=4)


class ImageList(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.image_view_list = list()
        self.master = master
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_propagate(True)
        self.create_canvas()

    def add_image_model(self, image_model):
        row = len(self.image_view_list)
        image_view = ImageView(self.image_frame, row=row)
        image_view.set_image_model(image_model)
        self.image_view_list.append(image_view)

    def create_canvas(self):
        self.canvas = tk.Canvas(self)
        self.canvas.grid(row=0, column=0, sticky="news")
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.vsb.grid(row=0, column=1, sticky='ns')
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.image_frame = tk.Frame(self.canvas)
        self.image_frame.grid(row=0, column=1, sticky='ns')
        self.canvas.create_window((0, 0), window=self, anchor='nw')

    def update(self):
        for image_model in self.image_view_list:
            image_model.update()

class ControlView(tk.Frame):
    def __init__(self, master=None, button_callback_dict=dict(), foucault_test=None):
        super().__init__(master)
        self.config_dict = foucault_test.generate_config_dict()
        self.button_callback_dict = button_callback_dict
        self.input_field_dict = dict()
        self.input_variable_dict = dict()
        self.button_field_dict = dict()
        self.generate_input_fields()

    def generate_input_fields(self):
        for i, key in enumerate(self.config_dict):
            label = key
            value = self.config_dict[key]
            tk.Label(self, text=label).grid(row=i, column=0)
            self.input_variable_dict[key] = tk.StringVar(self, value=value)
            self.input_field_dict[key] = tk.Entry(self, textvariable=self.input_variable_dict[key])
            self.input_field_dict[key].grid(row=i, column=1)
            
        for i, key in enumerate(self.button_callback_dict):
            callback = self.button_callback_dict[key]
            label = key
            i += len(self.config_dict)
            self.button_field_dict[key] = tk.Button(self, text=label, command=callback)
            self.button_field_dict[key].grid(row=i, column=0)

    

class ResultView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        
    def generate_result_plot(self, foucault_test):
        self.figure = Figure(figsize=(8, 5), dpi=100)
        axis = self.figure.add_subplot(111)
        axis.plot(foucault_test.h_mm, foucault_test.w_nm)
        axis.set_xlabel("Radius in mm")
        axis.set_ylabel("spherical deviation in nm")
        canvas = FigureCanvasTkAgg(self.figure, master=self)  # A tk.DrawingArea.
        canvas.draw()
        self.plot_widget = canvas.get_tk_widget()
        self.plot_widget.grid(column=0, row=0)

