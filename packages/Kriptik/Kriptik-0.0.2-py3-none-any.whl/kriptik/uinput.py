import keyboard
import win32api

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