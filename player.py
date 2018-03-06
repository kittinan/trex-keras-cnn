from keras.models import model_from_json
import os
import glob
import numpy as np
from PIL import Image
import pyscreenshot as ImageGrab
import keyboard

# Force to use only CPU
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
os.environ["CUDA_VISIBLE_DEVICES"] = ""

# Load Model
model = model_from_json(open("model.json", "r").read())
model.load_weights("trex_weight.h5")
print(model.summary())

# Down = 0, Right = 1, UP = 2
labels = ["Down", "Right", "Up"]

i = 0
while True:
    im = ImageGrab.grab(bbox=(350,350,1000,480))
    #im = ImageGrab.grab(bbox=(630,350,1280,480), childprocess=False)
    im = np.array(im.convert("L").resize((260, 52)))
    im = im / 255

    X = np.array([im])
    X = X.reshape(X.shape[0], 260, 52, 1)
    r = model.predict(X)
    result = np.argmax(r)

    if result == 0:
        keyboard.press_and_release("down")
    elif result == 2:
        keyboard.press_and_release("up")

    print("[{}] Predict: {}".format(i, labels[result]))
    i += 1
