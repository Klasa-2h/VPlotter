import math


image_path = "../res/zadanie2.png"
steps_file_path = "../res/Dane.txt"


color_range = 8


final_image_width = 200
starting_height_from_top = 200


resolution_vertically = 50
resolution_horizontally = 400

distance_between_motors = 1000
motor_diameter = 20
motor_step = 0.1125 * 16
length_of_the_rope_per_step = motor_step / 360 * motor_diameter * math.pi


simulation_line_thickness = 1



