from flask import Flask, render_template, request, make_response, redirect
import sqlite3
import time
import json

conn = sqlite3.connect('goat.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS users
    (id integer primary key autoincrement, username text, password text)
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS shoes
    (id integer primary key autoincrement, brand text, price integer, url text, user_id integer, foreign key(user_id) references users(id))
''')

app = Flask(__name__, static_url_path='')


@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/profile')
def profile():
    username = request.cookies.get('username')
    return render_template('profile.html', user=username)

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

@app.route('/new_shoe', methods=['GET', 'POST'])
def new_shoe():
    if request.method == 'POST':
        user_id = int(request.cookies.get('user_id'))
        print(user_id)
        shoe_brand = request.form['shoe_brand']
        price = int(request.form['shoe_price'])
        print (request.files)
        try:
            if 'file' in request.files:
                imageFile = request.files['file']
                savePath = "./static/{}".format(imageFile.filename)
                imageFile.save(savePath)
        except Exception as e:
            print(e)

        conn = sqlite3.connect('goat.db')

        c = conn.cursor()
        c.execute('''
            INSERT INTO shoes(brand, price, url, user_id)
            VALUES (?, ?, ?, ?) 
        ''', (shoe_brand, price, imageFile.filename, user_id))

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
        resp = make_response(redirect('/display_shoes', 302))
        resp.set_cookie('user_id', str(user_id))
        resp.set_cookie('username', str(username))
        return resp
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    username = "wow"
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
            return render_template('login.html', error='Password is wrong')

        print('found user', user)

        # store username and password in database
        resp = make_response(redirect('/display_shoes', 302))
        print("this is user id", user[0])
        resp.set_cookie('user_id', str(user[0]))
        resp.set_cookie('username', str(username))
        return resp
    else:
        return render_template('login.html')


@app.route('/display_shoes', methods=['GET', 'POST'])
def display_shoes():
    return render_template('display_shoes.html')

@app.route('/get_shoes')
def get_shoes():

    conn = sqlite3.connect('goat.db')

    c = conn.cursor()
    c.execute('''
            select * from shoes 
        ''')
    shoes = c.fetchall()

    return json.dumps(shoes)

@app.route('/get_shoes_of_user')
def get_shoes_of_user():
    user_id = int(request.cookies.get('user_id'))

    conn = sqlite3.connect('goat.db')

    c = conn.cursor()
    c.execute('''
            select * from shoes WHERE user_id=?
        ''', (user_id,))
    shoes = c.fetchall()

    return json.dumps(shoes)

@app.route('/search_item')
def search_item():
    search_item = request.args.get('searchitem') + '%'
    print('search item:', search_item)
    conn = sqlite3.connect('goat.db')

    c = conn.cursor()
    c.execute("select * from shoes WHERE brand LIKE ?", (search_item,))
    shoes = c.fetchall()

    return json.dumps(shoes)

app.run()
