import tensorflow as tf
from tensorflow.keras import layers
import numpy as np


def GAN_GLRU(x_train, y_train):
    
    def Generator(inputs):
        x = layers.Dense(128, activation='relu')(inputs)  # Increased initial Dense layer
        x = layers.SimpleRNN(256, return_sequences=True)(x)  # Increased size of RNN
        x = layers.BatchNormalization()(x)
        x = layers.LeakyReLU()(x)
        x = layers.LSTM(256, return_sequences=True)(x)  # Added more LSTM layers
        x = layers.LSTM(128, return_sequences=True)(x)
        x = layers.LSTM(64, return_sequences=False)(x)
        x = layers.Reshape((1, 64))(x)  # Reshape to 3D to make it compatible with the LSTM layer
        return x
    
    def Discriminator(input_shape, number_of_classes):
        inputs = layers.Input(shape=input_shape)
        x = Generator(inputs)
        x = layers.LSTM(256, return_sequences=True)(x)  # Using larger LSTM layer
        x = layers.LeakyReLU(alpha=0.2)(x)
        x = layers.SimpleRNN(256, return_sequences=True)(x)  # Larger SimpleRNN layers
        x = layers.LeakyReLU(alpha=0.2)(x)
        x = layers.SimpleRNN(128, return_sequences=True)(x)  # Additional SimpleRNN
        x = layers.LeakyReLU(alpha=0.2)(x)
        x = layers.SimpleRNN(64, return_sequences=False)(x)  # Final SimpleRNN layer
        x = layers.LeakyReLU(alpha=0.2)(x)
        
        # Classifier
        if number_of_classes == 2:
            outputs = layers.Dense(number_of_classes - 1, activation='sigmoid')(x)  # Binary classification
            model = tf.keras.Model(inputs, outputs)
            model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        else:
            outputs = layers.Dense(number_of_classes, activation='softmax')(x)  # Multi-class classification 
            model = tf.keras.Model(inputs, outputs)
            model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
           
        return model
    
    input_shape = x_train[0].shape
    number_of_classes = len(np.unique(y_train))
    GAN_GLRU_model = Discriminator(input_shape, number_of_classes)
    
    return GAN_GLRU_model





