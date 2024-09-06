import numpy as np
from PIL import Image
import config
import global_data


class ImageHandler:

    def __int__(self):
        self.img = None
        self.lines = []

    def read_image(self):
        self.img = Image.open(config.image_path)
        global_data.image_height_pixcels, global_data.image_width_pixcels, _ = np.array(self.img).shape
        print("Image read with size of: ", global_data.image_width_pixcels, global_data.image_height_pixcels)



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
            self.img.show()

    def initialize_image_objects(self):
        # zapisujemy liste Line'ow pod zmienna self.image
        pass

    def generate_steps(self):
        for i in range(len(self.lines)):
            self.lines[i].generate_steps()
            if i != len(self.lines) - 1:
                # przejdz do nastepnej lini
                pass


class Line:
    def __int__(self, pixcels: list[int]):
        self.pixcels = pixcels  # do tego obiektu przekazuj linie z img_handler.img

    def generate_steps(self):
        for i in range(config.resolution_horizontally):
            # rysujemy piksel i idziemy dalej
            pass


