from tkinter import ttk
import customtkinter
import screeninfo
from PIL import Image, ImageTk
import os
import sqlite3
import tkinter
import tkinter.filedialog


class AddTeam(customtkinter.CTkToplevel):

    def __init__(self, parent):

        super().__init__(parent)

        self.parent = parent

        self.geometry('500x500')

        self.logo_path = ''


        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure((0, 1, 2), weight=1)

        self.frame_sportsman = customtkinter.CTkFrame(master=self)
        self.frame_sportsman.grid(row=1, column=0)
        self.frame_sportsman.rowconfigure(tuple([i for i in range(11)]), weight=1)
        self.frame_sportsman.columnconfigure((0, 1), weight=1)

        self.team_name_entry = customtkinter.CTkEntry(master=self,
                                                      placeholder_text='Название команды',
                                                      # textvariable=self.team_name,
                                                      )
        self.team_name_entry.grid(row=0, column=0, sticky='we')

        self.entry_name = []
        self.entry_num = []
        for i in range(11):
            self.entry_num.append(customtkinter.CTkEntry(master=self.frame_sportsman,
                                                         placeholder_text='Номер игрока'),
                                                         )
            self.entry_num[i].grid(row=i, column=0)

            self.entry_name.append(customtkinter.CTkEntry(master=self.frame_sportsman,
                                                          placeholder_text=f'Игрок {i+1}'))
            self.entry_name[i].grid(row=i, column=1)

        self.team_logo = customtkinter.CTkButton(master=self,
                                                 # image=ImageTk.PhotoImage(image),
                                                 text='IMAGE',
                                                 command=self.set_logo
                                                 )

        self.team_logo.grid(row=1, column=1, rowspan=10)

        self.confirm_button = customtkinter.CTkButton(master=self,
                                                      text='Добавить',
                                                      command=self.add_team
                                                      )
        self.confirm_button.grid(row=2, column=1)

    def add_team(self):
        conn = sqlite3.connect('Arena.db')
        cur = conn.cursor()

        cur.execute(f"""INSERT OR IGNORE INTO team(name, emblem)
           VALUES('{self.team_name_entry.get()}', '{self.logo_path}');""")
        conn.commit()

        team_id = cur.execute(f"SELECT teamid FROM team WHERE name = '{self.team_name_entry.get()}';").fetchone()[0]

        for i in range(11):

            cur.execute(f"""INSERT OR IGNORE INTO sportsman(fullname)
                        VALUES('{self.entry_name[i].get()}');""")
            conn.commit()

            sportsman_id = cur.execute(f"SELECT sportsmanid FROM sportsman WHERE fullname = '{self.entry_name[i].get()}';").fetchone()[0]

            print(sportsman_id)
            cur.execute(f"""INSERT INTO sportsman_team(sportsmanid, teamid, sportsman_num)
                            VALUES('{sportsman_id}', '{team_id}', {self.entry_num[i].get()})""")
            conn.commit()

        cur.execute(f"SELECT * FROM team WHERE name = '{self.team_name_entry.get()}';")
        team = cur.fetchone()

        self.parent.table.insert(parent='', index='end', text='',
                                 values=team)
        self.destroy()

    def set_logo(self):
        global image
        self.data = tkinter.filedialog.askopenfile(parent=self, filetypes=[('Image Files', '*.png')])
        image = Image.open(self.data.name).resize((200, 200))
        self.logo_path = self.data.name
        self.team_logo.destroy()
        self.team_logo = customtkinter.CTkButton(master=self,
                                                 image=ImageTk.PhotoImage(image),
                                                 text='',
                                                 command=self.set_logo
                                                 )
        self.team_logo.grid(row=0, column=1, rowspan=2)

