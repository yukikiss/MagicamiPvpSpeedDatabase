import sqlite3
import datetime
import config

class StockDB:
    instance = None
    # database model for storing all symbol data and historical market data
    # with singleton pattern
    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(StockDB)
            return cls.instance
        return cls.instance

    def __init__(self, db_name=config.get_config()['DB_NAME']):
        self.name = db_name
        # connect takes url, dbname, user-id, password
        self.conn = self.connect()
        self.cursor = self.conn.cursor()

    def connect(self):
        try:
            return sqlite3.connect(self.name)
        except sqlite3.Error as e:
            pass

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def create_record_table(self):
        conn = self.conn
        c = self.cursor
        c.execute('''CREATE TABLE "Record" (
                        "Name"	TEXT,
                        "Date"	TEXT,
                        "Team"	TEXT,
                        "Speed"	TEXT,
                        PRIMARY KEY("Name")
                    )''')
        conn.commit()

    def insert_new_record(self, name, image_path, speed):
        conn = self.conn
        c = self.cursor
        c.execute('''INSERT INTO "Record" ("Name", "Date", "Team", "Speed") VALUES (?,?,?,?)''',
                  (name, datetime.datetime.now().strftime('%Y-%m-%d'), image_path, speed))
        conn.commit()

    def get_record_by_name(self, name):
        conn = self.conn
        c = self.cursor
        c.execute('''SELECT "Name", "Date", "Team", "Speed" FROM "Record" ORDER BY "Date" DESC''')

        result = []
        for row in c.fetchall():
            temp = {}
            temp['Name'] = row[0]
            temp['Date'] = row[1]
            temp['Team'] = row[2]
            temp['Speed'] = row[3]
            result.append(temp)

        return result
