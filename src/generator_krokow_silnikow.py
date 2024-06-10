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
                # W tej pętli idziemy w prawo
                xmm = start_x + x * odleglosc_miedzy_dzyndzlami
                i, j = self.znajdz_piksel(xmm, ymm)
                natezenie = self.obraz[j][i].natezenie
                dlugosc_dzyndzla = natezenie / maksymalne_natezenie_barw * max_dlugosc_dzyndzli
                self.kroki += (["11\n" for _ in range(odleglosc_na_kroki(dlugosc_dzyndzla))])
                self.kroki += (["10\n" for _ in range(odleglosc_na_kroki(dlugosc_dzyndzla))])

                prawy_do_zwiniecia = (oblicz_dlugosc_prawego_sznurka(xmm, ymm)
                                      - oblicz_dlugosc_prawego_sznurka(xmm + odleglosc_miedzy_dzyndzlami, ymm))
                lewy_do_rozwiniecia = -(oblicz_dlugosc_lewego_sznurka(xmm, ymm)
                                        - oblicz_dlugosc_lewego_sznurka(xmm + odleglosc_miedzy_dzyndzlami, ymm))
                
                stosunek_p_do_l = abs(prawy_do_zwiniecia / lewy_do_rozwiniecia)
                kroki_lewy = odleglosc_na_kroki(lewy_do_rozwiniecia)
                kroki_prawy = odleglosc_na_kroki(prawy_do_zwiniecia)
                
                # Synchronizacja kroków
                while kroki_lewy > 0 or kroki_prawy > 0:
                    if kroki_lewy > 0:
                        self.kroki.append("10\n")
                        kroki_lewy -= 1
                    if kroki_prawy > 0:
                        self.kroki.append("00\n")
                        kroki_prawy -= 1

            # Przejście do następnej linii w dół
            ymm += self.rozmiar_piksela

            prawy_do_rozwiniecia = -(oblicz_dlugosc_prawego_sznurka(xmm, ymm - self.rozmiar_piksela)
                                    - oblicz_dlugosc_prawego_sznurka(xmm, ymm))
            lewy_do_rozwiniecia = -(oblicz_dlugosc_lewego_sznurka(xmm, ymm - self.rozmiar_piksela)
                                   - oblicz_dlugosc_lewego_sznurka(xmm, ymm))
            
            kroki_lewy = odleglosc_na_kroki(lewy_do_rozwiniecia)
            kroki_prawy = odleglosc_na_kroki(prawy_do_rozwiniecia)
            
            while kroki_lewy > 0 or kroki_prawy > 0:
                if kroki_lewy > 0:
                    self.kroki.append("10\n")
                    kroki_lewy -= 1
                if kroki_prawy > 0:
                    self.kroki.append("01\n")
                    kroki_prawy -= 1

            for x in range(ilosc_dzyndzli_poziomo - 1, -1, -1):
                # W tej pętli idziemy w lewo
                xmm = start_x + x * odleglosc_miedzy_dzyndzlami
                i, j = self.znajdz_piksel(xmm, ymm)
                natezenie = self.obraz[j][i].natezenie
                dlugosc_dzyndzla = natezenie / maksymalne_natezenie_barw * max_dlugosc_dzyndzli
                self.kroki += (["11\n" for _ in range(odleglosc_na_kroki(dlugosc_dzyndzla))])
                self.kroki += (["10\n" for _ in range(odleglosc_na_kroki(dlugosc_dzyndzla))])

                prawy_do_rozwiniecia = -(oblicz_dlugosc_prawego_sznurka(xmm, ymm)
                                         - oblicz_dlugosc_prawego_sznurka(xmm - odleglosc_miedzy_dzyndzlami, ymm))
                lewy_do_zwiniecia = (oblicz_dlugosc_lewego_sznurka(xmm, ymm)
                                     - oblicz_dlugosc_lewego_sznurka(xmm - odleglosc_miedzy_dzyndzlami, ymm))
                
                kroki_lewy = odleglosc_na_kroki(lewy_do_zwiniecia)
                kroki_prawy = odleglosc_na_kroki(prawy_do_rozwiniecia)
                
                while kroki_lewy > 0 or kroki_prawy > 0:
                    if kroki_lewy > 0:
                        self.kroki.append("11\n")
                        kroki_lewy -= 1
                    if kroki_prawy > 0:
                        self.kroki.append("01\n")
                        kroki_prawy -= 1

            ymm += self.rozmiar_piksela

            prawy_do_rozwiniecia = (oblicz_dlugosc_prawego_sznurka(xmm, ymm + self.rozmiar_piksela)
                                    - oblicz_dlugosc_prawego_sznurka(xmm, ymm))
            lewy_do_rozwiniecia = (oblicz_dlugosc_lewego_sznurka(xmm, ymm + self.rozmiar_piksela)
                                   - oblicz_dlugosc_lewego_sznurka(xmm, ymm))
            
            kroki_lewy = odleglosc_na_kroki(lewy_do_rozwiniecia)
            kroki_prawy = odleglosc_na_kroki(prawy_do_rozwiniecia)
            
            while kroki_lewy > 0 or kroki_prawy > 0:
                if kroki_lewy > 0:
                    self.kroki.append("10\n")
                    kroki_lewy -= 1
                if kroki_prawy > 0:
                    self.kroki.append("01\n")
                    kroki_prawy -= 1


    def znajdz_piksel(self, xmm, ymm):
        ymm -= start_y
        xmm -= start_x
        ymm //= self.rozmiar_piksela
        xmm //= odleglosc_miedzy_dzyndzlami
        xmm = xmm/ilosc_dzyndzli_poziomo*len(self.obraz[0])
        return int(xmm), int(ymm)

    def zapisz_do_pliku(self):
        with open(os.path.join(resources_folder, "kroki.txt"), "w") as file:
            file.writelines(self.kroki)
    