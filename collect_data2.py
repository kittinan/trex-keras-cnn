import keyboard
import os
import uuid
from mss import mss
from PIL import Image
import time

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

while True:

    if keyboard.is_pressed(keyboard.KEY_UP):
        record_screen("up")
        time.sleep(0.5)
    elif keyboard.is_pressed(keyboard.KEY_DOWN):
        record_screen("down")
        time.sleep(0.5)
    else:
        record_screen("right")
        time.sleep(0.4)
