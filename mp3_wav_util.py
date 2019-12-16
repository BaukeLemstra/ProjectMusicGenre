from os import path
from pydub import AudioSegment


def mp3_to_wav(file_path):
    sound = AudioSegment.from_mp3(file_path)
    return sound
