import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import random
import os

def encrypt_image(image_path, key):
    img = Image.open(image_path)
    pixels = list(img.getdata())
    width, height = img.size

    random.seed(key)
    pixel_indices = list(range(len(pixels)))
    random.shuffle(pixel_indices)

    new_pixels = [0] * len(pixels)
    for i, pi in enumerate(pixel_indices):
        new_pixels[pi] = pixels[i]

    encrypted_img = Image.new(img.mode, img.size)
    encrypted_img.putdata(new_pixels)
    return encrypted_img

def decrypt_image(image_path, key):
    img = Image.open(image_path)
    pixels = list(img.getdata())
    width, height = img.size

    random.seed(key)
    pixel_indices = list(range(len(pixels)))
    random.shuffle(pixel_indices)

    new_pixels = [0] * len(pixels)
    for i, pi in enumerate(pixel_indices):
        new_pixels[pi] = pixels[i]

    decrypted_img = Image.new(img.mode, img.size)
    decrypted_img.putdata(new_pixels)
    return decrypted_img

class ImageEncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Encryption Tool")
        self.create_widgets()

    def create_widgets(self):
        tk.Button(self.root, text="Load Image", command=self.load_image).pack(pady=10)
        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack(pady=10)
        
        tk.Label(self.root, text="Enter encryption key:").pack(pady=5)
        self.key_entry = tk.Entry(self.root, show="*", width=20)
        self.key_entry.pack(pady=5)
        
        tk.Button(self.root, text="Encrypt Image", command=self.encrypt_image).pack(pady=10)
        tk.Button(self.root, text="Decrypt Image", command=self.decrypt_image).pack(pady=10)
        
        self.image_path = None
        self.original_image = None
        self.processed_image = None

    def load_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if self.image_path:
            self.original_image = Image.open(self.image_path)
            self.display_image(self.original_image)

    def display_image(self, img):
        img.thumbnail((400, 400))
        self.img_tk = ImageTk.PhotoImage(img)
        self.canvas.create_image(200, 200, image=self.img_tk)

    def encrypt_image(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please load an image first.")
            return
        key = self.key_entry.get()
        if not key.isdigit():
            messagebox.showerror("Error", "Please enter a valid key.")
            return
        key = int(key)
        self.processed_image = encrypt_image(self.image_path, key)
        self.display_image(self.processed_image)
        self.save_image(self.processed_image, "encrypted")

    def decrypt_image(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please load an image first.")
            return
        key = self.key_entry.get()
        if not key.isdigit():
            messagebox.showerror("Error", "Please enter a valid key.")
            return
        key = int(key)
        self.processed_image = decrypt_image(self.image_path, key)
        self.display_image(self.processed_image)
        self.save_image(self.processed_image, "decrypted")

    def save_image(self, img, suffix):
        directory, filename = os.path.split(self.image_path)
        name, ext = os.path.splitext(filename)
        new_filename = f"{name}_{suffix}{ext}"
        new_filepath = os.path.join(directory, new_filename)
        img.save(new_filepath)
        messagebox.showinfo("Image Saved", f"Image saved as {new_filepath}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEncryptionApp(root)
    root.mainloop()
