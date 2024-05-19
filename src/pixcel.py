from config import *

class Pixcel:
    def __init__(self, x, y, natezenie, rozmiar_piksela):
        self.x = x
        self.y = y
        self.natezenie = natezenie
        self.rozmiar_piksela = rozmiar_piksela
        self.start_x = start_x  
        self.start_y = start_y
        self.xmm = self.get_xmm()
        self.ymm = self.get_ymm()

    def get_xmm(self):
        return self.x * self.rozmiar_piksela + self.start_x

    def get_ymm(self):
        return self.y * self.rozmiar_piksela + self.start_y









