from flask import *
from sqlite3 import *
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object('config')
Bootstrap(app)

@app.route("/")
def hello():
	return render_template("template.html")

@app.route("/login.html")
def login():
	return render_template('login.html', msg="Welcome")

@app.route('/check',methods=['POST', 'GET'])
def check():
	msg = "something"
	if request.method == 'POST':
		try:
			print("posting")
			username = request.form['UserName']
			password = request.form['Password']

			with sql.connect('../database/websitedata.sqlite') as conn:
				print("connected")
				cur = conn.cursor()
				cur.execute("SELECT id, username, password from users")
				for row in cursor:
					if username == row[1]:
						print(row[1])
						if password == row[2]:
							msg = "Success You Have Logged In"
						else:
							msg = "Incorrect Password"
							break
					else:
						continue 
		except:
			con.rollback();
			msg = "error in login"

		finally:
			return render_template("login.html", msg = msg)
			conn.close()


if __name__ == "__main__":
	app.run(debug=True)