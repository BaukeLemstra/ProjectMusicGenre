import os
import pickle

import librosa
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

from deep_learning.model import get_rnn_model


def generate_taining_data():
    genres = 'blues classical country disco hiphop jazz metal pop reggae rock'.split()
    dataset = [[], []]
    for g in genres:
        for filename in os.listdir(f'./MIR/genres/{g}'):
            songname = f'./MIR/genres/{g}/{filename}'

            data_list = []
            y_list = [g] * 10

            for i in range(10):
                sub_data_list = []

                y, sr = librosa.load(songname, mono=True, duration=3, offset=i * 3)
                sub_data_list.append(librosa.feature.chroma_stft(y=y, sr=sr))
                sub_data_list.append(librosa.feature.spectral_centroid(y=y, sr=sr))
                sub_data_list.append(librosa.feature.spectral_bandwidth(y=y, sr=sr))
                sub_data_list.append(librosa.feature.spectral_rolloff(y=y, sr=sr))
                sub_data_list.append(librosa.feature.zero_crossing_rate(y))
                sub_data_list.append(librosa.feature.rms(y=y))
                mfcc = librosa.feature.mfcc(y=y, sr=sr)
                for e in mfcc:
                    sub_data_list.append(e)

                data_list.append(sub_data_list)

            dataset[0].append(data_list)
            dataset[1].append(y_list)

    with open('rnn_dataset.data', 'wb') as filehandle:
        # store the data as binary data stream
        pickle.dump(dataset, filehandle)


def main():
    if not os.path.exists("rnn_dataset.data"):
        generate_taining_data()

    with open('rnn_dataset.data', 'rb') as filehandle:
        dataset = pickle.load(filehandle)

    # fit label encoder
    genres = 'blues classical country disco hiphop jazz metal pop reggae rock'.split()
    encoder = LabelEncoder()
    encoder.fit(genres)

    for i in range(1000):
        for g in range(10):
            dataset[1][i][g] = encoder.transform([dataset[1][i][g]])

    print("hoi")

    X, Y = dataset[0], dataset[1]

    scaler = StandardScaler
    X = scaler.fit_transform(np.asmatrix(X, dtype=float))

    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)

    model = get_rnn_model()

    history = model.fit(X_train,
                        y_train,
                        epochs=1,
                        batch_size=1)

    results = model.evaluate(X_test, y_test)

    model.save('models/rnn_model.h5')


if __name__ == "__main__":
    main()
