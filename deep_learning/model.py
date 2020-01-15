import tensorflow as tf


def get_simple_model(input_shape):
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(1024, activation='relu', input_shape=(input_shape,)),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(512, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(256, activation='relu'),
        tf.keras.layers.Dense(10, activation='softmax')])

    model.compile(optimizer=tf.keras.optimizers.Adam(0.01),
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    return model


def get_rnn_model(return_sequences=True):
    model = tf.keras.Sequential([
        tf.keras.layers.LSTM(1024, return_sequences=return_sequences,
                             dropout=0.5,
                             recurrent_dropout=0.4,
                             ),
        tf.keras.layers.Dense(512, activation='relu'),
        tf.keras.layers.Dense(10, activation='softmax')])

    model.compile(optimizer=tf.keras.optimizers.Adam(0.01),
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    return model
