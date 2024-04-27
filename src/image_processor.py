import math

from PIL import Image
import numpy as np
from config import *
from src.luk import Luk


class ImageProcessor:
    def __init__(self) -> None:
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

    def mono_image(self) -> None:
        self.image = self.image.convert('L')

    def podziel_na_luki(self) -> list[Luk]:
        r = math.sqrt(start_x**2 + start_y**2)
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

                    if (abs(r - math.sqrt((start_y + i*self.rozmiar_piksela + self.rozmiar_piksela/2) ** 2 +
                                          (start_x + j*self.rozmiar_piksela + self.rozmiar_piksela/2)**2))
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
                luki.append(Luk(luk[::-1], sx*self.rozmiar_piksela+start_x, sy*self.rozmiar_piksela+start_y, ex*self.rozmiar_piksela+start_x, ey*self.rozmiar_piksela+start_y, r))

            r += odleglosc_miedzy_lukami
            luk = []

        return luki

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
