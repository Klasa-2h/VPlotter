import math

from PIL import Image
import numpy as np
from config import *
from luk import Luk


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

    def podziel_na_luki(self) -> tuple[float, list[Luk]]:
        r1 = round(math.sqrt(start_x ** 2 + (start_y + rozmiar_piksela / 2) ** 2), 3)
        r2 = round(math.sqrt(start_x ** 2 + (start_y + rozmiar_piksela / 2 + rozmiar_piksela) ** 2), 3)
        odleglosc_miedzy_lukami = round(r2 - r1, 2)
        r = r1
        img = np.array(self.image)
        luki = []
        luk = []
        czy_pusty = False

        while not czy_pusty:
            sx = None
            sy = None
            ex = None
            ey = None

            for i in range(len(img)):
                for j in range(len(img[0])-1, -1, -1):

                    if (abs(r - math.sqrt((start_y + i*rozmiar_piksela + rozmiar_piksela/2) ** 2 +
                                          (start_x + j*rozmiar_piksela + rozmiar_piksela/2)**2))
                            <= odleglosc_miedzy_lukami/2):

                        luk.append(img[i][j])

                        if sx is None and sy is None:
                            sx = i
                            sy = j

                        ex = i
                        ey = j

            if len(luk) == 0:
                czy_pusty = True

            else:
                luki.append(Luk(luk[::-1], sx*rozmiar_piksela+start_x, sy*rozmiar_piksela+start_y, ex*rozmiar_piksela+start_x, ey*rozmiar_piksela+start_y, r))

            r += odleglosc_miedzy_lukami
            luk = []

        return odleglosc_miedzy_lukami, luki

    def process_intensity_scale(self):
        gorny_limit = maksymalne_natezenie_barw
        szerokosc, wysokosc = self.image.size
        piksele = np.array(self.image)
        for y in range(wysokosc):
            for x in range(szerokosc):
                jasnosc = piksele[y, x]
                nowa_jasnosc = int(jasnosc * gorny_limit // 255)
                piksele[y, x] = nowa_jasnosc
                nowa_jasnosc -= gorny_limit
        self.image = Image.fromarray(piksele)