import math

from PIL import Image
import numpy as np
from config import *
from pixcel import Pixcel


class ImageProcessor:
    def __init__(self) -> None:
        self.wysokosc_obrazu = None
        self.wysokosc_piksele = None
        self.szerokosc_piksele = None
        self.rozmiar_piksela = None
        self.image = None
        
    def read_image(self, img_path: str) -> None:
        self.image = Image.open(img_path)
        self.szerokosc_piksele, self.wysokosc_piksele, _ = np.array(self.image).shape

    def zmiana_rozmiaru(self):
        zadana_wysokosc=pikseli_pionowo
        wysokosc,szerokosc, _ = np.array(self.image).shape
        proporcja=szerokosc/wysokosc
        nowa_szerokosc=int(zadana_wysokosc*proporcja)
        self.szerokosc_piksele = nowa_szerokosc
        self.wysokosc_piksele = zadana_wysokosc
        self.image = Image.fromarray(np.array(self.image)).resize((nowa_szerokosc, zadana_wysokosc), 4)

        self.rozmiar_piksela = szerokosc_obrazu / self.szerokosc_piksele
        self.wysokosc_obrazu = szerokosc_obrazu/proporcja

    def mono_image(self) -> None:
        self.image = self.image.convert('L')

    def process_intensity_scale_and_reverse(self):
        gorny_limit = maksymalne_natezenie_barw
        szerokosc, wysokosc = self.image.size
        piksele = np.array(self.image)
        for y in range(wysokosc):
            for x in range(szerokosc):
                jasnosc = piksele[y, x]
                nowa_jasnosc = int(jasnosc * gorny_limit // 255)
                piksele[y, x] = gorny_limit - nowa_jasnosc
        self.image = Image.fromarray(piksele)

    def get_image_with_pixcel_objects(self):
        pixcel_image = []
        for y in range(len(np.array(self.image))):
            pixcel_image.append([])
            for x in range(len(np.array(self.image)[0])):
                pixcel_image[-1].append(Pixcel(x, y, np.array(self.image)[y][x]))
        return pixcel_image