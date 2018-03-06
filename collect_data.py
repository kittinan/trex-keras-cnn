import keyboard
import pyscreenshot as ImageGrab
import os
import uuid

i = 0

def record_screen(key):
    global i
    i += 1
    print("{}: {}".format(key, i))
    im = ImageGrab.grab(bbox=(350,350,1000,480))
    im.save("./img/{}_{}_{}.png".format(key, i, uuid.uuid4()))


keyboard.add_hotkey(keyboard.KEY_UP, record_screen, args=["up"])
keyboard.add_hotkey(keyboard.KEY_DOWN, record_screen, args=["down"])
keyboard.add_hotkey("right", record_screen, args=["right"])

keyboard.wait('esc')
