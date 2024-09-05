import math


class Luk:
    def __init__(self, pixels, start_x: int, start_y: int, end_x: int, end_y: int, radius: int):
        self.pixels = pixels
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.radius = radius
        self.angle = self.oblicz_kat_luku()
        self.dlugosc_luku = self.oblicz_dlugosc_luku()

    def oblicz_kat_luku(self):
        c = math.sqrt((self.start_x - self.end_x)**2 + (self.start_y - self.end_y)**2)
        sinus_polowy = (c/2)/self.radius
        polowa_kata = math.degrees(math.asin(sinus_polowy))
        return round(polowa_kata * 2, 2)

    def oblicz_dlugosc_luku(self):
        return (self.angle * math.pi * self.radius) / 180

    def odwroc(self):
        self.pixels = self.pixels[::-1]
        self.start_x, self.start_y, self.end_x, self.end_y = self.end_x, self.end_y, self.start_x, self.start_y

