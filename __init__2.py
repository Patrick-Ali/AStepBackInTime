from flask import Flask, render_template, redirect, url_for, request, session, flash, g, make_response
from flask_bootstrap import Bootstrap
from functools import wraps
import sqlite3

app = Flask(__name__)
app.secret_key = "yINaP31znTy8Uhq51?9cQD4u]0E0.E"
app.database = "website.db"
Bootstrap(app)

def login_required(f):
	@wraps(f)
	def wrap(*arg, **kwargs):
		if 'logged_in' in session:
			return f(*arg, **kwargs)
		else:
			print("Redirecting")
			flash("You must be logged in to access this.")
			return redirect(url_for('login'))
	return wrap

@app.route("/")
def home():
	if "username" in session:
		user = session["username"]
		#print(user)
		return render_template("template.html", user = user)
	else:
		#print("Hello")
		return render_template("template.html", user = None)

@app.route("/register", methods=['GET', 'POST'])
def register():

	if "username" in session:
		user = session["username"]
	else:
		user = None

	error = None
	if request.method == 'POST':
		firstname = request.form['firstname']
		lastname = request.form['lastname']
		email = request.form['email']
		username = request.form['username']
		password = request.form['password']

		g.db = connect_db()
		cur = g.db.execute('SELECT id, username, email FROM users')
		data = cur.fetchall()

		#Remove Else from for lop, create variable to check email and user

		testUser = False
		testEmail = False

		for row in data:
			print(row[1])
			print(row[2])
			if row[1] == username:
				g.db.close()
				print("Username:" + str(row[1]))
				error = 'Username already used'
				testUser = True
				return render_template("register.html", error = error, user = user)
			elif row[2] == email:
				g.db.close()
				print(row[2])
				error = 'Email alreaddy in use'
				testEmail = True
				return render_template("register.html", error = error, user = user)
			
		if testEmail == False and testUser == False:
			g.db.execute('INSERT INTO users (firstname, lastname, email, username, password) VALUES (?,?,?,?,?);', \
			(firstname, lastname, email, username, password))
			g.db.commit()
			g.db.close()

			
			
			return redirect(url_for('special', username = username))

	else:
		return render_template("register.html", error = error, user = user)

@app.route('/special/<username>')
def special(username):
	return autoLog(username)


def autoLog(username):
			g.db = connect_db()
			cur = g.db.execute('SELECT id, username FROM users WHERE username = username;')
			dataSecond = cur.fetchall()
			session["logged_in"] = True
			for record in dataSecond:
				session["id"] = record[0]
				session["username"] = record[1]
			
			#session["id"] = row[0] + 1
			print(session["id"])

			return redirect(url_for('home'))


@app.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
	if request.method == 'POST':
		g.db = connect_db()
		ID = int(session["id"])
		cur = g.db.execute('DELETE FROM users WHERE id = ' + str(ID) + ';')
		g.db.commit()
		g.db.close()
		return redirect(url_for('logout'))

@app.route('/myProfile', methods=['GET', 'POST'])
@login_required
def myProfile():

	if "username" in session:
		user = session["username"]
	else:
		user = None

	if request.method == 'POST':

		firstname = request.form['firstname']
		lastname = request.form['lastname']
		email = request.form['email']
		username = request.form['username']
		password = request.form['password']

		g.db = connect_db()
		ID = int(session["id"])
		#ID = 8
		print(ID)
		cur = g.db.execute('UPDATE users SET firstname = (?), lastname = (?), email = (?), username = (?), password = (?) WHERE id =' + str(ID) + ';', \
		(firstname, lastname, email, username, password) )

		g.db.commit()
		g.db.close()

		return redirect(url_for('myProfile'))

	else:
		g.db = connect_db()
		ID = session["id"]
		print(ID)
		cur = g.db.execute('SELECT firstname, lastname, email, username, password FROM users WHERE id = ' + str(ID) + ';')
		data = cur.fetchall()

		for row in data:
			firstname = row[0]
			lastname = row[1]
			email = row[2]
			username = row[3]
			password = 	row[4]

		return render_template("myProfile.html", firstname = firstname, lastname = lastname, email = email, \
		 username = username, password = password, user = user)


@app.route('/login', methods=['GET','POST'])
def login():
	if "username" in session:
		user = session["username"]
	else:
		user = None

	error = None
	if request.method == 'POST':
		user = request.form['username']
		print(user)
		password = request.form['password']
		g.db = connect_db()
		cur = g.db.execute('SELECT id, username, password FROM users')
		data = cur.fetchall()
		for row in data:
			if row[1] == user:
				print(user)
				if row[2] == password:
					g.db.close()
					session["logged_in"] = True
					session["id"] = row[0]
					session["username"] = row[1]
					redirect(url_for('home'))
					return redirect(url_for('home'))

				else:
					g.db.close()
					error = 'Inccorect Password'

			else:
				g.db.close()
				error = 'Invalid credentials. Please try again.'

	return render_template('login.html', error=error, user = user)

@app.route('/logout')
@login_required
def logout():
	session.pop("logged_in", None)
	session.pop("id", None)
	session.pop("username", None)
	#loggin = False
	return redirect(url_for('home'))

def connect_db():
	return sqlite3.connect(app.database)

if __name__ == "__main__":
	app.run(debug=True)