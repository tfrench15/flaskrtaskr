import sqlite3
from _config import DATABASE_PATH

with sqlite3.connect(DATABASE_PATH) as connection:
	c = connection.cursor()

	c.execute("""CREATE TABLE Tasks(task_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
		due_date TEXT NOT NULL, priority INTEGER NOT NULL, status INTEGER NOT NULL)""")

	c.execute("INSERT INTO Tasks (name, due_date, priority, status) VALUES('Finish this tutorial', '03/25/2015', 10, 1)")

	