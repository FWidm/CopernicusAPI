import json
import sqlite3

import os

db = sqlite3.connect('file::api.db?cache=shared')
db.row_factory = lambda cursor, row: row[0]

cursor = db.cursor()
files = [(f,) for f in os.listdir("data/ecmwf") if
         os.path.isfile("data/ecmwf/" + f) and not f.startswith(".") and f.endswith(".grib")]
print files

db.commit()

cursor.execute('''
    SELECT name FROM files
''')
print cursor.fetchone()

print json.dumps(cursor.fetchall())


class DbHelper():
    def __init__(self, database='file::api.db?cache=shared'):
        self.db = database
        self.connect()

    def connect(self):
        """Connect to the SQLite3 database."""
        self.connection = sqlite3.connect(self.db)
        self.cursor = self.connection.cursor()
        self.connected = True
        self.statement = ''

    def close(self):
        """Close the SQLite3 database."""
        self.connection.commit()
        if self.connected:
            self.connection.close()
            self.connected = False

    def execute_query(self, query):
        close_connection=False
        if not self.connected:
            self.connect()
            close_connection=True
        if type(query) is str:
            self.cursor.execute(query)
            

