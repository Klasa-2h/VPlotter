import numpy as np
from PIL import Image
from steps_generator import move
import config
import global_data


class ImageHandler:

    def __init__(self):
        self.img = None
        self.lines = []

    def read_image(self):
        self.img = Image.open(config.image_path)
        global_data.image_height_pixcels, global_data.image_width_pixcels, _ = np.array(self.img).shape
        global_data.image_ratio = round(global_data.image_width_pixcels / global_data.image_height_pixcels, 3)
        global_data.final_image_height = round(config.final_image_width / global_data.image_ratio)
        print("Image read with size of: ", global_data.image_width_pixcels, global_data.image_height_pixcels, "Ratio: ", global_data.image_ratio, "Hight in milimeters: ", global_data.final_image_height)



    def process_image(self):
        # czarnobialy obraz + redukcja skali szarosci
        if self.img is not None:
            self.img = self.img.convert("L")
            print("Image converted to grayscale")
            pixcels = np.array(self.img)
            for y in range(global_data.image_height_pixcels):
                for x in range(global_data.image_width_pixcels):
                    brightness = pixcels[y][x]
                    new_brightness = int(brightness * config.color_range // 255)
                    pixcels[y][x] = config.color_range - new_brightness
            self.img = Image.fromarray(pixcels)
            print(f"Grayscale brightness range reduced to {config.color_range} shades of gray and inverted")

    def initialize_image_objects(self):
        for line in np.array(self.img):
            self.lines.append(Line(line))
        print("Image converted to an array of Line() objects")

    def generate_steps(self):
        for i in range(config.resolution_vertically):
            self.lines[i].generate_steps()
            if i != global_data.image_height_pixcels - 1:
                move(global_data.current_marker_position_x, global_data.current_marker_position_y + global_data.final_image_height/config.resolution_vertically)



class Line:
    def __init__(self, pixcels: list[int]):
        self.pixcels = pixcels  # jako argument tego obiektu przekazuj linie z img_handler.img

    def generate_steps(self):
        for i in range(config.resolution_horizontally):
            # rysujemy piksel i idziemy dalej
            pass


