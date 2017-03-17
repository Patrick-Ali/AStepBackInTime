import sqlite3

with sqlite3.connect("website.db") as connection:
	c = connection.cursor()
	#c.execute(""" CREATE TABLE users( \
		#id INTEGER PRIMARY KEY AUTOINCREMENT, firstname TEXT NOT NULL, lastname TEXT NOT NULL, email TEXT NOT NULL, username TEXT NOT NULL, \
		#password TEXT NOT NULL) """)
	#c.execute('INSERT INTO users (firstname, lastname, email, username, password)VALUES("Patrick", "Ali", "test@gmail.com", "admin", "password")')
	
	#c.execute('ALTER TABLE users ADD confirmed INTEGER NOT NULL DEFAULT 0; ')

	c.execute("""CREATE TABLE rome( \
		id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, userID INTEGER NOT NULL, score INTEGER NOT NULL, \
		FOREIGN KEY(userID) REFERENCES users(id)  );""")