from tkinter import ttk
import customtkinter
import screeninfo
from PIL import Image, ImageTk
import os
import sqlite3
import tkinter
import tkinter.filedialog
import datetime


class NewEvent(customtkinter.CTkToplevel):
    def __init__(self, parent, team_tuple):
        super().__init__(parent)
        self.geometry('1000x500')
        self.team_tuple = team_tuple
        self.rowconfigure((0, 1, 2), weight=1)
        self.columnconfigure((0, 1, 2), weight=1)

        self.event_name_entry = customtkinter.CTkEntry(master=self)
        self.event_name_entry.insert(0, 'Название турнира')
        self.event_name_entry.grid(row=0, column=0, columnspan=3, sticky='we', pady=10, padx=10)

        self.team_table = ttk.Treeview(self)
        self.team_table['columns'] = ('ID Команды', 'Название Команды')
        self.team_table.column("#0", width=0, stretch=False)
        self.team_table.column("ID Команды", anchor='center', width=80)
        self.team_table.column("Название Команды", anchor='center', width=80)

        self.team_table.heading("#0", text="", anchor='center')
        self.team_table.heading("ID Команды", text="ID Команды", anchor='center')
        self.team_table.heading("Название Команды", text="Название Команды", anchor='center')

        for team in team_tuple:
            self.team_table.insert(parent='', index='end', text='',
                              values=team)

        self.team_table.grid(row=1, column=0, columnspan=3, sticky='nsew', pady=10, padx=10)

        self.start_date_label = customtkinter.CTkLabel(master=self,
                                                       text='Дата начала:'
                                                       )
        self.start_date_label.grid(row=2, column=0)

        self.start_date_entry = customtkinter.CTkEntry(master=self)
        self.start_date_entry.insert(0, str(datetime.date.today()))

        self.start_date_entry.grid(row=2, column=1)

        self.confirm_button = customtkinter.CTkButton(master=self,
                                                      text='Создать',
                                                      command=self.create_event)
        self.confirm_button.grid(row=2, column=2)

    def create_event(self):
        conn = sqlite3.connect('Arena.db')
        cur = conn.cursor()

        cur.execute(f"""INSERT OR IGNORE INTO event(name, startdate)
                       VALUES('{self.event_name_entry.get()}', '{self.start_date_entry.get()}');
                    """)
        conn.commit()

        event_id = cur.execute(f"SELECT eventid FROM event WHERE name = '{self.event_name_entry.get()}';").fetchone()[0]

        for team in self.team_tuple:

            cur.execute(f"""INSERT INTO team_result(teamid, eventid)
                            VALUES('{team[0]}', '{event_id}')
                        """)
        conn.commit()

