from config import *
from pixcel import Pixcel
import os


def odleglosc_na_kroki(odleglosc: float) -> int:
    return int(odleglosc / dlugosc_sznurka_na_krok)


def oblicz_dlugosc_prawego_sznurka(x, y):
    return math.sqrt((motor_spacing - x)**2 + y**2)


class GeneratorKrokowSilnikow:
    def __init__(self, obraz: list[list[Pixcel]]):
        self.obraz = obraz
        self.kroki = []

    def generuj(self):
        for row in self.obraz[:-1:]:
            for pixcel in row[:-1:]:
                # Tutaj robimy ten dzyndzel od natezenia
                dlugosc_dzyndzla = max_dlugosc_dzyndzli * (pixcel.natezenie/maksymalne_natezenie_barw)
                ilosc_krokow_dzyndzla = odleglosc_na_kroki(dlugosc_dzyndzla)

                self.kroki += ["11\n" for _ in range(ilosc_krokow_dzyndzla)]
                self.kroki += ["10\n" for _ in range(ilosc_krokow_dzyndzla)]

                # to nizej to na dodatkowy kontrast
                self.kroki += ["00\n" for _ in range(ilosc_krokow_dzyndzla)]
                self.kroki += ["01\n" for _ in range(ilosc_krokow_dzyndzla)]
                # A potem idziemy do nastepnego piksela
                lewy_do_rozwiniecia = abs(math.sqrt(pixcel.xmm**2+pixcel.ymm**2)
                                          - math.sqrt(row[pixcel.x+1].xmm**2 + row[pixcel.x+1].ymm**2))
                prawy_do_zwiniecia = abs(math.sqrt((motor_spacing-pixcel.xmm)**2 + pixcel.ymm**2)
                                         - math.sqrt((motor_spacing - row[pixcel.x+1].xmm)**2 + row[pixcel.x+1].ymm**2))
                self.kroki += ["10\n" for _ in range(odleglosc_na_kroki(lewy_do_rozwiniecia))]
                self.kroki += ["00\n" for _ in range(odleglosc_na_kroki(prawy_do_zwiniecia))]

            self.kroki.append("1\n")

            p1 = row[-1]
            p2 = self.obraz[row[0].y+1][1]

            lewy_do_zwiniecia = math.sqrt(p1.xmm**2 + p1.ymm**2) - math.sqrt(p2.xmm**2 + p2.ymm**2)
            prawy_do_rozwiniecia = abs(math.sqrt((motor_spacing - p1.xmm)**2 + p1.ymm**2)
                                       - math.sqrt((motor_spacing - p2.xmm)**2 + p2.ymm**2))

            self.kroki += ["11\n" for _ in range(odleglosc_na_kroki(lewy_do_zwiniecia))]
            self.kroki += ["01\n" for _ in range(odleglosc_na_kroki(prawy_do_rozwiniecia))]

            self.kroki.append("0\n")


    def zapisz_do_pliku(self):
        with open(os.path.join(resources_folder, "kroki.txt"), "w") as file:
            file.writelines(self.kroki)
    