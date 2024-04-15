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
    print(img_processor.podziel_na_luki())
    # img_processor.image.show()


if __name__ == "__main__":
    main()

