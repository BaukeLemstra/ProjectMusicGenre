import os
import librosa

import thirdparty.utils as utils  # note my fix to fma utils, https://github.com/mdeff/fma/issues/34

AUDIO_DIR = 'fma_medium/'
tracks = utils.load('tracks.csv')
import time

base_dir = "Samples_medium/"

os.mkdir(base_dir[:-1])

small = tracks['set', 'subset'] <= 'medium'

y_small = tracks.loc[small, ('track', 'genre_top')]

sr = 44100

total_errors = 0
for track_id, genre in y_small.iteritems():
    if not os.path.exists(base_dir + genre):
        os.mkdir(base_dir + genre)

    mp3_filename = utils.get_audio_path(AUDIO_DIR, track_id)
    out_wav_filename = base_dir + genre + '/' + str(track_id) + '.wav'

    try:
        print("reading ", mp3_filename)
        data, sr = librosa.load(mp3_filename, sr=sr, mono=True)

        print("writing ", out_wav_filename)
        librosa.output.write_wav(out_wav_filename, data, sr=sr)
    except RuntimeError:
        total_errors += 1

print(str(total_errors))
