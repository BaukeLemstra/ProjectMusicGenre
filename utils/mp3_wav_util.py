from pydub import AudioSegment


def mp3_to_wav(file_path):
    sound = AudioSegment.from_mp3(file_path)

    split = file_path.split("/")
    filename = split[-1]
    filename = filename.replace(".mp3", ".wav")
    final_path = "wav_files/{}".format(filename)

    sound.export(final_path, format="wav")
    return final_path
