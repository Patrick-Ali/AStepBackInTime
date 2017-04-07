import sqlite3

with sqlite3.connect("database/website.db") as connection:
	c = connection.cursor()

	#SQL used to create, alter, insert and change tables

	#c.execute(""" CREATE TABLE users( \
		#id INTEGER PRIMARY KEY AUTOINCREMENT, firstname TEXT NOT NULL, lastname TEXT NOT NULL, email TEXT NOT NULL, username TEXT NOT NULL, \
		#password TEXT NOT NULL) """)
	#c.execute('INSERT INTO users (firstname, lastname, email, username, password)VALUES("Patrick", "Ali", "test@gmail.com", "admin", "password")')
	
	#c.execute('ALTER TABLE users ADD confirmed INTEGER NOT NULL DEFAULT 0; ')

	#c.execute("""CREATE TABLE rome( \
		#id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, userID INTEGER NOT NULL, score INTEGER NOT NULL, \
		#FOREIGN KEY(userID) REFERENCES users(id)  );""")

	#c.execute("""CREATE TABLE eygpt( \
		#id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, userID INTEGER NOT NULL, score INTEGER NOT NULL, dateDone NUMERIC NOT NULL DEFAULT CURRENT_TIMESTAMP, \
		#FOREIGN KEY(userID) REFERENCES users(id)  );""")
	
	#c.execute('INSERT INTO eygpt (userID, score)VALUES(7, 10);')		

	#c.execute('ALTER TABLE rome ADD dateDone NUMBER DEFAULT CURRENT_TIMESTAMP; ')

	#c.execute('DROP TABLE eygpt;') 
	#c.execute('DROP TABLE egypt;') 
	#c.execute('DROP TABLE rome;') 
	#c.execute('DROP TABLE macedonia;') 

	#c.execute("""CREATE TABLE rome( \
	# 	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, userID INTEGER NOT NULL, score INTEGER NOT NULL, dateDone DATETIME NOT NULL DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'LOCALTIME')), \
	# 	FOREIGN KEY(userID) REFERENCES users(id)  );""")

	# c.execute("""CREATE TABLE macedonia( \
	# 	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, userID INTEGER NOT NULL, score INTEGER NOT NULL, dateDone DATETIME NOT NULL DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'LOCALTIME')), \
	# 	FOREIGN KEY(userID) REFERENCES users(id)  );""")

	# c.execute("""CREATE TABLE egypt( \
	# 	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, userID INTEGER NOT NULL, score INTEGER NOT NULL, dateDone DATETIME NOT NULL DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'LOCALTIME')), \
	# 	FOREIGN KEY(userID) REFERENCES users(id)  );""")

	#c.execute("""SELECT datetime(CURRENT_TIMESTAMP, 'localtime'); """)

	#SQLite Indices for faster search

	#c.execute(""" DROP INDEX user_name """)
	
	#c.execute(""" CREATE INDEX user_id ON users (id); """)
	#c.execute(""" CREATE INDEX rome_user ON rome (userID); """)
	#c.execute(""" CREATE INDEX egypt_user ON egypt (userID); """), 
	#c.execute(""" CREATE INDEX macedonia_user ON macedonia (userID); """)

	#SQLite triggers to automate user deletion from database

	#c.execute(""" CREATE TRIGGER user_delete_rome AFTER DELETE ON users FOR EACH ROW BEGIN DELETE FROM rome WHERE userID = OLD.id; END; """)
	#c.execute(""" CREATE TRIGGER user_delete_macedonia AFTER DELETE ON users FOR EACH ROW BEGIN DELETE FROM macedonia WHERE userID = OLD.id; END; """)
	#c.execute(""" CREATE TRIGGER user_delete_egypt AFTER DELETE ON users FOR EACH ROW BEGIN DELETE FROM egypt WHERE userID = OLD.id; END; """)
