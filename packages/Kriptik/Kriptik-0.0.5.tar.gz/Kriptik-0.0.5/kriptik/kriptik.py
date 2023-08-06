import time
import keyboard
import win32api
import threading
import contextlib
from tkinter import *
from PIL import ImageTk, Image

with contextlib.redirect_stdout(None):
    import pygame

def sub_uint(x, y):
    result = x - y
    if result < 0:
        return -result
    return result

class Collision:
    def __init__(self, canvas, element1, element2):
        self.canvas = canvas
        self.e1 = self.canvas.bbox(element1)
        self.e2 = self.canvas.bbox(element2)
        self.a_y_len = sub_uint(self.e1[1], self.e1[3])
        self.b_x_len = sub_uint(self.e2[0], self.e2[2])
    
    def collision_loop(self, side_1, side_2):
        for x in range(self.e2[0], self.e2[0] + self.b_x_len):
            for i in range(self.e1[1], self.e1[1] + self.a_y_len):
                if self.e2[side_2] == i and self.e1[side_1] == x:
                    return True

    def collide(self):
        if self.collision_loop(2, 1): # right to top
            return True
        elif self.collision_loop(2, 3): # right to bottom
            return True
        if self.collision_loop(0, 1): # left to top
            return True
        elif self.collision_loop(0, 3): # left to bottom
            return True
        else:
            return False

class Thread:
    def __init__(self, func, fps: int=0):
        self.func = func
        self.fps = fps
        self.thread_on = False
    
    def thread(self):
        if self.fps == 0:
            while True:
                self.func()
        elif self.fps > 0:
            while True:
                self.func()
                time.sleep(1/self.fps)
        else:
            raise ValueError("\"fps\" argument must be above 0")
    
    def start(self):
        self.thread_on = True
        threading.Thread(target=self.thread).start()
    
    def stop(self):
        self.thread_on = False

class Sound:
    def __init__(self, file: str, play_count: int=1, volume: float=1):
        pygame.init()
        pygame.mixer.set_num_channels(499)

        self.file = file
        self.volume = volume
        self.play_count = play_count
    
    def play(self):
        self.channel = pygame.mixer.find_channel()
        self.channel.set_volume(self.volume)
        self.channel.play(pygame.mixer.Sound(self.file), self.play_count)
    
    def stop(self):
        self.channel.pause()

class elements:
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

class uinput:
    def key_pressed(val: str):
        if keyboard.is_pressed(val):
            return True
        else:
            return False
            
    def mouse_pressed(val: str):
        if val == "left_mouse":
            val = 0x01
        elif val == "right_mouse":
            val = 0x02
        elif val == "middle_mouse":
            val = 0x04
        elif val == "side_mouse1":
            val = 0x05
        elif val == "side_mouse2":
            val = 0x06
        else:
            raise ValueError("\"val\" argument must be one of the following: left_mouse, right_mouse, middle_mouse, side_mouse1, side_mouse2")
        
        key_state = win32api.GetKeyState(val)

        if key_state < 0:
            return True
        else:
            return False

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