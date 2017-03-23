from flask import Flask, render_template, redirect, url_for, request, session, flash, g, make_response
from flask_bootstrap import Bootstrap
from functools import wraps
import sqlite3
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message
from flask_wtf import Form
#from flask.ext.wtf import Form, widgets
from wtforms import SubmitField, SelectField, RadioField, BooleanField, TextField, HiddenField, SelectMultipleField, widgets

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class RomeQuiz(Form):
	#b1String = ['']
	q1 = RadioField("Who was the first king of Rome", choices = [("Romulus","Romulus"),("Remus","Remus")])
	q2 = RadioField("When was Rome founded", choices = [("720","720"),("850","850"),("600","600")])
	q3 = MultiCheckboxField("Which two groups sacked Rome", choices = [("Gauls","Gauls"),("Visigoths","Visigoths"),("Carthaginians", "Carthaginians"),("Greeks","Greeks")])
	q4 = TextField("What famous mountains did Hannable cross")
	q5 = RadioField("Who was the first king of Rome", choices = [("Augustus Ceaser","Augustus Ceaser"),("Julius Ceaser","Julius Ceaser"),("Nero","Nero"),("Trajan","Trajan")])
	q6 = RadioField("When was Rome founded", choices = [("45","45"),("30","30"),("100","100")])
	q7 = TextField("Ceaser's rival during the civil war was Pompey the")
	q8 = MultiCheckboxField("Select all correct provinces of the Roman empire", choices=[("Aegyptus","Aegyptus"),("Germania","Germania"),("Britania", "Britania"),("Grecce","Grecce")])
	q9 = TextField("Who was Mark Anthony's most famous lover")
	q10 = TextField("Which member of Julius Ceasers family infamously helped assassinate him")

	submit = SubmitField("Grade")


app = Flask(__name__)
app.secret_key = "yINaP31znTy8Uhq51?9cQD4u]0E0.E"
app.SECURITY_PASSWORD_HASH = "sha512_crypt"
app.SECURITY_PASSWORD_SALT = "xEjV.c8)!J30PF8X9ul0SwWk;|(4,7"
app.database = "website.db"
Bootstrap(app)

app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'patrick.ali345@gmail.com',
	MAIL_PASSWORD = 'Black31road*'
	)

mail = Mail(app)

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

#Real Python

def generate_confirmation_token(email): #Generates random string for conformation
    serializer = URLSafeTimedSerializer(app.secret_key)
    return serializer.dumps(email, salt=app.SECURITY_PASSWORD_SALT) 


def confirm_token(token, expiration=3600):#Gives the token a time to live, currently one hour
    serializer = URLSafeTimedSerializer(app.secret_key)
    try:
        email = serializer.loads(
            token,
            salt=app.SECURITY_PASSWORD_SALT,
            max_age=expiration
        )#Checks that the token isn't dead
    except:
        return False
    return email

def send_email(to, subject, template):#Sends e-mail
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender="patrick.ali345@gmail.com")
    mail.send(msg)

#end Real Python

@app.route("/")
def home():
	if "username" in session:
		user = session["username"]
		#print(user)
		return render_template("template.html", user = user)
	else:
		#print("Hello")
		return render_template("template.html", user = None)

@app.route("/rome_quiz", methods=['GET', 'POST'])
def romeQuiz():

	form = RomeQuiz()

	if request.method == 'POST':
		score = request.form['score']
		uID = session['id']

		g.db = connect_db()
		cur = g.db.execute('INSERT INTO rome (userID, score) VALUES (?,?);', (uID, score))
		g.db.commit()
		g.db.close()

		return render_template("rome_quiz.html", form = form)
	else:
		return render_template("rome_quiz.html", form = form)

@app.route("/loading")
def loading():
	return render_template("loading.html")


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

			token = generate_confirmation_token(email)
			confirm_url = url_for('confirm', token = token, _external=True)#External forces it to display full address
			html = render_template('/confirmEmail.html', confirm_url=confirm_url)
			subject = "Please confirm your email"
			send_email(email, subject, html)

			#msg = Message(
				#'Hello',
				#sender='patrick.ali345@gmail.com',
				#recipients=['alip@uni.coventry.ac.uk'])
			#msg.body = "This is the email body"
			#mail.send(msg)
			
			
			return redirect(url_for('special', username = username))

	else:
		return render_template("register.html", error = error, user = user)

@app.route('/confirm/<token>')
def confirm(token):
	try:
		email = confirm_token(token)
	except:
		error = "Something went wrong with the email"
		return redirect(url_for('login', error = error))
	
	g.db = connect_db()
	ID = session["id"]
	cur = g.db.execute('UPDATE users SET confirmed = (?) WHERE id =' + str(ID) + ';', (1,) )
	g.db.commit()
	g.db.close()

	return redirect(url_for('home'))


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