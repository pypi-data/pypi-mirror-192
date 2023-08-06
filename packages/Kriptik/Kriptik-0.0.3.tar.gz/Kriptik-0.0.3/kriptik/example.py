import kriptik as kr
import time

win = kr.Window(
    size=(640, 640),
    color="white",
    fps=60
)

win.set_icon_bitmap(r"assets\AcidicV2.ico")

rect1 = kr.elements.Rect(
    win,
    size=(50, 50),
    pos=(10, 10),
    color="#F94D4D",
)

oval = kr.elements.Oval(
    win,
    size=(50, 50),
    pos=(110, 10),
    color="pink"
)

label = kr.elements.TextLabel(
    win,
    pos=(210, 10),
    text="Kriptik",
    width=7,
    height=1
)

input_ = kr.elements.InputText(
    win,
    pos=(310, 10),
    height=1,
    width=10
)

img = kr.elements.ImageRect(
    win,
    r"assets\king.png",
    pos=(410, 10),
    size=(64, 64)
)

def mainloop():
    global angle, img
    start_time = time.perf_counter()

    if kr.uinput.key_pressed("a"):
        img.move_left(10)
        rect1.move_left(10)
    if kr.uinput.key_pressed("d"):
        rect1.move_right(10)
        img.move_right(10)
    if kr.uinput.key_pressed("w"):
        rect1.move_up(10)
        img.move_up(10)
    if kr.uinput.key_pressed("s"):
        rect1.move_down(10)
        img.move_down(10)
    if kr.uinput.key_pressed("space"):
        kr.Sound(r"assets\sound.wav", play_count=1, volume=0.5).play()
    
    if kr.uinput.mouse_pressed("left_mouse"):
        img.rotate(45, win.element_pos(img.rect))

    label.change_text(f"FPS: {int(1/(time.perf_counter() - start_time))}")
    win.update()

loop = win.thread(mainloop)
loop.start()

win.start()