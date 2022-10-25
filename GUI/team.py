import tkinter
import tkinter.filedialog
# from PIL import Image, ImageTk
from GUI.score_mixin import ScoreMixin
import os

PATH = os.path.dirname(os.path.realpath(__file__))
stats = ['Владение, %', 'Удары', 'Удары в створ', 'Угловые', 'Фолы', 'Желтые карточки', 'Красные карточки']


class Team(ScoreMixin):

    def __init__(self, name='Название команды', ID=int(), logo=PATH+"/test_images/red.png"):
        ScoreMixin.__init__(self)
        self.name = tkinter.StringVar()
        self.set_name(name)
        self._logo = logo
        self._ID = ID

        self.stats = {stat: tkinter.IntVar() for stat in stats}
        for stat in stats:
            self.stats[stat].set(0)

    def get_name(self):
        return self.name.get()

    def set_name(self, var):
        self.name.set(var)

    def get_logo(self):
        return self._logo

    def get_ID(self):
        return self._ID

    def set_ID(self, var):
        self._ID = var
