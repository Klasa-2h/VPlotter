from PIL import Image
import numpy as np
from config import pikseli_pionowo
from config import maksymalne_natezenie_barw


class ImageProcessor:
    def __init__(self) -> None:
        self.image = None
        
    def read_image(self, image_path: str) -> None:
        self.image = Image.open(image_path)

    def zmiana_rozmiaru(self):
        zadana_wysokosc=pikseli_pionowo
        wysokosc,szerokosc, _ = np.array(self.image).shape
        proporcja=szerokosc/wysokosc
        nowa_szerokosc=int(zadana_wysokosc*proporcja)
        self.image = Image.fromarray(np.array(self.image)).resize((nowa_szerokosc, zadana_wysokosc), 4)
    
    def mono_image(self) -> None:
        self.image = self.image.convert('1')
    
    def process_intensity_scale(self):
        gorny_limit = maksymalne_natezenie_barw
        szerokosc, wysokosc = self.image.size
        piksele = self.image.load()
        for y in range(wysokosc):
            for x in range(szerokosc):
                jasnosc = piksele[x, y]
                nowa_jasnosc = int(jasnosc * gorny_limit // 255)
                piksele[x, y] = nowa_jasnosc
        self.image = self.image


