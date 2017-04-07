from flask import Flask, render_template, redirect, url_for, request, session, flash, g, make_response
from flask_bootstrap import Bootstrap
from functools import wraps
import sqlite3
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message
from flask_wtf import Form
from wtforms import SubmitField, SelectField, RadioField, BooleanField, TextField, HiddenField, SelectMultipleField, widgets

#Following taken from https://gist.github.com/doobeh/4668212
class MultiCheckboxField(SelectMultipleField):
	#Used to create text boxes for WTF
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()
#End

# Begin Quiz Classes for WTF

class RomeQuiz(Form):
	q1 = RadioField("Who was the first king of Rome", choices = [("Romulus","Romulus"),("Remus","Remus")])#Romulus
	q2 = RadioField("When was Rome founded (All are in B.C. time)", choices = [("753","753"),("850","850"),("600","600")])#753
	q3 = MultiCheckboxField("Which two groups sacked Rome", choices = [("Gauls","Gauls"),("Visigoths","Visigoths"),("Carthaginians", "Carthaginians"),("Greeks","Greeks")])#Gauls and Visigoths
	q4 = TextField("What famous mountains did Hannibal cross")#Alps
	q5 = RadioField("Who was the first Emperor of the Roman Empire", choices = [("Augustus Caesar","Augustus Caesar"),("Julius Caesar","Julius Caesar"),("Nero","Nero"),("Trajan","Trajan")])#Augustus Caesar
	q6 = RadioField("When was the Roman Empire founded (All are in B.C. time)", choices = [("45","45"),("27","27"),("100","100")])#27
	q7 = TextField("Caesar's rival during the civil war was Pompey the")#Great
	q8 = MultiCheckboxField("Select all correct provinces of the Roman empire", choices=[("Aegyptus","Aegyptus"),("Germania","Germania"),("Britannia", "Britannia"),("Greece","Greece")])#Aegyptus and Britannia
	q9 = TextField("Who was Mark Anthony's most famous lover")#Cleopatra
	q10 = TextField("Which member of Julius Caesar's family infamously helped assassinate him")#Brutus

	submit = SubmitField("Grade")

class EgyptQuiz(Form):
	q1 = RadioField("Who was the first king of Egypt", choices = [("Ramses","Ramses"),("Narmer","Narmer")])#Narmer
	q2 = RadioField("Which is the capital of ancient Egypt", choices = [("Alexandra","Alexandra"),("Memphis","Memphis"),("Cairo","Cairo")])#Memphis
	q3 = MultiCheckboxField("Which two groups were rivals of ancient Egypt", choices = [("Canaanites","Canaanites"),("Rome","Rome"),("Nubians", "Nubians"),("Persia","Persia")])#Canaanites and Nubians
	q4 = TextField("What famous river runs through Egypt")#Nile
	q5 = RadioField("What was ancient Egypt's paper called", choices = [("Papyrus","Papyrus"),("Reed","Reed"),("Stone","Stone"),("Clay","Clay")])#Papyrus
	q6 = RadioField("When was the ancient Egyptian kingdom believed to have been founded founded (All are in B.C. time)", choices = [("3100","3100"),("2900","2900"),("5000","5000")])#3100
	q7 = TextField("Complete the title of this famous ruler, Tutan") #khamun
	q8 = MultiCheckboxField("Which two kingdoms united to form ancient Egypt?", choices=[("Upper Egypt","Upper Egypt"),("Judea","Judea"),("Sudan", "Sudan"),("Lower Egypt","Lower Egypt")])# Upper and Lower Egypt
	q9 = TextField("What are is the famous last resting places of Egypt's ancient rulers?")#Valley of the kings
	q10 = TextField("Who famously parted the Red sea?")#Moses

	submit = SubmitField("Grade")

class MacedoniaQuiz(Form):
	q1 = RadioField("Who was the first king of Macedonia", choices = [("Karanos","Karanos"),("Alexander","Alexander")])#Karanos
	q2 = RadioField("When was Aigai supposedly founded (All are in B.C. time)", choices = [("808","808"),("399","399"),("500","500")])#808
	q3 = MultiCheckboxField("Which two cities did Alexander famously raze to the ground", choices = [("Massaga","Massaga"),("Athens","Athens"),("Gaza", "Gaza"),("Thebes","Thebes")])#Massaga and Thebes
	q4 = TextField("What was the name of Alexander's farther")#Philip
	q5 = RadioField("Which province of Alexander's empire proclaimed him a God", choices = [("Egypt","Egypt"),("Persia","Persia"),("Greece","Greece"),("India","India")])# Egypt
	q6 = RadioField("When did Alexander come to the thrown (All are in B.C. time)", choices = [("336","336"),("323","323"),("350","350")])#336
	q7 = TextField("Alexander was given the grand title of") #King of Asia
	q8 = MultiCheckboxField("Select all correct provinces of the Alexanders kingdom", choices=[("Egypt","Egypt"),("Italia","Italia"),("Hispania", "Hispania"),("Persia","Persia")])# Egypt and Persia
	q9 = TextField("What was the name of Alexander the greats successor")# Alexander IV
	q10 = TextField("How old was Alexander when he died")#32

	submit = SubmitField("Grade")

