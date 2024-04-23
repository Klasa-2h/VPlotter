from config import *
from luk import Luk
import os


def odleglosc_na_kroki(odleglosc: float) -> int:
    return int(odleglosc / dlugosc_sznurka_na_krok)


class GeneratorKrokowSilnikow:
    def __init__(self, luki: list[Luk]):
        self.luki = luki
        self.odleglosc_miedzy_lukami = self.luki[1].radius - self.luki[0].radius
        self.kroki = []

    def generuj(self):
        for luk in self.luki:
            odleglosc_miedzy_pikselami = luk.dlugosc_luku / len(luk.pixels)
            for pixcel in luk.pixels:
                self.kroki += self.natezenie_na_kroki(pixcel)

    def natezenie_na_kroki(self, pixcel) -> list[str]:
        wysokosc_wyskoku = self.odleglosc_miedzy_lukami / 7 * pixcel
        kroki = odleglosc_na_kroki(wysokosc_wyskoku)
        return [obrot["lewy_silnik_lewo"] + "\n" for _ in range(kroki)] + [obrot["lewy_silnik_prawo"] + "\n" for _ in range(kroki)]

    def zapisz_do_pliku(self):
        with open(os.path.join(resources_folder, "kroki.txt"), "w") as file:
            file.writelines(self.kroki)
