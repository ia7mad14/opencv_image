import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageProcessingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Processing App")
        self.image = None
        self.create_widgets()

    def open_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = cv2.imread(file_path)
            self.update_image_label(self.image)

    def apply_filter(self, kernel):
        # Apply a filter to the image
        filtered_image = cv2.filter2D(self.image, -1, kernel=kernel)
        
        # Update the image label with the filtered image
        self.update_image_label(filtered_image)

    def grayscale(self):
        # Convert the image to grayscale
        gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        
        # Update the image label with the grayscale image
        self.update_image_label(gray_image)

    def increase_height(self):
        # Increase the height of the image by 10%
        height, width, _ = self.image.shape
        new_height = int(height * 1.1)
        self.image = cv2.resize(self.image, (width, new_height), interpolation=cv2.INTER_LINEAR)
        
        # Update the image label with the resized image
        self.update_image_label(self.image)

    def decrease_height(self):
        # Decrease the height of the image by 10%
        height, width, _ = self.image.shape
        new_height = int(height * 0.9)
        self.image = cv2.resize(self.image, (width, new_height), interpolation=cv2.INTER_LINEAR)
        
        # Update the image label with the resized image
        self.update_image_label(self.image)

    def increase_width(self):
        # Increase the width of the image by 10%
        height, width, _ = self.image.shape
        new_width = int(width * 1.1)
        self.image = cv2.resize(self.image, (new_width, height), interpolation=cv2.INTER_LINEAR)
        
        # Update the image label with the resized image
        self.update_image_label(self.image)

    def decrease_width(self):
        # Decrease the width of the image by 10%
        height, width, _ = self.image.shape
        new_width = int(width * 0.9)
        self.image = cv2.resize(self.image, (new_width, height), interpolation=cv2.INTER_LINEAR)
        
        # Update the image label with the resized image
        self.update_image_label(self.image)

    def save_image(self):
        # Save the image to a file
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg")
        if file_path:
            cv2.imwrite(file_path, self.image)

    def update_image_label(self, image):
        # Convert the image to RGB format
        if len(image.shape) == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        else:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Resize the image to fit the label
        height, width, _ = image.shape
        max_height = 500
        max_width = 500
        if height > max_height or width > max_width:
            scale_factor = min(max_height / height, max_width / width)
            image = cv2.resize(image, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_AREA)

        # Convert the image to PIL format and update the label
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
        image = Image.fromarray(image)
        photo_image = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo_image)
        self.image_label.image = photo_image

    def create_widgets(self):
        # Create a frame for the image display
        self.image_frame = tk.Frame(self.master)
        self.image_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Create a label for the image display
        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack()

        # Create a frame for the editing options
        self.edit_frame = tk.Frame(self.master)
        self.edit_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.Y)

        # Create buttons for opening an image and applying a filter
        self.open_button = tk.Button(self.edit_frame, text="Open Image", command=self.open_image)
        self.open_button.pack(pady=10)

        self.gray_button = tk.Button(self.edit_frame, text="Grayscale", command=self.grayscale)
        self.gray_button.pack(pady=10)

        self.filter_button =tk.Button(self.edit_frame, text="Apply Filter", command=self.show_filter_options)
        self.filter_button.pack(pady=10)

        # Create buttons for resizing the image
        self.resize_label = tk.Label(self.edit_frame, text="Resize Image")
        self.resize_label.pack(pady=10)

        self.increase_height_button = tk.Button(self.edit_frame, text="Increase Height", command=self.increase_height)
        self.increase_height_button.pack()

        self.decrease_height_button = tk.Button(self.edit_frame, text="Decrease Height", command=self.decrease_height)
        self.decrease_height_button.pack()

        self.increase_width_button = tk.Button(self.edit_frame, text="Increase Width", command=self.increase_width)
        self.increase_width_button.pack()

        self.decrease_width_button = tk.Button(self.edit_frame, text="Decrease Width", command=self.decrease_width)
        self.decrease_width_button.pack()

        # Create a button for saving the image
        self.save_button = tk.Button(self.edit_frame, text="Save Image", command=self.save_image)
        self.save_button.pack(pady=10)

    def show_filter_options(self):
        # Create a new window for the filter options
        self.filter_window = tk.Toplevel(self.master)
        self.filter_window.title("Filter Options")

        # Create a label and dropdown for selecting a filter type
        self.filter_type_label = tk.Label(self.filter_window, text="Select filter type:")
        self.filter_type_label.pack()

        self.filter_type_var = tk.StringVar()
        self.filter_type_dropdown = tk.OptionMenu(self.filter_window, self.filter_type_var, "Blur", "Sharpen", "Edge Detection")
        self.filter_type_dropdown.pack()

        # Create a label and slider for selecting the kernel size
        self.kernel_size_label = tk.Label(self.filter_window, text="Select kernel size:")
        self.kernel_size_label.pack()

        self.kernel_size_var = tk.DoubleVar()
        self.kernel_size_slider = tk.Scale(self.filter_window, from_=1, to=10, resolution=0.1, orient=tk.HORIZONTAL, variable=self.kernel_size_var)
        self.kernel_size_slider.pack()

        # Create a button for applying the filter
        self.apply_filter_button = tk.Button(self.filter_window, text="Apply Filter", command=self.apply_selected_filter)
        self.apply_filter_button.pack(pady=10)

    def apply_selected_filter(self):
        # Get the selected filter type and kernel size
        filter_type = self.filter_type_var.get()
        kernel_size = int(self.kernel_size_var.get() * 10)

        # Apply the selected filter
        if filter_type == "Blur":
            kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size * kernel_size)
            self.apply_filter(kernel)
        elif filter_type == "Sharpen":
            kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
            self.apply_filter(kernel)
        elif filter_type == "Edge Detection":
            kernel = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
            self.apply_filter(kernel)

        # Close the filter options window
        self.filter_window.destroy()

# Create the main window
root = tk.Tk()
app = ImageProcessingApp(root)
root.mainloop()