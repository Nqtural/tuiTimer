class Database:
    import sqlite3
    from datetime import datetime

    def get_date(self):
        return self.datetime.now().strftime('%Y%m%d%H%M%S')

    def new_session(self, sessions_dir="sessions"):
        # Make sessions directory if it does not already exist
        import os
        if not os.path.exists(sessions_dir):
            os.makedirs(sessions_dir)

        # Make sure to not overwrite another session by creating a unique
        # session name
        date = self.get_date()[:8]
        i = 0
        while os.path.exists(f"{sessions_dir}/{date}-{i}.db"):
            i+=1
        
        # Connect to database
        self.con = self.sqlite3.connect(f"{sessions_dir}/{date}-{i}.db")
        self.cur = self.con.cursor()

        # Create table for storing solves
        self.cur.execute("CREATE TABLE IF NOT EXISTS solves (date, time, scramble, plustwo);")

    def write(self, time, scramble, plustwo=False):
        self.cur.execute("INSERT INTO solves VALUES (?, ?, ?, ?)", (self.get_date(), time, scramble, plustwo))
        self.con.commit()

    def read(self, last=15):
        self.cur.execute("SELECT * FROM solves")
        if last > 0:
            return self.cur.fetchall()[-last:]
        else:
            return self.cur.fetchall()
