import tkinter

class ScoreMixin:
    def __init__(self):
        self.score = tkinter.IntVar()
        self.score.set(0)

    def add_point(self, entry):
        entry.after(0, self.score.set(self.score.get() + 1))

    def remove_point(self, entry):
        entry.after(0, self.score.set(self.score.get() - 1))

    def reset_point(self, entry):
        entry.after(0, self.score.set(0))