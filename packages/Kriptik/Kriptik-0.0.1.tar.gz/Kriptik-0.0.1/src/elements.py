from tkinter import *
from PIL import ImageTk, Image

class Rect:
    def __init__(self, parent, size: tuple=(10, 10), pos: tuple=(0, 0), color: str="black"):
        self.parent = parent.canvas
        self.size = size
        self.rect = self.parent.create_rectangle(pos[0] + size[0], pos[1] + size[1], pos[0], pos[1], fill=color)

    def move_right(self, speed: float):
        self.parent.move(self.rect, speed, 0)

    def move_left(self, speed: float):
        self.parent.move(self.rect, -speed, 0)

    def move_up(self, speed: float):
        self.parent.move(self.rect, 0, -speed)

    def move_down(self, speed: float):
        self.parent.move(self.rect, 0, speed)

class Oval:
    def __init__(self, parent, size: tuple=(10, 10), pos: tuple=(0, 0), color: str="black"):
        self.parent = parent.canvas
        self.size = size
        self.oval = self.parent.create_oval(pos[0] + size[0], pos[1] + size[1], pos[0], pos[1], fill=color)

    def move_right(self, speed: float):
        self.parent.move(self.oval, speed, 0)

    def move_left(self, speed: float):
        self.parent.move(self.oval, -speed, 0)

    def move_up(self, speed: float):
        self.parent.move(self.oval, 0, -speed)

    def move_down(self, speed: float):
        self.parent.move(self.oval, 0, speed)

class ImageRect(Rect):
    def __init__(self, parent, image_path: str, pos: tuple=(0, 0), size: tuple=(128, 128)):
        self.image = Image.open(image_path).resize(size)
        self.photo_image = ImageTk.PhotoImage(self.image)
        self.parent = parent.canvas
        self.parent_root = parent
        self.parent_root.root.one = self.photo_image
        self.rect = self.parent.create_image(pos, image=self.photo_image, anchor="nw")
    
    def rotate(self, angle: float, new_pos: tuple):
        self.image = self.image.rotate(angle)
        self.photo_image = ImageTk.PhotoImage(self.image)
        self.parent_root.root.one = self.photo_image
        self.rect = self.parent.create_image(new_pos, image=self.photo_image, anchor="nw")

class TextLabel:
    def __init__(self, parent, pos: tuple=(0, 0), **kwargs):
        self.parent = parent.canvas
        self.text = Label(self.parent, **kwargs)
        self.text.place(x=pos[0], y=pos[1])
    
    def change_text(self, text: str):
        self.text.config(text=text)

class InputText:
    def __init__(self, parent, pos: tuple=(0, 0), **kwargs):
        self.parent = parent.canvas
        self.input = Text(self.parent, **kwargs)
        self.input.place(x=pos[0], y=pos[1])

    def get(self):
        return self.input.get(1.0, "end-1c")
    
    def insert(self, text: str):
        self.input.insert(1.0, text)
    
    def clear(self):
        self.input.delete(1.0, "end")