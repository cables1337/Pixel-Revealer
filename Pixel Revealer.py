import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np

class PixelRevealerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pixel Revealer")
        
        # Load the initial image
        self.img_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if not self.img_path:
            messagebox.showerror("Erreur", "Aucune image sélectionnée.")
            self.root.destroy()
            return

        self.image = Image.open(self.img_path)
        self.img_array = np.array(self.image)
        
        # Create a blank image with the same dimensions
        self.blank_img_array = np.zeros_like(self.img_array)
        self.revealed_img_array = np.copy(self.blank_img_array)
        
        # Create a canvas to display the image
        self.canvas = tk.Canvas(root, width=self.image.width, height=self.image.height)
        self.canvas.pack()
        
        self.update_image(self.blank_img_array)
        
        # Input for number of pixels
        self.pixel_input = tk.Entry(root)
        self.pixel_input.pack()
        
        # Button to reveal pixels
        self.reveal_button = tk.Button(root, text="Révéler")
        self.reveal_button.pack()
        self.reveal_button.bind("<Button-1>", self.reveal_pixels)

        # Label to show the percentage of revealed pixels
        self.percentage_label = tk.Label(root, text="Pourcentage de pixels révélés : 0.00%")
        self.percentage_label.pack()

    def update_image(self, img_array):
        # Update the canvas with the new image
        self.tk_img = ImageTk.PhotoImage(image=Image.fromarray(img_array))
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_img)
        
    def reveal_pixels(self, event):
        try:
            # Get the number of pixels to reveal
            num_pixels = int(self.pixel_input.get())
            if num_pixels <= 0:
                raise ValueError("Le nombre de pixels doit être supérieur à zéro.")
            
            # Generate random indices to reveal pixels
            total_pixels = self.image.size[0] * self.image.size[1]
            if num_pixels > total_pixels:
                raise ValueError(f"Le nombre de pixels ne peut pas dépasser {total_pixels}.")
                
            indices = np.random.choice(total_pixels, num_pixels, replace=False)
            
            # Update the revealed image array with the selected pixels
            flat_img = self.img_array.reshape(-1, self.img_array.shape[2])
            flat_revealed_img = self.revealed_img_array.reshape(-1, self.revealed_img_array.shape[2])
            
            for index in indices:
                flat_revealed_img[index] = flat_img[index]
                
            self.revealed_img_array = flat_revealed_img.reshape(self.img_array.shape)
            
            # Update the displayed image
            self.update_image(self.revealed_img_array)
            
            # Save the current number of revealed pixels
            self.current_pixels_revealed = np.count_nonzero(np.any(self.revealed_img_array, axis=2))
            
            # Update the percentage of revealed pixels
            percentage_revealed = (self.current_pixels_revealed / total_pixels) * 100
            self.percentage_label.config(text=f"Pourcentage de pixels révélés : {percentage_revealed:.2f}%")
        
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = PixelRevealerApp(root)
    root.mainloop()
