import tkinter
import customtkinter
import screeninfo
import os
import configparser
from PIL import Image, ImageTk


#
class Board(customtkinter.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        # Получаем разрешение второго монитора
        screen_2 = screeninfo.get_monitors()[1]

        PATH = os.path.dirname(os.path.realpath(__file__))
        self.config = configparser.ConfigParser()  # создаём объекта парсера
        self.config.read("config.ini")  # читаем конфиг

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
        self.team_1_logo = Image.open(parent.team_1.logo_path).resize((int(self.config["board"]["width"]), (int(self.config["board"]["height"]))))

        self.team_2_name = parent.team_2.team_name
        self.team_2_state = parent.team_2.team_state
        self.team_2_score = parent.team_2.team_score
        self.team_2_logo = Image.open(parent.team_2.logo_path).resize((int(self.config["board"]["width"]), (int(self.config["board"]["height"]))))

        self.half = parent.half.half_num

        # ============ Основной фрейм ============

        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0, 1), weight=1)


        self.label_info = customtkinter.CTkLabel(master=self,
                                                   text=parent.entry1_info_1.get(),
                                                   height=20,
                                                   text_font=('Arials', (int(self.config["board"]["title"])), ''),
                                                   corner_radius=5,  # <- custom corner radius
                                                   # fg_color=("white", "gray38"),  # <- custom tuple-color
                                                   justify=tkinter.LEFT)
        self.label_info.grid(column=0, row=0, columnspan=3, sticky=self.config["board"]["title_sticky"])

        # ============ Фрейм гербов + таймов ============


        self.frame_team_1 = customtkinter.CTkFrame(master=self,
                                                   fg_color=("white", "#212325"))
        self.frame_team_1.grid(row=1, column=0, sticky=self.config["board"]["team1_sticky"])

        self.frame_team_1.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_team_1.columnconfigure(0, weight=1)


        self.team1_logo = customtkinter.CTkButton(master=self.frame_team_1,
                                                  image=ImageTk.PhotoImage(self.team_1_logo),
                                                  text='',
                                                  state='diable',
                                                  fg_color=("white", "#212325")
                                                 )
        self.team1_logo.grid(row=0, column=0, sticky=self.config["board"]["team1_sticky"])

        self.team1_name = customtkinter.CTkLabel(master=self.frame_team_1,
                                                 text=parent.team_1.team_name.get(),
                                                 text_font=('Arials', (int(self.config["board"]["team1_name"])), ''),
                                                 anchor="center")
        self.team1_name.grid(row=1, column=0, sticky=self.config["board"]["team1_sticky"])

        self.team1_state = customtkinter.CTkLabel(master=self.frame_team_1,
                                                 text=parent.team_1.team_state.get(),
                                                 text_font=('Arials', (int(self.config["board"]["team1_state"])), ''),
                                                 anchor="center")
        self.team1_state.grid(row=2, column=0, sticky=self.config["board"]["team1_sticky"])

        self.team1_score = customtkinter.CTkLabel(master=self.frame_team_1,
                                                  text=parent.team_1.team_score.get(),
                                                  text_font=('Arials', (int(self.config["board"]["team1_score"])), ''),
                                                  anchor="center",
                                                  # fg_color=("white", "gray38")
                                                  )
        self.team1_score.grid(row=3, column=0, sticky=self.config["board"]["team1_sticky"])



        self.frame_time = customtkinter.CTkFrame(master=self,
                                                   fg_color=("white", "#212325"))
        self.frame_time.grid(row=1, column=1, sticky=self.config["board"]["timer_sticky"])
        self.frame_time.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_time.columnconfigure(0, weight=1)

        self.half_label = customtkinter.CTkLabel(master=self.frame_time,
                                                 text=parent.half.half_name.get(),
                                                 text_font=('Arials', (int(self.config["board"]["half"])), ''))
        self.half_label.grid(row=0, column=0, sticky=self.config["board"]["timer_sticky"])

        self.half_label_num = customtkinter.CTkLabel(master=self.frame_time,
                                                     text=parent.half.half_num.get(),
                                                     text_font=('Arials', (int(self.config["board"]["half_num"])), ''))
        self.half_label_num.grid(row=1, column=0, sticky=self.config["board"]["timer_sticky"])

        self.label = customtkinter.CTkLabel(master=self.frame_time,
                                            text=parent.timer.time.get(),
                                            text_font=('Arials', (int(self.config["board"]["timer"])), ''),
                                            anchor="center",
                                            corner_radius=5,  # <- custom corner radius
                                            # fg_color=("white", "gray38"),  # <- custom tuple-color
                                            )
        self.label.grid(row=2, column=0, sticky=self.config["board"]["timer_sticky"])
        self.label.after(10, self.update12)


        self.frame_team_2 = customtkinter.CTkFrame(master=self,
                                                   fg_color=("white", "#212325"))
        self.frame_team_2.grid(row=1, column=2, sticky=self.config["board"]["team2_sticky"])

        self.frame_team_2.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_team_2.columnconfigure(0, weight=1)

        self.team2_logo = customtkinter.CTkButton(master=self.frame_team_2,
                                                  image=ImageTk.PhotoImage(self.team_2_logo),
                                                  state='disabled',
                                                  text='',
                                                  fg_color=("white", "#212325")
                                                  )
        self.team2_logo.grid(row=0, column=0, sticky=self.config["board"]["team2_sticky"])

        self.team2_name = customtkinter.CTkLabel(master=self.frame_team_2,
                                                 text=parent.team_2.team_name.get(),
                                                 text_font=('Arials', (int(self.config["board"]["team2_name"])), ''),
                                                 anchor="center")
        self.team2_name.grid(row=1, column=0, sticky=self.config["board"]["team2_sticky"])

        self.team2_state = customtkinter.CTkLabel(master=self.frame_team_2,
                                                  text=parent.team_2.team_state.get(),
                                                  text_font=('Arials', (int(self.config["board"]["team2_state"])), ''),
                                                  anchor="center")
        self.team2_state.grid(row=2, column=0, sticky=self.config["board"]["team2_sticky"])

        self.team2_score = customtkinter.CTkLabel(master=self.frame_team_2,
                                                  text=parent.team_2.team_score.get(),
                                                  text_font=('Arials', (int(self.config["board"]["team2_score"])), ''),
                                                  anchor="center",
                                                  # fg_color=("white", "gray38")
                                                  )
        self.team2_score.grid(row=3, column=0, sticky=self.config["board"]["team2_sticky"])

    # бесконечный цикл для постоянного обновления данных
    def update12(self):
        if self.parent.timer.show_flag and self.parent.timer.M == self.parent.timer.add_M:
            self.label.configure(text=self.board_time.get())
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
            self.label.after(500, self.update12)

    # Если включен переключатель для доп.таймера - включение другой функции обновления
    def show_add_timer(self):
        self.label2 = customtkinter.CTkLabel(master=self.frame_time,
                                            text=self.add_board_time.get(),
                                            #  text=self.a,
                                            width=400,
                                            text_font=('Arials', (int(self.config["board"]["add_timer"])), ''),
                                            anchor="center",
                                            corner_radius=5,  # <- custom corner radius
                                            # fg_color=("white", "gray38"),  # <- custom tuple-color
                                            )
        self.label2.grid(row=3, column=0, sticky="nsew")
        self.label2.after(500, self.update13)

    # Переопределить функцию обновления с назначением обновляемого таймера - дублируемый код
    def update13(self):
        if self.parent.timer.add_time_switch.get():
            self.label_info.configure(text=self.label_info_text.get())

            self.team1_name.configure(text=self.team_1_name.get())
            self.team1_state.configure(text=self.team_1_state.get())
            self.team1_score.configure(text=self.team_1_score.get())

            self.team2_name.configure(text=self.team_2_name.get())
            self.team2_state.configure(text=self.team_2_state.get())
            self.team2_score.configure(text=self.team_2_score.get())

            self.half_label_num.configure(text=self.half.get())

            self.label2.configure(text=self.add_board_time.get())
            self.label2.after(500, self.update13)
        else:
            self.label2.destroy()
            self.parent.timer.show_flag = False
            self.label.after(500, self.update12)