import tkinter as tk
from PIL import Image, ImageTk
import time
from simulation import Simulation
import tempfile

# Create the application window with a larger size
root = tk.Tk()
root.title("Vplotter GUI")
root.geometry("800x800")  # Set a larger window size

# Create an area to display the image with larger dimensions
canvas = tk.Canvas(root, width=750, height=750)
canvas.pack()

# Placeholder for the actual "generate" function, which generates the image
def generate(file_path):
    # The owner of the simulation should add their own code here to generate the simulation image
    # This is just an example generating a 500x500 white image
    simulation = Simulation()
    simulated_image = simulation.img()
    simulated_image.save(file_path)

# Function to simulate generating and saving the image to a temporary file
def generate_simulation_image():
    # Create a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    
    # Call the generate function, which will save the image to the temporary file
    generate(temp_file.name)
    
    # Return the path to the temporary file
    return temp_file.name

# Function to display "Loading..." text and load the image
def show_loading():
    # Remove previous elements from the canvas
    canvas.delete("all")
    
    # Display "Loading..." text
    canvas.create_text(375, 375, text="Loading...", font=("Arial", 24), fill="black")
    root.update()  # Update the GUI to immediately show the text

    # Simulate loading time (this simulates the time taken by the image generation process)
    time.sleep(2)  # Simulate delay

    # After the image has loaded
    show_image()

# Function to resize the image to fit the window size
def resize_image(image, max_width, max_height):
    # Get the current dimensions of the original image
    width, height = image.size

    # Calculate the scale to ensure the image fits within the window
    scale = min(max_width / width, max_height / height)
    new_width = int(width * scale)
    new_height = int(height * scale)

    # Return the resized image
    return image.resize((new_width, new_height), Image.Resampling.LANCZOS)

# Function to display the loaded image from the temporary file
def show_image():
    # Remove the "Loading..." text
    canvas.delete("all")

    # Get the path to the generated simulation image (from the temporary file)
    temp_image_path = generate_simulation_image()

    # Load the image from the temporary file
    image = Image.open(temp_image_path)

    # Resize the image to fit the canvas size
    resized_image = resize_image(image, 750, 750)

    # Convert the image to a format accepted by Tkinter
    tk_image = ImageTk.PhotoImage(resized_image)

    # Display the image on the canvas
    canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
    canvas.image = tk_image  # Ensure the image is not removed from memory

# Button to generate simulation and load the image
btn_simulation = tk.Button(root, text="Generate Steps and show simulation", command=show_loading)
btn_simulation.pack()

# Start the Tkinter event loop
root.mainloop()