# End Quiz Classes for WTF

#Begin App settings

app = Flask(__name__)

app.secret_key = "yINaP31znTy8Uhq51?9cQD4u]0E0.E"
app.SECURITY_PASSWORD_HASH = "sha512_crypt"
app.SECURITY_PASSWORD_SALT = "xEjV.c8)!J30PF8X9ul0SwWk;|(4,7"
app.database = "database/website.db"

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

#End App settings

# Taken from https://www.youtube.com/watch?v=BnBjhmspw4c (YouTube)

def login_required(f):
	@wraps(f)
	def wrap(*arg, **kwargs):
		"""Used to prevent people entering pages they need to be logged in to use by redirecting them to the login page"""
		if 'logged_in' in session:
			return f(*arg, **kwargs)
		else:
			#print("Redirecting")
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
	""" Route the user to the site homepage """
	if "username" in session:
		user = session["username"]
		return render_template("index.html", user = user)
	else:
		return render_template("index.html", user = None)

@app.route("/quiz")
def quiz():
	""" Route the user to the site quiz page """
	if "username" in session:
		user = session["username"]
		return render_template("quiz.html", user = user)
	else:
		return render_template("quiz.html", user = None) 

@app.route("/rome")
def rome():
	""" Route the user to the Rome information page """
	if "username" in session:
		user = session["username"]
		return render_template("rome.html", user = user)
	else:
		return render_template("rome.html", user = None)

@app.route("/macedonia")
def macedonia():
	""" Route the user to the Macedonia information page """
	if "username" in session:
		user = session["username"]
		return render_template("macedonia.html", user = user)
	else:
		return render_template("macedonia.html", user = None)

@app.route("/egypt")
def egypt():
	""" Route the user to the Egypt information page """
	if "username" in session:
		user = session["username"]
		return render_template("egypt.html", user = user)
	else:
		return render_template("egypt.html", user = None)

@app.route("/rome_quiz", methods=['GET', 'POST'])
@login_required
def romeQuiz():
	""" Route the user to the Rome quiz page or if they submit a quiz it will input the results into the database """
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

		return redirect(url_for("loading", quiz = 'romeComplete'))
	else:
		return render_template("rome_quiz.html", form = form, user = user)

@app.route("/macedonia_quiz", methods=['GET', 'POST'])
@login_required
def macedoniaQuiz():
	""" Route the user to the Macedonia quiz page or if they submit a quiz it will input the results into the database """
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

		return redirect(url_for("loading", quiz = 'macedoniaComplete'))
	else:
		return render_template("macedonia_quiz.html", form = form, user = user)

@app.route("/egypt_quiz", methods=['GET', 'POST'])
@login_required
def egyptQuiz():
	""" Route the user to the Egypt quiz page or if they submit a quiz it will input the results into the database """
	if "username" in session:
		user = session["username"]
	else:
		user = None

	form = EgyptQuiz()

	if request.method == 'POST':
		score = request.form['score']
		uID = session['id']

		g.db = connect_db()
		cur = g.db.execute('INSERT INTO egypt (userID, score) VALUES (?,?);', (uID, score))
		g.db.commit()
		g.db.close()

		return redirect(url_for("loading", quiz = 'egyptComplete'))
	else:
		return render_template("egypt_quiz.html", form = form, user = user)		

@app.route("/complete_rome", methods=['GET', 'POST'])
@login_required
def romeComplete():
	""" Route the user to their score for all the Rome quizzes they have done by pulling the users information from the database """

	if "username" in session:
		user = session["username"]
	else:
		user = None

	g.db = connect_db()
	ID = session["id"]
	cur = g.db.execute('SELECT score, dateDone FROM rome WHERE userID =' + str(ID) + ' ORDER BY score DESC, dateDone DESC;')
	data = cur.fetchall()
	g.db.close()

	return render_template("complete_rome.html", data = data, user = user)

