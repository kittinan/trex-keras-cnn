import keyboard
import os
import uuid
from mss import mss
from PIL import Image

mon = {'top': 350, 'left': 625, 'width': 650, 'height': 130}
sct = mss()

i = 0

def record_screen(key):
    global i
    i += 1
    print("{}: {}".format(key, i))
    img = sct.grab(mon)
    im = Image.frombytes('RGB', img.size, img.rgb)
    im.save("./img/{}_{}_{}.png".format(key, i, uuid.uuid4()))


keyboard.add_hotkey(keyboard.KEY_UP, record_screen, args=["up"])
keyboard.add_hotkey(keyboard.KEY_DOWN, record_screen, args=["down"])
keyboard.add_hotkey("right", record_screen, args=["right"])

keyboard.wait('esc')
