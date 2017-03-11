import sqlite3

with sqlite3.connect("website.db") as connection:
	c = connection.cursor()
	c.execute(""" CREATE TABLE users( \
		firstname TEXT, lastname TEXT, email TEXT, username TEXT, \
		password TEXT) """)
	c.execute('INSERT INTO users VALUES("Patrick", "Ali", "test@gmail.com", "admin", "password")')
	