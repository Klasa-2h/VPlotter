import math
from config import *
import global_data
from PIL import Image, ImageDraw


class Simulation:
    def __init__(self) -> None:
        self.mm_to_px = 3.9
        self.value_x = global_data.starting_x_position*self.mm_to_px
        self.value_y = global_data.starting_y_position*self.mm_to_px
        self.distance_between_motors = distance_between_motors*self.mm_to_px
        self.l_str_length = math.sqrt(self.value_x**2 + self.value_y**2)
        self.r_str_length = math.sqrt((self.distance_between_motors - self.value_x)**2 + self.value_y**2)
        self.length_of_the_rope_per_step = length_of_the_rope_per_step*self.mm_to_px

        self.img = Image.new("RGB", (int(self.distance_between_motors), int(self.distance_between_motors)), "white") #wysokość jako odległość między silnikami
        self.simulation = ImageDraw.Draw(self.img)
        
    def new_value_y(self, left_string_length, right_string_length):
        p = (self.distance_between_motors + left_string_length + right_string_length)/2
        area = math.sqrt(p*(p-right_string_length)*(p-left_string_length)*(p-self.distance_between_motors))
        return (2*area)/self.distance_between_motors

    def new_value_x(self, left_string_length, right_string_length):
        return math.sqrt(left_string_length**2 - self.new_value_y(left_string_length, right_string_length)**2)
    
    def draw(self, left_string_change, right_string_change):
        end_x = self.new_value_x(self.l_str_length + left_string_change, self.r_str_length + right_string_change)
        end_y = self.new_value_y(self.l_str_length + left_string_change, self.r_str_length + right_string_change)
        self.simulation.line([(self.value_x, self.value_y), (end_x, end_y)], fill = "black", width = simulation_line_thickness)
        self.value_x, self.value_y, self.l_str_length, self.r_str_length = end_x, end_y, self.l_str_length+left_string_change, self.r_str_length+right_string_change
        
    def create_simulation(self):
        with open(steps_file_path, "r") as steps:
            lines = steps.readlines()
            for line in lines:
                data = line.strip()
                data = data.split(' ')
                data[0], data[1] = int(data[0]), int(data[1])
                try:    
                    self.draw(self.length_of_the_rope_per_step*data[0], self.length_of_the_rope_per_step*data[1])
                except Exception as e:
                    print(e)
        self.img.show()
        
