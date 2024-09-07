import config


def move(end_x, end_y):
    steps = []
    # tu generujemy liste krokow potrzebnych do wykonania ruchu
    # tu zapisujemy kroki do pliku


def save_steps_to_file(steps) -> None:
    with open(config.steps_file_path, "a") as file:
        file.writelines(steps)

