import customtkinter
import tkinter
from decimal import Decimal


class Statistics(customtkinter.CTk):
    def __init__(self, master, row=0, column=0):
        list = ['Владение, %', 'Удары', 'Удары в створ', 'Угловые', 'Фолы', 'Желтые карточки', 'Красные карточки']
        self.static_frame = customtkinter.CTkFrame(master=master)
        self.static_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
        self.static_frame.columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.static_frame.grid(row=row, column=column, columnspan=3)
        self.timer_flag = False
        self.dict_1 = {}
        self.dict_2 = {}
        self.possession_1 = 0
        self.possession_2 = 0
        for i in list:
            self.dict_1.setdefault(i, tkinter.IntVar())
            self.dict_1.get(i).set(0)
            self.dict_2.setdefault(i, tkinter.IntVar())
            self.dict_2.get(i).set(0)

        self.label = customtkinter.CTkLabel(master=self.static_frame,
                                            text=f'{list[0]}',
                                            text_font=('Arials', 20, ''),
                                            height=20,
                                            corner_radius=5,  # <- custom corner radius
                                            fg_color=("white", "gray38"),  # <- custom tuple-color
                                            )
        self.label.grid(column=3, row=0, sticky='nsew', pady=2)

        self.entry_1 = customtkinter.CTkEntry(master=self.static_frame,
                                              textvariable=self.dict_1.get(list[0]),
                                              text_font=('Arials', 20, ''),
                                              justify=tkinter.CENTER,
                                              validate='key',
                                              state='disabled'
                                              )
        self.entry_1.grid(column=0, row=0, sticky='nsew', pady=2)

        self.entry_2 = customtkinter.CTkEntry(master=self.static_frame,
                                              textvariable=self.dict_2.get(list[0]),
                                              text_font=('Arials', 20, ''),
                                              justify=tkinter.CENTER,
                                              validate='key',
                                              state='disabled'
                                              )
        self.entry_2.grid(column=6, row=0, sticky='nsew', pady=2)

        self.radio_1 = customtkinter.CTkCheckBox(master=self.static_frame,
                                                    text='',
                                                 state='disabled')
        self.radio_1.grid(column=2, row=0, pady=2)
        self.radio_1.select()

        self.radio_2 = customtkinter.CTkCheckBox(master=self.static_frame,
                                                    text='',
                                                 state='disabled'
                                                )
        self.radio_2.grid(column=4, row=0, pady=2)
        # self.radio_2.select()




        for i in range(1, 7):
            self.label = customtkinter.CTkLabel(master=self.static_frame,
                                                text=f'{list[i]}',
                                                text_font=('Arials',20, ''),
                                                height=20,
                                                corner_radius=5,  # <- custom corner radius
                                                fg_color=("white", "gray38"),  # <- custom tuple-color
                                                )
            self.label.grid(column=3, row=i, sticky='nsew', pady=2)

            self.entry_11 = customtkinter.CTkEntry(master=self.static_frame,
                                                  textvariable=self.dict_1.get(list[i]),
                                                  text_font=('Arials',20, ''),
                                                  justify=tkinter.CENTER,
                                                  validate='key',
                                                  state='disabled'
                                                  )
            self.entry_11.grid(column=0, row=i, sticky='nsew', pady=2)

            self.entry_22 = customtkinter.CTkEntry(master=self.static_frame,
                                                  textvariable=self.dict_2.get(list[i]),
                                                  text_font=('Arials',20, ''),
                                                  justify=tkinter.CENTER,
                                                  validate='key',
                                                  state='disabled'
                                                  )
            self.entry_22.grid(column=6, row=i, sticky='nsew', pady=2)

            self.button_plus_1 = customtkinter.CTkButton(self.static_frame,
                                                         text='+',
                                                         text_font=('Arials',20, ''),
                                                         command=lambda i=i: (self.add_point(self.dict_1, list[i]))
                                                         )
            self.button_plus_1.grid(row=i, column=2)

            self.button_minus_1 = customtkinter.CTkButton(self.static_frame,
                                                         text='-',
                                                         text_font=('Arials',20, ''),
                                                         command=lambda i=i: (self.remove_point(self.dict_1, list[i]))
                                                          )
            self.button_minus_1.grid(row=i, column=1)

            self.button_plus_2 = customtkinter.CTkButton(self.static_frame,
                                                         text='+',
                                                         text_font=('Arials',20, ''),
                                                         command=lambda i=i: (self.add_point(self.dict_2, list[i]))
                                                         )
            self.button_plus_2.grid(row=i, column=4)

            self.button_minus_2 = customtkinter.CTkButton(self.static_frame,
                                                         text='-',
                                                         text_font=('Arials',20, ''),
                                                         command=lambda i=i: (self.remove_point(self.dict_2, list[i]))
                                                          )
            self.button_minus_2.grid(row=i, column=5)



    def add_point(self, dict, key):
        dict.get(key).set(dict.get(key).get()+1)

    def remove_point(self, dict, key):
        dict.get(key).set(dict.get(key).get()-1)

    def possess_1(self, rt):
        if self.radio_2.get():
            self.radio_2.deselect()
            self.entry_1.after(100, self.check)
        self.radio_1.select()

    def possess_2(self, rt):
        if self.radio_1.get() == 1:
            self.radio_1.deselect()
            self.entry_2.after(100, self.check)
        self.radio_2.select()

    def possess_3(self, rt):
        self.radio_1.deselect()
        self.radio_2.deselect()


    def check(self):
        if self.timer_flag:
            if self.radio_1.get() == 1:
                self.possession_1 += 1
                self.dict_1.get('Владение, %').set(Decimal(
                    self.possession_1 / (self.possession_1+self.possession_2)*100).quantize(int()))
                self.dict_2.get('Владение, %').set(Decimal(
                    self.possession_2 / (self.possession_1 + self.possession_2) * 100).quantize(int()))

            elif self.radio_2.get() == 1:
                self.possession_2 += 1
                self.dict_1.get('Владение, %').set(Decimal(
                    self.possession_1 / (self.possession_1 + self.possession_2) * 100).quantize(int()))
                self.dict_2.get('Владение, %').set(Decimal(
                    self.possession_2 / (self.possession_1+self.possession_2)*100).quantize(int()))

        self.static_frame.after(900, self.check)