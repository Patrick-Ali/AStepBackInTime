import sqlite3

with sqlite3.connect("website.db") as connection:
	c = connection.cursor()
	c.execute(""" CREATE TABLE users( \
		id INTEGER PRIMARY KEY AUTOINCREMENT, firstname TEXT NOT NULL, lastname TEXT NOT NULL, email TEXT NOT NULL, username TEXT NOT NULL, \
		password TEXT NOT NULL) """)
	c.execute('INSERT INTO users (firstname, lastname, email, username, password)VALUES("Patrick", "Ali", "test@gmail.com", "admin", "password")')
	