@app.route("/complete_macedonia", methods=['GET', 'POST'])
@login_required
def macedoniaComplete():
	""" Route the user to their score for all the Macedonia quizzes they have done by pulling the users information from the database """

	if "username" in session:
		user = session["username"]
	else:
		user = None

	g.db = connect_db()
	ID = session["id"]
	cur = g.db.execute('SELECT score, dateDone FROM macedonia WHERE userID =' + str(ID) + ' ORDER BY score DESC, dateDone DESC;')
	data = cur.fetchall()
	g.db.close()

	return render_template("complete_macedonia.html", data = data, user = user)

@app.route("/complete_egypt", methods=['GET', 'POST'])
@login_required
def egyptComplete():
	""" Route the user to their score for all the Egypt quizzes they have done by pulling the users information from the database """

	if "username" in session:
		user = session["username"]
	else:
		user = None

	g.db = connect_db()
	ID = session["id"]
	cur = g.db.execute('SELECT score, dateDone FROM egypt WHERE userID =' + str(ID) + ' ORDER BY score DESC, dateDone DESC;')
	data = cur.fetchall()
	g.db.close()

	return render_template("complete_egypt.html", data = data, user = user)
	

@app.route("/loading/<quiz>")
@login_required
def loading(quiz):
	""" Renders the grading screen which will take them to the correct quiz score screen """

	if "username" in session:
		user = session["username"]
	else:
		user = None

	return render_template("loading.html", user = user , quiz = url_for(quiz, _external = True))


@app.route("/register", methods=['GET', 'POST'])
def register():
	""" If the user access this page through a GET request it will load the form for them to fill out
		otherwise if they submit the form it will check the database for users with the same
		 username and email before adding them to the database and redirecting them to the temp login screen  """

	if "username" in session:
		user = session["username"]
	else:
		user = None

	error = None

	if request.method == 'POST':
		# Gather data
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

		# Checks the database for users with the same name
		for row in data:
			if row[1] == username:
				g.db.close()
				error = 'Username already used'
				testUser = True
				return render_template("register.html", error = error, user = user)
			elif row[2] == email:
				g.db.close()
				error = 'Email alreaddy in use'
				testEmail = True
				return render_template("register.html", error = error, user = user)
			
		if testEmail == False and testUser == False:
			# Enter information into the database
			g.db.execute('INSERT INTO users (firstname, lastname, email, username, password) VALUES (?,?,?,?,?);', \
			(firstname, lastname, email, username, password))
			g.db.commit()
			g.db.close()

			return redirect(url_for('tempLogin', username = username, error = error))

	else:
		return render_template("register.html", error = error, user = user)

@app.route('/confirm/<token>')
def confirm(token):
	""" Generates page for the user to confirm their email """
	try:
		email = confirm_token(token)
	except:
		error = "Something went wrong with the email"
		return redirect(url_for('login', error = error))
	
	g.db = connect_db()
	ID = session["id"]

	#Update database to confirm the user
	cur = g.db.execute('UPDATE users SET confirmed = (?) WHERE id =' + str(ID) + ';', (1,) )
	g.db.commit()
	g.db.close()

	return redirect(url_for('login'))


@app.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
	""" Function used to remove the user from the database """
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
	""" Renders template displaying the users information, if a submission is registered it will check the username and email
	    for changes. If neither changed user data will be updated, if user name changed there will be a check it is not in use, 
	     if email changed a new confirmation email is sent and verified is changed to unverified"""

	if "username" in session:
		user = session["username"]
	else:
		user = None

	if request.method == 'POST':
		#Gather data
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

		#Check username and email aren't in use by someone else
		for row in data:
			if row[1] == username:
				g.db.close()
				error = 'Username already used'
				testUser = True
				if row[0] == session["id"]:
					testUser = False
					continue
				else:
					return render_template("myProfile.html", firstname = firstname, lastname = lastname, email = email, \
						username = username, password = password, user = user, error = error)
			elif row[2] == email:
				g.db.close()
				error = 'Email alreaddy in use'
				testEmail = True
				if row[0] == session["id"]:
					testEmail = False
					continue
				else:
					return render_template("myProfile.html", firstname = firstname, lastname = lastname, email = email, \
						username = username, password = password, user = user, error = error)
			
		if testEmail == False and testUser == False:
			#Update the database with the new information
			g.db = connect_db()
			ID = int(session["id"])
			cur = g.db.execute('SELECT email FROM users WHERE id =' + str(ID) + ';')
			data = cur.fetchall()
			for row in data:
				oldEmail = row[0]
			if oldEmail != email:
				#If email has been changed and not in use a new confirmation email is sent
				token = generate_confirmation_token(email)
				confirm_url = url_for('confirm', token = token, _external=True)#External forces it to display full address
				html = render_template('/confirmEmail.html', confirm_url=confirm_url)
				subject = "Please confirm your email"
				send_email(email, subject, html)
				cur = g.db.execute('UPDATE users SET confirmed = (?) WHERE id =' + str(ID) + ';', (0,) )
				g.db.commit()
				error = "Please Confirm Email"

			cur = g.db.execute('UPDATE users SET firstname = (?), lastname = (?), email = (?), username = (?), password = (?) WHERE id =' + str(ID) + ';', \
			(firstname, lastname, email, username, password) )
			g.db.commit()
			g.db.close()

			return render_template("myProfile.html", firstname = firstname, lastname = lastname, email = email, \
				username = username, password = password, user = user, error = error)

	else:
		#Output user information
		g.db = connect_db()
		ID = session["id"]
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


