import config
import math
import global_data

def transform_distance_per_steps(distance, use_steps_in_reserve=False):
    if not use_steps_in_reserve:
        return round(distance / config.length_of_the_rope_per_step), 0
    steps = distance / config.length_of_the_rope_per_step
    freaction_remainder = steps - int(steps)
    return steps, freaction_remainder


def calculate_length_right_rope(x, y):
    return math.sqrt((config.distance_between_motors - x)**2 + y**2)


def calculate_length_left_rope(x, y):
    return math.sqrt(x**2 + y**2)


def move(end_x, end_y, use_steps_in_reserve=False):
    steps = []
    
    start_right_rope_length = calculate_length_right_rope(global_data.current_marker_position_x, global_data.current_marker_position_y)
    start_left_rope_length = calculate_length_left_rope(global_data.current_marker_position_x, global_data.current_marker_position_y)
    end_right_rope_length = calculate_length_right_rope(end_x,end_y)
    end_left_rope_length = calculate_length_left_rope(end_x,end_y)

    delta_right_rope_length = end_right_rope_length - start_right_rope_length
    delta_left_rope_length = end_left_rope_length - start_left_rope_length
    
    steps_left, left_reserve = transform_distance_per_steps(delta_left_rope_length)
    steps_right, right_reserve = transform_distance_per_steps(delta_right_rope_length)
    """
    if use_steps_in_reserve:
        if abs(global_data.steps_in_reserve_l) >= 1:
            steps_left += int(global_data.steps_in_reserve_l)
            global_data.steps_in_reserve_l -= int(global_data.steps_in_reserve_l)
        if abs(global_data.steps_in_reserve_r) >= 1:
            steps_right += int(global_data.steps_in_reserve_r)
            global_data.steps_in_reserve_r -= int(global_data.steps_in_reserve_r)

        global_data.steps_in_reserve_l += left_reserve
        global_data.steps_in_reserve_r += right_reserve
    """

    steps.append(steps_left)
    steps.append(steps_right)
    
    save_steps_to_file(steps)

    global_data.current_marker_position_x = end_x
    global_data.current_marker_position_y = end_y


def save_steps_to_file(steps) -> None:
    with open(config.steps_file_path, "a") as file:
        file.writelines(" ".join([str(steps[0]),str(steps[1])])+"\n")

