import glob
import os
import random
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from PIL import Image
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split

# Limit GPU memory usage
# https://github.com/keras-team/keras/issues/1538#issuecomment-241975687
"""
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session
config = tf.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.7
set_session(tf.Session(config=config))
"""

def onehot_labels(values):
    label_encoder = LabelEncoder()
    integer_encoded = label_encoder.fit_transform(values)
    onehot_encoder = OneHotEncoder(sparse=False)
    integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
    onehot_encoded = onehot_encoder.fit_transform(integer_encoded)
    return onehot_encoded

imgs = glob.glob("./img/*.png")

width = 200
height = 40

X = []
Y = []
for img in imgs:
    filename = os.path.basename(img)
    label = filename.split("_")[0]
    im = np.array(Image.open(img).convert("L").resize((width, height)))
    im = im / 255
    X.append(im)
    Y.append(label)

X = np.array(X)
X = X.reshape(X.shape[0], width, height, 1)
Y = onehot_labels(Y)

train_X, test_X, train_y, test_y = train_test_split(X, Y, test_size=0.25, random_state=random.randint(112, 1112))

model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=(width, height, 1)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.4))
model.add(Dense(3, activation='softmax'))

if os.path.exists("./trex_weight.h5"):
    model.load_weights('trex_weight.h5')
    print("Load weight file")

print(model.summary())

model.compile(loss='categorical_crossentropy', optimizer='SGD', metrics=['accuracy'])

model.fit(train_X, train_y, epochs=20, batch_size=64)

scores = model.evaluate(train_X, train_y)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

scores = model.evaluate(test_X, test_y)
print("\nTEST %s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

#print(model.evaluate(X, Y))
open("model.json", "w").write(model.to_json())
model.save_weights('trex_weight.h5')
