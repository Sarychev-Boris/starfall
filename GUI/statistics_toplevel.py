import tkinter
import customtkinter
import screeninfo
import os
import configparser
import sqlite3
from PIL import Image, ImageTk
import time

class StatTopLevel(customtkinter.CTkToplevel):
    def __init__(self, parent):

        super().__init__(parent)

        conn = sqlite3.connect('Arena.db')
        cur = conn.cursor()

        self.parent = parent
        screen_2 = screeninfo.get_monitors()[1]

        config = configparser.ConfigParser()  # создаём объекта парсера
        config.read("config.ini")  # читаем конфиг

        self.geometry('%dx%d+%d+%d' % (screen_2.width, screen_2.height, self.winfo_screenwidth(), 0))
        self.overrideredirect(True)

        self.logo1_path = self.parent.team_1.logo_path
        self.logo2_path = self.parent.team_2.logo_path
        self.team1_img = Image.open(self.logo1_path).resize(
            (int(config["stats"]["width"]), (int(config["stats"]["height"]))))
        self.team2_img = Image.open(self.logo2_path).resize(
            (int(config["stats"]["width"]), (int(config["stats"]["height"]))))

        self.rowconfigure(tuple(i for i in range(7)), weight=1)
        self.columnconfigure(tuple(i for i in range(5)), weight=1)

        self.team1_frame = customtkinter.CTkFrame(master=self,
                                                  fg_color=("white", "#212325")
                                                  )
        self.team1_frame.grid(row=0, column=0, rowspan=7, sticky='nsw')
        self.team1_frame.rowconfigure((0, 1, 2), weight=1)
        self.team1_frame.columnconfigure(0, weight=1)

        self.team2_frame = customtkinter.CTkFrame(master=self,
                                                  fg_color=("white", "#212325")
                                                  )
        self.team2_frame.grid(row=0, column=4, rowspan=7, sticky='nse')
        self.team2_frame.rowconfigure((0, 1, 2), weight=1)
        self.team2_frame.columnconfigure(0, weight=1)

        self.team1_logo = customtkinter.CTkButton(master=self.team1_frame,
                                                  text='',
                                                  image=ImageTk.PhotoImage(self.team1_img),
                                                  state='disabled',
                                                  fg_color=("white", "#212325")
                                                  )
        self.team1_logo.grid(row=0, column=0, rowspan=2, sticky='nsew')

        self.team1_score = customtkinter.CTkLabel(master=self.team1_frame,
                                                  text=parent.team_1.team_score.get(),
                                                  text_font=('Arials', (int(config["board"]["team1_score"])), ''),
                                                  anchor="center",
                                                  # fg_color=("white", "gray38")
                                                  )
        self.team1_score.grid(row=2, column=0, sticky='nsew')

        self.team2_logo = customtkinter.CTkButton(master=self.team2_frame,
                                                  text='',
                                                  image=ImageTk.PhotoImage(self.team2_img),
                                                  state='disabled',
                                                  fg_color=("white", "#212325")
                                                  )
        self.team2_logo.grid(row=0, column=0, rowspan=2, sticky='nsew')

        self.team2_score = customtkinter.CTkLabel(master=self.team2_frame,
                                                  text=parent.team_2.team_score.get(),
                                                  text_font=('Arials', (int(config["board"]["team1_score"])), ''),
                                                  anchor="center",
                                                  # fg_color=("white", "gray38")
                                                  )
        self.team2_score.grid(row=2, column=0, sticky='nsew')

        list = ['Владение, %', 'Удары', 'Удары в створ', 'Угловые', 'Фолы', 'Желтые карточки', 'Красные карточки']
        i=0
        for stat in list:
            self.label = customtkinter.CTkLabel(master=self,
                                                text=f'{stat}',
                                                text_font=('Arials',(int(config["stats"]["stats_name"])), '')
                                                )
            self.label.grid(column=2, row=i, sticky='nsew', pady=2)

            self.team1_stat = customtkinter.CTkLabel(master=self,
                                                text=f'{self.parent.statistics.dict_1.get(stat).get()}',
                                                text_font=('Arials', (int(config["stats"]["stats"])), '')
                                                )
            self.team1_stat.grid(column=1, row=i, sticky='nsew', pady=2)

            self.team2_stat = customtkinter.CTkLabel(master=self,
                                                text=f'{self.parent.statistics.dict_2.get(stat).get()}',
                                                text_font=('Arials', (int(config["stats"]["stats"])), '')
                                                )
            self.team2_stat.grid(column=3, row=i, sticky='nsew', pady=2)

            i+=1

