from tkinter import *

from upload_sound_file import let_user_select_file


class Gui:
    def __init__(self):
        # init for Gui
        self.root = Tk()

        topFrame = Frame(self.root)
        topFrame.pack()
        bottomFrame = Frame(self.root)
        bottomFrame.pack(side=BOTTOM)

        button1 = Button(topFrame, text="Selecteer Audiobestand", fg="green", command=self.recieve_user_sound_file)
        button2 = Button(topFrame, text="Quit", fg="red", command=self.quit)
        button1.pack()
        button2.pack()

        label1 = Label(self.root, text="Huidig geselecteerd audiobestand: ")
        label1.pack()

        # init for vars
        self.current_sound_file = None

    def run(self):
        self.root.mainloop()

    def quit(self):
        self.root.destroy()

    def recieve_user_sound_file(self):
        self.current_sound_file = let_user_select_file()


gui = Gui()

gui.run()
