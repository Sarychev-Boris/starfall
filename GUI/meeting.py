from tkinter import ttk
import customtkinter
import tkinter
import sqlite3
from GUI.score_mixin import ScoreMixin

class Meeting(ScoreMixin):
    def __init__(self):
        ScoreMixin.__init__(self)
        list = ['Владение, %', 'Удары', 'Удары в створ', 'Угловые', 'Фолы', 'Желтые карточки', 'Красные карточки']


class MeetingTable(customtkinter.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        conn = sqlite3.connect('Arena.db')
        cur = conn.cursor()

        if parent.eventid:
            cur.execute(f"""SELECT meeting.meetingid, team1.name as teamid_1, team2.name as teamid_2, meeting.date, event.name
                            FROM meeting
	                        INNER JOIN team AS team1 ON meeting.teamid_1 = team1.teamid
	                        INNER JOIN team AS team2 ON meeting.teamid_2 = team2.teamid
	                        INNER JOIN event ON event.eventid = meeting.eventid;""")
            self.all_results = cur.fetchall()
        else:
            cur.execute(f"""SELECT meeting.meetingid, team1.name as teamid_1, team2.name as teamid_2, meeting.date, event.name
                                        FROM meeting
            	                        INNER JOIN team AS team1 ON meeting.teamid_1 = team1.teamid
            	                        INNER JOIN team AS team2 ON meeting.teamid_2 = team2.teamid
            	                        LEFT JOIN event ON event.eventid = meeting.eventid;""")
            self.all_results = cur.fetchall()

        self.geometry('1000x500')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.frame = customtkinter.CTkFrame(master=self)
        self.frame.grid(row=0, column=0, sticky='nsew')
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)

        self.meeting_table = ttk.Treeview(self)
        self.meeting_table['columns'] = ('ID Встречи', 'Команда 1', 'Команда 2', 'Дата', 'Турнир')
        self.meeting_table.column("#0", width=0, stretch=False)
        self.meeting_table.heading("#0", text="", anchor='center')
        for column in self.meeting_table['columns']:
            self.meeting_table.column(f"{column}", anchor='center', width=80)
            self.meeting_table.heading(f"{column}", text=f"{column}", anchor='center')


        for meeting in self.all_results:
            self.meeting_table.insert(parent='', index='end', text='',
                              values=meeting)

        self.meeting_table.grid(row=0, column=0, sticky='nsew')