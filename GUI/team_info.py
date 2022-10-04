from tkinter import ttk
import customtkinter
import screeninfo
from PIL import Image, ImageTk
import os
import sqlite3
import tkinter
import tkinter.filedialog
from GUI.add_team import AddTeam

class TeamInfo(AddTeam):
    def __init__(self, parent, team_id):

        super().__init__(parent)
        self.parent = parent
        self.focused = self.parent.table.focus()
        conn = sqlite3.connect('Arena.db')
        cur = conn.cursor()

        self.team_id = team_id
        self.team_name = cur.execute(f"SELECT name FROM team WHERE teamid = '{team_id}';").fetchone()[0]
        self.logo_path = cur.execute(f"SELECT emblem FROM team WHERE teamid = '{team_id}';").fetchone()[0]

        # self.team_name.set(cur.execute(f"SELECT name FROM team WHERE teamid = '{team_id}';").fetchone()[0])


        print(self.team_name)

        # self.team_name_entry.textvariable = tkinter.StringVar()
        self.team_name_entry.insert(0, self.team_name)

        self.team_name_entry.after(0, self.team_name_entry.update())

        self.squad = cur.execute(f"""SELECT fullname, sportsman_num
                                     FROM sportsman, sportsman_team
                                     WHERE sportsman_team.teamid = {self.team_id} 
                                     AND sportsman_team.sportsmanid = sportsman.sportsmanid;      
                                  """).fetchall()

        # print(self.squad)
        i = 0
        for sportsman in self.squad:
            self.entry_name[i].insert(0, sportsman[0])
            self.entry_num[i].insert(0, sportsman[1])
            i += 1

        self.team_logo.destroy()
        self.team_image = ImageTk.PhotoImage(Image.open(self.logo_path).resize((200, 200)))
        self.team_logo = customtkinter.CTkButton(master=self,
                                                 image=self.team_image,
                                                 text='',
                                                 command=self.set_logo
                                                 )
        self.team_logo.grid(row=0, column=1, rowspan=2)

        self.confirm_button.configure(text='Изменить')
        self.confirm_button.command = self.change_info

        self.delete_button = customtkinter.CTkButton(master=self,
                                                     text='Удалить',
                                                     command=self.delete_team
                                                      )
        self.delete_button.grid(row=2, column=0)

    def change_info(self):

        conn = sqlite3.connect('Arena.db')
        cur = conn.cursor()
        print(self.team_name_entry.get())
        print(self.logo_path)
        cur.execute(f"""UPDATE team
                        SET name = '{self.team_name_entry.get()}',
                        emblem = '{self.logo_path}'
                        WHERE teamid = {self.team_id};
        """)
        cur.execute(f"SELECT * FROM team WHERE teamid = '{self.team_id}';")
        team = cur.fetchone()
        print(team)

        self.parent.table.item(self.focused, values=(team))
        conn.commit()

        cur.execute(f"""DELETE FROM sportsman_team
                       WHERE teamid = '{self.team_id}'
                    """)

        for i in range(11):

            cur.execute(f"""INSERT OR IGNORE INTO sportsman(fullname)
                        VALUES('{self.entry_name[i].get()}');""")
            conn.commit()

            sportsman_id = cur.execute(f"SELECT sportsmanid FROM sportsman WHERE fullname = '{self.entry_name[i].get()}';").fetchone()[0]
            conn.commit()
            print(sportsman_id)
            cur.execute(f"""INSERT INTO sportsman_team(sportsmanid, teamid, sportsman_num)
                            VALUES('{sportsman_id}', '{self.team_id}', {self.entry_num[i].get()})""")
            conn.commit()


        self.destroy()

    def delete_team(self):
        conn = sqlite3.connect('Arena.db')
        cur = conn.cursor()

        cur.execute(f"""DELETE FROM sportsman_team
                        WHERE teamid = '{self.team_id}'
                    """)
        conn.commit()

        cur.execute(f"""DELETE FROM team
                        WHERE teamid = '{self.team_id}'
                    """)
        conn.commit()
        self.parent.table.delete(self.focused)
        self.destroy()


