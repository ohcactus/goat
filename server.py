from flask import Flask, render_template, request, make_response, redirect
import sqlite3

conn = sqlite3.connect('goat.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS users
    (id integer primary key autoincrement, username text, password text)
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS shoes
    (id integer primary key autoincrement, brand text, price integer, user_id integer, foreign key(user_id) references users(id))
''')

app = Flask(__name__, static_url_path='')

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/new_shoe', methods=['GET', 'POST'])
def new_shoe():

    if request.method == 'POST':
        user_id = int(request.cookies.get('user_id'))
        print(user_id)
        shoe_brand = request.form['shoe_brand']
        price = int(request.form['shoe_price'])


        conn = sqlite3.connect('goat.db')

        c = conn.cursor()
        c.execute('''
            INSERT INTO shoes(brand, price, user_id)
            VALUES (?, ?, ?) 
        ''', (shoe_brand, price, user_id))

        print('saved user')

        shoe_id = c.lastrowid


        conn.commit()
        return redirect('/display_shoes', 302)

    return render_template('signedin.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
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

        user_id = c.lastrowid

        conn.commit()

        # store username and password in database
        resp = make_response 
        (redirect('/display_shoes', 302))
        resp.set_cookie('user_id', str(user_id))
    else:
        return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.form)
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('goat.db')

        c = conn.cursor()
        c.execute('''
            select * from users where username=? and password=?
        ''', (username, password)) 
        user = c.fetchone()
        if not user:
            return render_template('login.html', error = 'Password is wrong')

        print('found user', user)

        # store username and password in database
        resp = make_response (redirect('/display_shoes', 302))
        print("this is user id", user[0])
        resp.set_cookie('user_id', str(user[0]))
        return resp
    else:
        return render_template('login.html')

@app.route('/display_shoes', methods=['GET', 'POST'])
def display_shoes():
    
        conn = sqlite3.connect('goat.db')

        c = conn.cursor()
        c.execute('''
            select * from shoes 
        ''') 
        shoes = c.fetchall()
        return render_template('display_shoes.html', shoes = shoes)


app.run()