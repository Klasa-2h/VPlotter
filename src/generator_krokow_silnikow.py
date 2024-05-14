from config import *
from luk import Luk
import os


def odleglosc_na_kroki(odleglosc: float) -> int:
    return int(odleglosc / dlugosc_sznurka_na_krok)


def oblicz_dlugosc_prawego_sznurka(x, y):
    return math.sqrt((motor_spacing - x)**2 + y**2)


class GeneratorKrokowSilnikow:
    def __init__(self, obraz):
        self.obraz = obraz
        self.kroki = []

    def generuj(self):
        pass

    def zapisz_do_pliku(self):
        with open(os.path.join(resources_folder, "kroki.txt"), "w") as file:
            file.writelines(self.kroki)
    