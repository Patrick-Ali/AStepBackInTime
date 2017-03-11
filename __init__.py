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

@app.route('/login', methods=['GET','POST'])
def login():
	error = None
	if request.method == 'POST':
		user = request.form['username']
		password = request.form['password']
		g.db = connect_db()
		cur = g.db.execute('SELECT username, password FROM users')
		data = cur.fetchall()
		for row in data:
			if row[0] == user:
				if row[1] == password:
					g.db.close()
					session["logged_in"] = True
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
	return redirect(url_for('home'))

def connect_db():
	return sqlite3.connect(app.database)

if __name__ == "__main__":
	app.run()