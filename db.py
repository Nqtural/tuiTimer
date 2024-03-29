class Database:
    import sqlite3
    from datetime import datetime
    import os

    def get_date(self):
        return self.datetime.now().strftime("%Y%m%d%H%M%S")

    def connect(self, path, new=False):
        if not self.os.path.exists(path) and not new:
            return 1

        self.con = self.sqlite3.connect(path)
        self.cur = self.con.cursor()

    def new_session(self, sessions_dir="sessions"):
        # Make sessions directory if it does not already exist
        if not self.os.path.exists(sessions_dir):
            self.os.makedirs(sessions_dir)

        # Make sure to not overwrite another session by creating a unique
        # session name
        date = self.get_date()[:8]
        i = 0
        while self.os.path.exists(f"{sessions_dir}/{date}-{i}.db"): i+=1

        # Connect to database
        self.connect(f"{sessions_dir}/{date}-{i}.db", new=True)

        # Create table for storing solves
        self.cur.execute("""CREATE TABLE IF NOT EXISTS solves (
            id INTEGER PRIMARY KEY,
            date,
            time,
            scramble,
            plustwo,
            dnf);""")

    def write(self, time, scramble, plustwo=False, dnf=False):
        time = float(time) + 2 if plustwo else float(time)
        self.cur.execute(
            "INSERT INTO solves (date, time, scramble, plustwo, dnf) VALUES (?, ?, ?, ?, ?)",
            (self.get_date(), time, scramble, plustwo, dnf))
        self.con.commit()

    def toggle_plustwo(self, id):
        self.cur.execute("SELECT time, plustwo FROM solves WHERE id = ?", (id,))
        time, plustwo = self.cur.fetchone()
        self.cur.execute(
            "UPDATE solves SET plustwo = ?, time = ? WHERE id = ?",
            (plustwo == False,
             time - 2 if plustwo else time + 2,
             id))
        self.con.commit()

    def toggle_dnf(self, id):
        self.cur.execute("SELECT dnf FROM solves WHERE id = ?", (id,))
        dnf = self.cur.fetchone()[0]
        self.cur.execute(
            "UPDATE solves SET dnf = ? WHERE id = ?",
            (dnf == False, id))
        self.con.commit()

    def read(self, last=-1):
        self.cur.execute("SELECT * FROM solves")
        if last > 0:
            return self.cur.fetchall()[-last:]
        else:
            return self.cur.fetchall()

    def delete(self, id):
        self.cur.execute("DELETE FROM solves WHERE id = ?", (id,))
        self.con.commit()
