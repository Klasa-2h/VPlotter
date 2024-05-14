from image_processor import ImageProcessor
from generator_krokow_silnikow import GeneratorKrokowSilnikow
from config import *
from simulation import Simulation


def main() -> None:
    img_processor = ImageProcessor()
    img_processor.read_image(image_path)
    img_processor.zmiana_rozmiaru()
    img_processor.mono_image()
    img_processor.process_intensity_scale_and_reverse()
    obraz = img_processor.get_image_with_pixcel_objects()
    generator_krokow = GeneratorKrokowSilnikow(obraz)
    generator_krokow.generuj()
    generator_krokow.zapisz_do_pliku()
    sym = Simulation()
    # sym.stworz_symulacje()


if __name__ == "__main__":
    main()
