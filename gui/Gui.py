import winsound
from tkinter import *

from deep_learning.infer import SimpleInference, RnnInference
from utils.mp3_wav_util import mp3_to_wav
from utils.upload_sound_file import let_user_select_file


class Gui:
    def __init__(self, model_type="rnn"):
        # init for Gui
        self.root = Tk()
        # self.root.geometry("800x600")
        self.root.title("Muziek genre herkenner")

        button = Button(self.root, text="Selecteer Audiobestand", fg="green", command=self.recieve_user_sound_file,
                        width=22)
        button.grid(row=0, column=0)
        button2 = Button(self.root, text="Afspelen", fg="red", command=self.play, width=22)
        button2.grid(row=0, column=1)
        button3 = Button(self.root, text="Stop", fg="red", command=self.stop, width=22)
        button3.grid(row=0, column=2)

        self.label = Label(self.root, text="Huidig geselecteerd audiobestand: Geen")
        self.label.grid(row=2, column=1)

        self.text = Text(self.root)
        self.text.insert('1.0', "Predictie")
        self.text.grid(row=3, column=1)

        self.root.grid()

        # init for vars
        self.current_sound_file = None

        self.root.protocol("WM_DELETE_WINDOW", self._delete_window)

        # init for inference class
        if model_type == "simple":
            self.inference = SimpleInference()
        elif model_type == "rnn":
            self.inference = RnnInference()
        self.pred = None
        self.current_rnn_prediction = 0

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

    def predict_and_show(self, mode="rnn"):
        self.pred = self.inference.infer(self.current_sound_file)
        if mode == "simple":
            self.draw_prediction(self.pred)

        elif mode == "rnn":
            self.continuously_update_predict_window()

    def continuously_update_predict_window(self):
        """ refresh the content of the label every second """
        # schrijf om de 3 seconden een nieuw deel van de prediction
        self.draw_prediction(self.pred[self.current_rnn_prediction])
        self.current_rnn_prediction += 1
        self.root.after(3000, self.continuously_update_predict_window)

    def draw_prediction(self, pred):
        self.text.delete('1.0', '10.0')

        for x in pred:
            to_insert = (str(x[0]) + " " + str(x[1]))
            self.text.insert('end', to_insert + '\n')

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
