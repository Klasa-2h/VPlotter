import os
import math

# ustawienia programu

image_file_name: str = "zadanie2.png"   # plik z folderu res

pikseli_pionowo: int = 100
maksymalne_natezenie_barw = 7

start_x: int = 200    # odluglosc lewego silnika od lewego-gornego rogu obrazu w poziomie (wspolrzedne x) [milimetry]
start_y: int = 300    # odluglosc lewego silnika od lewego-gornego rogu obrazu w pionie (wspolrzedne y) [milimetry]
motor_spacing = 1000   # odleglosc miedzy silnikami

rozmiar_piksela = 2    # krawedz piksela [milimetry]

krok_silnika = 0.1125    # stopni na jeden krok
srednica_silnika = 30    # [milimetry]

# PONIZSZYCH WARTOSCI NIE ZMIENIAC

obrot = {"lewy_silnik_prawo":"10", "lewy_silnik_lewo":"11", "prawy_silnik_lewo":"01", "prawy_silnik_prawo":"00", "gora":"1", "dol":"0"}
dlugosc_sznurka_na_krok = krok_silnika / 360 * srednica_silnika * math.pi

resources_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../res"))
image_path = os.path.join(resources_folder, image_file_name)



