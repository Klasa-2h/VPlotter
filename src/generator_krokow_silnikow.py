from config import *
from luk import Luk
import os


def odleglosc_na_kroki(odleglosc: float) -> int:
    return int(odleglosc / dlugosc_sznurka_na_krok)


def oblicz_dlugosc_prawego_sznurka(x, y):
    return math.sqrt((motor_spacing - x)**2 + y**2)


class GeneratorKrokowSilnikow:
    def __init__(self, luki: list[Luk]):
        self.luki = luki
        self.odleglosc_miedzy_lukami = self.luki[1].radius - self.luki[0].radius
        self.kroki = []

    def generuj(self):

        for luk_index in range(0, len(self.luki)-2, 2):
            # W jednej petli rysuje 2 luki (jeden w gore i drugi w dol)
            luk1, luk2 = self.luki[luk_index], self.luki[luk_index+1]
            # poniewaz wracamy z gory na dol, od konca do poczatku
            luk2.odwroc()
            odleglosc_miedzy_pikselami = luk1.dlugosc_luku / len(luk1.pixels)

            # Ide w gore pierwszego luku
            for pixcel in luk1.pixels:
                self.kroki += self.natezenie_na_kroki(pixcel)
                self.kroki += [obrot["prawy_silnik_prawo"] + "\n" for _ in range(odleglosc_na_kroki(odleglosc_miedzy_pikselami))]

            # Przechodze do nastepnego promienia (ruch lewym)
            self.kroki += [obrot["lewy_silnik_prawo"] + "\n"] * odleglosc_na_kroki(odleglosc_miedzy_lukami)

            # Wyrownuje prawym
            dlugosc_prawego_sznurka_do_przesuniecia = (oblicz_dlugosc_prawego_sznurka(luk1.end_x, luk1.end_y) -
                                                       oblicz_dlugosc_prawego_sznurka(luk2.start_x, luk2.start_y))
            if dlugosc_prawego_sznurka_do_przesuniecia >= 0:
                self.kroki += [obrot["prawy_silnik_prawo"] + "\n"] * odleglosc_na_kroki(dlugosc_prawego_sznurka_do_przesuniecia)
            else:
                self.kroki += [obrot["prawy_silnik_lewo"] + "\n"] * odleglosc_na_kroki(-dlugosc_prawego_sznurka_do_przesuniecia)
            # Ide w dol drugiego luku
            for pixcel in luk2.pixels:
                self.kroki += self.natezenie_na_kroki(pixcel)
                self.kroki += [obrot["prawy_silnik_lewo"] + "\n" for _ in range(odleglosc_na_kroki(odleglosc_miedzy_pikselami))]
            # Ide na poczatek kolejnego luku
            luk3 = self.luki[luk_index+2]

            self.kroki += [obrot["lewy_silnik_prawo"] + "\n"] * odleglosc_na_kroki(odleglosc_miedzy_lukami)
            dlugosc_prawego_sznurka_do_przesuniecia = (oblicz_dlugosc_prawego_sznurka(luk2.end_x, luk2.end_y) -
                                                       oblicz_dlugosc_prawego_sznurka(luk3.start_x,
                                                                                      luk3.start_y))
            if dlugosc_prawego_sznurka_do_przesuniecia < 0:
                self.kroki += [obrot["prawy_silnik_lewo"] + "\n"] * odleglosc_na_kroki(-dlugosc_prawego_sznurka_do_przesuniecia)
            else:
                self.kroki += [obrot["prawy_silnik_prawo"] + "\n"] * odleglosc_na_kroki(dlugosc_prawego_sznurka_do_przesuniecia)

    def natezenie_na_kroki(self, pixcel) -> list[str]:
        wysokosc_wyskoku = self.odleglosc_miedzy_lukami / maksymalne_natezenie_barw * pixcel
        kroki = odleglosc_na_kroki(wysokosc_wyskoku)
        return [obrot["lewy_silnik_lewo"] + "\n" for _ in range(kroki)] + [obrot["lewy_silnik_prawo"] + "\n" for _ in range(kroki)]

    def zapisz_do_pliku(self):
        with open(os.path.join(resources_folder, "kroki.txt"), "w") as file:
            file.writelines(self.kroki)
    