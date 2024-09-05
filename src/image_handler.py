
class ImageHandler:
    def __int__(self):
        self.image = []

    def read_image(self):
        #wczytujemy z pliku
        pass

    def process_image(self):
        # czarnobialy obraz + redukcja skali szarosci
        pass

    def initialize_image_objects(self):
        # zapisujemy liste Line'ow pod zmienna self.image
        pass

    def generate_steps(self):
        for i in range(len(self.image)):
            self.image[i].generate_steps()
            if i != len(self.image) - 1:
                # przejdz do nastepnej lini
                pass


class Line:
    def __int__(self, pixcels: list[int]):
        self.pixcels = pixcels

    def generate_steps(self):
        for pixcel in self.pixcels:
            # rysujemy piksel i idziemy dalej
            pass


