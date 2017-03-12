from flask import Flask, render_template, redirect, url_for, request, session, flash, g
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
	return render_template("template.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
	error = None
	if request.method == 'POST':
		firstname = request.form['firstname']
		lastname = request.form['lastname']
		email = request.form['email']
		username = request.form['username']
		password = request.form['password']

		g.db = connect_db()
		cur = g.db.execute('SELECT username, email FROM users')
		data = cur.fetchall()

		#Remove Else from for lop, create variable to check email and user

		for row in data:
			print(row[0])
			print(row[1])
			if row[0] == username:
				g.db.close()
				print(row[0])
				error = 'Username already used'
				break
			elif row[1] == email:
				g.db.close()
				print(row[1])
				error = 'Email alreaddy in use'
				break
			else:
				g.db.execute('INSERT INTO users (firstname, lastname, email, username, password) VALUES (?,?,?,?,?);', \
					(firstname, lastname, email, username, password))
				g.db.commit()
				g.db.close()
				return redirect(url_for('login'))
	else:
		return render_template("register.html", error = error)

@app.route('/login', methods=['GET','POST'])
def login():
	error = None
	if request.method == 'POST':
		user = request.form['username']
		password = request.form['password']
		g.db = connect_db()
		cur = g.db.execute('SELECT id, username, password FROM users')
		data = cur.fetchall()
		for row in data:
			if row[1] == user:
				if row[2] == password:
					g.db.close()
					session["logged_in"] = True
					session["id"] = row[0]
					print(session["id"])
					return redirect(url_for('home'))
				else:
					g.db.close()
					error = 'Inccorect Password'

			else:
				g.db.close()
				error = 'Invalid credentials. Please try again.'
		#else:
			 #render_template("template.html") 

	return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
	session.pop("logged_in", None)
	session.pop("id", None)
	return redirect(url_for('home'))

def connect_db():
	return sqlite3.connect(app.database)

if __name__ == "__main__":
	app.run(debug=True)