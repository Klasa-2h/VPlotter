from image_processor import ImageProcessor
from generator_krokow_silnikow import GeneratorKrokowSilnikow
from config import *


def main() -> None:
    img_processor = ImageProcessor()
    img_processor.read_image(image_path)
    img_processor.zmiana_rozmiaru()
    img_processor.mono_image()
    img_processor.process_intensity_scale_and_reverse()
    luki = img_processor.podziel_na_luki()
    generator_krokow = GeneratorKrokowSilnikow(luki)
    generator_krokow.generuj()
    generator_krokow.zapisz_do_pliku()


if __name__ == "__main__":
    main()
