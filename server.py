from flask import Flask, render_template, request
import sqlite3

conn = sqlite3.connect('goat.db')
c = conn.cursor()

c.execute('''
	CREATE TABLE IF NOT EXISTS users
	(id integer primary key autoincrement, username text, password text)
''')

app = Flask(__name__, static_url_path='')

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	print(request.form)
	username = request.form['username']
	password = request.form['password']

	conn = sqlite3.connect('goat.db')

	c = conn.cursor()
	c.execute('''
		INSERT INTO users(username, password)
		VALUES (?, ?) 
	''', (username, password))

	print('saved user')

	conn.commit()

	# store username and password in database
	return ""

app.run()