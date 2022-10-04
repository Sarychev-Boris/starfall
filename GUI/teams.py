from tkinter import ttk
import customtkinter
import tkinter
import screeninfo
from PIL import Image, ImageTk
import os
from GUI.add_team import AddTeam
from GUI.team_info import TeamInfo
from GUI.event import NewEvent
import sqlite3


class TeamsTable(customtkinter.CTkToplevel):
    def __init__(self, parent, eventid):
        super().__init__(parent)
        self.parent = parent
        conn = sqlite3.connect('Arena.db')
        cur = conn.cursor()
        if eventid:
            cur.execute(f"""SELECT team.teamid, team.name, team.emblem FROM team
                            INNER JOIN team_result ON team_result.teamid = team.teamid
                            INNER JOIN event ON event.eventid = team_result.eventid
                            WHERE event.eventid = '{eventid}';""")
            self.all_results = cur.fetchall()
        else:
            cur.execute("SELECT * FROM team")
            self.all_results = cur.fetchall()


        self.geometry('1000x500')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.frame = customtkinter.CTkFrame(master=self)
        self.frame.grid(row=0, column=0, sticky='nsew')
        self.frame.rowconfigure((0, 1), weight=1)
        self.frame.columnconfigure(0, weight=1)

        self.table = ttk.Treeview(self.frame)
        self.table['columns']  = ('ID Команды', 'Название Команды', 'Путь к гербу')
        self.table.column("#0", width=0, stretch=False)
        self.table.column("ID Команды", anchor='center', width=80)
        self.table.column("Название Команды", anchor='center', width=80)

        self.table.heading("#0", text="", anchor='center')
        self.table.heading("ID Команды", text="ID Команды", anchor='center')
        self.table.heading("Название Команды", text="Название Команды", anchor='center')
        self.table.heading("Путь к гербу", text="Путь к гербу", anchor='center')


        for team in self.all_results:
            self.table.insert(parent='', index='end', text='',
                              values=team)

        self.table.grid(row=0, column=0, sticky='nsew')
        # self.table.bind("<Double-1>", self.team_settings)

        self.add_button = customtkinter.CTkButton(master=self.frame,
                                                  text='Добавить команду',
                                                  command=self.add_team
                                                  )
        self.add_button.grid(row=1, column=0, sticky='se')

        self.add_button = customtkinter.CTkButton(master=self.frame,
                                                  text='Создать турнир',
                                                  command=self.create_event
                                                  )
        self.add_button.grid(row=2, column=0, sticky='se')

        self.window_add_team = None
        self.window_team_info = None
        self.window_create_event = None

    def add_team(self):
        if self.window_add_team == None or tkinter.Toplevel.winfo_exists(self.window_add_team) == 0:
            self.window_add_team = AddTeam(self)

    def team_settings(self, event):
        if self.window_team_info == None or tkinter.Toplevel.winfo_exists(self.window_team_info) == 0:
            self.window_team_info = TeamInfo(self, self.table.item(self.table.focus()).get('values')[0])

    def create_event(self):
        self.selected = self.table.selection()
        self.teamlist=[]
        for i in self.selected:
            self.teamlist.append(self.table.item(i).get('values')[0:2])

        if self.window_create_event == None or tkinter.Toplevel.winfo_exists(self.window_create_event) == 0:
            self.window_create_event = NewEvent(self, self.teamlist)

    def select(self):
        pass

class TeamSelect(customtkinter.CTkToplevel):
    def __init__(self, parent, eventid, team):
        super().__init__(parent)
        self.team_frame = team
        self.parent = parent
        conn = sqlite3.connect('Arena.db')
        cur = conn.cursor()
        if eventid:
            cur.execute(f"""SELECT team.teamid, team.name, team.emblem FROM team
                            INNER JOIN team_result ON team_result.teamid = team.teamid
                            INNER JOIN event ON event.eventid = team_result.eventid
                            WHERE event.eventid = '{eventid}';""")
            self.all_results = cur.fetchall()
        else:
            cur.execute("SELECT * FROM team")
            self.all_results = cur.fetchall()


        self.geometry('1000x500')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.table = ttk.Treeview(self)
        self.table['columns']  = ('ID Команды', 'Название Команды', 'Путь к гербу')
        self.table.column("#0", width=0, stretch=False)
        self.table.column("ID Команды", anchor='center', width=80)
        self.table.column("Название Команды", anchor='center', width=80)

        self.table.heading("#0", text="", anchor='center')
        self.table.heading("ID Команды", text="ID Команды", anchor='center')
        self.table.heading("Название Команды", text="Название Команды", anchor='center')
        self.table.heading("Путь к гербу", text="Путь к гербу", anchor='center')

        for team in self.all_results:
            self.table.insert(parent='', index='end', text='',
                              values=team)

        self.table.grid(row=0, column=0, sticky='nsew')
        self.table.bind("<Double-1>", self.select)

    def select(self, event):
        self.selected = self.table.selection()
        self.team_data = self.table.item(self.selected[0]).get('values')
        image = Image.open(self.team_data[2]).resize((250, 250))
        self.team_frame.team_name.set(self.team_data[1])
        self.team_frame.teamid = self.team_data[0]
        self.team_frame.team_logo.destroy()

        self.team_frame.logo_path = self.team_data[2]
        self.logo_img = Image.open(self.team_frame.logo_path).resize((250, 250))

        self.team_frame.team_logo = customtkinter.CTkButton(master=self.team_frame.frame_team,
                                                 image=ImageTk.PhotoImage(self.logo_img),
                                                 text='',
                                                 command=self.team_frame.set_logo
                                                 )
        self.team_frame.team_logo.grid(row=0, column=0, sticky='nwe')
        self.destroy()






