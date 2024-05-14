import math
from config import *
from PIL import Image, ImageDraw
import os

class Simulation:
    def __init__(self) -> None:
        self.mm_na_px = 3.77957517575
        self.start_x = start_x*self.mm_na_px
        self.start_y = start_y*self.mm_na_px
        self.motor_spacing = motor_spacing*self.mm_na_px
        self.l_str_length = math.sqrt(self.start_x**2 + self.start_y**2)
        self.r_str_length = math.sqrt((self.motor_spacing - self.start_x)**2 + self.start_y**2)
        self.dlugosc_sznurka_na_krok = dlugosc_sznurka_na_krok*self.mm_na_px
        self.marker = True

        self.img = Image.new("RGB", (int(self.motor_spacing), int(self.motor_spacing)), "white") #wysokość jako odległość między silnikami
        self.symulacja = ImageDraw.Draw(self.img)
        
    def wart_y(self, left_string_length: float, right_string_length: float):
        p = (self.motor_spacing + left_string_length + right_string_length)/2
        pole = math.sqrt(p*(p-right_string_length)*(p-left_string_length)*(p-self.motor_spacing))
        return (2*pole)/self.motor_spacing

    def wart_x(self, left_string_length: float, right_string_length: float):
        return math.sqrt(left_string_length**2 - self.wart_y(left_string_length, right_string_length)**2)
    
    def rysuj(self, zmiana_lewego_sznurka, zmiana_prawego_sznurka):
        end_x = self.wart_x(self.l_str_length + zmiana_lewego_sznurka, self.r_str_length + zmiana_prawego_sznurka)
        end_y = self.wart_y(self.l_str_length + zmiana_lewego_sznurka, self.r_str_length + zmiana_prawego_sznurka)
        if self.marker:
            self.symulacja.line([(self.start_x, self.start_y), (end_x, end_y)], fill = "black", width = 1)
        self.start_x, self.start_y, self.l_str_length, self.r_str_length = end_x, end_y, self.l_str_length+zmiana_lewego_sznurka, self.r_str_length+zmiana_prawego_sznurka
        
    def stworz_symulacje(self):
        with open(os.path.join(resources_folder, "kroki.txt"), "r") as kroki:
            lines = kroki.readlines()
            for line in lines:
                match line.strip():
                    case "10":
                        self.rysuj(self.dlugosc_sznurka_na_krok, 0)
                    case "11":
                        self.rysuj(-self.dlugosc_sznurka_na_krok, 0)
                    case "01":
                        self.rysuj(0, self.dlugosc_sznurka_na_krok)
                    case "00":
                        self.rysuj(0, -self.dlugosc_sznurka_na_krok)
                    case "1":
                        self.marker = False
                    case "0":
                        self.marker = True
        self.img.show()


