import sqlite3


def create_db():
    conn = sqlite3.connect('Arena.db')
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS sportsman(
       sportsmanid INTEGER PRIMARY KEY AUTOINCREMENT,
       fullname TEXT UNIQUE);
    """)
    conn.commit()

    cur.execute("""CREATE TABLE IF NOT EXISTS team(
       teamid INTEGER PRIMARY KEY AUTOINCREMENT,
       name TEXT UNIQUE,
       emblem TEXT);
    """)
    conn.commit()

    cur.execute("""CREATE TABLE IF NOT EXISTS event(
       eventid INTEGER PRIMARY KEY AUTOINCREMENT,
       name TEXT UNIQUE,
       startdate TEXT,
       enddate TEXT,
       current INTEGER NOT NULL DEFAULT 1);
    """)
    conn.commit()

    cur.execute("""CREATE TABLE IF NOT EXISTS meeting(
       meetingid INTEGER PRIMARY KEY AUTOINCREMENT,
       teamid_1 INT,
       teamid_2 INT,
       eventid INT,
       date TEXT,
       FOREIGN KEY (teamid_1) REFERENCES team (teamid),
       FOREIGN KEY (teamid_2) REFERENCES team (teamid),
       FOREIGN KEY (eventid) REFERENCES event (eventid) ON DELETE CASCADE);
    """)
    conn.commit()

    cur.execute("""CREATE TABLE IF NOT EXISTS meeting_result(
       meetingid INT,
       teamid INT,
       score INT,
       win INT DEFAULT 0,
       draw INT DEFAULT 0,
       lose INT DEFAULT 0,
       possession INT,
       kicks INT,
       gates INT,
       foul INT,
       yellow INT,
       red INT,
       FOREIGN KEY (teamid) REFERENCES team (teamid),
       FOREIGN KEY (meetingid) REFERENCES meeting (meetingid) ON DELETE CASCADE);
    """)
    conn.commit()

    cur.execute("""CREATE TABLE IF NOT EXISTS team_result(
       teamid INT,
       eventid INT,
       win INT DEFAULT 0,
       draw INT DEFAULT 0,
       lose INT DEFAULT 0,
       place INT,
       points INT DEFAULT 0,
       FOREIGN KEY (teamid) REFERENCES team (teamid),
       FOREIGN KEY (eventid) REFERENCES event (eventid) ON DELETE CASCADE);
    """)
    conn.commit()

    cur.execute("""CREATE TABLE IF NOT EXISTS sportsman_team(
       sportsmanid INT,
       teamid INT,
       sportsman_num INT,
       FOREIGN KEY (sportsmanid) REFERENCES sportsman (sportsmanid),
       FOREIGN KEY (teamid) REFERENCES team (teamid));
    """)
    conn.commit()



