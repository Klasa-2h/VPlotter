import math

image_path = "C:/Users/murek/Projects/VPlotter/res/zadanie2.png"
steps_file_path = "C:/Users/murek/Projects/VPlotter/res/steps.txt"

color_range = 8

final_image_width = 150
starting_height_from_top = 200
distance_between_motors = 1000
motor_diameter = 20
motor_step = 0.1125 * 2
length_of_the_rope_per_step = motor_step / 360 * motor_diameter * math.pi

resolution_vertically = 10
resolution_horizontally = 30

