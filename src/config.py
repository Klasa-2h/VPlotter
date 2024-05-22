import os
import math

# ustawienia programu

image_file_name: str = "zadanie2.png"  # plik z folderu res

pikseli_pionowo: int = 49   # Ilosc poziomych lini
maksymalne_natezenie_barw: int = 7
odleglosc_miedzy_lukami: float = 8  # [milimetry]

start_x: float = 350  # odluglosc lewego silnika od lewego-gornego rogu obrazu w poziomie (wspolrzedne x) [milimetry]
start_y: float = 450  # odluglosc lewego silnika od lewego-gornego rogu obrazu w pionie (wspolrzedne y) [milimetry]

krok_silnika: float = 0.1125 * 4  # stopni na jeden krok
motor_spacing: float = 1000  # odleglosc miedzy silnikami
srednica_silnika: float = 20  # [milimetry]

obrot = {"lewy_silnik_prawo": "10",
         "lewy_silnik_lewo": "11",
         "prawy_silnik_lewo": "01",
         "prawy_silnik_prawo": "00",
         "gora": "1",
         "dol": "0"}

# PONIZSZYCH WARTOSCI NIE ZMIENIAC

szerokosc_obrazu = motor_spacing - 2 * start_x
dlugosc_sznurka_na_krok = krok_silnika / 360 * srednica_silnika * math.pi

resources_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../res"))
image_path = os.path.join(resources_folder, image_file_name)



