import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk, ImageSequence

class ImageViewer:
    def __init__(self, image_path, width, height, gif_speed=50):
        self.root = ctk.CTk()
        self.root.geometry(f"{width}x{height}")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True) 
        self.root.configure(bg="black")

        self.image_path = image_path
        self.is_gif = image_path.lower().endswith(".gif")
        self.label = tk.Label(self.root, bg="black")
        self.label.pack(expand=True, fill="both")

        self.gif_speed = gif_speed
        self.frames = []
        self.index = 0
        self.last_size = (width, height)

        self.load_media()

        # Eventos
        self.root.bind("<Escape>", lambda e: self.root.destroy())
        self.root.bind("<B1-Motion>", self.move_window)
        self.root.bind("<Configure>", self.check_resize)

        self.root.mainloop()

    def load_media(self):
        """Carrega imagem ou GIF"""
        if self.is_gif:
            self.gif = Image.open(self.image_path)
            self.original_frames = [frame.copy() for frame in ImageSequence.Iterator(self.gif)]
            self.resize_gif()
        else:
            self.original_image = Image.open(self.image_path)
            self.resize_image()

    def check_resize(self, event=None):
        """Verifica se o tamanho da janela mudou antes de redimensionar"""
        width, height = self.root.winfo_width(), self.root.winfo_height()
        if (width, height) != self.last_size:
            self.last_size = (width, height)
            self.resize_media()

    def resize_media(self):
        """Redimensiona a imagem ou GIF"""
        if not self.is_gif:
            self.resize_image()
        else:
            self.resize_gif()

    def resize_image(self):
        """Redimensiona uma imagem estática"""
        width, height = self.last_size
        img = self.original_image.resize((width, height), Image.LANCZOS)
        self.img_tk = ImageTk.PhotoImage(img)
        self.label.config(image=self.img_tk)

    def resize_gif(self):
        """Redimensiona cada frame do GIF"""
        width, height = self.last_size
        self.frames = [ImageTk.PhotoImage(frame.resize((width, height), Image.LANCZOS)) for frame in self.original_frames]

        if self.index >= len(self.frames):
            self.index = 0

        self.animate_gif()

    def animate_gif(self):
        """Anima o GIF sem acelerar"""
        self.label.config(image=self.frames[self.index])
        self.index = (self.index + 1) % len(self.frames)
        self.root.after(self.gif_speed, self.animate_gif)

    def move_window(self, event):
        """Move a janela ao segurar e arrastar"""
        self.root.geometry(f"+{event.x_root}+{event.y_root}")

# Exemplo de uso:
# Caminho da imagem, tamanho inicial, posição inicial (x, y) e velocidade do GIF
ImageViewer("calma.png", 100, 100, gif_speed=10)
