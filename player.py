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

width = 200
height = 40

# Load Model
model = model_from_json(open("model.json", "r").read())
model.load_weights("trex_weight.h5")
print(model.summary())

# Down = 0, Right = 1, UP = 2
labels = ["Down", "Right", "Up"]


framerate_time = time.time()
counter = 0
i = 0
current_framerate = 0
delay = 0.04
count_time = 0
last_result = 1

while True:

    time_start = time.time()
    img = sct.grab(mon)
    im = Image.frombytes('RGB', img.size, img.rgb)
    im = np.array(im.convert("L").resize((width, height)))
    im = im / 255

    time_grab = time.time() - time_start
    time_start = time.time()

    X = np.array([im])
    X = X.reshape(X.shape[0], width, height, 1)
    r = model.predict(X)
    result = np.argmax(r)

    time_predict = time.time() - time_start

    if ((result == 0) and (last_result != 0)):
        # Hold down button
        keyboard.press(keyboard.KEY_DOWN)
    elif result == 2:
        if last_result == 0:
            # Release down button
            keyboard.release(keyboard.KEY_DOWN)
        keyboard.press_and_release(keyboard.KEY_UP)

    last_result = result

    counter+=1
    if (time.time() - framerate_time) > 1 :
        current_framerate = counter / (time.time() - framerate_time)
        counter = 0
        framerate_time = time.time()
        delay -= 0.0001
        if delay < 0:
            delay = 0

    os.system('clear')
    print("Down: {:3.2%} \nRight: {:3.2%} \nUp: {:3.2%} \n".format(r[0][0], r[0][1], r[0][2]), end="\r")
    print("=========================")
    print("Frame Count: {}\nCurrent Frame Rate: {:.2f}\nGrab Screen: {:.5f}\nPredict: {:.5f}".format(i, current_framerate, time_grab, time_predict))
    print("=========================")
    print("Delay: {:.5f}".format(delay))
    i += 1
    time.sleep(delay)
