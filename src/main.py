import os
from image_processor import ImageProcessor
from config import *


resources_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../res"))
image_path = os.path.join(resources_folder, image_file_name)


def main() -> None:
    img_processor = ImageProcessor()
    img_processor.read_image(image_path)
    img_processor.zmiana_rozmiaru()
    img_processor.mono_image()
    img_processor.process_intensity_scale()
    odleglosc_miedzy_lukami, luki = img_processor.podziel_na_luki()
    for luk in luki:
        print(luk.angle, luk.radius, luk.dlugosc_luku)


if __name__ == "__main__":
    main()

>>>>>>> main
