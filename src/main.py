
from image_handler import ImageHandler
import global_data
import config
import simulation


def set_starting_marker_position_as_current():
    global_data.starting_x_position = (config.distance_between_motors - config.final_image_width) / 2
    global_data.starting_y_position = config.starting_height_from_top

    global_data.current_marker_position_x = global_data.starting_x_position
    global_data.current_marker_position_y = global_data.starting_y_position



def create_steps_file():
    open(config.steps_file_path, "w")
            
def main() -> None:
    set_starting_marker_position_as_current()
    create_steps_file()

    img_handler = ImageHandler()
    img_handler.read_image()
    img_handler.process_image()
    img_handler.initialize_image_objects()
    img_handler.generate_steps()
    sim = simulation.Simulation()
    sim.create_simulation()


if __name__=="__main__":
    main()