class Event(customtkinter.CTkToplevel):

    def __init__(self, parent, eventid):
        super().__init__(parent)
        self.parent = parent
        self.eventid = eventid
        conn = sqlite3.connect('Arena.db')
        cur = conn.cursor()
        self.event_data = cur.execute(f"""SELECT * FROM event WHERE eventid = {eventid}""").fetchone()
        self.geometry('1000x500')
        self.rowconfigure((0, 1, 2, 3), weight=1)
        self.columnconfigure((0, 1, 2), weight=1)

        self.event_name_label = customtkinter.CTkLabel(master=self,
                                                       text=self.event_data[1]
                                                       )

        self.event_name_label.grid(row=0, column=0, columnspan=2, sticky='we', pady=3, padx=3)



        self.team_table = ttk.Treeview(self)
        self.team_table['columns'] = ('ID Команды', 'Название Команды', 'Место', 'Win', 'Draw', 'Lose', 'Points')
        self.team_table.column("#0", width=0, stretch=False)
        self.team_table.heading("#0", text="", anchor='center')
        for column in self.team_table['columns']:
            self.team_table.column(f"{column}", anchor='center', width=80)
            self.team_table.heading(f"{column}", text=f"{column}", anchor='center')

        for team in cur.execute(f"""SELECT team.teamid, team.name, place, win, draw, lose, points
                                    FROM team_result
                                    INNER JOIN team ON team_result.teamid = team.teamid
                                    WHERE eventid = {eventid};"""):
            self.team_table.insert(parent='', index='end', text='',
                              values=team)

        self.team_table.grid(row=1, column=0, columnspan=3, sticky='nsew', pady=10, padx=10)

        self.start_date_label1 = customtkinter.CTkLabel(master=self,
                                                        text='Дата начала:'
                                                       )
        self.start_date_label1.grid(row=2, column=0)

        self.start_date_label2 = customtkinter.CTkLabel(master=self,
                                                        text=self.event_data[2]
                                                       )
        self.start_date_label2.grid(row=2, column=1)

        self.end_date_label1 = customtkinter.CTkLabel(master=self,
                                                      text='Дата окончания:'
                                                     )
        self.end_date_label1.grid(row=3, column=0)

        self.delete_button = customtkinter.CTkButton(master=self,
                                                     text='Удалить',
                                                     command=self.deleteEvent
                                                     )
        self.delete_button.grid(row=2, column=2)

        if self.event_data[4]:
            self.end_date_entry = customtkinter.CTkEntry(master=self)
            self.end_date_entry.grid(row=3, column=1)
            self.end_date_entry.insert(0, str(datetime.date.today()))

            self.end_button = customtkinter.CTkButton(master=self,
                                                      text='Завершить',
                                                      command=self.eventEnd
                                                      )
            self.end_button.grid(row=3, column=2)
            self.event_select_button = customtkinter.CTkButton(master=self,
                                                               command=self.event_select,
                                                               text='Провести встречу')
            self.event_select_button.grid(row=0, column=2, sticky='we', pady=3, padx=3)
        else:
            self.end_date_label2 = customtkinter.CTkLabel(master=self,
                                                          text=self.event_data[3])
            self.end_date_label2.grid(row=3, column=1)

    def deleteEvent(self):
        conn = sqlite3.connect('Arena.db')
        cur = conn.cursor()

        cur.execute(f"""DELETE FROM event WHERE {self.event_data[0]}""")
        conn.commit()

    def eventEnd(self):
        conn = sqlite3.connect('Arena.db')
        cur = conn.cursor()

        cur.execute(f"""UPDATE event SET enddate = '{self.end_date_entry.get()}', current = 0 
                        WHERE eventid = '{self.event_data[0]}';""")
        conn.commit()

    def event_select(self):
        self.parent.parent.eventid = self.eventid
        self.parent.parent.event_info.insert(0, self.event_data[1])
        self.parent.parent.team_1.eventid = self.eventid
        self.parent.parent.team_2.eventid = self.eventid



class EventTable(customtkinter.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        conn = sqlite3.connect('Arena.db')
        cur = conn.cursor()
        self.parent= parent
        self.geometry('1000x500')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.event_table = ttk.Treeview(self)
        self.event_table['columns'] = ('ID Турнира', 'Название Турнира', 'Дата начала', 'Дата окончания')
        self.event_table.column("#0", width=0, stretch=False)
        self.event_table.heading("#0", text="", anchor='center')
        for column in self.event_table['columns']:
            self.event_table.column(f"{column}", anchor='center', width=80)
            self.event_table.heading(f"{column}", text=f"{column}", anchor='center')

        event_list = cur.execute("""SELECT * FROM event""")

        for event in event_list:
            self.event_table.insert(parent='', index='end', text='', values=event)

        self.event_table.grid(row=0, column=0, sticky='nsew')

        self.event_table.bind("<Double-1>", self.show_event)
        self.window_event = None

    def show_event(self, event):
        if self.window_event == None or tkinter.Toplevel.winfo_exists(self.window_event) == 0:
            self.window_team_info = Event(self, self.event_table.item(self.event_table.focus()).get('values')[0])


# class EventSelection(customtkinter.CTkToplevel):
#     def __init__(self, parent):
#         super().__init__(parent)
#         self.parent = parent
#         conn = sqlite3.connect('Arena.db')
#         cur = conn.cursor()
#
#         self.geometry('1000x500')
#         self.rowconfigure(0, weight=1)
#         self.columnconfigure(0, weight=1)
#
#         self.event_table = ttk.Treeview(self)
#         self.event_table['columns'] = ('ID Турнира', 'Название Турнира', 'Дата начала', 'Дата окончания')
#         self.event_table.column("#0", width=0, stretch=False)
#         self.event_table.heading("#0", text="", anchor='center')
#         for column in self.event_table['columns']:
#             self.event_table.column(f"{column}", anchor='center', width=80)
#             self.event_table.heading(f"{column}", text=f"{column}", anchor='center')
#
#         event_list = cur.execute("""SELECT * FROM event WHERE current=1""")
#
#         for event in event_list:
#             self.event_table.insert(parent='', index='end', text='', values=event)
#
#         self.event_table.grid(row=0, column=0, sticky='nsew')
#
#         self.event_table.bind("<Double-1>", self.parent.select(self.event_table.item(self.event_table.focus()).get('values')))
#
#     def select_event(self):
#         self.parent.eventid = self.event_table.item(self.event_table.focus()).get('values')[0]
#         self.parent.event_info.insert(0, self.event_table.item(self.event_table.focus()).get('values')[1])

