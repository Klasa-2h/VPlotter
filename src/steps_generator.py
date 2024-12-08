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


def distribute_and_save_steps(target1, target2):
    n = max(abs(target1), abs(target2))

    result = [[0, 0] for _ in range(n)]

    def distribute_single_value(target, index):
        values = [0] * n
        # Count how many 1's and -1's are needed
        ones_needed = target
        step = 1 if ones_needed > 0 else -1

        # Distribute 1's or -1's across the list evenly
        for i in range(abs(ones_needed)):
            values[i] = step

        return values

    # Distribute for target1 (first element of each pair)
    first_elements = distribute_single_value(target1, 0)
    for i in range(n):
        result[i][0] = first_elements[i]

    # Distribute for target2 (second element of each pair)
    second_elements = distribute_single_value(target2, 1)
    for i in range(n):
        result[i][1] = second_elements[i]

    for line in result:
        save_steps_to_file(line)


def move(end_x, end_y, use_steps_in_reserve=False):
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

    distribute_and_save_steps(steps_left, steps_right)

    global_data.current_marker_position_x = end_x
    global_data.current_marker_position_y = end_y


def save_steps_to_file(steps) -> None:
    with open(config.steps_file_path, "a") as file:
        file.writelines(" ".join([str(steps[0]),str(steps[1])])+"\n")

