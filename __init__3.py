from flask import Flask, render_template, redirect, url_for, request, session, flash, g, make_response
from flask_bootstrap import Bootstrap
from functools import wraps
import sqlite3
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message
from flask_wtf import Form
#from flask.ext.wtf import Form, widgets
from wtforms import SubmitField, SelectField, RadioField, BooleanField, TextField, HiddenField, SelectMultipleField, widgets

#Following taken from https://gist.github.com/doobeh/4668212
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()
#End

class RomeQuiz(Form):
	q1 = RadioField("Who was the first king of Rome", choices = [("Romulus","Romulus"),("Remus","Remus")])#Romulus
	q2 = RadioField("When was Rome founded", choices = [("753","753"),("850","850"),("600","600")])#753
	q3 = MultiCheckboxField("Which two groups sacked Rome", choices = [("Gauls","Gauls"),("Visigoths","Visigoths"),("Carthaginians", "Carthaginians"),("Greeks","Greeks")])#Gauls and Visigoths
	q4 = TextField("What famous mountains did Hannibal cross")#Alps
	q5 = RadioField("Who was the first king of Rome", choices = [("Augustus Caesar","Augustus Caesar"),("Julius Caesar","Julius Caesar"),("Nero","Nero"),("Trajan","Trajan")])#Augustus Caesar
	q6 = RadioField("When was Rome founded", choices = [("45","45"),("27","27"),("100","100")])#27
	q7 = TextField("Caesar's rival during the civil war was Pompey the")#Great
	q8 = MultiCheckboxField("Select all correct provinces of the Roman empire", choices=[("Aegyptus","Aegyptus"),("Germania","Germania"),("Britannia", "Britannia"),("Greece","Greece")])#Aegyptus and Britannia
	q9 = TextField("Who was Mark Anthony's most famous lover")#Cleopatra
	q10 = TextField("Which member of Julius Caesar's family infamously helped assassinate him")#Brutus

	submit = SubmitField("Grade")

class EygptQuiz(Form):
	q1 = RadioField("Who was the first king of Egypt", choices = [("Ramses","Ramses"),("Narmer","Narmer")])#Narmer
	q2 = RadioField("Which is the capital of ancient Egypt", choices = [("Alexandra","Alexandra"),("Memphis","Memphis"),("Cairo","Cairo")])#Memphis
	q3 = MultiCheckboxField("Which two groups were rivals of ancient Egypt", choices = [("Canaanites","Canaanites"),("Rome","Rome"),("Nubians", "Nubians"),("Persia","Persia")])#Canaanites and Nubians
	q4 = TextField("What famous river runs through Egypt")#Nile
	q5 = RadioField("What was ancient Egypt's paper called", choices = [("Papyrus","Papyrus"),("Reed","Reed"),("Stone","Stone"),("Clay","Clay")])#Papyrus
	q6 = RadioField("When was the ancient Egyptian kingdom believed to have been founded founded", choices = [("3100","3100"),("2900","2900"),("5000","5000")])#3100
	q7 = TextField("Complete the title of this famous ruler, Tutan") #khamun
	q8 = MultiCheckboxField("Which two kingdoms united to form ancient Egypt?", choices=[("Upper Egypt","Upper Egypt"),("Judea","Judea"),("Sudan", "Sudan"),("Lower Egypt","Lower Egypt")])# Upper and Lower Egypt
	q9 = TextField("What are is the famous last resting places of Egypt's ancient rulers?")#Valley of the kings
	q10 = TextField("Who famously parted the Red sea?")#Moses

	submit = SubmitField("Grade")

class MacedoniaQuiz(Form):
	q1 = RadioField("Who was the first king of Macedonia", choices = [("Karanos","Karanos"),("Alexander","Alexander")])#Karanos
	q2 = RadioField("When was Aigai supposedly founded", choices = [("808","808"),("399","399"),("500","500")])#808
	q3 = MultiCheckboxField("Which two cities did Alexander famously raze to the ground", choices = [("Massaga","Massaga"),("Athens","Athens"),("Gaza", "Gaza"),("Thebes","Thebes")])#Massaga and Thebes
	q4 = TextField("What was the name of Alexander's farther")#Philip
	q5 = RadioField("Which province of Alexander's empire proclaimed him a God", choices = [("Egypt","Egypt"),("Persia","Persia"),("Greece","Greece"),("India","India")])# Egypt
	q6 = RadioField("When did Alexander come to the thrown", choices = [("336","336"),("323","323"),("350","350")])#336
	q7 = TextField("Alexander was given the grand title of") #King of Asia
	q8 = MultiCheckboxField("Select all correct provinces of the Alexanders kingdom", choices=[("Egypt","Egypt"),("Italia","Italia"),("Hispania", "Hispania"),("Persia","Persia")])# Egypt and Persia
	q9 = TextField("What was the name of Alexander the greats successor")# Alexander IV
	q10 = TextField("How old was Alexander when he died")#32

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

