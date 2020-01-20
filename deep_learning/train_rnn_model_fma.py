import logging
import os
import pickle

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from deep_learning.model import get_rnn_model

logger = logging.getLogger("logger")
logging.basicConfig(level=logging.DEBUG)


def generate_taining_data():
    import os
    import librosa

    import thirdparty.utils as utils  # note my fix to fma utils, https://github.com/mdeff/fma/issues/34

    AUDIO_DIR = 'fma_medium/'
    tracks = utils.load('tracks.csv')
    base_dir = "Samples_medium/"

    os.mkdir(base_dir[:-1])

    small = tracks['set', 'subset'] <= 'medium'

    y_small = tracks.loc[small, ('track', 'genre_top')]

    sr = 44100
    for track_id, genre in y_small.iteritems():
        if not os.path.exists(base_dir + genre):
            os.mkdir(base_dir + genre)

        mp3_filename = utils.get_audio_path(AUDIO_DIR, track_id)
        out_wav_filename = base_dir + genre + '/' + str(track_id) + '.wav'

        print("reading ", mp3_filename)
        data, sr = librosa.load(mp3_filename, sr=sr, mono=True)

        print("writing ", out_wav_filename)
        librosa.output.write_wav(out_wav_filename, data, sr=sr)


def main(return_sequences=True):
    if not os.path.exists("rnn_dataset.data"):
        generate_taining_data()

    with open('rnn_dataset.data', 'rb') as filehandle:
        dataset = pickle.load(filehandle)

    X, Y = dataset[0], dataset[1]

    # normalize de dataset
    scalers = []
    for i in range(26):
        slice = X[:, :, i]
        scaler = StandardScaler()
        scaled_slice = scaler.fit_transform(slice)
        X[:, :, i] = scaled_slice
        scalers.append(scaler)

    # sla de scaler data op om tijdens inference de data op dezelfde manier te kunnen scalen
    with open('saved_scalers.data', 'wb') as filehandle:
        # store the data as binary data stream
        pickle.dump(scalers, filehandle)

    model = get_rnn_model(return_sequences=return_sequences)

    # als de RNN niet een sequence aan data returned, moeten alle labels behavle de eerste weg
    if not return_sequences:
        Y = np.delete(Y, [1, 2, 3, 4, 5, 6, 7, 8, 9], axis=1)

    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)

    history = model.fit(X_train,
                        y_train,
                        epochs=100,
                        batch_size=64)

    results = model.evaluate(X_test, y_test)

    model.save('models/rnn_model.h5')


if __name__ == "__main__":
    main()
