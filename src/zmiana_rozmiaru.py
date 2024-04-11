from PIL import Image
import numpy as np


class ImageProcessor:
    def __init__(self) -> None:
        self.image = None
    def read_image(self, image_path: str) -> None:
        self.image = np.array(Image.open(image_path))
    def zmiana_rozmiaru(self):
        from config import pikseli_pionowo
        zadana_wysokosc=pikseli_pionowo
        wysokosc,szerokosc, _=self.image.shape
        proporcja=szerokosc/wysokosc
        nowa_szerokosc=int(zadana_wysokosc*proporcja)
        zmieniony_obraz = Image.fromarray(self.image).resize((nowa_szerokosc, zadana_wysokosc))
        return zmieniony_obraz
    def process_and_show_image(self, image_path: str) -> None:
        self.read_image(image_path)
        self.processed_image = self.zmiana_rozmiaru()
        self.processed_image.show()

if __name__ == "__main__":
    image_processor = ImageProcessor()
    input_image_path = "przyklad.png"
    image_processor.process_and_show_image(input_image_path)
print("obraz jest zapisany do zmiennej image_processor.processed_image")
