from config import *
from pixcel import Pixcel
import os


def odleglosc_na_kroki(odleglosc: float) -> int:
    return int(odleglosc / dlugosc_sznurka_na_krok)


def oblicz_dlugosc_prawego_sznurka(x, y):
    return math.sqrt((motor_spacing - x)**2 + y**2)


def oblicz_dlugosc_lewego_sznurka(x, y):
    return math.sqrt(x**2 + y**2)


class GeneratorKrokowSilnikow:
    def __init__(self, obraz: list[list[Pixcel]], rozmiar_piksela):
        self.rozmiar_piksela = rozmiar_piksela
        self.obraz = obraz
        self.kroki = []

    def generuj(self):
        for y in range(0, len(self.obraz[:-1:]), 2):
            ymm = start_y + y * self.rozmiar_piksela
            for x in range(ilosc_dzyndzli_poziomo):
                # w tej petli idziemy w prawo
                # obliczam miejsce na kartce gdzie jestesmy
                xmm = start_x + x * odleglosc_miedzy_dzyndzlami
                # rysuje dzyndzel
                i, j = self.znajdz_piksel(xmm, ymm)
                natezenie = self.obraz[j][i].natezenie
                dlugosc_dzyndzla = natezenie / maksymalne_natezenie_barw * max_dlugosc_dzyndzli
                self.kroki += (["11\n" for _ in range(odleglosc_na_kroki(dlugosc_dzyndzla))])
                self.kroki += (["10\n" for _ in range(odleglosc_na_kroki(dlugosc_dzyndzla))])

                # obliczam dlugosci sznurkow do przesuniecia do przejscia na kolejny dzyndzel
                prawy_do_zwiniecia = (oblicz_dlugosc_prawego_sznurka(xmm, ymm)
                                      - oblicz_dlugosc_prawego_sznurka(xmm + odleglosc_miedzy_dzyndzlami, ymm))
                lewy_do_rozwiniecia = -(oblicz_dlugosc_lewego_sznurka(xmm, ymm)
                                        - oblicz_dlugosc_lewego_sznurka(xmm + odleglosc_miedzy_dzyndzlami, ymm))
                # zamieniam dlugosc na kroki
                self.kroki += ["10\n" for _ in range(odleglosc_na_kroki(lewy_do_rozwiniecia))]
                self.kroki += ["00\n" for _ in range(odleglosc_na_kroki(prawy_do_zwiniecia))]
            # przechodze do nastepnej lini w dol
            ymm += self.rozmiar_piksela

            prawy_do_rozwiniecia = -(oblicz_dlugosc_prawego_sznurka(xmm, ymm - self.rozmiar_piksela)
                                    - oblicz_dlugosc_prawego_sznurka(xmm, ymm))
            lewy_do_rozwiniecia = -(oblicz_dlugosc_lewego_sznurka(xmm, ymm - self.rozmiar_piksela)
                                   - oblicz_dlugosc_lewego_sznurka(xmm, ymm))
            # zamieniam dlugosc na kroki
            self.kroki += ["10\n" for _ in range(odleglosc_na_kroki(lewy_do_rozwiniecia))]
            self.kroki += ["01\n" for _ in range(odleglosc_na_kroki(prawy_do_rozwiniecia))]

            for x in range(ilosc_dzyndzli_poziomo - 1, -1, -1):
                # w tej petli idziemy w lewo
                xmm = start_x + x * odleglosc_miedzy_dzyndzlami
                # rysuje dzyndzel
                i, j = self.znajdz_piksel(xmm, ymm)
                natezenie = self.obraz[j][i].natezenie
                dlugosc_dzyndzla = natezenie / maksymalne_natezenie_barw * max_dlugosc_dzyndzli
                self.kroki += (["11\n" for _ in range(odleglosc_na_kroki(dlugosc_dzyndzla))])
                self.kroki += (["10\n" for _ in range(odleglosc_na_kroki(dlugosc_dzyndzla))])

                prawy_do_rozwiniecia = -(oblicz_dlugosc_prawego_sznurka(xmm, ymm)
                                         - oblicz_dlugosc_prawego_sznurka(xmm - odleglosc_miedzy_dzyndzlami, ymm))
                lewy_do_zwiniecia = (oblicz_dlugosc_lewego_sznurka(xmm, ymm)
                                     - oblicz_dlugosc_lewego_sznurka(xmm - odleglosc_miedzy_dzyndzlami, ymm))
                self.kroki += ["01\n" for _ in range(odleglosc_na_kroki(prawy_do_rozwiniecia))]
                self.kroki += ["11\n" for _ in range(odleglosc_na_kroki(lewy_do_zwiniecia))]

            ymm += self.rozmiar_piksela

            prawy_do_rozwiniecia = (oblicz_dlugosc_prawego_sznurka(xmm, ymm + self.rozmiar_piksela)
                                    - oblicz_dlugosc_prawego_sznurka(xmm, ymm))
            lewy_do_rozwiniecia = (oblicz_dlugosc_lewego_sznurka(xmm, ymm + self.rozmiar_piksela)
                                   - oblicz_dlugosc_lewego_sznurka(xmm, ymm))

            # zamieniam dlugosc na kroki
            self.kroki += ["10\n" for _ in range(odleglosc_na_kroki(lewy_do_rozwiniecia))]
            self.kroki += ["01\n" for _ in range(odleglosc_na_kroki(prawy_do_rozwiniecia))]



    def znajdz_piksel(self, xmm, ymm):
        ymm -= start_y
        xmm -= start_x
        ymm //= self.rozmiar_piksela
        xmm //= odleglosc_miedzy_dzyndzlami
        xmm = xmm/ilosc_dzyndzli_poziomo*len(self.obraz[0])
        return int(xmm), int(ymm)

    def zapisz_do_pliku(self):
        with open(os.path.join(resources_folder, "Dane.txt"), "w") as file:
            file.writelines(self.kroki)
    