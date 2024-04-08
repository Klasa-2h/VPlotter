from PIL import Image
import numpy as np


class ImageProcessor:
    def __init__(self) -> None:
        self.image = None

    def read_image(self, image_path: str) -> None:
        self.image = np.array(Image.open(image_path))


