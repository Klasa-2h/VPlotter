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
        global_data.image_ratio = round(global_data.image_width_pixcels /
                                        global_data.image_height_pixcels, 3)
        global_data.final_image_height = round(config.final_image_width /
                                               global_data.image_ratio)
        global_data.distance_between_pixcels_horizontally = config.final_image_width/config.resolution_horizontally
        global_data.distance_between_pixcels_vertically = global_data.final_image_height/config.resolution_vertically

        print("Image read with size of: ", global_data.image_width_pixcels, global_data.image_height_pixcels,
              "Ratio: ", global_data.image_ratio, "Hight in milimeters: ", global_data.final_image_height)

    def process_image(self):
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
        img_array = np.array(self.img)
        for i in range(config.resolution_vertically):
            self.lines.append(Line(img_array[round(i/config.resolution_vertically * global_data.image_height_pixcels)], i))
        print("Image converted to an array of Line() objects")

    def generate_steps(self):
        print("Generating steps...")

        for i in range(config.resolution_vertically):
            self.lines[i].generate_steps()

            if i != config.resolution_vertically - 1:
                move(global_data.current_marker_position_x,
                     global_data.current_marker_position_y +
                     global_data.final_image_height/config.resolution_vertically)
        print("Steps generated")


class Line:
    def __init__(self, pixcels, num: int):
        self.pixcels = pixcels
        self.num = num
        self.drawing_direction = self.get_drawing_direction()
        if self.drawing_direction == "L":
            self.pixcels = self.pixcels[::-1]

    def generate_steps(self):
        for i in range(config.resolution_horizontally):

            darkness = self.pixcels[int(i/config.resolution_horizontally *
                                          global_data.image_width_pixcels)]

            if darkness > 0:
                move(global_data.current_marker_position_x,
                     global_data.current_marker_position_y -
                     global_data.final_image_height/config.resolution_vertically * darkness/config.color_range)
                move(global_data.current_marker_position_x,
                     global_data.current_marker_position_y +
                     global_data.final_image_height/config.resolution_vertically * darkness/config.color_range)

            if self.drawing_direction == "R":
                move(global_data.current_marker_position_x + global_data.distance_between_pixcels_horizontally,
                     global_data.current_marker_position_y, use_steps_in_reserve=True)
            else:
                move(global_data.current_marker_position_x - global_data.distance_between_pixcels_horizontally,
                     global_data.current_marker_position_y, use_steps_in_reserve=True)

    def get_drawing_direction(self):
        return "R" if self.num % 2 == 0 else "L"

