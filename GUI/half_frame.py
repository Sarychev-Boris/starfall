import tkinter
import tkinter.messagebox
import customtkinter


class Half(customtkinter.CTk):
    def __init__(self, master, row=0, column=0):

        self.half_name = tkinter.StringVar()
        self.half_name.set('Тайм')

        self.half_num = tkinter.IntVar()
        self.half_num.set(0)

        self.frame_half = customtkinter.CTkFrame(master=master)
        self.frame_half.grid(row=row, column=column, pady=5, padx=5, sticky="nsew")
        self.frame_half.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_half.columnconfigure((0, 1, 2), weight=1)

        self.half_label = customtkinter.CTkLabel(master=self.frame_half,
                                                      height=20,
                                                      text='Отрезок времени',
                                                      text_font=("Arial", 25, ""),
                                                      corner_radius=5,  # <- custom corner radius
                                                      fg_color=("white", "gray38"),  # <- custom tuple-color
                                                      justify=tkinter.LEFT)
        self.half_label.grid(row=0, column=0, columnspan=3, pady=5, padx=5, sticky="nsew")

        self.half_entry_name = customtkinter.CTkEntry(master=self.frame_half,
                                                      textvariable=self.half_name,
                                                      text_font=("Arial", 25, ""),
                                                      justify=tkinter.CENTER
                                                        )
        self.half_entry_name.grid(row=1, column=0, columnspan=3, pady=5, padx=5, sticky="nsew")

        self.half_button_remove = customtkinter.CTkButton(master=self.frame_half,
                                                          command=self.remove_point,
                                                          text='-1',
                                                          text_font=("Arial", 20, ""),
                                                          height=60)
        self.half_button_remove.grid(row=2, column=0, rowspan=2, pady=5, padx=5, sticky="nsew")

        self.half_entry_num = customtkinter.CTkEntry(master=self.frame_half,
                                                     height=60,
                                                     textvariable=self.half_num,
                                                     text_font=("Arial", 50, ""),
                                                     justify=tkinter.CENTER,
                                                     state='disabled'
                                                     )
        self.half_entry_num.grid(row=2, column=1, rowspan=2, pady=5, padx=5, sticky="nsew")

        self.half_button_add = customtkinter.CTkButton(master=self.frame_half,
                                                       height=60,
                                                       command=self.add_point,
                                                       text='+1',
                                                       text_font=("Arial", 20, "")
                                                       )
        self.half_button_add.grid(row=2, column=2, rowspan=2, pady=5, padx=5, sticky="nsew")

    def add_point(self):
        self.half_entry_num.after(0, self.half_num.set(self.half_num.get() + 1))

    def remove_point(self):
        self.half_entry_num.after(0, self.half_num.set(self.half_num.get() - 1))