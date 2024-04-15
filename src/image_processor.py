import math

from PIL import Image
import numpy as np
from config import *


class ImageProcessor:
    def __init__(self) -> None:
        self.wysokosc_piksele = None
        self.szerokosc_piksele = None
        self.image = None
        
    def read_image(self, image_path: str) -> None:
        self.image = Image.open(image_path)
        self.szerokosc_piksele, self.wysokosc_piksele, _ = np.array(self.image).shape

    def zmiana_rozmiaru(self):
        zadana_wysokosc=pikseli_pionowo
        wysokosc,szerokosc, _ = np.array(self.image).shape
        proporcja=szerokosc/wysokosc
        nowa_szerokosc=int(zadana_wysokosc*proporcja)
        self.szerokosc_piksele = nowa_szerokosc
        self.wysokosc_piksele = zadana_wysokosc
        self.image = Image.fromarray(np.array(self.image)).resize((nowa_szerokosc, zadana_wysokosc), 4)
    
    def mono_image(self) -> None:
        self.image = self.image.convert('L')

    def podziel_na_luki(self):
        r1 = round(math.sqrt(start_x ** 2 + (start_y + rozmiar_piksela / 2) ** 2), 1)
        r2 = round(math.sqrt(start_x ** 2 + (start_y + rozmiar_piksela / 2 + rozmiar_piksela) ** 2), 1)
        odleglosc_miedzy_lukami = round(r2 - r1, 1)
        r = r1
        img = np.array(self.image)
        luki = []
        luk = []
        czy_pusty = False
        while not czy_pusty:
            for i in range(len(img)):
                for j in range(len(img[0])):
                    if abs(r - math.sqrt((start_y + i*rozmiar_piksela + rozmiar_piksela/2) ** 2 + (start_x + j*rozmiar_piksela + rozmiar_piksela/2)**2)) <= odleglosc_miedzy_lukami/2:
                        luk.append(img[i][j])
            if len(luk) == 0:
                czy_pusty = True
            else:
                luki.append(luk)
            r += odleglosc_miedzy_lukami
            print(r, len(luk))
            luk = []

        return luki

    def process_intensity_scale(self):
        gorny_limit = maksymalne_natezenie_barw
        szerokosc, wysokosc = self.image.size
        piksele = np.array(self.image)
        for y in range(wysokosc):
            for x in range(szerokosc):
                jasnosc = piksele[y, x]
                nowa_jasnosc = int(jasnosc * gorny_limit // 255)
                piksele[y, x] = nowa_jasnosc
        self.image = Image.fromarray(piksele)
