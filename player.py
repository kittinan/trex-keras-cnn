from keras.models import model_from_json
import os
import glob
import numpy as np
from PIL import Image
import keyboard
import time
from mss import mss

mon = {'top': 350, 'left': 625, 'width': 650, 'height': 130}
sct = mss()

"""
# Limit GPU memory usage
# https://github.com/keras-team/keras/issues/1538#issuecomment-241975687
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session
config = tf.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.15
set_session(tf.Session(config=config))
"""

# Force to use only CPU
#os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
#os.environ["CUDA_VISIBLE_DEVICES"] = ""

width = 250
heigh = 50

# Load Model
model = model_from_json(open("model.json", "r").read())
model.load_weights("trex_weight.h5")
print(model.summary())

# Down = 0, Right = 1, UP = 2
labels = ["Down", "Right", "Up"]

os.system('clear')

time_start = time.clock()
i = 0
while True:
    img = sct.grab(mon)
    im = Image.frombytes('RGB', img.size, img.rgb)
    im = np.array(im.convert("L").resize((width, heigh)))
    im = im / 255

    X = np.array([im])
    X = X.reshape(X.shape[0], width, heigh, 1)
    r = model.predict(X)
    result = np.argmax(r)

    if r[0][0] > 0.5:
        keyboard.press_and_release(keyboard.KEY_DOWN)
    elif r[0][2] > 0.5:
        keyboard.press_and_release(keyboard.KEY_UP)

    #print("[{}] Predict: {}".format(i, labels[result]))
    print("", end="\r")
    print("Down: {:7.2%} | Right: {:7.2%} | Up: {:7.2%}".format(r[0][0], r[0][1], r[0][2]), end="\r")
    i += 1
    time.sleep(0.15)