@app.route('/confirm_email')
def confirmEmail():
	""" Render page asking the user to confirm their email """
	if "username" in session:
		user = session["username"]
	else:
		user = None

	if "logged_in" in session:
		return redirect(url_for("home"))

	error = None

	return render_template('confirm_email.html', error = error, user = user)

@app.route('/temp_login', methods=['GET','POST'])
def tempLogin():
	""" This function will have the user enter their login information so as to know who to send the confirmation email to """
	if "username" in session:
		user = session["username"]
	else:
		user = None
	if "logged_in" in session:
		return redirect(url_for("home"))

	error = "Please login so we can send you a confirmation email"
	if request.method == 'POST':
		user = request.form['username']
		password = request.form['password']
		g.db = connect_db()
		cur = g.db.execute('SELECT id, username, password, confirmed, email FROM users')
		data = cur.fetchall()
		#Check the login information is correct
		for row in data:
			email = row[4]
			if row[1] == user:
				if row[2] == password:
					g.db.close()
					session["id"] = row[0]
					if row[3] == 0:
						#If information is correct send confirmation email
						token = generate_confirmation_token(email)
						confirm_url = url_for('confirm', token = token, _external=True)#External forces it to display full address
						html = render_template('/confirmEmail.html', confirm_url=confirm_url)
						subject = "Please confirm your email"
						send_email(email, subject, html)
						return redirect(url_for('confirmEmail'))
					else:
						return redirect(url_for('home'))

				else:
					g.db.close()
					error = 'Inccorect Password'

			else:
				g.db.close()
				error = 'Invalid credentials. Please try again.'

	return render_template('temp_login.html', error=error, user = user)


@app.route('/login', methods=['GET','POST'])
def login():
	""" Render page for the user to login """

	if "username" in session:
		user = session["username"]
	else:
		user = None

	error = None
	if request.method == 'POST':
		user = request.form['username']
		password = request.form['password']
		g.db = connect_db()
		cur = g.db.execute('SELECT id, username, password, confirmed, email FROM users')
		data = cur.fetchall()
		#Check the login information is correct
		for row in data:
			email = row[4]
			if row[1] == user:
				if row[2] == password:
					g.db.close()
					session["id"] = row[0]
					if row[3] == 0:
						#if the user is not verified it will redirect them to the temp login
						error = "Please login here so we can send you a confirmation email"
						return redirect(url_for('tempLogin', error = error))
					else:
						session["logged_in"] = True
						session["username"] = row[1]
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
	""" Allow the user to logout """
	session.pop("logged_in", None)
	session.pop("id", None)
	session.pop("username", None)

	return redirect(url_for('home'))

@app.route('/au')
def au():
	""" Renders about us page """
	if "username" in session:
		user = session["username"]
	else:
		user = None
	error = None
	return render_template('about_us.html', error=error, user = user)

@app.route('/pcp')
def pcp():
	""" Renders privacy and cookie policy page """
	if "username" in session:
		user = session["username"]
	else:
		user = None
	error = None
	return render_template('privacy_and_cookie_policy.html', error=error, user = user)

@app.route('/tu')
def tu():
	""" Renders terms of use page """
	if "username" in session:
		user = session["username"]
	else:
		user = None
	error = None
	return render_template('terms_of_use.html', error=error, user = user)

@app.route('/sm')
def sm():
	""" Renders site map page """
	if "username" in session:
		user = session["username"]
	else:
		user = None
	error = None
	return render_template('site_map.html', error=error, user = user)

@app.route('/cu')
def cu():
	""" Renders contact us page """
	if "username" in session:
		user = session["username"]
	else:
		user = None
	error = None
	return render_template('contact_us.html', error=error, user = user)

def connect_db():
	""" Make a connection to the database """
	return sqlite3.connect(app.database)

if __name__ == "__main__":
	app.run(debug=True)