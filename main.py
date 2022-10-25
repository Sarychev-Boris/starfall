import datetime
import tkinter
import tkinter.messagebox
import customtkinter
from GUI.timer import Timer
from GUI.board import Board
from GUI.intro import Intro
from GUI.teams import TeamsTable, TeamSelect
from GUI.team_frame import TeamFrame
from GUI.statistics import Statistics
from GUI.half_frame import Half
from GUI.event import EventTable
from GUI.meeting import MeetingTable
from SQL.DB import create_db
from GUI.statistics_toplevel import StatTopLevel
import configparser
import sqlite3

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):

    WIDTH = 1280
    HEIGHT = 1024
    def __init__(self):
        super().__init__()

        self.title("Starfall.py")
        self.minsize(App.WIDTH, App.HEIGHT)
        # Приложение плохо ведет себя при растягивании, лучше сразу пускать в полный экран
        self.state('zoomed')

        # Для использования в функциях за пределами __init__
        self.conn = sqlite3.connect('Arena.db')
        self.cur = self.conn.cursor()
        # Меняется при назначении турнира
        self.eventid = None

        # Вытягивается для КД жизни окна состава команд
        self.config = configparser.ConfigParser()  # создаём объекта парсера
        self.config.read("config.ini")  # читаем конфиг

        # ============ create frames ============

        # configure grid layout (3x1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        # Временная заглушка - заменить на панель с возможностью скрыть правый фрейм
        self.frame_center = customtkinter.CTkFrame(master=self, width=5,
                                                 corner_radius=5)
        self.frame_center.grid(row=0, column=1, sticky="e", padx=2)

        self.frame_right = customtkinter.CTkFrame(master=self, width=400,
                                                 corner_radius=5)
        self.frame_right.grid(row=0, column=2, sticky="nswe")

        # ============ frame_left ============
        self.frame_left.rowconfigure(0, weight=1)
        self.frame_left.rowconfigure(1, weight=30)
        self.frame_left.columnconfigure(0, weight=1)

        # ============ frame_info ============
        # Для заголовка табло и названия турнира
        self.frame_info = customtkinter.CTkFrame(master=self.frame_left)
        self.frame_info.grid(row=0, column=0, pady=20, padx=20, sticky="new")

        self.frame_info.rowconfigure((0, 1, 2), weight=1)
        self.frame_info.columnconfigure(0, weight=40)
        self.frame_info.columnconfigure(1, weight=1)



        self.label_entry_1_text = tkinter.StringVar()
        self.label_entry_1_text.set("Заголовок табло")
        self.label_info_1 = customtkinter.CTkLabel(master=self.frame_info,
                                                   text="Заголовок табло",
                                                   height=20,
                                                   corner_radius=5,  # <- custom corner radius
                                                   fg_color=("white", "gray38"),  # <- custom tuple-color
                                                   justify=tkinter.LEFT)

        self.label_info_1.grid(column=0, row=0, columnspan=2, sticky="nwe", padx=5, pady=5)

        self.entry1_info_1 = customtkinter.CTkEntry(master=self.frame_info,
                                                    placeholder_text="Заголовок матча")
        self.entry1_info_1.insert(0, 'Заголовок матча')
        self.entry1_info_1.grid(column=0, row=1, columnspan=2, sticky="nwe", padx=5, pady=5)


        self.event_info = customtkinter.CTkEntry(master=self.frame_info,
                                                 placeholder_text = 'Турнир не выбран'
                                                 )

        self.event_info.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)


        # ============ frame_game ============
        self.frame_game = customtkinter.CTkFrame(master=self.frame_left)
        self.frame_game.grid(row=1, column=0, pady=20, padx=20, sticky="nsew")
        self.frame_game.rowconfigure((0, 1), weight=1)
        self.frame_game.columnconfigure((0, 1, 2), weight=1)

        # Создание экземпляров TeamFrame и StatsFrame - заменить названия классов

        self.team_1 = TeamFrame(master=self.frame_game)
        self.team_2 = TeamFrame(master=self.frame_game, row=0, column=2)
        self.statistics = Statistics(self.frame_game, row=1, column=0)

        # Бинд горячих клавиш для назначения флагов владения мячом
        self.bind("<Control-Key-o>", self.statistics.possess_1)
        self.bind("<Control-Key-p>", self.statistics.possess_2)
        self.bind("<Control-Key-[>", self.statistics.possess_3)

        # Функция проверки активных флагов и работы таймера - изменить функцию
        # Должна принимать флаг работы таймера, а не обращаться к родителю, как в данном случае
        self.statistics.check()

        # ============ frame_time ============
        # Шаблоны под объекты класса HalfFrame и TimerFrame - нагружают интерфейс
        # Требуется удалить и переназначить master для используемых фреймов
        self.frame_time = customtkinter.CTkFrame(master=self.frame_game)
        self.frame_time.grid(row=0, column=1, pady=15, padx=15, sticky="new")
        self.frame_time.rowconfigure((0, 1), weight=1)
        self.frame_time.columnconfigure(0, weight=1)

        # ============ frame_time_half ============

        self.frame_time_half = customtkinter.CTkFrame(master=self.frame_time)
        self.frame_time_half.grid(row=0, column=0, pady=5, padx=5, sticky="nsew")
        self.frame_time_half.rowconfigure((0, 1), weight=1)
        self.frame_time_half.columnconfigure((0), weight=1)

        self.half = Half(self.frame_time_half, 0, 0)

        # ============ frame_time_timer ============

        self.timer = Timer(self.frame_time, 1, 0)


        # ============ frame_right ============

        # Много одинаковых кнопок и много функций - выделить в отдельный файл + использовать цикл

        self.board_button1 = customtkinter.CTkButton(master=self.frame_right,
                                                          text="Показать табло",
                                                          command=self.show_board
                                                          )
        self.board_button1.grid(row=0, column=0, sticky="nsew", pady=5)

        self.board_button2 = customtkinter.CTkButton(master=self.frame_right,
                                                          text="Скрыть табло",
                                                          command=self.hide_board
                                                          )
        self.board_button2.grid(row=1, column=0, sticky="nsew", pady=5)


        self.board_button3 = customtkinter.CTkButton(master=self.frame_right,
                                                          text="Просмотр команд",
                                                          command=self.show_teams
                                                          )
        self.board_button3.grid(row=3, column=0, sticky="nsew", pady=5)

        self.board_button4 = customtkinter.CTkButton(master=self.frame_right,
                                                          text="Просмотр турниров",
                                                          command=self.show_events
                                                          )
        self.board_button4.grid(row=4, column=0, sticky="nsew", pady=5)

        self.board_button5 = customtkinter.CTkButton(master=self.frame_right,
                                                          text="Назначить команду 1",
                                                          command=self.select_team_1
                                                          )
        self.board_button5.grid(row=5, column=0, sticky="nsew", pady=5)

        self.board_button6 = customtkinter.CTkButton(master=self.frame_right,
                                                          text="Назначить команду 2",
                                                          command=self.select_team_2
                                                          )
        self.board_button6.grid(row=6, column=0, sticky="nsew", pady=5)

        self.board_button7 = customtkinter.CTkButton(master=self.frame_right,
                                                          text="Демонстрация команд",
                                                          command=self.start_intro
                                                          )
        self.board_button7.grid(row=7, column=0, sticky="nsew", pady=5)

        self.board_button8 = customtkinter.CTkButton(master=self.frame_right,
                                                          text="Скрыть демонстрацию команд",
                                                          command=self.stop_intro
                                                          )
        self.board_button8.grid(row=8, column=0, sticky="nsew", pady=5)

        self.board_button9 = customtkinter.CTkButton(master=self.frame_right,
                                                          text="Демонстрация статистики",
                                                          command=self.show_stats
                                                          )
        self.board_button9.grid(row=9, column=0, sticky="nsew", pady=5)

        self.board_button10 = customtkinter.CTkButton(master=self.frame_right,
                                                          text="Скрыть статистику",
                                                          command=self.hide_stats
                                                          )
        self.board_button10.grid(row=10, column=0, sticky="nsew", pady=5)

        self.board_button11 = customtkinter.CTkButton(master=self.frame_right,
                                                          text="Просмотр встреч",
                                                          command=self.show_meetings
                                                          )
        self.board_button11.grid(row=11, column=0, sticky="nsew", pady=5)

        self.board_button12 = customtkinter.CTkButton(master=self.frame_right,
                                                          text="Сохранить результат",
                                                          command=self.save_meeting
                                                          )
        self.board_button12.grid(row=12, column=0, sticky="nsew", pady=5)

        # Для использования в функции демонстрации составов команд - назначить более понятное название
        self.show_flag = False

        # Для проверки существования окон
        # Требуется расширить обработку исключений для случаев, когда команды не назначены и производится попытка
        # запуска некоторых из окон
        self.window = None
        self.window_teams = None
        self.window_events = None
        self.window_teams_select = None
        self.window_intro1 = None
        self.window_intro2 = None
        self.window_stats = None
        self.window_meetings = None

    # Много одинаковых функций - пересобрать в одну
    # Повторяющиеся окна таблиц - собрать в общий класс с наследованием под таблицу нужного элемента

    def show_meetings(self):
        if self.window_meetings == None or tkinter.Toplevel.winfo_exists(self.window_meetings) == 0:
            self.window_meetings = MeetingTable(self)

    # Не включится без второго дислпея и выбранных команд
    # Стартовая функция для запуска рекурсии
    def start_intro(self):
        if self.team_1.teamid:
            self.show_flag = True
            self.label_info_1.after(0, self.show_intro_1)

    # Прекращает рекурсию
    def stop_intro(self):
        self.show_flag = False
        try:
            self.label_info_1.after(0, self.window_intro1.destroy)
            self.label_info_1.after(0, self.window_intro2.destroy)
        except AttributeError:
            pass

    # Собрать в одну функцию - дублирующийся код
    def show_intro_1(self):

        if self.show_flag is False:
            return
        if self.window_intro1 == None:
            self.window_intro1 = Intro(self, self.team_1.teamid)
            self.label_info_1.after(int(self.config["intro"]["CD"]), self.show_intro_2)

        else:
            self.label_info_1.after(0, self.window_intro1.destroy)
            self.window_intro1 = Intro(self, self.team_1.teamid)
            self.label_info_1.after(int(self.config["intro"]["CD"]), self.show_intro_2)

    def show_intro_2(self):
        if self.show_flag is False:
            return
        if self.window_intro2 == None:
            self.window_intro2 = Intro(self, self.team_2.teamid)
            self.label_info_1.after(int(self.config["intro"]["CD"]), self.show_intro_1)

        else:
            self.label_info_1.after(0, self.window_intro2.destroy)
            self.window_intro2 = Intro(self, self.team_2.teamid)
            self.label_info_1.after(int(self.config["intro"]["CD"]), self.show_intro_1)




    def show_stats(self):
        if self.window_stats == None or tkinter.Toplevel.winfo_exists(self.window_stats) == 0:
            self.window_stats = StatTopLevel(self)

    def hide_stats(self):
        try:
            self.window_stats.destroy()   # Переделать под withdraw для отображения окна предпросмотра
        except AttributeError:
            pass

    def show_board(self):
        if self.window == None or tkinter.Toplevel.winfo_exists(self.window) == 0:
            self.window = Board(self)

    def hide_board(self):
        try:
            self.window.destroy()   # Переделать под withdraw для отображения окна предпросмотра
        except AttributeError:
            pass

    def show_teams(self):
        if self.window_teams == None or tkinter.Toplevel.winfo_exists(self.window_teams) == 0:
            self.window_teams = TeamsTable(self, None)
            self.window_teams.table.bind("<Double-1>", self.window_teams.team_settings)

    def show_events(self):
        if self.window_events == None or tkinter.Toplevel.winfo_exists(self.window_events) == 0:
            self.window_events = EventTable(self)

    def select_team_1(self):
        if self.window_teams_select == None or tkinter.Toplevel.winfo_exists(self.window_teams_select) == 0:
            self.window_teams_select = TeamSelect(self, self.eventid, self.team_1)

    def select_team_2(self):
        if self.window_teams_select == None or tkinter.Toplevel.winfo_exists(self.window_teams_select) == 0:
            self.window_teams_select = TeamSelect(self, self.eventid, self.team_2)

    # Для проверки работы таймера - без включенного таймера владение не считает

    def change_flags(self):
        if self.timer.timer_flag:
            self.statistics.timer_flag = True
        else:
            self.statistics.timer_flag = False
        self.after(1000, self.change_flags)


    # Страшна функция сохранения результата встречи
    # Вставить проверку на выбор турнира, функция работает только когда турнир назначен
    def save_meeting(self):

        # Создание новой записи в БД
        self.cur.execute(f"""INSERT INTO meeting(teamid_1, teamid_2, eventid, date) 
                             VALUES ('{self.team_1.teamid}', '{self.team_2.teamid}', '{self.eventid}',
                              '{datetime.date.today()}');
                          """)
        self.conn.commit()
        # Выделить отдельный класс team, назначить ему функцию получения статистики
        # Получение кортежей статистики
        self.team_1_result = self.cur.execute(f"""SELECT * from team_result WHERE teamid = '{self.team_1.teamid}'
                                                  AND  eventid = '{self.eventid}';""").fetchone()

        self.team_2_result = self.cur.execute(f"""SELECT * from team_result WHERE teamid = '{self.team_2.teamid}'
                                                  AND  eventid = '{self.eventid}';""").fetchone()

        # Сразу получаем ID встречи для создания записи со статистикой
        # Встречу выделить в отдельный класс с функцией добавления в нее результата
        meeting_id = self.cur.execute(f"""SELECT meetingid FROM meeting WHERE teamid_1 = {self.team_1.teamid} 
                                          AND teamid_1 = '{self.team_1.teamid}'
                                          AND teamid_2 = '{self.team_2.teamid}'
                                          AND eventid = '{self.eventid}'
                                          AND date = '{datetime.date.today()}';
                                        """).fetchone()[0]


        self.cur.execute(f"""INSERT INTO meeting_result(meetingid, teamid, score, win, lose, draw, possession, kicks,
                                                        gates, foul, yellow, red)
                             VALUES (
                                    '{meeting_id}', '{self.team_1.teamid}', '{self.team_1.team_score.get()}',
                                    '{0}', '{0}', '{0}',
                                    '{self.statistics.dict_1['Владение, %'].get()}', '{self.statistics.dict_1['Удары'].get()}',
                                     '{self.statistics.dict_1['Удары в створ'].get()}',
                                    '{self.statistics.dict_1['Фолы'].get()}', '{self.statistics.dict_1['Желтые карточки'].get()}',
                                     '{self.statistics.dict_1['Красные карточки'].get()}');
                          """)
        self.conn.commit()

        self.cur.execute(f"""INSERT INTO meeting_result(meetingid, teamid, score, win, lose, draw, possession, kicks,
                                                        gates, foul, yellow, red)
                             VALUES (
                                    '{meeting_id}', '{self.team_2.teamid}', '{self.team_2.team_score.get()}',
                                    '{0}', '{0}', '{0}',
                                    '{self.statistics.dict_2['Владение, %'].get()}', '{self.statistics.dict_2['Удары'].get()}',
                                     '{self.statistics.dict_2['Удары в створ'].get()}',
                                    '{self.statistics.dict_2['Фолы'].get()}', '{self.statistics.dict_2['Желтые карточки'].get()}',
                                     '{self.statistics.dict_2['Красные карточки'].get()}');
                          """)
        self.conn.commit()
        # Обновление статистик команд в выбранном турнире по результатам встречи
        if self.team_1.team_score.get() > self.team_2.team_score.get():
            self.cur.execute(f"""UPDATE team_result
                                 SET win = '{self.team_1_result[2]+1}',
                                     points = '{self.team_1_result[6]+3}'
                                 WHERE teamid = '{self.team_1.teamid}' AND eventid = '{self.eventid}';
                                """)
            self.conn.commit()
            self.cur.execute(f"""UPDATE team_result
                                 SET lose = '{self.team_2_result[4]+1}'
                                 WHERE teamid = '{self.team_2.teamid}' AND eventid = '{self.eventid}';
                                """)
            self.conn.commit()
            self.cur.execute(f"""UPDATE meeting_result
                                 SET lose = '1'
                                 WHERE teamid = '{self.team_2.teamid}' AND meetingid = '{meeting_id}';
                                """)
            self.conn.commit()
            self.cur.execute(f"""UPDATE meeting_result
                                 SET win = '1'
                                 WHERE teamid = '{self.team_1.teamid}' AND meetingid = '{meeting_id}';
                                """)
            self.conn.commit()
        elif self.team_1.team_score.get() == self.team_2.team_score.get():
            self.cur.execute(f"""UPDATE team_result
                                 SET draw = '{self.team_1_result[3]+1}',
                                     points = '{self.team_1_result[6]+1}'
                                 WHERE teamid = '{self.team_1.teamid}' AND eventid = '{self.eventid}';
                                """)
            self.conn.commit()
            self.cur.execute(f"""UPDATE team_result
                                 SET draw = '{self.team_2_result[3]+1}',
                                     points = '{self.team_2_result[6]+1}'
                                 WHERE teamid = '{self.team_2.teamid}' AND eventid = '{self.eventid}';
                                """)
            self.conn.commit()
            self.cur.execute(f"""UPDATE meeting_result
                                 SET draw = '1'
                                 WHERE teamid = '{self.team_2.teamid}' AND meetingid = '{meeting_id}';
                                """)
            self.conn.commit()
            self.cur.execute(f"""UPDATE meeting_result
                                 SET draw = '1'
                                 WHERE teamid = '{self.team_1.teamid}' AND meetingid = '{meeting_id}';
                                """)
            self.conn.commit()
        else:
            self.cur.execute(f"""UPDATE team_result
                                 SET win = '{self.team_2_result[2]+1}',
                                     points = '{self.team_2_result[6]+3}'
                                 WHERE teamid = '{self.team_2.teamid}' AND eventid = '{self.eventid}';
                                """)
            self.conn.commit()
            self.cur.execute(f"""UPDATE team_result
                                 SET lose = '{self.team_1_result[4]+1}'
                                 WHERE teamid = '{self.team_1.teamid}' AND eventid = '{self.eventid}';
                                """)
            self.conn.commit()
            self.cur.execute(f"""UPDATE meeting_result
                                 SET win = '1'
                                 WHERE teamid = '{self.team_2.teamid}' AND meetingid = '{meeting_id}';
                                """)
            self.conn.commit()
            self.cur.execute(f"""UPDATE meeting_result
                                 SET lose = '1'
                                 WHERE teamid = '{self.team_1.teamid}' AND meetingid = '{meeting_id}';
                                """)
            self.conn.commit()
        # Получение списка всех команд, участвующих в турнире [(ID команды, очки команды), (...), ...]
        team_list = self.cur.execute(
            f"""SELECT teamid, points FROM team_result WHERE eventid = {self.eventid}""").fetchall()


        global sorted
        # Получение сортированного по количеству очков списка
        sorted = sorted(team_list, key = lambda tuple: tuple[1], reverse=True)

        # Назначение места каждой команде согласно индексу в списке
        for team in sorted:
            self.cur.execute(f"""UPDATE team_result
                                 SET place = {sorted.index(team)+1}
                                 WHERE teamid = {team[0]}
                                 AND eventid = {self.eventid}
                              """)
            self.conn.commit()



if __name__ == "__main__":
    # Создание БД если ее нет
    create_db()
    app = App()
    # вернуть вызов функции в __init__
    app.change_flags()
    app.mainloop()