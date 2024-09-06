from image_handler import ImageHandler
from steps_generator import StepsGenerator


def main() -> None:
    img_handler = ImageHandler()
    img_handler.read_image()
    img_handler.process_image()
    img_handler.initialize_image_objects()



if __name__=="__main__":
    main()
