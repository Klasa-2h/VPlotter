from PIL import Image
import numpy as np
from config import pikseli_pionowo


class ImageProcessor:
    def __init__(self) -> None:
        self.image = None
        
    def read_image(self, image_path: str) -> None:
        self.image = np.array(Image.open(image_path))

    def zmiana_rozmiaru(self):
        zadana_wysokosc=pikseli_pionowo
        wysokosc,szerokosc = self.image.shape
        proporcja=szerokosc/wysokosc
        nowa_szerokosc=int(zadana_wysokosc*proporcja)
        self.image = Image.fromarray(self.image).resize((nowa_szerokosc, zadana_wysokosc))
    
    def mono_image(self) -> None:
        self.image = self.image.convert('1')

