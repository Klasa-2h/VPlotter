import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import time
import main
import config


def create_label(text, font, x_co, y_co):
    label = tk.Label(window, text=text, font=font)
    label.place(x=x_co, y=y_co)


def open_file_explorer(file_type):
    file_path = filedialog.askopenfilename()
    if file_path:
        if file_type == "image":
            file_path_entry.delete(0, tk.END)
            file_path_entry.insert(0, file_path)
        else:
            file_path_steps_entry.delete(0, tk.END)
            file_path_steps_entry.insert(0, file_path)


def save_to_config(entries_list,  steps_entry, file_entry):
    config_attributes = ["image_path","steps_file_path", "color_range", "final_image_width", "resolution_vertically", "resolution_horizontally", "starting_height_from_top", "distance_between_motors", "motor_diameter"]
    setattr(config, config_attributes[1], steps_entry.get())
    setattr(config, config_attributes[0], file_entry.get())
    for i in range(2, len(config_attributes),1):
        try:
            value = int(entries_list[i-2].get())
            setattr(config, config_attributes[i], value)
        except ValueError:
            messagebox.showerror("Error",f"Input correct number for {config_attributes[i]}")
            return
        
    with open('config.py', 'r') as f:
        lines = f.readlines()
    for i in range(len(lines)):
        for a in config_attributes:
            if lines[i].startswith(a):
                if a == "image_path" or a == "steps_file_path":  # Handle file paths as strings
                     lines[i] = "{} = '{}'\n".format(a, getattr(config, a))
                else:
                    lines[i] = "{} = {}\n".format(a, getattr(config, a))
    with open('config.py', 'w') as f:
        f.writelines(lines)
    steps_generator_button()  
        
        
def steps_generator_button():
    print("Button.")
    main.main()
    generated_image_path = "logo.png"
    show_loading(generated_image_path)


def show_loading(image_path):
    canvas.delete("all") 
    canvas.create_text(205, 200, text="Loading...", font=("Arial", 24), fill="black")
    window.update() 
    time.sleep(2)
    show_image(image_path)


def resize_image(image, max_width, max_height):
    width, height = image.size
    scale = min(max_width / width, max_height / height)
    new_width = int(width * scale)
    new_height = int(height * scale)
    return image.resize((new_width, new_height), Image.Resampling.LANCZOS)


def show_image(image_path):
    canvas.delete("all") 
    img = Image.open(image_path)
    resized_image = resize_image(img, 450, 450)
    tk_image = ImageTk.PhotoImage(resized_image)
    canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
    canvas.image = tk_image
    

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".png",filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
    if file_path:
        image = Image.open("example_image.png")
        image.save(file_path)
        print(f"Simulation saved as: {file_path}")


# WINDOW
window = tk.Tk()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.geometry(f"{screen_width}x{screen_height}+0+0")
#window.attributes('-fullscreen', True)
window.title("Vplotter GUI")


# LOGO
image = tk.PhotoImage(file="logo.png")
window.iconphoto(False, image)
label_photo = tk.Label(window, image=image)
label_photo.place(x=20, y =20)
label_title = create_label("Vplotter GUI", ("Arial", 30, "bold"), 115,35)


# SELECT FILE
label2 = create_label("Photo file location:", ("Arial", 20),30, 120)
label3 = create_label("Steps file location:", ("Arial", 20), 30, 230)

open_file_button = tk.Button(window, text="Select image file", command=lambda:open_file_explorer("image"),  font = ("Arial", 12), width=15, height=1, bg="#b3b1b1", activebackground="#8c8989").place(x=270,y=125)
open_file_steps_button = tk.Button(window, text="Select steps file", command=lambda:open_file_explorer("steps"),  font = ("Arial", 12), width=15, height=1, bg="#b3b1b1", activebackground="#8c8989").place(x=270,y=235)

file_path_entry = tk.Entry(window, width=55)
file_path_entry.place(x=30,y=170)
file_path_entry.insert(1, config.image_path)

file_path_steps_entry = tk.Entry(window, width=55)
file_path_steps_entry.place(x=30,y=280)
file_path_steps_entry.insert(1, config.steps_file_path)



# CONFIG
label4 = create_label("Config settings:", ("Arial", 20), 30, 350)
config_text_label = ["Color range:", "Final image width:", "Resolution vertically:", "Resolution horizontally:", "Height from the top:", "Distance between motors:", "Motor diameter:"]
config_values = [config.color_range, config.final_image_width, config.resolution_vertically, config.resolution_horizontally, config.starting_height_from_top, config.distance_between_motors, config.motor_diameter]
y_coordinate = 400
entries = []

for i in range(len(config_text_label)):
    create_label(config_text_label[i],("Arial",15), 30, y_coordinate)
    entry = tk.Entry(window,  width=10)
    entry.place(x=275, y=y_coordinate+5)
    entry.insert(-1, config_values[i])
    entries.append(entry)
    y_coordinate += 50


# STYLE
label12 = create_label("Style:",("Arial",15), 450, 50)
style_list = ["Lines", "Spirals", "Contours"]
clicked = tk.StringVar()
clicked.set(style_list[0])
options = tk.OptionMenu(window, clicked, *style_list)
options.config(fg = "#222",font = ("Arial", 15))
options.place(x=520, y=45, height = 40, width = 120)


# SIMULATION
canvas = tk.Canvas(window, width=450, height=450)
canvas.place(x=900, y=200)

# GENERATE STEPS AND SHOW SIMULATION BUTTON
btn_steps_generator = tk.Button(window, text="GENERATE STEPS FILE AND SHOW SIMULATION", command=lambda:save_to_config(entries, file_path_steps_entry, file_path_entry), font = ("Arial", 15), width=45, height=4, bg="#b3b1b1", activebackground="#8c8989").place(x=750,y=35)

#SAVE SUTTON
btn_steps_generator = tk.Button(window, text="SAVE", command=save_file, font = ("Arial", 15), width=15, height=4, bg="#b3b1b1", activebackground="#8c8989").place(x=1280,y=35)

window.mainloop()