import os
import math

# ustawienia programu

image_file_name: str = "zadanie2.png"  # plik z folderu res

pikseli_pionowo: int = 100    # Ilosc poziomych lini;   >= 2
maksymalne_natezenie_barw: int = 7
ilosc_dzyndzli_poziomo: int = 175

start_x: float = 420  # odluglosc lewego silnika od lewego-gornego rogu obrazu w poziomie (wspolrzedne x) [milimetry]
start_y: float = 300  # odluglosc lewego silnika od lewego-gornego rogu obrazu w pionie (wspolrzedne y) [milimetry]

krok_silnika: float = 0.1125 * 2  # stopni na jeden krok
motor_spacing: float = 1000  # odleglosc miedzy silnikami
srednica_silnika: float = 20  # [milimetry]

obrot = {"lewy_silnik_prawo": "10",
         "lewy_silnik_lewo": "11",
         "prawy_silnik_lewo": "01",
         "prawy_silnik_prawo": "00",
         "gora": "1",
         "dol": "0"}

grubosc_lini_symulacji = 1

# PONIZSZYCH WARTOSCI NIE ZMIENIAC

szerokosc_obrazu = motor_spacing - 2 * start_x
dlugosc_sznurka_na_krok = krok_silnika / 360 * srednica_silnika * math.pi

resources_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../res"))
image_path = os.path.join(resources_folder, image_file_name)

odleglosc_miedzy_dzyndzlami = szerokosc_obrazu / ilosc_dzyndzli_poziomo
kompresja_w_pionie = .95