# Taken from https://www.youtube.com/watch?v=BnBjhmspw4c (YouTube)

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

# End YouTube

# Adapted from https://realpython.com/blog/python/handling-email-confirmation-in-flask/ (Real Python)

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

@app.route("/quiz")
def quiz():
	if "username" in session:
		user = session["username"]
		#print(user)
		return render_template("quiz.html", user = user)
	else:
		#print("Hello")
		return render_template("quiz.html", user = None) 

@app.route("/rome")
def rome():
	if "username" in session:
		user = session["username"]
		#print(user)
		return render_template("rome.html", user = user)
	else:
		#print("Hello")
		return render_template("rome.html", user = None)

@app.route("/macedonia")
def macedonia():
	if "username" in session:
		user = session["username"]
		#print(user)
		return render_template("macedonia.html", user = user)
	else:
		#print("Hello")
		return render_template("macedonia.html", user = None)

@app.route("/eygpt")
def eygpt():
	if "username" in session:
		user = session["username"]
		#print(user)
		return render_template("eygpt.html", user = user)
	else:
		#print("Hello")
		return render_template("eygpt.html", user = None)

@app.route("/rome_quiz", methods=['GET', 'POST'])
def romeQuiz():

	if "username" in session:
		user = session["username"]
	else:
		user = None

	form = RomeQuiz()

	if request.method == 'POST':
		score = request.form['score']
		uID = session['id']

		g.db = connect_db()
		cur = g.db.execute('INSERT INTO rome (userID, score) VALUES (?,?);', (uID, score))
		g.db.commit()
		g.db.close()

		return render_template("loading.html", form = form, user = user)
	else:
		return render_template("rome_quiz.html", form = form, user = user)

@app.route("/macedonia_quiz", methods=['GET', 'POST'])
def macedoniaQuiz():

	if "username" in session:
		user = session["username"]
	else:
		user = None

	form = MacedoniaQuiz()

	if request.method == 'POST':
		score = request.form['score']
		uID = session['id']

		g.db = connect_db()
		cur = g.db.execute('INSERT INTO macedonia (userID, score) VALUES (?,?);', (uID, score))
		g.db.commit()
		g.db.close()

		return render_template("loading.html", form = form, user = user)
	else:
		return render_template("macedonia_quiz.html", form = form, user = user)

@app.route("/egypt_quiz", methods=['GET', 'POST'])
def egyptQuiz():

	if "username" in session:
		user = session["username"]
	else:
		user = None

	form = EygptQuiz()

	if request.method == 'POST':
		score = request.form['score']
		uID = session['id']

		g.db = connect_db()
		cur = g.db.execute('INSERT INTO eygpt (userID, score) VALUES (?,?);', (uID, score))
		g.db.commit()
		g.db.close()

		return render_template("loading.html", form = form, user = user)
	else:
		return render_template("egypt_quiz.html", form = form, user = user)		

@app.route("/complete_rome", methods=['GET', 'POST'])
def complete():

	if "username" in session:
		user = session["username"]
	else:
		user = None

	g.db = connect_db()
	ID = session["id"]
	print(ID)
	cur = g.db.execute('SELECT score, dateDone FROM rome WHERE userID =' + str(ID) + ' ORDER BY score, dateDone DESC;')
	data = cur.fetchall()
	for row in data:
		print(row[0])
		print(row[1])
	g.db.close()

	return render_template("complete_rome.html", data = data, user = user)
	

@app.route("/loading")
def loading():

	if "username" in session:
		user = session["username"]
	else:
		user = None

	return render_template("loading.html", user = user)


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
		#print(ID)
		cur = g.db.execute('UPDATE users SET firstname = (?), lastname = (?), email = (?), username = (?), password = (?) WHERE id =' + str(ID) + ';', \
		(firstname, lastname, email, username, password) )

		g.db.commit()
		g.db.close()

		return redirect(url_for('myProfile'))

	else:
		g.db = connect_db()
		ID = session["id"]
		#print(ID)
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

	return redirect(url_for('home'))

def connect_db():
	return sqlite3.connect(app.database)

if __name__ == "__main__":
	app.run(debug=True)