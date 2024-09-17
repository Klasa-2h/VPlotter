import config


current_marker_position_x = None
current_marker_position_y = None

image_width_pixcels = None
image_height_pixcels = None

distance_between_pixcels_horizontally = None
distance_between_pixcels_vertically = None

image_ratio = None
final_image_height = None

steps_in_reserve_r = 0
steps_in_reserve_l = 0

starting_x_position = None
starting_y_position = None

length_of_the_rope_per_step = config.motor_step_angle / 360 * config.motor_diameter * 3.1415
