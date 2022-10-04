import tkinter
import tkinter.messagebox
import tkinter.filedialog
import customtkinter
from PIL import Image, ImageTk
from GUI.teams import TeamSelect
import os

PATH = os.path.dirname(os.path.realpath(__file__))

class Team(customtkinter.CTk):

    def __init__(self, master, row=0, column=0):
        self.parent = master
        self.eventid = None
        self.teamid = None
        self.team_score = tkinter.IntVar()
        self.team_score.set(0)

        self.team_name = tkinter.StringVar()
        self.team_name.set('Название команды')

        self.team_state = tkinter.StringVar()
        self.team_state.set('Регион')

        self.logo_path = PATH + "/test_images/red.png"
        # self.logo_path =

        self.logo_img = Image.open(self.logo_path).resize((250, 250))

        self.frame_team = customtkinter.CTkFrame(master=master)
        self.frame_team.grid(row=row, column=column, pady=15, padx=15, sticky="new")
        self.frame_team.rowconfigure((0, 1, 2), weight=1)
        self.frame_team.columnconfigure(0, weight=1)

        self.team_logo = customtkinter.CTkButton(master=self.frame_team,
                                                image=ImageTk.PhotoImage(self.logo_img),
                                                text='',
                                                command=self.set_logo
                                                )

        self.team_logo.grid(row=0, column=0, sticky="new", pady=5, padx=5,)

        self.frame_team_name = customtkinter.CTkFrame(master=self.frame_team)
        self.frame_team_name.grid(row=1, column=0, pady=5, padx=5, sticky="new")
        self.frame_team_name.rowconfigure((0, 1, 2), weight=1)
        self.frame_team_name.columnconfigure(0, weight=1)

        # self.team_name_label = customtkinter.CTkLabel(master=self.frame_team_name,
        #                                               text="Название команды",
        #                                               height=20,
        #                                               corner_radius=5,  # <- custom corner radius
        #                                               fg_color=("white", "gray38")  # <- custom tuple-color
        #                                               )
        # self.team_name_label.grid(row=0, column=0, pady=5, padx=5, sticky="new")

        self.select_team_button = customtkinter.CTkLabel(master=self.frame_team_name,
                                                          text="Название команды",
                                                          height=20,
                                                          corner_radius=5,  # <- custom corner radius
                                                          fg_color=("white", "gray38")
                                                         )
        self.select_team_button.grid(row=0, column=0, pady=5, padx=5, sticky="new")

        self.team_name_entry_name = customtkinter.CTkEntry(master=self.frame_team_name,
                                                           textvariable=self.team_name,
                                                           text_font=("Arial", 25, ""),
                                                           justify=tkinter.CENTER
                                                           )
        self.team_name_entry_name.grid(row=1, column=0, pady=2, padx=2, sticky="new")

        self.team_name_entry_state = customtkinter.CTkEntry(master=self.frame_team_name,
                                                            textvariable=self.team_state,
                                                            text_font=("Arial", 25, ""),
                                                            justify=tkinter.CENTER
                                                            )
        self.team_name_entry_state.grid(row=2, column=0, pady=2, padx=2, sticky="new")

        # ============ frame_team_score =======
        self.frame_team_score = customtkinter.CTkFrame(master=self.frame_team)
        self.frame_team_score.grid(row=2, column=0, pady=5, padx=5, sticky="new")

        self.frame_team_score.rowconfigure((0, 1, 2), weight=1)
        self.frame_team_score.columnconfigure((0, 1, 2), weight=1)

        self.team_score_label = customtkinter.CTkLabel(master=self.frame_team_score, height=20,
                                                       text='Счёт',
                                                       text_font=("Arial", 25, ""),
                                                       corner_radius=5,  # <- custom corner radius
                                                       fg_color=("white", "gray38")  # <- custom tuple-color
                                                       )

        self.team_score_label.grid(row=0, column=0, columnspan=3, pady=5, padx=5, sticky="new")

        self.team_score_button_remove = customtkinter.CTkButton(master=self.frame_team_score,
                                                                command=self.remove_point,
                                                                text='-1',
                                                                text_font=("Arial", 15, "")
                                                                )
        self.team_score_button_remove.grid(row=1, column=0, pady=5, padx=5, sticky="new")

        self.team_score_button_reset = customtkinter.CTkButton(master=self.frame_team_score,
                                                               command=self.reset_point,
                                                               text='RESET',
                                                               text_font=("Arial", 15, "")
                                                               )
        self.team_score_button_reset.grid(row=2, column=0, pady=5, padx=5, sticky="new")

        self.team_score_entry = customtkinter.CTkEntry(master=self.frame_team_score,
                                                       textvariable=self.team_score,
                                                       text_font=("Arial", 50, ""),
                                                       justify='center',
                                                       validate='key',
                                                       state='disabled'
                                                       )
        self.team_score_entry.grid(row=1, column=1, rowspan=2, pady=5, padx=5, sticky="nsew")

        self.team_score_button_add = customtkinter.CTkButton(master=self.frame_team_score,
                                                             command=self.add_point,
                                                             text='+1',
                                                             text_font=("Arial", 20, "")
                                                             )
        self.team_score_button_add.grid(row=1, column=2, rowspan=2, pady=5, padx=5, sticky="nsew")

        self.window_teams = None

    def add_point(self):
        self.team_score_entry.after(0, self.team_score.set(self.team_score.get() + 1))

    def remove_point(self):
        self.team_score_entry.after(0, self.team_score.set(self.team_score.get() - 1))

    def reset_point(self):
        self.team_score_entry.after(0, self.team_score.set(0))

    def set_logo(self):
        global image
        self.data = tkinter.filedialog.askopenfile(filetypes=[('Image Files', '*.png')])
        # image = Image.open(self.data.name).resize((250, 250))

        self.logo_path = self.data.name

        self.logo_img = Image.open(self.logo_path).resize((250, 250))

        self.team_logo.destroy()
        self.team_logo = customtkinter.CTkButton(master=self.frame_team,
                                                 image=ImageTk.PhotoImage(self.logo_img),
                                                 text='',
                                                 command=self.set_logo
                                                 )
        self.team_logo.grid(row=0, column=0, sticky='nwe')

    def update_data(self, window_teams):
        self.selected = window_teams.table.selection()
        self.team_data = window_teams.table.item(self.selected[0]).get('values')
