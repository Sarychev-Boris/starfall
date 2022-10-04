import tkinter
import customtkinter
import tkinter
import customtkinter
import screeninfo
from PIL import Image, ImageTk
import os

PATH = os.path.dirname(os.path.realpath(__file__))

class Board(customtkinter.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        screen_2 = screeninfo.get_monitors()[1]

        self.geometry('%dx%d+%d+%d' % (screen_2.width, screen_2.height, self.winfo_screenwidth(), 0))
        self.overrideredirect(True)

        # ============ Связи с объектами main.py ============

        self.board_time = parent.timer.time
        self.add_board_time = self.parent.timer.add_time
        self.shown_time = self.board_time.get()
        self.label_info_text = parent.entry1_info_1

        self.team_1_name = parent.team_1.team_name
        self.team_1_state = parent.team_1.team_state
        self.team_1_score = parent.team_1.team_score

        self.team_2_name = parent.team_2.team_name
        self.team_2_state = parent.team_2.team_state
        self.team_2_score = parent.team_2.team_score

        self.half = parent.half.half_num

        # ============ Основной фрейм ============

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)


        self.label_info = customtkinter.CTkLabel(master=self,
                                                   text=parent.entry1_info_1.get(),
                                                   height=20,
                                                   text_font=('Arials', 65, ''),
                                                   corner_radius=5,  # <- custom corner radius
                                                   # fg_color=("white", "gray38"),  # <- custom tuple-color
                                                   justify=tkinter.LEFT)
        self.label_info.grid(column=0, row=0, sticky='nswe')

        # ============ Фрейм гербов + таймов ============

        self.frame_logo = customtkinter.CTkFrame(master=self,
                                                 fg_color=("white", "#212325"))
        self.frame_logo.grid(row=1, column=0, sticky='nsew')

        self.frame_logo.grid_columnconfigure((0, 1, 2), weight=1)
        self.frame_logo.grid_rowconfigure((0, 1), weight=1)

        self.team1_logo = customtkinter.CTkLabel(master=self.frame_logo,
                                                 image=parent.team_1.team_logo.image,
                                                 height=250,
                                                 width=250)
        self.team1_logo.grid(row=0, column=0, rowspan=2, sticky='nsew')

        self.half_label = customtkinter.CTkLabel(master=self.frame_logo,
                                                 text=parent.half.half_name.get(),
                                                 text_font=('Arials', 50, ''))
        self.half_label.grid(row=0, column=1)

        self.half_label_num = customtkinter.CTkLabel(master=self.frame_logo,
                                                     text=parent.half.half_num.get(),
                                                     text_font=('Arials', 50, ''))
        self.half_label_num.grid(row=1, column=1)

        self.team2_logo = customtkinter.CTkLabel(master=self.frame_logo,
                                                 height=250,
                                                 width=250,
                                                 image=parent.team_2.team_logo.image)
        self.team2_logo.grid(row=0, column=2, rowspan=2, sticky='nsew')

        # ============ Фрейм имен команд ============

        self.frame_team_name = customtkinter.CTkFrame(master=self,
                                                      fg_color=("white", "#212325")
                                                      )
        self.frame_team_name.grid(row=2, column=0, sticky='nswe')

        self.frame_team_name.rowconfigure((0, 1), weight=1)
        self.frame_team_name.columnconfigure((0, 1), weight=1)

        self.team1_name = customtkinter.CTkLabel(master=self.frame_team_name,
                                                 text=parent.team_1.team_name.get(),
                                                 text_font=('Arials', 50, ''),
                                                 width=400,
                                                 anchor="center")
        self.team1_name.grid(row=0, column=0, sticky='nsw', padx=40)

        self.team1_state = customtkinter.CTkLabel(master=self.frame_team_name,
                                                 text=parent.team_1.team_state.get(),
                                                 text_font=('Arials', 30, ''),
                                                 width=400,
                                                 anchor="center")
        self.team1_state.grid(row=1, column=0, sticky='nsw', padx=40)

        self.team2_name = customtkinter.CTkLabel(master=self.frame_team_name,
                                                 text=parent.team_2.team_name.get(),
                                                 text_font=('Arials', 50, ''),
                                                 width=400,
                                                 anchor="center")
        self.team2_name.grid(row=0, column=1, sticky='nse', padx=40)

        self.team2_state = customtkinter.CTkLabel(master=self.frame_team_name,
                                                 text=parent.team_2.team_state.get(),
                                                 text_font=('Arials', 30, ''),
                                                 width=400,
                                                 anchor="center")
        self.team2_state.grid(row=1, column=1, sticky='nse', padx=40)


        # ============ Фрейм счёта таймера ============

        self.frame_timer = customtkinter.CTkFrame(master=self,
                                                  fg_color=("white", "#212325")
                                                  )
        self.frame_timer.grid(row=3, column=0, sticky='nsew')

        self.frame_timer.rowconfigure((0, 1), weight=1)
        self.frame_timer.columnconfigure((0, 1, 2), weight=1)

        self.team1_score = customtkinter.CTkLabel(master=self.frame_timer,
                                                  text=parent.team_1.team_score.get(),
                                                  text_font=('Arials', 150, ''),
                                                  anchor="center",
                                                  # fg_color=("white", "gray38")
                                                  )
        self.team1_score.grid(row=0, column=0, rowspan=2, sticky='nesw')
        # self.team1_score.place(relx=0.5, rely=0.5, anchor='center')

        self.label = customtkinter.CTkLabel(master=self.frame_timer,
                                            text=parent.timer.time.get(),
                                            width=400,
                                            text_font=('Arials', 100, ''),
                                            anchor="center",
                                            corner_radius=5,  # <- custom corner radius
                                            # fg_color=("white", "gray38"),  # <- custom tuple-color
                                            )
        self.label.grid(row=0, column=1, sticky="nesw")
        self.label.after(10, self.update12)

        self.team2_score = customtkinter.CTkLabel(master=self.frame_timer,
                                                  text=parent.team_2.team_score.get(),
                                                  text_font=('Arials', 150, ''),
                                                  anchor="center",
                                                  # fg_color=("white", "gray38")
                                                  )
        self.team2_score.grid(row=0, column=2, rowspan=2, sticky='w')


    def update12(self):
        if self.parent.timer.show_flag and self.parent.timer.M == self.parent.timer.add_M:
            self.show_add_timer()
        else:
            self.label_info.configure(text=self.label_info_text.get())

            self.team1_name.configure(text=self.team_1_name.get())
            self.team1_state.configure(text=self.team_1_state.get())
            self.team1_score.configure(text=self.team_1_score.get())

            self.team2_name.configure(text=self.team_2_name.get())
            self.team2_state.configure(text=self.team_2_state.get())
            self.team2_score.configure(text=self.team_2_score.get())

            self.half_label_num.configure(text=self.half.get())

            self.label.configure(text=self.board_time.get())
            self.label.after(10, self.update12)

    def show_add_timer(self):
        self.label2 = customtkinter.CTkLabel(master=self.frame_timer,
                                            text=self.add_board_time.get(),
                                            #  text=self.a,
                                            width=400,
                                            text_font=('Arials', 50, ''),
                                            anchor="center",
                                            corner_radius=5,  # <- custom corner radius
                                            # fg_color=("white", "gray38"),  # <- custom tuple-color
                                            )
        self.label2.grid(row=1, column=1, sticky="nsew")
        self.label2.after(10, self.update13)

    def update13(self):
        self.label_info.configure(text=self.label_info_text.get())

        self.team1_name.configure(text=self.team_1_name.get())
        self.team1_state.configure(text=self.team_1_state.get())
        self.team1_score.configure(text=self.team_1_score.get())

        self.team2_name.configure(text=self.team_2_name.get())
        self.team2_state.configure(text=self.team_2_state.get())
        self.team2_score.configure(text=self.team_2_score.get())

        self.half_label_num.configure(text=self.half.get())

        self.label2.configure(text=self.add_board_time.get())
        self.label2.after(1000, self.update13)