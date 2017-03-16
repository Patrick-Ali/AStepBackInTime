import sqlite3

conn = sqlite3.connect('database/websitedata.db')

print ("opened database successfully")

#conn.execute(''' CREATE TABLE users (id INT PRIMARY KEY NOT NULL,
#username TEXT NOT NULL, 
#password TEXT NOT NULL ); ''')

conn.execute("INSERT INTO users (id, username, password) VALUES (1, 'admin', 'password')")

conn.commit()

cursor = conn.execute("SELECT id, username, password from users")

for row in cursor:
	print("ID = ", row[0])
	print("Username = ", row[1])
	print("Password = ", row[2])

print("Table create successfully")

conn.close()