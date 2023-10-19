from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Blueprint
from passlib.hash import pbkdf2_sha256
from views.settings_view import settings
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  
app.register_blueprint(settings, url_prefix='/settings')

# Create SQLite database and table
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password_hash TEXT
    )
''')
conn.commit()
conn.close()

def hash_password(password):
    return pbkdf2_sha256.hash(password)

def verify_password(password, password_hash):
    return pbkdf2_sha256.verify(password, password_hash)

@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()

        if user and verify_password(password, user[2]):
            session['username'] = username
            return redirect(url_for('home'))

    return render_template('login.html')

@app.route('/logout', methods=['GET','POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    user_exists = False  # Flag to indicate whether the user already exists

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # Check if the username already exists
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            user_exists = True
        else:
            hashed_password = hash_password(password)
            cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, hashed_password))
            conn.commit()
            session['username'] = username
            return redirect(url_for('home'))

        conn.close()

    return render_template('create_account.html', user_exists=user_exists)




if __name__ == '__main__':
    app.run(debug=True)
