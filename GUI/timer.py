import tkinter
import tkinter.messagebox
import customtkinter
import datetime



class Timer(customtkinter.CTk):
    def __init__(self, master, row=0, column=0):

        self.timer_flag = False
        self.add_timer_flag = False
        self.show_flag = False
        self.frozen_seconds = 0

        self.frame_time_timer = customtkinter.CTkFrame(master=master)
        self.frame_time_timer.grid(row=row, column=column, pady=5, padx=5, sticky="nsew")
        self.frame_time_timer.rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.frame_time_timer.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        self.time_timer_label = customtkinter.CTkLabel(master=self.frame_time_timer,
                                                       text="Время",
                                                       height=20,
                                                       anchor="w",
                                                       corner_radius=5,  # <- custom corner radius
                                                       fg_color=("white", "gray38"),  # <- custom tuple-color
                                                       justify=tkinter.LEFT)
        self.time_timer_label.grid(row=0, column=0, columnspan=6, pady=5, padx=5, sticky="nsew")

        self.time_timer_button_reset = customtkinter.CTkButton(master=self.frame_time_timer,
                                                               text="СБРОС",
                                                               height=20,
                                                               width=20,
                                                               command=self.time_reset)
        self.time_timer_button_reset.grid(row=0, column=5, pady=5, padx=5, sticky="sne")

        self.M = 0
        self.M2 = 0
        self.S = '00'
        self.S2 = '00'
        self.time = tkinter.StringVar()
        self.time.set(f'{self.M:02}:{self.S.zfill(2)}')

        self.add_time = tkinter.StringVar()
        self.add_time.set(f'{self.M2:02}:{self.S2.zfill(2)}')

        self.time_timer_entry1 = customtkinter.CTkEntry(master=self.frame_time_timer,
                                                        height=60,
                                                        justify='center',
                                                        text_font=("Arial", 50, ""),
                                                        textvariable=self.time,
                                                        )
        self.time_timer_entry1.grid(row=1, column=0, columnspan=6, pady=5, padx=5, sticky="nsew")

        self.time_timer_button_stop = customtkinter.CTkButton(master=self.frame_time_timer,
                                                               text="Стоп",
                                                               height=20,
                                                               width=40,
                                                               command=self.time_stop
                                                               )
        self.time_timer_button_stop.grid(row=2, column=0, columnspan=3, pady=5, padx=5, sticky="nsew")

        self.time_timer_button_start = customtkinter.CTkButton(master=self.frame_time_timer,
                                                              text="Старт",
                                                              command=self.time_start
                                                              )
        self.time_timer_button_start.grid(row=2, column=3, columnspan=4, pady=5, padx=5, sticky="nsew")

        self.set_add_time_entry = customtkinter.CTkEntry(master=self.frame_time_timer,
                                                         justify='left'
                                                         )
        self.set_add_time_entry.grid(row=3, column=3, pady=5, padx=5, sticky="nsew")
        self.set_add_time_entry.insert(0, '45')

        self.add_time_switch = customtkinter.CTkSwitch(master=self.frame_time_timer,
                                                       text=''
                                                       )
        self.add_time_switch.grid(row=3, column=5, pady=5, padx=5, sticky='nsew')

        self.radio_stop = customtkinter.CTkCheckBox(master=self.frame_time_timer,
                                                    text='')
        self.radio_stop.grid(column=4, row=3, pady=2, sticky='nsew')

        # self.add_time_switch2 = customtkinter.CTkSwitch(master=self.frame_time_timer,
        #                                                text=''
        #                                                )
        # self.add_time_switch2.grid(row=3, column=4, pady=5, padx=5, sticky='nsew')

        self.add_time_label = customtkinter.CTkLabel(master=self.frame_time_timer,
                                                       text="Доп. время после минуты:",
                                                       height=20,
                                                       width=40,
                                                       corner_radius=5,  # <- custom corner radius
                                                       fg_color=("white", "gray38"),  # <- custom tuple-color
                                                       justify=tkinter.LEFT)
        self.add_time_label.grid(row=3, column=0, columnspan=3, pady=5, padx=5, sticky="nsew")

        self.time_timer_entry2 = customtkinter.CTkEntry(master=self.frame_time_timer,
                                                        height=30,
                                                        justify='center',
                                                        text_font=("Arial", 25, ""),
                                                        textvariable=self.add_time,
                                                        )
        self.time_timer_entry2.grid(row=4, column=0, columnspan=5, pady=5, padx=5, sticky="nsew")

        self.add_time_button = customtkinter.CTkButton(master=self.frame_time_timer,
                                                       text='Старт/Стоп',
                                                       command=self.change_add_flag
                                                       # width=20
                                                       )
        self.add_time_button.grid(row=4, column=5, pady=5, padx=5, sticky="nsew")

    def get_current_seconds(self):
        if self.timer_flag:
            # self.current = datetime.datetime.now().strftime('%H:%M:%S:%f')
            self.current = datetime.datetime.now().strftime('%H:%M:%S')
            b = [int(_) for _ in self.current.split(':')]
            # self.current_seconds = b[0]*3600 + b[1]*60 + b[2] + b[3]/1000000
            self.current_seconds = b[0] * 3600 + b[1] * 60 + b[2]

            if float(self.S) >= 60:
                self.start_seconds = self.current_seconds
                self.S = '00'
                self.M += 1
                self.frozen_seconds = 0
            else:
                # self.S = '%.2f' % (self.current_seconds-self.start_seconds+self.frozen_seconds)
                self.S = f'{int(self.current_seconds - self.start_seconds + self.frozen_seconds)}'
            # self.time.set('%.2f'%(self.current_seconds-self.start_seconds+self.frozen_seconds))
            self.time.set(f'{self.M:02}:{self.S.zfill(2)}')
            self.time_timer_entry1.after(10, self.get_current_seconds)
        if self.M == self.add_M and self.add_time_switch.get():
            self.time_stop()
            self.add_timer_flag = True
            self.show_flag = True
            self.start_add_timer()

    def time_start(self):
        self.add_M = int(self.set_add_time_entry.get())
        if self.timer_flag is False:
            self.timer_flag = True
            self.M = int(self.time_timer_entry1.get().split(':')[0])
            self.frozen_seconds = float(self.time_timer_entry1.get().split(':')[1])
            self.start = datetime.datetime.now().strftime('%H:%M:%S')
            self.a = [int(_) for _ in self.start.split(':')]
            self.start_seconds = self.a[0]*3600+self.a[1]*60+self.a[2]
            self.get_current_seconds()

    def time_stop(self):
        self.timer_flag = False
        self.frozen_seconds = self.current_seconds-self.start_seconds+self.frozen_seconds

    def time_reset(self):
        self.timer_flag = False
        self.add_timer_flag = False
        self.M = 0
        self.M2 = 0
        self.frozen_seconds = 0
        self.current_seconds = 0
        self.start_seconds = 0
        self.time.set('00:00')
        self.add_time.set('00:00')

    def start_add_timer(self):
        if self.add_timer_flag:
            self.current = datetime.datetime.now().strftime('%H:%M:%S')
            b = [int(_) for _ in self.current.split(':')]
            # self.current_seconds = b[0]*3600 + b[1]*60 + b[2] + b[3]/1000000
            self.current_seconds = b[0] * 3600 + b[1] * 60 + b[2]
            if float(self.S) >= 60:
                self.start_seconds = self.current_seconds
                self.S = '00'
                self.M2 += 1
                self.frozen_seconds = 0
            else:
                # self.S = '%.2f' % (self.current_seconds-self.start_seconds+self.frozen_seconds)
                self.S = f'{int(self.current_seconds - self.start_seconds + self.frozen_seconds)}'
            self.add_time.set(f'{self.M2:02}:{self.S.zfill(2)}')
        self.time_timer_entry2.after(10, self.start_add_timer)

    def change_add_flag(self):
        if self.add_timer_flag:
            self.add_timer_flag = False
            self.frozen_seconds = self.current_seconds - self.start_seconds + self.frozen_seconds
        else:
            self.add_timer_flag = True
            self.start = datetime.datetime.now().strftime('%H:%M:%S')
            self.a = [int(_) for _ in self.start.split(':')]
            self.start_seconds = self.a[0] * 3600 + self.a[1] * 60 + self.a[2]
            self.frozen_seconds = float(self.time_timer_entry2.get().split(':')[1])

