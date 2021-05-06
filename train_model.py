import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.utils import to_categorical
from keras.preprocessing import image
import numpy as np
import os
from keras.optimizers import SGD
from keras.layers import LeakyReLU
from keras.models import load_model

from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
from tqdm import tqdm
from keras.models import Sequential
import cv2


# Load Images from Swing
loadedImages = []
for j in range(6):
    for i in range(0, 101):
        # try:
        image = cv2.imread('C:/Users/DELL/PycharmProjects/btech_p/Dataset/'+str(j)+'/' + str(i) + '.png',cv2.IMREAD_UNCHANGED)
        # gray_image = cv2.cvtColor(image, cv2.IMREAD_UNCHANGED)
        loadedImages.append(image)
        # except:
        #     print("notload",i,j)
X = np.array(loadedImages)
print(X.shape)
X = X.reshape(X.shape[0],X.shape[1],X.shape[2],1)
X = X.astype('float32')
X /= 255
print(X.shape)
# Create OutputVector
outputVectors = []
for j in range(6):
    arr=[0,0,0,0,0,0]
    arr[j]=1
    for i in range(0, 101):
        outputVectors.append(arr)
y=np.array(outputVectors)
print(y.shape)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0, test_size=0.10)

model = Sequential()

# first conv layer
model.add(Conv2D(32, kernel_size=(3, 3),activation='relu',input_shape=(200,200,1)))
# second conv layer
model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
# model.add(Dropout(0.25))
# second conv layer
model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
# flatten and put a fully connected layer
model.add(Flatten())
model.add(Dense(128, activation='relu')) # fully connected
model.add(Dropout(0.25))
# softmax layer
model.add(Dense(6, activation='softmax'))

# model summary
model.summary()


#model.compile(loss='sparse_categorical_crossentropy',optimizer='Adam',metrics=['accuracy'])
model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adadelta(),
              metrics=['accuracy'])

model.fit(X_train, y_train,batch_size = 32,epochs = 6,
         verbose = 1,validation_data=(X_test, y_test))
model.save('my_model6.h5')  # creates a HDF5 file 'my_model.h5'
