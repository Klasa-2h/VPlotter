# ustawienia programu

image_file_name: str = "zadanie2.png"   # plik z folderu res

pikseli_pionowo: int = 100
maksymalne_natezenie_barw = 7

start_x: int = 200    # odluglosc lewego silnika od lewego-gornego rogu obrazu w poziomie (wspolrzedne x) [milimetry]
start_y: int = 300    # odluglosc lewego silnika od lewego-gornego rogu obrazu w pionie (wspolrzedne y) [milimetry]
motor_spacing = 1000   # odleglosc miedzy silnikami
najmniejszy_obrot_kat = 0.1125 #najmniejsza wartość kąta o jaką może się obrócić silnik krokowy
obrot = {"lewy_silnik_prawo":11, "lewy_silnik_lewo":12, "prawy_silnik_lewo":21, "prawy_silnik_prawo":22, "gora":3, "dol":4}

rozmiar_piksela = 2    # krawedz piksela [milimetry]
