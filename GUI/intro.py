import tkinter
import customtkinter
import screeninfo
import os
import configparser
import sqlite3
from PIL import Image, ImageTk
import time

class Intro(customtkinter.CTkToplevel):
    def __init__(self, parent, team_id):

        super().__init__(parent)

        conn = sqlite3.connect('Arena.db')
        cur = conn.cursor()

        self.parent = parent
        screen_2 = screeninfo.get_monitors()[1]
        self.destroy_flag = False

        PATH = os.path.dirname(os.path.realpath(__file__))
        self.config = configparser.ConfigParser()  # создаём объекта парсера
        self.config.read("config.ini")  # читаем конфиг

        self.geometry('%dx%d+%d+%d' % (screen_2.width, screen_2.height, self.winfo_screenwidth(), 0))
        self.overrideredirect(True)


        self.rowconfigure(tuple(i for i in range(12)), weight=1)
        self.columnconfigure((0, 1), weight=1)

        self.logo_path = cur.execute(f"""SELECT emblem FROM team WHERE teamid = '{team_id}';""").fetchone()[0]
        self.team_logo = Image.open(self.logo_path).resize(
            (int(self.config["intro"]["width"]), (int(self.config["intro"]["height"]))))

        self.label_teamname = customtkinter.CTkLabel(master=self,
                                                     text=cur.execute(f"""SELECT name FROM team WHERE teamid = '{team_id}';""").fetchone()[0],
                                                     height = 20,
                                                     text_font = ('Arials', (int(self.config["intro"]["team_name"])), '')
                                                     )
        self.label_teamname.grid(row=0, column=0, columnspan=2)

        self.sportsmanlist = cur.execute(f"""SELECT sportsman_num, fullname FROM sportsman_team
                                             INNER JOIN team ON sportsman_team.teamid = team.teamid
                                             INNER JOIN sportsman ON sportsman_team.sportsmanid = sportsman.sportsmanid
                                             WHERE sportsman_team.teamid = {team_id};
                                          """)

        i = 1
        for sportsman in self.sportsmanlist:
            self.label_sportsmanname = customtkinter.CTkLabel(master=self,
                                                              text=str(sportsman[0]) + '        ' + sportsman[1],
                                                              text_font=('Arials', (int(self.config["intro"]["fullname"])), '')
                                                              )
            self.label_sportsmanname.grid(row=i, column=0, sticky='nsw', pady=int(self.config["intro"]["pady"]))
            i += 1

        self.button_teamlogo = customtkinter.CTkButton(master=self,
                                                       text='',
                                                       image=ImageTk.PhotoImage(self.team_logo),
                                                       state='disable',
                                                       fg_color=("white", "#212325")
                                                       )

        self.button_teamlogo.grid(row=1, column=1, rowspan=10)
        self.a=0.0
        self.wm_attributes('-alpha', self.a)

        self.label_teamname.after(0, self.merge)

    def merge(self):
        if self.a < 1.5:
            self.wm_attributes('-alpha', self.a)
            self.a += 0.05

            self.label_teamname.after(100, self.merge)


