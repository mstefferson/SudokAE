import numpy as np
from glob import glob
from keras.layers import Input, Dense
from keras.models import Model
from keras import regularizers
from keras.datasets import mnist
import numpy as np
from keras.layers import Input, Dense, Lambda, Conv2D
from keras.layers import MaxPooling2D, UpSampling2D
from keras.models import Model
from keras import backend as K
from keras.callbacks import TensorBoard


def read_data(dir2read):
    all_files = glob(dir2read + '*')
    data = []
    for f in all_files:
        data.append(np.loadtxt(f))
    data = np.array(data)
    data = data.reshape(data.shape[0], data.shape[1] * data.shape[2])
    return data


def model(hidden_layer=[128, 64, 32]):
    # set sudoku size
    ni = 81
    input_img = Input(shape=(ni,))

    # for now, write out all layers (turn to loop later)
    # encode
    encoded = Dense(hidden_layer[0], activation='relu')(input_img)
    encoded = Dense(hidden_layer[1], activation='relu')(encoded)
    # bottle neck
    encoded = Dense(hidden_layer[2], activation='relu')(encoded)
    # decode
    decoded = Dense(hidden_layer[1], activation='relu')(encoded)
    decoded = Dense(hidden_layer[0], activation='relu')(decoded)
    decoded = Dense(ni, activation='sigmoid')(decoded)
    # build models
    autoencoder = Model(input_img, decoded)
    # this model maps an input to its encoded representation
    encoder = Model(input_img, encoded)
    # create a placeholder for an encoded (32-dimensional) input
    encoded_input = Input(shape=(encoding_dim,))
    # retrieve the last layer of the autoencoder model
    # create the decoder model
    # build decoded tensors from autoencoder layers
    encoded_input = Input(shape=(encoding_dim,))
    _decode = autoencoder.layers[-3](encoded_input)
    _decode = autoencoder.layers[-2](_decode)
    _decode = autoencoder.layers[-1](_decode)
    decoder = Model(encoded_input, _decode)
    # return the models
    return autoencoder, encoder, decoder


def fit(autoencoder, encoder, decoder,
        x_train, y_train, x_test, y_test,
        ep=100, bs=64):
    autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')
    autoencoder.fit(x_train, y_train,
                    epochs=ep,
                    batch_size=bs,
                    shuffle=True,
                    validation_data=(x_test, y_test))
    encoded_imgs = encoder.predict(x_test)
    decoded_imgs = decoder.predict(encoded_imgs)
    return encoded_imgs, decoded_imgs


def loss(y_true, y_pred):
    return keras.losses.binary_crossentropy(y_true, y_pred)


if __name__ == '__main__':
    dir2read = 'data/easy/x/'
    x = read_data(dir2read)
    dir2read = 'data/easy/y/'
    y = read_data(dir2read)
    print(x[0])
    print(y[0])
    print(x.shape)
    print(y.shape)
