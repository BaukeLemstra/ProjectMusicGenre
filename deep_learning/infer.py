import librosa
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder, StandardScaler


class Inference:
    def __init__(self):
        self.model = tf.keras.models.load_model(
            "C:/Users/machi/Desktop/ProjectMusicGenre-master/deep_learning/genre_model.h5")

    def infer(self, path_to_file):
        # filename,chroma_stft,rmse,spectral_centroid,spectral_bandwidth,rolloff,zero_crossing_rate,mfcc1,mfcc2,mfcc3,mfcc4,mfcc5,mfcc6,mfcc7,mfcc8,mfcc9,mfcc10,mfcc11,mfcc12,mfcc13,mfcc14,mfcc15,mfcc16,mfcc17,mfcc18,mfcc19,mfcc20,label

        y, sr = librosa.load(path_to_file, mono=True)
        chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
        spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
        spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        zcr = librosa.feature.zero_crossing_rate(y)
        mfcc = librosa.feature.mfcc(y=y, sr=sr)
        rms = librosa.feature.rms(y=y)

        input = [np.mean(chroma_stft), np.mean(rms), np.mean(spec_cent), np.mean(spec_bw), np.mean(rolloff),
                 np.mean(zcr)]

        for e in mfcc:
            input.append(np.mean(e))

        data = pd.read_csv("C:/Users/machi/Desktop/ProjectMusicGenre-master/deep_learning/data.csv")
        data.head()
        data = data.drop(['filename'], axis=1)

        scaler = StandardScaler()
        scaler.fit(np.array(data.iloc[:, :-1], dtype=float))

        genre_list = data.iloc[:, -1]
        encoder = LabelEncoder()
        encoder.fit(genre_list)

        arr = np.array(input, dtype=float)
        arr = np.expand_dims(arr, 0)
        X = scaler.transform(arr)

        prediction_list = self.model.predict(X)
        prediction_list = np.squeeze(prediction_list)

        final_result = []
        for i in range(0, 3):
            res = np.argmax(prediction_list)
            final_result.append([encoder.inverse_transform([res]), prediction_list[res]])
            prediction_list[res] = 0
        return final_result
