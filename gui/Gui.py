import winsound
from tkinter import *

from deep_learning.infer import Inference
from utils.mp3_wav_util import mp3_to_wav
from utils.upload_sound_file import let_user_select_file


class Gui:
    def __init__(self):
        # init for Gui
        self.root = Tk()

        self.root.geometry("800x600")
        self.root.title("Muziek genre herkenner")

        self.topFrame = Frame(self.root)
        self.topFrame.pack()
        self.bottomFrame = Frame(self.root)
        self.bottomFrame.pack(side=BOTTOM)

        button1 = Button(self.topFrame, text="Selecteer Audiobestand", fg="green", command=self.recieve_user_sound_file)
        button1.pack()
        button3 = Button(self.topFrame, text="Afspelen", fg="red", command=self.play)
        button3.pack()
        button3 = Button(self.topFrame, text="Stop", fg="red", command=self.stop)
        button3.pack()

        self.label = Label(self.root, text="Huidig geselecteerd audiobestand: Geen")
        self.label.pack()

        self.label2 = Label(self.root, text="Huidige prediction: Geen")
        self.label2.pack()

        # init for vars
        self.current_sound_file = None

        self.root.protocol("WM_DELETE_WINDOW", self._delete_window)

        # init for inference class
        self.inference = Inference()

    def run(self):
        self.root.mainloop()

    def recieve_user_sound_file(self):
        user_selected_file = let_user_select_file()

        if user_selected_file.endswith("mp3") or user_selected_file.endswith("wav"):
            self.current_sound_file = user_selected_file

            if self.current_sound_file.endswith("mp3"):
                self.current_sound_file = mp3_to_wav(self.current_sound_file)

            split = self.current_sound_file.split("/")
            new_text = "Huidig geselecteerd audiobestand: {}".format(split[len(split) - 1])
            self.label.config(text=new_text)

        else:
            self.popupmsg("Selecteer een mp3 of een wav bestand.")

    def play(self):
        if self.current_sound_file is not None:
            self.predict_and_show()
            winsound.PlaySound(self.current_sound_file, winsound.SND_ASYNC)

    def _delete_window(self):
        self.root.destroy()
        winsound.PlaySound(None, winsound.SND_PURGE)

    def predict_and_show(self):
        new_text = self.inference.infer(self.current_sound_file)
        self.label2.config(text=new_text)

    @staticmethod
    def stop():
        winsound.PlaySound(None, winsound.SND_PURGE)

    @staticmethod
    def get_selected_file():
        return let_user_select_file()

    @staticmethod
    def popupmsg(msg):
        NORM_FONT = ("Helvetica", 10)
        popup = Tk()
        popup.wm_title("!")
        label = Label(popup, text=msg, font=NORM_FONT)
        label.pack(side="top", fill="x", pady=10)
        B1 = Button(popup, text="Ok", command=popup.destroy)
        B1.pack()
        popup.mainloop()
