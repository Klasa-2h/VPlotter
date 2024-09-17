import config
import math
import global_data

def transform_distance_per_steps(distance):
    steps = distance / global_data.length_of_the_rope_per_step
    freaction_remainder = steps - int(steps)
    return int(steps), freaction_remainder


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

    if use_steps_in_reserve:
        global_data.steps_in_reserve_l += left_reserve
        global_data.steps_in_reserve_r += right_reserve
        if abs(global_data.steps_in_reserve_l) >= 1:
            if global_data.steps_in_reserve_l < 0:
                steps_left -= 1
                global_data.steps_in_reserve_l += 1
            else:
                steps_left += 1
                global_data.steps_in_reserve_l -= 1

        if abs(global_data.steps_in_reserve_r) >= 1:
            if global_data.steps_in_reserve_r < 0:
                steps_right -= 1
                global_data.steps_in_reserve_r += 1
            else:
                steps_right += 1
                global_data.steps_in_reserve_r -= 1

    steps.append(steps_left)
    steps.append(steps_right)

    save_steps_to_file(steps)

    global_data.current_marker_position_x = end_x
    global_data.current_marker_position_y = end_y


def save_steps_to_file(steps) -> None:
    with open(config.steps_file_path, "a") as file:
        file.writelines(" ".join([str(steps[0]),str(steps[1])])+"\n")

