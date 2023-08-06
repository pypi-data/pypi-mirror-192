from tkinter import *
from PIL import ImageTk, Image

import uinput
import elements
from sound import Sound
from threads import Thread
from collision import Collision

def sub_uint(x, y):
    result = x - y
    if result < 0:
        return -result
    return result

class Window:
    def __init__(self, size: tuple=(500, 500), color: str="black", fps: int=0):
        self.root = Tk()
        self.title = "Kriptik"
        self.fullscreen = False
        self.mouse_pos = ()
        self.init()

        self.fps = fps
        self.size = size
        self.color = color
        self.canvas = Canvas(self.root, width=size[0], height=size[1], bg=color)
        self.canvas.pack()

    def init(self):
        self.root.title(self.title)
        self.root.attributes("-fullscreen", self.fullscreen)
        self.root.bind("<Motion>", self.mp)

    def set_icon_bitmap(self, image_path: str):
        self.root.wm_iconbitmap(image_path)

    def update(self):
        self.canvas.update()

    def start(self):
        self.root.mainloop()

    def element_pos(self, element):
        return tuple(self.canvas.coords(element))

    def delete_element(self, element):
        self.canvas.delete(element)
    
    def mp(self, event):
        self.mouse_pos = (event.x, event.y)

    def thread(self, func):
        return Thread(func, self.fps)
        
    def collide(self, element1, element2):
        return Collision(self.canvas, element1, element2).collide()